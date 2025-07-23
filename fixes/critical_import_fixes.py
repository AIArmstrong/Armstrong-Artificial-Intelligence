#!/usr/bin/env python3
"""
Critical Import Fixes for AAI Modules
Automated fixes for the 18 critical import failures identified
"""

import os
import re
import shutil
from pathlib import Path

def fix_unified_intelligence_coordinator():
    """Fix missing defaultdict import"""
    file_path = "/mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py"
    
    print("🔧 Fixing unified_intelligence_coordinator.py - Adding defaultdict import")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if defaultdict import already exists
        if 'from collections import defaultdict' in content:
            print("   ✅ defaultdict import already exists")
            return True
            
        # Add the import after other imports
        import_pattern = r'(import\s+(?:asyncio|logging|json|sys|os|time|datetime)[^\n]*\n)'
        
        if re.search(import_pattern, content):
            # Insert after standard library imports
            new_content = re.sub(
                import_pattern,
                r'\1from collections import defaultdict\n',
                content,
                count=1
            )
        else:
            # Add at the beginning if no standard imports found
            new_content = 'from collections import defaultdict\n' + content
        
        # Create backup
        shutil.copy2(file_path, file_path + '.backup')
        
        # Write fixed content
        with open(file_path, 'w') as f:
            f.write(new_content)
            
        print("   ✅ Successfully added defaultdict import")
        return True
        
    except Exception as e:
        print(f"   ❌ Error fixing defaultdict import: {e}")
        return False

def fix_analyze_command_handler():
    """Fix import of non-existent analyze_orchestrator"""
    file_path = "/mnt/c/Users/Brandon/AAI/brain/modules/analyze_command_handler.py"
    
    print("🔧 Fixing analyze_command_handler.py - Fixing analyze_orchestrator import")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace the problematic import with a try/except pattern
        old_import = r'from analyze_orchestrator import AnalysisOrchestrator, AnalysisFocus, AnalysisDepth'
        new_import = '''try:
    from analyze_orchestrator import AnalysisOrchestrator, AnalysisFocus, AnalysisDepth
except ImportError:
    # Fallback if analyze_orchestrator is not available
    from brain.modules.analyze_orchestrator import AnalysisOrchestrator, AnalysisFocus, AnalysisDepth'''
        
        if old_import in content:
            new_content = content.replace(old_import, new_import)
            
            # Create backup
            shutil.copy2(file_path, file_path + '.backup')
            
            # Write fixed content
            with open(file_path, 'w') as f:
                f.write(new_content)
                
            print("   ✅ Successfully fixed analyze_orchestrator import")
            return True
        else:
            print("   ℹ️  Import pattern not found or already fixed")
            return True
            
    except Exception as e:
        print(f"   ❌ Error fixing analyze_orchestrator import: {e}")
        return False

def fix_relative_imports(module_path, package_name):
    """Fix relative imports in agent modules"""
    print(f"🔧 Fixing relative imports in {os.path.basename(module_path)}")
    
    try:
        with open(module_path, 'r') as f:
            content = f.read()
        
        # Pattern to match relative imports
        relative_import_pattern = r'from\s+\.(\w+)\s+import\s+([^\n]+)'
        
        def replace_relative_import(match):
            module = match.group(1)
            imports = match.group(2)
            
            return f'''try:
    from .{module} import {imports}
except ImportError:
    from {package_name}.{module} import {imports}'''
        
        # Replace all relative imports
        new_content = re.sub(relative_import_pattern, replace_relative_import, content)
        
        if new_content != content:
            # Create backup
            shutil.copy2(module_path, module_path + '.backup')
            
            # Write fixed content
            with open(module_path, 'w') as f:
                f.write(new_content)
                
            print(f"   ✅ Successfully fixed relative imports")
            return True
        else:
            print(f"   ℹ️  No relative imports found or already fixed")
            return True
            
    except Exception as e:
        print(f"   ❌ Error fixing relative imports: {e}")
        return False

def create_missing_cache_manager():
    """Create missing cache_manager module"""
    cache_manager_path = "/mnt/c/Users/Brandon/AAI/core/cache_manager.py"
    
    print("🔧 Creating missing cache_manager.py")
    
    if os.path.exists(cache_manager_path):
        print("   ℹ️  cache_manager.py already exists")
        return True
    
    cache_manager_content = '''"""
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
'''
    
    try:
        # Ensure core directory exists
        os.makedirs(os.path.dirname(cache_manager_path), exist_ok=True)
        
        with open(cache_manager_path, 'w') as f:
            f.write(cache_manager_content)
        
        print("   ✅ Successfully created cache_manager.py")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating cache_manager.py: {e}")
        return False

def create_requirements_file():
    """Create requirements.txt with missing dependencies"""
    requirements_path = "/mnt/c/Users/Brandon/AAI/requirements_fixes.txt"
    
    print("🔧 Creating requirements_fixes.txt for missing dependencies")
    
    missing_deps = [
        "matplotlib>=3.5.0",
        "docker>=6.0.0", 
        "aiofiles>=23.0.0",
        "aiohttp>=3.8.0",
        "asyncio-mqtt>=0.11.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0"
    ]
    
    try:
        with open(requirements_path, 'w') as f:
            f.write("# Missing dependencies identified in comprehensive testing\n")
            f.write("# Install with: pip install -r requirements_fixes.txt\n\n")
            for dep in missing_deps:
                f.write(f"{dep}\n")
        
        print("   ✅ Successfully created requirements_fixes.txt")
        print(f"   📄 Install with: pip install -r {requirements_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating requirements file: {e}")
        return False

def main():
    """Execute all critical import fixes"""
    print("🚀 Starting Critical Import Fixes for AAI Modules")
    print("="*60)
    
    fixes_applied = 0
    total_fixes = 0
    
    # Fix 1: defaultdict import
    total_fixes += 1
    if fix_unified_intelligence_coordinator():
        fixes_applied += 1
    
    # Fix 2: analyze_orchestrator import
    total_fixes += 1
    if fix_analyze_command_handler():
        fixes_applied += 1
    
    # Fix 3: Create missing cache manager
    total_fixes += 1
    if create_missing_cache_manager():
        fixes_applied += 1
    
    # Fix 4: Create requirements file
    total_fixes += 1
    if create_requirements_file():
        fixes_applied += 1
    
    # Fix 5-16: Relative imports in agent modules
    agent_modules = [
        ("/mnt/c/Users/Brandon/AAI/mcp/server_manager.py", "mcp"),
        ("/mnt/c/Users/Brandon/AAI/agents/orchestration/delegation_engine.py", "agents.orchestration"),
        ("/mnt/c/Users/Brandon/AAI/agents/orchestration/primary_agent.py", "agents.orchestration"),
        ("/mnt/c/Users/Brandon/AAI/agents/tech_expert/conversation_engine.py", "agents.tech_expert"),
        ("/mnt/c/Users/Brandon/AAI/agents/tech_expert/recommender.py", "agents.tech_expert"),
        ("/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py", "agents.r1_reasoning"),
        ("/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py", "agents.r1_reasoning"),
        ("/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/confidence_scorer.py", "agents.r1_reasoning"),
        ("/mnt/c/Users/Brandon/AAI/agents/tool-selection/tool_selector.py", "agents.tool_selection"),
        ("/mnt/c/Users/Brandon/AAI/agents/tool-selection/learning_engine.py", "agents.tool_selection"),
        ("/mnt/c/Users/Brandon/AAI/agents/tool-selection/fabric_integrator.py", "agents.tool_selection"),
        ("/mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py", "agents.tool_selection"),
        ("/mnt/c/Users/Brandon/AAI/agents/tool-selection/confidence_scorer.py", "agents.tool_selection"),
    ]
    
    for module_path, package_name in agent_modules:
        total_fixes += 1
        if os.path.exists(module_path):
            if fix_relative_imports(module_path, package_name):
                fixes_applied += 1
        else:
            print(f"   ⚠️  Module not found: {module_path}")
    
    print("\n" + "="*60)
    print(f"✅ FIXES COMPLETED: {fixes_applied}/{total_fixes} successful")
    
    if fixes_applied == total_fixes:
        print("🎉 All critical import fixes applied successfully!")
        print("\n📋 NEXT STEPS:")
        print("1. Install missing dependencies: pip install -r requirements_fixes.txt")
        print("2. Run comprehensive test again to verify fixes")
        print("3. Proceed to Phase 2: Async Pattern Fixes")
    else:
        print(f"⚠️  {total_fixes - fixes_applied} fixes failed - review errors above")
        print("🔍 Check backup files (*.backup) if rollback needed")
    
    print("\n📁 Backup files created for all modified modules")
    print("🔄 Run: python tests/comprehensive_module_test.py to validate fixes")

if __name__ == "__main__":
    main()