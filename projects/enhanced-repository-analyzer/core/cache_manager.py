#!/usr/bin/env python3
"""
CacheManager - Multi-layer caching system with LRU memory cache and persistent disk cache
Provides significant performance improvements for repeated operations
"""

import asyncio
import hashlib
import json
import logging
import pickle
import time
from collections import OrderedDict
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import diskcache
import aiosqlite

logger = logging.getLogger(__name__)

class LRUCache:
    """
    Thread-safe Least Recently Used (LRU) cache implementation.
    """
    
    def __init__(self, maxsize: int = 1000):
        """
        Initialize LRU cache with maximum size.
        
        Args:
            maxsize: Maximum number of items to store in cache
        """
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self._lock = asyncio.Lock()
        self.hits = 0
        self.misses = 0
    
    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache, updating access order"""
        async with self._lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                self.hits += 1
                return self.cache[key]
            self.misses += 1
            return None
    
    async def set(self, key: str, value: Any) -> None:
        """Set item in cache, evicting LRU item if needed"""
        async with self._lock:
            if key in self.cache:
                # Update existing key
                self.cache.move_to_end(key)
                self.cache[key] = value
            else:
                # Add new key
                self.cache[key] = value
                if len(self.cache) > self.maxsize:
                    # Remove least recently used item
                    self.cache.popitem(last=False)
    
    async def delete(self, key: str) -> bool:
        """Delete item from cache"""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    async def clear(self) -> None:
        """Clear all items from cache"""
        async with self._lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'maxsize': self.maxsize,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'total_requests': total
        }

class CacheManager:
    """
    Multi-layer caching system with memory and disk persistence.
    Implements caching strategies for various analysis operations.
    """
    
    def __init__(self, 
                 memory_size: int = 1000,
                 disk_cache_dir: Optional[Path] = None,
                 db_path: Optional[Path] = None,
                 ttl_hours: int = 24):
        """
        Initialize cache manager with multi-layer caching.
        
        Args:
            memory_size: Maximum items in memory cache
            disk_cache_dir: Directory for disk cache storage
            db_path: Path to SQLite database for metadata
            ttl_hours: Time-to-live for cached items in hours
        """
        self.memory_cache = LRUCache(maxsize=memory_size)
        self.disk_cache_dir = disk_cache_dir or Path('.cache')
        self.disk_cache = diskcache.Cache(str(self.disk_cache_dir))
        self.db_path = db_path or self.disk_cache_dir / 'cache_metadata.db'
        self.ttl = timedelta(hours=ttl_hours)
        
        # Ensure cache directory exists
        self.disk_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database synchronously
        self._init_database_sync()
        
        # Cache statistics
        self.stats = {
            'memory_hits': 0,
            'disk_hits': 0,
            'cache_misses': 0,
            'cache_sets': 0,
            'evictions': 0
        }
    
    def _init_database_sync(self):
        """Initialize SQLite database for cache metadata (synchronous)"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_metadata (
                cache_key TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                access_count INTEGER DEFAULT 1,
                size_bytes INTEGER,
                tags TEXT  -- JSON array of tags
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cache_created 
            ON cache_metadata(created_at)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cache_accessed 
            ON cache_metadata(last_accessed)
        ''')
        
        conn.commit()
        conn.close()
    
    async def _init_database(self):
        """Initialize SQLite database for cache metadata (async)"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS cache_metadata (
                    cache_key TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    access_count INTEGER DEFAULT 1,
                    size_bytes INTEGER,
                    tags TEXT  -- JSON array of tags
                )
            ''')
            
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_cache_created 
                ON cache_metadata(created_at)
            ''')
            
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_cache_accessed 
                ON cache_metadata(last_accessed)
            ''')
            
            await db.commit()
    
    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate consistent cache key from arguments"""
        # Create a string representation of all arguments
        key_parts = []
        
        # Add positional arguments
        for arg in args:
            if isinstance(arg, (str, int, float, bool, type(None))):
                key_parts.append(str(arg))
            else:
                # For complex objects, use pickle
                key_parts.append(hashlib.md5(
                    pickle.dumps(arg, protocol=pickle.HIGHEST_PROTOCOL)
                ).hexdigest())
        
        # Add keyword arguments in sorted order
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        
        # Generate hash of all parts
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    async def get(self, cache_key: str) -> Optional[Any]:
        """
        Get item from cache, checking memory first, then disk.
        
        Args:
            cache_key: Key to retrieve
            
        Returns:
            Cached value or None if not found
        """
        # Check memory cache first
        value = await self.memory_cache.get(cache_key)
        if value is not None:
            self.stats['memory_hits'] += 1
            await self._update_metadata(cache_key)
            return value
        
        # Check disk cache
        try:
            value = self.disk_cache.get(cache_key)
            if value is not None:
                self.stats['disk_hits'] += 1
                # Promote to memory cache
                await self.memory_cache.set(cache_key, value)
                await self._update_metadata(cache_key)
                return value
        except Exception as e:
            logger.error(f"Error reading from disk cache: {e}")
        
        self.stats['cache_misses'] += 1
        return None
    
    async def set(self, cache_key: str, value: Any, tags: Optional[List[str]] = None) -> None:
        """
        Set item in both memory and disk cache.
        
        Args:
            cache_key: Key to store under
            value: Value to cache
            tags: Optional tags for categorization
        """
        self.stats['cache_sets'] += 1
        
        # Store in memory cache
        await self.memory_cache.set(cache_key, value)
        
        # Store in disk cache with TTL
        try:
            self.disk_cache.set(cache_key, value, expire=self.ttl.total_seconds())
        except Exception as e:
            logger.error(f"Error writing to disk cache: {e}")
        
        # Update metadata
        await self._store_metadata(cache_key, value, tags)
    
    async def delete(self, cache_key: str) -> bool:
        """Delete item from all cache layers"""
        memory_deleted = await self.memory_cache.delete(cache_key)
        
        disk_deleted = False
        try:
            disk_deleted = self.disk_cache.delete(cache_key)
        except Exception as e:
            logger.error(f"Error deleting from disk cache: {e}")
        
        # Delete metadata
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM cache_metadata WHERE cache_key = ?",
                (cache_key,)
            )
            await db.commit()
        
        return memory_deleted or disk_deleted
    
    async def clear_expired(self) -> int:
        """Clear expired items from cache"""
        expired_count = 0
        cutoff_time = datetime.now() - self.ttl
        
        async with aiosqlite.connect(self.db_path) as db:
            # Find expired keys
            async with db.execute(
                "SELECT cache_key FROM cache_metadata WHERE created_at < ?",
                (cutoff_time.isoformat(),)
            ) as cursor:
                expired_keys = [row[0] for row in await cursor.fetchall()]
            
            # Delete expired items
            for key in expired_keys:
                if await self.delete(key):
                    expired_count += 1
        
        self.stats['evictions'] += expired_count
        return expired_count
    
    async def cached_analysis(self, 
                            cache_key: str,
                            analysis_func: Callable,
                            *args,
                            force_refresh: bool = False,
                            tags: Optional[List[str]] = None,
                            **kwargs) -> Any:
        """
        Execute analysis function with caching.
        
        Args:
            cache_key: Key for caching
            analysis_func: Async function to execute if cache miss
            force_refresh: Force re-computation even if cached
            tags: Tags for categorization
            *args, **kwargs: Arguments for analysis function
            
        Returns:
            Analysis result (from cache or newly computed)
        """
        if not force_refresh:
            # Try to get from cache
            cached_result = await self.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
        
        # Compute result
        logger.debug(f"Cache miss for key: {cache_key}, computing...")
        start_time = time.time()
        
        try:
            result = await analysis_func(*args, **kwargs)
            computation_time = time.time() - start_time
            
            # Cache the result
            await self.set(cache_key, result, tags)
            
            logger.info(f"Computed and cached result in {computation_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error in cached analysis: {e}")
            raise
    
    async def _store_metadata(self, cache_key: str, value: Any, tags: Optional[List[str]] = None):
        """Store cache metadata in database"""
        try:
            # Estimate size
            size_bytes = len(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL))
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO cache_metadata 
                    (cache_key, created_at, last_accessed, access_count, size_bytes, tags)
                    VALUES (?, ?, ?, 1, ?, ?)
                ''', (
                    cache_key,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    size_bytes,
                    json.dumps(tags or [])
                ))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error storing cache metadata: {e}")
    
    async def _update_metadata(self, cache_key: str):
        """Update access metadata for cache key"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    UPDATE cache_metadata 
                    SET last_accessed = ?, access_count = access_count + 1
                    WHERE cache_key = ?
                ''', (datetime.now().isoformat(), cache_key))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error updating cache metadata: {e}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        memory_stats = self.memory_cache.get_stats()
        
        # Get disk cache stats
        disk_stats = {
            'size': len(self.disk_cache),
            'volume': self.disk_cache.volume(),
            'directory': str(self.disk_cache_dir)
        }
        
        # Get metadata stats
        metadata_stats = {}
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(
                    "SELECT COUNT(*), SUM(size_bytes), AVG(access_count) FROM cache_metadata"
                ) as cursor:
                    row = await cursor.fetchone()
                    metadata_stats = {
                        'total_entries': row[0] or 0,
                        'total_size_mb': (row[1] or 0) / (1024 * 1024),
                        'avg_access_count': row[2] or 0
                    }
        except Exception as e:
            logger.error(f"Error getting metadata stats: {e}")
        
        # Calculate overall hit rate
        total_hits = self.stats['memory_hits'] + self.stats['disk_hits']
        total_requests = total_hits + self.stats['cache_misses']
        overall_hit_rate = total_hits / total_requests if total_requests > 0 else 0
        
        return {
            'memory_cache': memory_stats,
            'disk_cache': disk_stats,
            'metadata': metadata_stats,
            'performance': {
                'memory_hits': self.stats['memory_hits'],
                'disk_hits': self.stats['disk_hits'],
                'cache_misses': self.stats['cache_misses'],
                'cache_sets': self.stats['cache_sets'],
                'evictions': self.stats['evictions'],
                'overall_hit_rate': overall_hit_rate,
                'memory_hit_rate': self.stats['memory_hits'] / total_requests if total_requests > 0 else 0,
                'disk_hit_rate': self.stats['disk_hits'] / total_requests if total_requests > 0 else 0
            }
        }
    
    def cache_method(self, ttl_override: Optional[int] = None, tags: Optional[List[str]] = None):
        """
        Decorator for caching method results.
        
        Args:
            ttl_override: Override default TTL in hours
            tags: Tags for categorization
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                # Generate cache key from function name and arguments
                cache_key = f"{func.__name__}:{self._generate_cache_key(*args, **kwargs)}"
                
                return await self.cached_analysis(
                    cache_key=cache_key,
                    analysis_func=func,
                    tags=tags,
                    *args,
                    **kwargs
                )
            return wrapper
        return decorator