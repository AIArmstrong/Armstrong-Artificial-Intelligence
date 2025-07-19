#!/usr/bin/env python3
"""
Semantic Search System for Research Engine
AI-powered search across all research using embeddings
"""

import json
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import requests
# import numpy as np  # Optional dependency - fallback to basic search if not available
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("NumPy not available - using fallback mathematical operations")
from datetime import datetime
import sqlite3
import pickle

@dataclass
class SearchResult:
    """Individual search result"""
    file_path: str
    technology: str
    research_type: str  # 'general', 'project-specific'
    project: Optional[str]
    content_snippet: str
    similarity_score: float
    quality_score: float
    last_updated: str

@dataclass
class SearchQuery:
    """Search query with context"""
    query: str
    technology_filter: Optional[str] = None
    project_filter: Optional[str] = None
    research_type_filter: Optional[str] = None
    min_similarity: float = 0.7
    max_results: int = 10

class SemanticSearchEngine:
    """Semantic search engine for research content"""
    
    def __init__(self, research_dir: str, openrouter_api_key: Optional[str] = None):
        self.research_dir = Path(research_dir)
        self.semantic_dir = self.research_dir / "_semantic"
        self.index_dir = self.semantic_dir / "index"
        self.embeddings_dir = self.semantic_dir / "embeddings"
        
        # Create directories
        self.semantic_dir.mkdir(exist_ok=True)
        self.index_dir.mkdir(exist_ok=True)
        self.embeddings_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.index_dir / "search_index.db"
        self.init_database()
        
        # OpenRouter configuration
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.embedding_model = "openai/text-embedding-3-small"
        self.embedding_dimensions = 1536
        
        # Search configuration
        self.chunk_size = 500  # Characters per chunk
        self.chunk_overlap = 50  # Overlap between chunks
        
        print(f"Semantic search engine initialized for {research_dir}")
    
    def init_database(self):
        """Initialize SQLite database for search index"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    technology TEXT NOT NULL,
                    research_type TEXT NOT NULL,
                    project TEXT,
                    content_chunk TEXT NOT NULL,
                    chunk_hash TEXT UNIQUE NOT NULL,
                    embedding_file TEXT NOT NULL,
                    quality_score REAL DEFAULT 0.0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_technology ON search_index(technology)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_research_type ON search_index(research_type)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_project ON search_index(project)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_chunk_hash ON search_index(chunk_hash)
            ''')
    
    def index_all_research(self):
        """Index all research files for semantic search"""
        print("Starting semantic indexing of all research files...")
        
        indexed_count = 0
        skipped_count = 0
        
        # Index knowledge base files
        knowledge_base = self.research_dir / "_knowledge-base"
        if knowledge_base.exists():
            for category_dir in knowledge_base.iterdir():
                if category_dir.is_dir():
                    for research_file in category_dir.glob("*.md"):
                        try:
                            result = self.index_research_file(research_file)
                            if result:
                                indexed_count += 1
                                print(f"Indexed: {research_file.name}")
                            else:
                                skipped_count += 1
                        except Exception as e:
                            print(f"Error indexing {research_file}: {e}")
                            skipped_count += 1
        
        print(f"Semantic indexing complete: {indexed_count} indexed, {skipped_count} skipped")
        
        # Update index metadata
        self.update_index_metadata(indexed_count)
    
    def index_research_file(self, file_path: Path) -> bool:
        """Index a single research file"""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = self.extract_file_metadata(file_path, content)
            
            # Check if file needs reindexing
            if not self.needs_reindexing(file_path, content):
                return False
            
            # Remove existing entries for this file
            self.remove_file_from_index(str(file_path))
            
            # Create content chunks
            chunks = self.create_content_chunks(content)
            
            # Process each chunk
            for chunk in chunks:
                chunk_hash = self.get_chunk_hash(chunk)
                
                # Generate embedding
                embedding = self.get_embedding(chunk)
                if embedding is None:
                    continue
                
                # Save embedding
                embedding_file = self.save_embedding(chunk_hash, embedding)
                
                # Add to database
                self.add_to_database(
                    file_path=str(file_path),
                    technology=metadata['technology'],
                    research_type=metadata['research_type'],
                    project=metadata.get('project'),
                    content_chunk=chunk,
                    chunk_hash=chunk_hash,
                    embedding_file=embedding_file,
                    quality_score=metadata.get('quality_score', 0.0)
                )
            
            return True
            
        except Exception as e:
            print(f"Error indexing file {file_path}: {e}")
            return False
    
    def extract_file_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from research file"""
        import re
        
        # Parse filename for technology and type
        filename = file_path.stem
        
        if '-general' in filename:
            technology = filename.replace('-general', '')
            research_type = 'general'
            project = None
        elif '-' in filename:
            parts = filename.split('-')
            technology = parts[0]
            project = parts[-1]
            research_type = 'project-specific'
        else:
            technology = filename
            research_type = 'general'
            project = None
        
        # Extract quality score
        quality_match = re.search(r'Quality Score:\s*(\d+\.\d+)', content)
        quality_score = float(quality_match.group(1)) if quality_match else 0.0
        
        return {
            'technology': technology,
            'research_type': research_type,
            'project': project,
            'quality_score': quality_score
        }
    
    def needs_reindexing(self, file_path: Path, content: str) -> bool:
        """Check if file needs reindexing"""
        # Check if file exists in index
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT last_updated FROM search_index WHERE file_path = ? LIMIT 1",
                (str(file_path),)
            )
            result = cursor.fetchone()
            
            if not result:
                return True  # File not in index
            
            # Check if file was modified after last indexing
            last_indexed = datetime.fromisoformat(result[0])
            file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            return file_modified > last_indexed
    
    def remove_file_from_index(self, file_path: str):
        """Remove all entries for a file from the index"""
        with sqlite3.connect(self.db_path) as conn:
            # Get embedding files to delete
            cursor = conn.cursor()
            cursor.execute(
                "SELECT embedding_file FROM search_index WHERE file_path = ?",
                (file_path,)
            )
            embedding_files = [row[0] for row in cursor.fetchall()]
            
            # Delete embedding files
            for embedding_file in embedding_files:
                embedding_path = self.embeddings_dir / embedding_file
                if embedding_path.exists():
                    embedding_path.unlink()
            
            # Remove from database
            conn.execute("DELETE FROM search_index WHERE file_path = ?", (file_path,))
    
    def create_content_chunks(self, content: str) -> List[str]:
        """Create overlapping content chunks for better search"""
        chunks = []
        
        # Split content into sections first
        sections = self.split_into_sections(content)
        
        for section in sections:
            # Create chunks from each section
            section_chunks = self.chunk_text(section, self.chunk_size, self.chunk_overlap)
            chunks.extend(section_chunks)
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]  # Filter short chunks
    
    def split_into_sections(self, content: str) -> List[str]:
        """Split content into logical sections"""
        import re
        
        # Split by markdown headers
        sections = re.split(r'\n(?=#{1,6}\s)', content)
        
        # Clean up sections
        sections = [section.strip() for section in sections if section.strip()]
        
        return sections
    
    def chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to end at word boundary
            if end < len(text):
                last_space = chunk.rfind(' ')
                if last_space > chunk_size * 0.8:  # If we have a good word boundary
                    chunk = chunk[:last_space]
                    end = start + last_space
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def get_chunk_hash(self, chunk: str) -> str:
        """Generate hash for chunk to avoid duplicates"""
        return hashlib.md5(chunk.encode()).hexdigest()
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for text using OpenRouter"""
        if not self.openrouter_api_key:
            print("OpenRouter API key not available, skipping embedding generation")
            return None
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://aai-research-engine.local",
                    "X-Title": "AAI Research Engine"
                },
                json={
                    "model": self.embedding_model,
                    "input": text
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                embedding = result["data"][0]["embedding"]
                if NUMPY_AVAILABLE:
                    return np.array(embedding)
                else:
                    return embedding
            else:
                print(f"Embedding API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def save_embedding(self, chunk_hash: str, embedding: List[float]) -> str:
        """Save embedding to file"""
        embedding_file = f"{chunk_hash}.pkl"
        embedding_path = self.embeddings_dir / embedding_file
        
        with open(embedding_path, 'wb') as f:
            pickle.dump(embedding, f)
        
        return embedding_file
    
    def load_embedding(self, embedding_file: str) -> Optional[List[float]]:
        """Load embedding from file"""
        embedding_path = self.embeddings_dir / embedding_file
        
        if not embedding_path.exists():
            return None
        
        try:
            with open(embedding_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading embedding {embedding_file}: {e}")
            return None
    
    def add_to_database(self, **kwargs):
        """Add entry to search database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO search_index 
                (file_path, technology, research_type, project, content_chunk, 
                 chunk_hash, embedding_file, quality_score, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                kwargs['file_path'],
                kwargs['technology'],
                kwargs['research_type'],
                kwargs['project'],
                kwargs['content_chunk'],
                kwargs['chunk_hash'],
                kwargs['embedding_file'],
                kwargs['quality_score'],
                datetime.now().isoformat()
            ))
    
    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Perform semantic search"""
        if not self.openrouter_api_key:
            print("OpenRouter API key not available, falling back to keyword search")
            return self.keyword_search(query)
        
        # Get query embedding
        query_embedding = self.get_embedding(query.query)
        if query_embedding is None:
            return self.keyword_search(query)
        
        # Build SQL query with filters
        sql_query = "SELECT * FROM search_index WHERE 1=1"
        params = []
        
        if query.technology_filter:
            sql_query += " AND technology = ?"
            params.append(query.technology_filter)
        
        if query.project_filter:
            sql_query += " AND project = ?"
            params.append(query.project_filter)
        
        if query.research_type_filter:
            sql_query += " AND research_type = ?"
            params.append(query.research_type_filter)
        
        # Get all matching chunks
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, params)
            chunks = cursor.fetchall()
        
        # Calculate similarities
        results = []
        for chunk in chunks:
            (id, file_path, technology, research_type, project, content_chunk, 
             chunk_hash, embedding_file, quality_score, last_updated) = chunk
            
            # Load embedding
            chunk_embedding = self.load_embedding(embedding_file)
            if chunk_embedding is None:
                continue
            
            # Calculate similarity
            similarity = self.cosine_similarity(query_embedding, chunk_embedding)
            
            if similarity >= query.min_similarity:
                result = SearchResult(
                    file_path=file_path,
                    technology=technology,
                    research_type=research_type,
                    project=project,
                    content_snippet=content_chunk[:200] + "..." if len(content_chunk) > 200 else content_chunk,
                    similarity_score=similarity,
                    quality_score=quality_score,
                    last_updated=last_updated
                )
                results.append(result)
        
        # Sort by similarity score
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Return top results
        return results[:query.max_results]
    
    def keyword_search(self, query: SearchQuery) -> List[SearchResult]:
        """Fallback keyword search when embeddings unavailable"""
        # Build SQL query with keyword search
        sql_query = '''
            SELECT * FROM search_index 
            WHERE content_chunk LIKE ? 
        '''
        params = [f"%{query.query}%"]
        
        if query.technology_filter:
            sql_query += " AND technology = ?"
            params.append(query.technology_filter)
        
        if query.project_filter:
            sql_query += " AND project = ?"
            params.append(query.project_filter)
        
        if query.research_type_filter:
            sql_query += " AND research_type = ?"
            params.append(query.research_type_filter)
        
        sql_query += " ORDER BY quality_score DESC LIMIT ?"
        params.append(query.max_results)
        
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, params)
            
            for row in cursor.fetchall():
                (id, file_path, technology, research_type, project, content_chunk, 
                 chunk_hash, embedding_file, quality_score, last_updated) = row
                
                # Simple keyword relevance score
                query_words = query.query.lower().split()
                content_lower = content_chunk.lower()
                matches = sum(1 for word in query_words if word in content_lower)
                similarity = matches / len(query_words) if query_words else 0
                
                if similarity >= query.min_similarity:
                    result = SearchResult(
                        file_path=file_path,
                        technology=technology,
                        research_type=research_type,
                        project=project,
                        content_snippet=content_chunk[:200] + "..." if len(content_chunk) > 200 else content_chunk,
                        similarity_score=similarity,
                        quality_score=quality_score,
                        last_updated=last_updated
                    )
                    results.append(result)
        
        return results
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if NUMPY_AVAILABLE:
            a_np = np.array(a) if not isinstance(a, np.ndarray) else a
            b_np = np.array(b) if not isinstance(b, np.ndarray) else b
            dot_product = np.dot(a_np, b_np)
            norm_a = np.linalg.norm(a_np)
            norm_b = np.linalg.norm(b_np)
        else:
            # Fallback implementation without NumPy
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def update_index_metadata(self, indexed_count: int):
        """Update index metadata"""
        metadata = {
            "last_indexed": datetime.now().isoformat(),
            "total_chunks": indexed_count,
            "embedding_model": self.embedding_model,
            "embedding_dimensions": self.embedding_dimensions,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
        
        metadata_file = self.index_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search index statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total chunks
            cursor.execute("SELECT COUNT(*) FROM search_index")
            total_chunks = cursor.fetchone()[0]
            
            # By technology
            cursor.execute("""
                SELECT technology, COUNT(*) 
                FROM search_index 
                GROUP BY technology 
                ORDER BY COUNT(*) DESC
            """)
            by_technology = dict(cursor.fetchall())
            
            # By research type
            cursor.execute("""
                SELECT research_type, COUNT(*) 
                FROM search_index 
                GROUP BY research_type
            """)
            by_research_type = dict(cursor.fetchall())
            
            # By project
            cursor.execute("""
                SELECT project, COUNT(*) 
                FROM search_index 
                WHERE project IS NOT NULL
                GROUP BY project 
                ORDER BY COUNT(*) DESC
            """)
            by_project = dict(cursor.fetchall())
            
            return {
                "total_chunks": total_chunks,
                "by_technology": by_technology,
                "by_research_type": by_research_type,
                "by_project": by_project
            }

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python semantic_search.py <research_directory> [command] [options]")
        print("Commands:")
        print("  index - Index all research files")
        print("  search <query> [--technology=<tech>] [--project=<proj>] [--type=<type>]")
        print("  stats - Show search index statistics")
        sys.exit(1)
    
    research_dir = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "index"
    
    # Initialize search engine
    search_engine = SemanticSearchEngine(research_dir)
    
    if command == "index":
        search_engine.index_all_research()
    
    elif command == "search":
        if len(sys.argv) < 4:
            print("Usage: search <query> [--technology=<tech>] [--project=<proj>] [--type=<type>]")
            sys.exit(1)
        
        query_text = sys.argv[3]
        
        # Parse filters
        technology_filter = None
        project_filter = None
        research_type_filter = None
        
        for arg in sys.argv[4:]:
            if arg.startswith("--technology="):
                technology_filter = arg.split("=", 1)[1]
            elif arg.startswith("--project="):
                project_filter = arg.split("=", 1)[1]
            elif arg.startswith("--type="):
                research_type_filter = arg.split("=", 1)[1]
        
        # Create search query
        query = SearchQuery(
            query=query_text,
            technology_filter=technology_filter,
            project_filter=project_filter,
            research_type_filter=research_type_filter
        )
        
        # Perform search
        results = search_engine.search(query)
        
        print(f"\nSearch Results for '{query_text}' ({len(results)} results):")
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.technology} ({result.research_type})")
            if result.project:
                print(f"   Project: {result.project}")
            print(f"   File: {result.file_path}")
            print(f"   Similarity: {result.similarity_score:.3f}")
            print(f"   Quality: {result.quality_score:.2f}")
            print(f"   Snippet: {result.content_snippet}")
    
    elif command == "stats":
        stats = search_engine.get_search_stats()
        print(f"\nSearch Index Statistics:")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"\nBy Technology:")
        for tech, count in stats['by_technology'].items():
            print(f"  {tech}: {count}")
        print(f"\nBy Research Type:")
        for rtype, count in stats['by_research_type'].items():
            print(f"  {rtype}: {count}")
        if stats['by_project']:
            print(f"\nBy Project:")
            for project, count in stats['by_project'].items():
                print(f"  {project}: {count}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()