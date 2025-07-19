"""
Supabase Cache Integration Module
Tag-based intelligent caching with batch updates
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseCache:
    """
    Intelligent cache management with tag-based organization
    Supports pattern recognition and semantic queries
    """
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        self._batch_queue = []
        self._batch_size = 10  # Process in batches of 10
        
    def add_to_batch(self, key: str, value: Dict[Any, Any], tags: List[str]) -> str:
        """
        Add item to batch queue for later processing
        Returns UUID for tracking
        """
        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cache_item = {
            "id": item_id,
            "key": key,
            "value": value,
            "tags": tags,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        self._batch_queue.append(cache_item)
        
        # Auto-flush if batch is full
        if len(self._batch_queue) >= self._batch_size:
            self.flush_batch()
            
        return item_id
    
    def flush_batch(self) -> Dict[str, Any]:
        """
        Process all queued items in single batch operation
        Returns status and metrics
        """
        if not self._batch_queue:
            return {"status": "empty", "processed": 0}
        
        try:
            # Batch insert to Supabase
            result = self.supabase.table("cache_items").insert(self._batch_queue).execute()
            
            processed_count = len(self._batch_queue)
            self._batch_queue.clear()
            
            return {
                "status": "success",
                "processed": processed_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            # Log error but don't lose data
            error_backup = f"brain/cache/batch_error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            with open(error_backup, 'w') as f:
                json.dump(self._batch_queue, f, indent=2)
            
            self._batch_queue.clear()
            
            return {
                "status": "error",
                "error": str(e),
                "backup_file": error_backup
            }
    
    def query_by_tags(self, tags: List[str], match_all: bool = False) -> List[Dict]:
        """
        Query cache items by tags
        
        Args:
            tags: List of tags to search for
            match_all: If True, requires ALL tags. If False, requires ANY tag.
        """
        try:
            if match_all:
                # PostgreSQL array contains all specified tags
                query = self.supabase.table("cache_items").select("*")
                for tag in tags:
                    query = query.contains("tags", [tag])
                result = query.execute()
            else:
                # PostgreSQL array overlaps with any specified tags
                result = self.supabase.table("cache_items").select("*").overlaps("tags", tags).execute()
            
            return result.data
            
        except Exception as e:
            print(f"Query error: {e}")
            return []
    
    def search_values(self, search_term: str, tags: Optional[List[str]] = None) -> List[Dict]:
        """
        Full-text search within cached values
        Optionally filter by tags
        """
        try:
            query = self.supabase.table("cache_items").select("*")
            
            # PostgreSQL full-text search on JSONB values
            query = query.textSearch("value", search_term)
            
            if tags:
                query = query.overlaps("tags", tags)
            
            result = query.execute()
            return result.data
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_by_key(self, key: str) -> Optional[Dict]:
        """Get most recent item by key"""
        try:
            result = self.supabase.table("cache_items").select("*").eq("key", key).order("updated_at", desc=True).limit(1).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Get error: {e}")
            return None
    
    def update_item(self, item_id: str, value: Dict[Any, Any], tags: Optional[List[str]] = None) -> bool:
        """Update existing cache item"""
        try:
            update_data = {
                "value": value,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            if tags is not None:
                update_data["tags"] = tags
            
            result = self.supabase.table("cache_items").update(update_data).eq("id", item_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def cleanup_old_items(self, days_old: int = 30) -> int:
        """Remove items older than specified days"""
        try:
            cutoff_date = datetime.utcnow().replace(day=datetime.utcnow().day - days_old).isoformat()
            result = self.supabase.table("cache_items").delete().lt("created_at", cutoff_date).execute()
            return len(result.data)
        except Exception as e:
            print(f"Cleanup error: {e}")
            return 0

# Convenience functions for brain system integration
def cache_intent_pattern(intent: str, pattern_data: Dict, confidence: float, tags: List[str] = None):
    """Cache intent recognition pattern for future similarity matching"""
    cache = SupabaseCache()
    
    default_tags = ["#intent", "#pattern"]
    if tags:
        default_tags.extend(tags)
    
    value = {
        "intent": intent,
        "pattern_data": pattern_data,
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return cache.add_to_batch(f"intent_pattern_{intent}", value, default_tags)

def cache_decision_correlation(decision_id: str, correlations: Dict, impact_score: float):
    """Cache decision correlation mapping for systems thinking"""
    cache = SupabaseCache()
    
    value = {
        "decision_id": decision_id,
        "correlations": correlations,
        "impact_score": impact_score,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return cache.add_to_batch(f"decision_correlation_{decision_id}", value, ["#decision", "#correlation", "#mapping"])

def cache_learning_event(event_type: str, event_data: Dict, success_score: float):
    """Cache learning events for pattern recognition and improvement tracking"""
    cache = SupabaseCache()
    
    value = {
        "event_type": event_type,
        "event_data": event_data,
        "success_score": success_score,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return cache.add_to_batch(f"learning_event_{event_type}", value, ["#learning", "#feedback", f"#{event_type}"])

def trigger_batch_sync():
    """Manual trigger for batch processing - called by /log commands"""
    cache = SupabaseCache()
    return cache.flush_batch()

if __name__ == "__main__":
    # Test basic functionality
    cache = SupabaseCache()
    
    # Test batch adding
    test_id = cache.add_to_batch(
        "test_key", 
        {"test": "data", "number": 123}, 
        ["#test", "#demo"]
    )
    
    # Force flush for testing
    result = cache.flush_batch()
    print(f"Batch result: {result}")
    
    # Test querying
    results = cache.query_by_tags(["#test"])
    print(f"Query results: {len(results)} items found")