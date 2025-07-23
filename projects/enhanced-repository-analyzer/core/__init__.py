"""
Core infrastructure modules for the Enhanced Repository Analyzer
"""

from .streaming_walker import StreamingFileWalker, FileInfo, FileProcessingResult, BatchProcessingResult
from .cache_manager import CacheManager, LRUCache
from .pattern_registry import PatternRegistry, CompiledPattern, PatternMatch

__all__ = [
    'StreamingFileWalker',
    'FileInfo',
    'FileProcessingResult',
    'BatchProcessingResult',
    'CacheManager',
    'LRUCache',
    'PatternRegistry',
    'CompiledPattern',
    'PatternMatch'
]