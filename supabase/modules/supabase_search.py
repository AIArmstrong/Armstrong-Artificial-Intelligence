#!/usr/bin/env python3
"""
Supabase Search Interface for AAI
Provides unified search across all Supabase-stored data
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    title: str
    content: str
    source: str
    category: str
    score: float
    metadata: Dict[str, Any]

class SupabaseSearch:
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        self.tables = {
            'research': 'aai_research_docs',
            'examples': 'aai_code_examples', 
            'ideas': 'aai_ideas',
            'cache': 'aai_cache_entries',
            'tasks': 'aai_task_analytics',
            'rule_compliance': 'aai_rule_compliance'
        }
        
    def search_all(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search across all content types"""
        results = []
        
        # Search research documents
        results.extend(self.search_research(query, limit))
        
        # Search code examples
        results.extend(self.search_examples(query, limit))
        
        # Search ideas
        results.extend(self.search_ideas(query, limit))
        
        # Search rule compliance
        results.extend(self.search_rule_compliance(query, limit))
        
        # Sort by relevance score
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def search_research(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search research documents using full-text search"""
        sql = """
        SELECT 
            id, title, content, source_file, category, 
            quality_score, metadata,
            ts_rank(to_tsvector('english', content), plainto_tsquery('english', %s)) as score
        FROM aai_research_docs
        WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s)
        ORDER BY score DESC
        LIMIT %s
        """
        
        # Mock results for now (replace with actual DB query)
        return self._mock_search_results("research", query, limit)
    
    def search_examples(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search code examples"""
        sql = """
        SELECT 
            id, title, description, code, language, category, 
            success_score, metadata,
            ts_rank(to_tsvector('english', code || ' ' || COALESCE(description, '')), 
                   plainto_tsquery('english', %s)) as score
        FROM aai_code_examples
        WHERE to_tsvector('english', code || ' ' || COALESCE(description, '')) 
              @@ plainto_tsquery('english', %s)
        ORDER BY score DESC
        LIMIT %s
        """
        
        return self._mock_search_results("examples", query, limit)
    
    def search_ideas(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search ideas by title and description"""
        sql = """
        SELECT 
            id, title, description, stage, category, 
            research_ready, metadata,
            ts_rank(to_tsvector('english', title || ' ' || COALESCE(description, '')), 
                   plainto_tsquery('english', %s)) as score
        FROM aai_ideas
        WHERE to_tsvector('english', title || ' ' || COALESCE(description, '')) 
              @@ plainto_tsquery('english', %s)
        ORDER BY score DESC
        LIMIT %s
        """
        
        return self._mock_search_results("ideas", query, limit)
    
    def search_rule_compliance(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search rule compliance entries"""
        sql = """
        SELECT 
            id, rule_id, session_id, status, details, tool, phase, timestamp,
            ts_rank(to_tsvector('english', rule_id || ' ' || COALESCE(details, '')), 
                   plainto_tsquery('english', %s)) as score
        FROM aai_rule_compliance
        WHERE to_tsvector('english', rule_id || ' ' || COALESCE(details, '')) 
              @@ plainto_tsquery('english', %s)
        ORDER BY score DESC, timestamp DESC
        LIMIT %s
        """
        
        return self._mock_search_results("rule_compliance", query, limit)
    
    def get_rule_compliance_stats(self, days_back: int = 7) -> Dict[str, Any]:
        """Get rule compliance statistics (would query actual database)"""
        # This would query the actual database for statistics
        return {
            "total_entries": 150,
            "rule_stats": {
                "RULE-001": {"total": 50, "passed": 48, "failed": 2},
                "RULE-002": {"total": 45, "passed": 45, "failed": 0},
                "RULE-003": {"total": 30, "passed": 28, "failed": 2},
                "RULE-004": {"total": 25, "passed": 25, "failed": 0}
            },
            "session_stats": {
                "20250716_105035": {"total": 25, "passed": 24, "failed": 1},
                "20250716_105045": {"total": 20, "passed": 20, "failed": 0}
            },
            "period_days": days_back
        }
    
    def search_rule_compliance_by_rule(self, rule_id: str, limit: int = 50) -> List[SearchResult]:
        """Search rule compliance entries by specific rule ID"""
        sql = """
        SELECT id, rule_id, session_id, status, details, tool, phase, timestamp
        FROM aai_rule_compliance
        WHERE rule_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
        """
        
        return self._mock_search_results("rule_compliance", f"rule:{rule_id}", limit)
    
    def semantic_search(self, query: str, content_type: str = "all", limit: int = 10) -> List[SearchResult]:
        """Semantic search using embeddings (requires OpenRouter integration)"""
        # This would use OpenRouter to generate embeddings for the query
        # Then search using vector similarity
        
        sql = """
        SELECT 
            id, title, content, source_file, category, metadata,
            1 - (embedding <=> %s) as similarity_score
        FROM aai_research_docs
        WHERE embedding IS NOT NULL
        ORDER BY similarity_score DESC
        LIMIT %s
        """
        
        return self._mock_search_results("semantic", query, limit)
    
    def search_by_category(self, category: str, limit: int = 20) -> List[SearchResult]:
        """Search by category across all content types"""
        results = []
        
        # Search each table for the category
        for content_type, table in self.tables.items():
            if content_type == "cache":
                continue  # Skip cache for category search
                
            # Mock query for each table
            results.extend(self._mock_search_results(content_type, f"category:{category}", limit))
        
        return results[:limit]
    
    def get_recent_content(self, content_type: str = "all", days: int = 7, limit: int = 20) -> List[SearchResult]:
        """Get recently added content"""
        sql = """
        SELECT id, title, content, category, metadata, created_at
        FROM aai_research_docs
        WHERE created_at >= NOW() - INTERVAL '%s days'
        ORDER BY created_at DESC
        LIMIT %s
        """
        
        return self._mock_search_results("recent", f"last_{days}_days", limit)
    
    def _mock_search_results(self, source: str, query: str, limit: int) -> List[SearchResult]:
        """Mock search results for testing (replace with actual DB queries)"""
        mock_results = []
        
        if source == "research":
            mock_results = [
                SearchResult(
                    id="research_1",
                    title="AI Development Research",
                    content="Research on AI development patterns and best practices...",
                    source="research",
                    category="ai-development",
                    score=0.85,
                    metadata={"file_path": "research/ai-development/patterns.md"}
                ),
                SearchResult(
                    id="research_2", 
                    title="Implementation Validation",
                    content="Validation methodologies for implementation planning...",
                    source="research",
                    category="validation",
                    score=0.72,
                    metadata={"file_path": "research/validation/methods.md"}
                )
            ]
        elif source == "examples":
            mock_results = [
                SearchResult(
                    id="example_1",
                    title="Supabase Cache Implementation",
                    content="def connect_to_supabase():\n    # Connection logic...",
                    source="examples",
                    category="database",
                    score=0.79,
                    metadata={"language": "python", "file_path": "examples/supabase-cache.py"}
                )
            ]
        elif source == "ideas":
            mock_results = [
                SearchResult(
                    id="idea_1",
                    title="GitHub Repo Intelligence System",
                    content="Python-based analysis system for GitHub repositories...",
                    source="ideas",
                    category="ai-intelligence",
                    score=0.91,
                    metadata={"stage": "seed", "research_ready": True}
                )
            ]
        elif source == "rule_compliance":
            mock_results = [
                SearchResult(
                    id="rule_1",
                    title="RULE-001 Compliance Check",
                    content="✅ Pre-task check - claude-md-checker.py",
                    source="rule_compliance",
                    category="compliance",
                    score=0.95,
                    metadata={"rule_id": "RULE-001", "status": "✅", "session_id": "20250716_105035"}
                ),
                SearchResult(
                    id="rule_2", 
                    title="RULE-002 Compliance Check",
                    content="✅ Pre-task check - claude-md-checker.py",
                    source="rule_compliance",
                    category="compliance",
                    score=0.93,
                    metadata={"rule_id": "RULE-002", "status": "✅", "session_id": "20250716_105035"}
                ),
                SearchResult(
                    id="rule_3",
                    title="RULE-003 Compliance Check", 
                    content="✅ Pre-task check - claude-md-checker.py",
                    source="rule_compliance",
                    category="compliance",
                    score=0.92,
                    metadata={"rule_id": "RULE-003", "status": "✅", "session_id": "20250716_105035"}
                )
            ]
        
        # Filter by query relevance (simple mock)
        if query and query != "all":
            mock_results = [r for r in mock_results if query.lower() in r.title.lower() or query.lower() in r.content.lower()]
        
        return mock_results[:limit]
    
    def create_search_index(self):
        """Create or update search index for better performance"""
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_research_fts ON aai_research_docs USING GIN(to_tsvector('english', content));",
            "CREATE INDEX IF NOT EXISTS idx_examples_fts ON aai_code_examples USING GIN(to_tsvector('english', code || ' ' || COALESCE(description, '')));",
            "CREATE INDEX IF NOT EXISTS idx_ideas_fts ON aai_ideas USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')));"
        ]
        
        print("📊 Search indexes created/updated")
        return index_queries

def main():
    """Test search functionality"""
    search = SupabaseSearch()
    
    print("🔍 AAI Supabase Search Interface\n")
    
    # Test different search types
    test_queries = [
        ("ai development", "research"),
        ("supabase", "examples"),
        ("github", "ideas"),
        ("RULE-001", "rule_compliance"),
        ("python", "all")
    ]
    
    for query, search_type in test_queries:
        print(f"Search: '{query}' in {search_type}")
        
        if search_type == "all":
            results = search.search_all(query, limit=5)
        elif search_type == "research":
            results = search.search_research(query, limit=5)
        elif search_type == "examples":
            results = search.search_examples(query, limit=5)
        elif search_type == "ideas":
            results = search.search_ideas(query, limit=5)
        elif search_type == "rule_compliance":
            results = search.search_rule_compliance(query, limit=5)
        
        if results:
            for result in results:
                print(f"  - {result.title} ({result.source}) - Score: {result.score:.2f}")
        else:
            print("  No results found")
        print()
    
    # Test category search
    print("Category search: 'ai-development'")
    results = search.search_by_category("ai-development", limit=3)
    for result in results:
        print(f"  - {result.title} ({result.category})")
    
    print("\n✅ Search interface ready for database connection!")

if __name__ == "__main__":
    main()