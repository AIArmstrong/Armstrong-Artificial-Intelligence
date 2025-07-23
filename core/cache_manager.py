"""
Cache Manager for AAI System
Provides centralized caching functionality across all modules
"""

import asyncio
import time
import json
import logging
from typing import Any, Optional, Dict, Union
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Represents a cache entry with value and metadata"""
    value: Any
    created_at: float
    ttl: Optional[float] = None
    access_count: int = 0
    last_accessed: float = None
    
    def __post_init__(self):
        if self.last_accessed is None:
            self.last_accessed = self.created_at
    
    @property
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def touch(self):
        """Update access statistics"""
        self.access_count += 1
        self.last_accessed = time.time()

class CacheManager:
    """
    Centralized cache manager for AAI system
    Provides in-memory caching with TTL support and persistence options
    """
    
    def __init__(self, default_ttl: Optional[float] = 3600, max_size: int = 10000):
        """
        Initialize cache manager
        
        Args:
            default_ttl: Default TTL in seconds (None for no expiration)
            max_size: Maximum number of cache entries
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._lock = asyncio.Lock()
        
        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "evictions": 0
        }
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        async with self._lock:
            if key not in self.cache:
                self.stats["misses"] += 1
                return None
            
            entry = self.cache[key]
            
            if entry.is_expired:
                del self.cache[key]
                self.stats["misses"] += 1
                return None
            
            entry.touch()
            self.stats["hits"] += 1
            return entry.value
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """
        Store value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            True if stored successfully
        """
        async with self._lock:
            try:
                # Use default TTL if not specified
                if ttl is None:
                    ttl = self.default_ttl
                
                # Evict expired entries if cache is full
                if len(self.cache) >= self.max_size:
                    await self._evict_entries()
                
                # Create cache entry
                entry = CacheEntry(
                    value=value,
                    created_at=time.time(),
                    ttl=ttl
                )
                
                self.cache[key] = entry
                self.stats["sets"] += 1
                
                logger.debug(f"Cached key '{key}' with TTL {ttl}")
                return True
                
            except Exception as e:
                logger.error(f"Error setting cache key '{key}': {e}")
                return False
    
    async def delete(self, key: str) -> bool:
        """
        Remove key from cache
        
        Args:
            key: Cache key to remove
            
        Returns:
            True if key was removed, False if not found
        """
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Deleted cache key '{key}'")
                return True
            return False
    
    async def clear(self) -> None:
        """Clear all cache entries"""
        async with self._lock:
            cleared_count = len(self.cache)
            self.cache.clear()
            logger.info(f"Cleared {cleared_count} cache entries")
    
    async def _evict_entries(self) -> None:
        """Evict expired and least recently used entries"""
        current_time = time.time()
        
        # First, remove expired entries
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired
        ]
        
        for key in expired_keys:
            del self.cache[key]
            self.stats["evictions"] += 1
        
        # If still over capacity, remove least recently used
        while len(self.cache) >= self.max_size:
            lru_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k].last_accessed
            )
            del self.cache[lru_key]
            self.stats["evictions"] += 1
    
    async def exists(self, key: str) -> bool:
        """Check if key exists and is not expired"""
        return await self.get(key) is not None
    
    async def size(self) -> int:
        """Get current cache size"""
        async with self._lock:
            return len(self.cache)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        async with self._lock:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0
            
            return {
                **self.stats,
                "size": len(self.cache),
                "hit_rate": hit_rate,
                "max_size": self.max_size
            }
    
    async def cleanup(self) -> int:
        """Remove all expired entries and return count"""
        async with self._lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry.is_expired
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
            return len(expired_keys)

# Global cache manager instance
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """Get or create global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager

# Convenience functions
async def cache_get(key: str) -> Optional[Any]:
    """Get value from global cache"""
    return await get_cache_manager().get(key)

async def cache_set(key: str, value: Any, ttl: Optional[float] = None) -> bool:
    """Set value in global cache"""
    return await get_cache_manager().set(key, value, ttl)

async def cache_delete(key: str) -> bool:
    """Delete key from global cache"""
    return await get_cache_manager().delete(key)

async def cache_clear() -> None:
    """Clear global cache"""
    await get_cache_manager().clear()
