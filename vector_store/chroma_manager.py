"""
Chroma Vector Database Manager for R1 Reasoning Engine

Local vector storage using ChromaDB with AAI patterns,
confidence scoring, and reasoning optimization.
"""
import logging
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Chroma imports with fallback
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# Vector operations
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from agents.r1_reasoning.models import (
    VectorSearchRequest, VectorSearchResult, DocumentChunk
)

logger = logging.getLogger(__name__)


class ChromaManager:
    """
    Local vector database manager using ChromaDB.
    
    Features:
    - Local vector storage with persistence
    - AAI confidence scoring integration
    - Reasoning-optimized retrieval
    - Collection management with metadata
    - Batch operations for efficiency
    """
    
    def __init__(self, 
                 persist_directory: str = "./data/chroma_db",
                 collection_name: str = "reasoning_documents",
                 embedding_function: Optional[Any] = None):
        """Initialize Chroma manager"""
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.embedding_function = embedding_function
        
        # Ensure persist directory exists
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client
        self.client = None
        self.collection = None
        self.chroma_ready = False
        
        if CHROMA_AVAILABLE:
            try:
                self._initialize_client()
                self.chroma_ready = True
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB: {e}")
        else:
            logger.warning("ChromaDB not available - install chromadb package")
    
    def _initialize_client(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Configure Chroma settings
            settings = Settings(
                persist_directory=str(self.persist_directory),
                anonymized_telemetry=False
            )
            
            # Create client
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=settings
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"reasoning_engine": "r1", "aai_compliant": True}
            )
            
            logger.info(f"ChromaDB initialized with collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"ChromaDB initialization failed: {e}")
            raise
    
    async def store_chunks(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """
        Store document chunks in Chroma collection.
        
        Args:
            chunks: List of DocumentChunk objects
            
        Returns:
            Storage result with success metrics
        """
        if not self.chroma_ready:
            return {
                "success": False,
                "stored_count": 0,
                "error": "ChromaDB not available"
            }
        
        stored_count = 0
        failed_count = 0
        start_time = datetime.now()
        
        try:
            # Prepare batch data
            ids = []
            documents = []
            embeddings = []
            metadatas = []
            
            for chunk in chunks:
                try:
                    ids.append(chunk.chunk_id)
                    documents.append(chunk.content)
                    
                    # Use embedding if available
                    if chunk.embedding:
                        embeddings.append(chunk.embedding)
                    
                    # Prepare metadata with AAI compliance
                    metadata = {
                        "document_id": chunk.document_id,
                        "chunk_index": chunk.chunk_index,
                        "confidence_score": chunk.confidence_score,
                        "quality_score": chunk.quality_score,
                        "chunk_type": chunk.chunk_type,
                        "created_at": chunk.processing_timestamp.isoformat(),
                        **chunk.metadata  # Include additional metadata
                    }
                    metadatas.append(metadata)
                    
                except Exception as e:
                    logger.warning(f"Failed to prepare chunk {chunk.chunk_id}: {e}")
                    failed_count += 1
                    continue
            
            # Batch insert into Chroma
            if ids:
                if embeddings and len(embeddings) == len(ids):
                    # Store with embeddings
                    self.collection.add(
                        ids=ids,
                        documents=documents,
                        embeddings=embeddings,
                        metadatas=metadatas
                    )
                else:
                    # Store without embeddings (Chroma will generate them)
                    self.collection.add(
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas
                    )
                
                stored_count = len(ids)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": stored_count > 0,
                "stored_count": stored_count,
                "failed_count": failed_count,
                "processing_time_ms": int(processing_time),
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Chroma storage failed: {e}")
            return {
                "success": False,
                "stored_count": 0,
                "error": str(e)
            }
    
    async def search_similar(self, request: VectorSearchRequest) -> List[VectorSearchResult]:
        """
        Search for similar chunks using Chroma's similarity search.
        
        Args:
            request: Vector search request parameters
            
        Returns:
            List of ranked search results
        """
        if not self.chroma_ready:
            return []
        
        try:
            # Prepare query parameters
            query_params = {
                "query_texts": [request.query],
                "n_results": min(request.max_results, 100),  # Chroma limit
                "include": ["documents", "metadatas", "distances"]
            }
            
            # Add filters if specified
            where_filter = self._build_where_filter(request)
            if where_filter:
                query_params["where"] = where_filter
            
            # Perform search
            results = self.collection.query(**query_params)
            
            # Process results
            search_results = []
            
            if results and results["ids"]:
                for i, chunk_id in enumerate(results["ids"][0]):
                    try:
                        # Extract result data
                        content = results["documents"][0][i]
                        metadata = results["metadatas"][0][i]
                        distance = results["distances"][0][i]
                        
                        # Convert distance to similarity (Chroma uses cosine distance)
                        similarity_score = max(0.0, 1.0 - distance)
                        
                        # Get confidence score from metadata
                        confidence_score = metadata.get("confidence_score", 0.70)
                        
                        # Apply thresholds
                        if (similarity_score >= request.similarity_threshold and
                            confidence_score >= request.min_confidence):
                            
                            search_result = VectorSearchResult(
                                chunk_id=chunk_id,
                                content=content,
                                filename=metadata.get("filename", "unknown"),
                                similarity_score=similarity_score,
                                confidence_score=confidence_score,
                                metadata=metadata,
                                chunk_type=metadata.get("chunk_type", "text"),
                                page_number=metadata.get("page_number")
                            )
                            search_results.append(search_result)
                            
                    except Exception as e:
                        logger.warning(f"Failed to process search result {i}: {e}")
                        continue
            
            # Sort by similarity score (highest first)
            search_results.sort(key=lambda x: x.similarity_score, reverse=True)
            
            return search_results[:request.max_results]
            
        except Exception as e:
            logger.error(f"Chroma search failed: {e}")
            return []
    
    def _build_where_filter(self, request: VectorSearchRequest) -> Optional[Dict[str, Any]]:
        """Build Chroma where filter from search request"""
        filters = {}
        
        # Document type filter
        if request.document_type_filter:
            filters["chunk_type"] = {"$eq": request.document_type_filter}
        
        # Date range filter
        if request.date_range_filter:
            date_filters = {}
            if "start_date" in request.date_range_filter:
                date_filters["$gte"] = request.date_range_filter["start_date"]
            if "end_date" in request.date_range_filter:
                date_filters["$lte"] = request.date_range_filter["end_date"]
            
            if date_filters:
                filters["created_at"] = date_filters
        
        return filters if filters else None
    
    async def get_chunk_by_id(self, chunk_id: str) -> Optional[VectorSearchResult]:
        """Retrieve specific chunk by ID"""
        try:
            if not self.chroma_ready:
                return None
            
            # Get chunk from Chroma
            results = self.collection.get(
                ids=[chunk_id],
                include=["documents", "metadatas"]
            )
            
            if results and results["ids"]:
                content = results["documents"][0]
                metadata = results["metadatas"][0]
                
                return VectorSearchResult(
                    chunk_id=chunk_id,
                    content=content,
                    filename=metadata.get("filename", "unknown"),
                    similarity_score=1.0,  # Perfect match by ID
                    confidence_score=metadata.get("confidence_score", 0.70),
                    metadata=metadata,
                    chunk_type=metadata.get("chunk_type", "text"),
                    page_number=metadata.get("page_number")
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Chunk retrieval failed: {e}")
            return None
    
    async def delete_document_chunks(self, document_id: str) -> Dict[str, Any]:
        """Delete all chunks for a document"""
        try:
            if not self.chroma_ready:
                return {"success": False, "error": "ChromaDB not available"}
            
            # Get all chunks for the document
            results = self.collection.get(
                where={"document_id": {"$eq": document_id}},
                include=["documents"]
            )
            
            if results and results["ids"]:
                # Delete the chunks
                self.collection.delete(ids=results["ids"])
                
                return {
                    "success": True,
                    "deleted_count": len(results["ids"])
                }
            else:
                return {
                    "success": True,
                    "deleted_count": 0
                }
            
        except Exception as e:
            logger.error(f"Document chunk deletion failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_chunk_metadata(self, 
                                  chunk_id: str, 
                                  metadata_updates: Dict[str, Any]) -> bool:
        """Update metadata for a chunk"""
        try:
            if not self.chroma_ready:
                return False
            
            # Get current chunk data
            current = self.collection.get(
                ids=[chunk_id],
                include=["documents", "metadatas"]
            )
            
            if not current or not current["ids"]:
                return False
            
            # Update metadata
            current_metadata = current["metadatas"][0]
            current_metadata.update(metadata_updates)
            
            # Upsert with updated metadata
            self.collection.upsert(
                ids=[chunk_id],
                documents=[current["documents"][0]],
                metadatas=[current_metadata]
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Metadata update failed: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            if not self.chroma_ready:
                return {"available": False}
            
            # Get collection count
            count = self.collection.count()
            
            # Get sample to calculate averages
            sample_results = self.collection.peek(limit=min(100, count))
            
            average_confidence = 0.75
            if sample_results and sample_results["metadatas"]:
                confidences = [
                    m.get("confidence_score", 0.70) 
                    for m in sample_results["metadatas"]
                ]
                if confidences:
                    average_confidence = sum(confidences) / len(confidences)
            
            return {
                "available": True,
                "total_chunks": count,
                "collection_name": self.collection_name,
                "average_confidence": average_confidence,
                "persist_directory": str(self.persist_directory),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Stats retrieval failed: {e}")
            return {"available": False, "error": str(e)}
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get Chroma manager status"""
        return {
            "chroma_ready": self.chroma_ready,
            "chroma_available": CHROMA_AVAILABLE,
            "numpy_available": NUMPY_AVAILABLE,
            "collection_name": self.collection_name,
            "persist_directory": str(self.persist_directory),
            "capabilities": {
                "local_storage": True,
                "persistence": True,
                "batch_operations": True,
                "metadata_filtering": True,
                "confidence_scoring": True
            }
        }


async def test_chroma_manager():
    """Test Chroma manager functionality"""
    
    manager = ChromaManager()
    
    print("🧪 Testing Chroma Manager")
    print("=" * 30)
    
    # Check manager status
    status = manager.get_manager_status()
    print(f"Chroma ready: {status['chroma_ready']}")
    print(f"Collection: {status['collection_name']}")
    print(f"Persist directory: {status['persist_directory']}")
    print(f"Capabilities: {status['capabilities']}")
    
    if not status['chroma_ready']:
        print("❌ Chroma manager not ready")
        return
    
    # Test with sample data
    sample_chunks = [
        DocumentChunk(
            chunk_id=str(uuid.uuid4()),
            document_id="test_doc_1",
            content="Artificial intelligence reasoning systems use logical inference.",
            chunk_index=0,
            confidence_score=0.85,
            quality_score=0.75,
            chunk_type="text"
        ),
        DocumentChunk(
            chunk_id=str(uuid.uuid4()),
            document_id="test_doc_1",
            content="Machine learning models can analyze complex patterns in data.",
            chunk_index=1,
            confidence_score=0.78,
            quality_score=0.65,
            chunk_type="text"
        )
    ]
    
    print(f"\n📄 Testing with {len(sample_chunks)} sample chunks")
    
    # Test storage
    storage_result = await manager.store_chunks(sample_chunks)
    print(f"\n📊 Storage Results:")
    print(f"Success: {storage_result['success']}")
    print(f"Stored: {storage_result['stored_count']}")
    print(f"Processing time: {storage_result.get('processing_time_ms', 0)}ms")
    
    # Test search
    search_request = VectorSearchRequest(
        query="artificial intelligence reasoning",
        max_results=5,
        similarity_threshold=0.3,
        min_confidence=0.70
    )
    
    print(f"\n🔍 Testing search: '{search_request.query}'")
    search_results = await manager.search_similar(search_request)
    print(f"Found {len(search_results)} results")
    
    for i, result in enumerate(search_results):
        print(f"  {i+1}. Similarity: {result.similarity_score:.3f}, "
              f"Confidence: {result.confidence_score:.3f}")
    
    # Test collection stats
    stats = manager.get_collection_stats()
    print(f"\n📈 Collection Stats:")
    if stats['available']:
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Average confidence: {stats['average_confidence']:.3f}")
    else:
        print("Stats not available")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_chroma_manager())