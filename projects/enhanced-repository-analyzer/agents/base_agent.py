#!/usr/bin/env python3
"""
BaseAgent - Enhanced base class for all analyzer agents with streaming support
Extends the existing agent pattern with async processing and caching
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncIterator, Set
from datetime import datetime

from core.cache_manager import CacheManager
from core.pattern_registry import PatternRegistry, PatternMatch
from core.streaming_walker import FileInfo

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Enhanced analysis result with streaming support"""
    agent_name: str
    success: bool
    execution_time: float
    data: Dict[str, Any]
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    patterns_matched: List[PatternMatch] = field(default_factory=list)
    cache_hit: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class StreamingAnalysisResult:
    """Result for streaming analysis operations"""
    file_path: Path
    agent_name: str
    analysis_type: str
    data: Dict[str, Any]
    processing_time: float
    success: bool = True
    error: Optional[str] = None

class BaseAnalyzerAgent(ABC):
    """
    Enhanced base class for all analyzer agents with streaming and caching support.
    Provides common functionality for file processing and pattern matching.
    """
    
    def __init__(self, 
                 name: str,
                 cache_manager: Optional[CacheManager] = None,
                 pattern_registry: Optional[PatternRegistry] = None,
                 timeout: int = 300):
        """
        Initialize base analyzer agent.
        
        Args:
            name: Agent name
            cache_manager: Optional cache manager for result caching
            pattern_registry: Optional pattern registry for pattern matching
            timeout: Maximum execution time in seconds
        """
        self.name = name
        self.timeout = timeout
        self.cache_manager = cache_manager
        self.pattern_registry = pattern_registry
        
        # Agent capabilities
        self.supported_extensions: Set[str] = set()
        self.supported_mime_types: Set[str] = set()
        self.analysis_types: List[str] = []
        
        # Performance tracking
        self.total_files_processed = 0
        self.total_processing_time = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
    
    @abstractmethod
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """
        Perform full repository analysis (legacy compatibility).
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Complete analysis result
        """
        pass
    
    @abstractmethod
    async def process_file(self, file_info: FileInfo) -> Dict[str, Any]:
        """
        Process a single file for streaming analysis.
        
        Args:
            file_info: File information
            
        Returns:
            Analysis data for the file
        """
        pass
    
    async def analyze_streaming(self, 
                              files: AsyncIterator[FileInfo],
                              progress_callback: Optional[callable] = None) -> AsyncIterator[StreamingAnalysisResult]:
        """
        Analyze files in streaming mode.
        
        Args:
            files: Async iterator of files to process
            progress_callback: Optional callback for progress updates
            
        Yields:
            Streaming analysis results as they complete
        """
        processed = 0
        
        async for file_info in files:
            # Check if we support this file type
            if not self._can_process_file(file_info):
                continue
            
            start_time = time.time()
            
            try:
                # Try cache first if available
                result_data = None
                cache_key = None
                
                if self.cache_manager:
                    cache_key = f"{self.name}:{file_info.path}"
                    result_data = await self.cache_manager.get(cache_key)
                    
                    if result_data is not None:
                        self.cache_hits += 1
                        processing_time = time.time() - start_time
                        
                        yield StreamingAnalysisResult(
                            file_path=file_info.path,
                            agent_name=self.name,
                            analysis_type='cached',
                            data=result_data,
                            processing_time=processing_time
                        )
                        
                        processed += 1
                        if progress_callback:
                            await progress_callback(processed, file_info.path)
                        continue
                
                # Cache miss - process file
                self.cache_misses += 1
                result_data = await self.process_file(file_info)
                
                # Cache result if available
                if self.cache_manager and cache_key:
                    await self.cache_manager.set(cache_key, result_data, tags=[self.name])
                
                processing_time = time.time() - start_time
                self.total_processing_time += processing_time
                self.total_files_processed += 1
                
                yield StreamingAnalysisResult(
                    file_path=file_info.path,
                    agent_name=self.name,
                    analysis_type='processed',
                    data=result_data,
                    processing_time=processing_time
                )
                
                processed += 1
                if progress_callback:
                    await progress_callback(processed, file_info.path)
                    
            except Exception as e:
                logger.error(f"Error processing {file_info.path}: {e}")
                
                yield StreamingAnalysisResult(
                    file_path=file_info.path,
                    agent_name=self.name,
                    analysis_type='error',
                    data={},
                    processing_time=time.time() - start_time,
                    success=False,
                    error=str(e)
                )
    
    def _can_process_file(self, file_info: FileInfo) -> bool:
        """Check if agent can process this file type"""
        if self.supported_extensions and file_info.extension not in self.supported_extensions:
            return False
            
        if self.supported_mime_types and file_info.mime_type and file_info.mime_type not in self.supported_mime_types:
            return False
            
        return True
    
    async def match_patterns(self, 
                           content: str,
                           file_path: Path,
                           pattern_tags: Optional[List[str]] = None) -> List[PatternMatch]:
        """
        Match patterns against file content.
        
        Args:
            content: File content
            file_path: Path to file
            pattern_tags: Optional tags to filter patterns
            
        Returns:
            List of pattern matches
        """
        if not self.pattern_registry:
            return []
        
        # Match regex patterns
        matches = self.pattern_registry.match_regex_patterns(
            content=content,
            tags=pattern_tags,
            min_confidence=0.5
        )
        
        # Add file context to matches
        for match in matches:
            if not match.metadata:
                match.metadata = {}
            match.metadata['file_path'] = str(file_path)
            match.metadata['agent'] = self.name
        
        return matches
    
    def _create_result(self, 
                      success: bool,
                      data: Dict[str, Any],
                      execution_time: float,
                      errors: List[str] = None,
                      warnings: List[str] = None,
                      patterns_matched: List[PatternMatch] = None,
                      cache_hit: bool = False) -> AnalysisResult:
        """Helper to create standardized results"""
        return AnalysisResult(
            agent_name=self.name,
            success=success,
            execution_time=execution_time,
            data=data or {},
            errors=errors or [],
            warnings=warnings or [],
            patterns_matched=patterns_matched or [],
            cache_hit=cache_hit
        )
    
    async def _read_file_content(self, file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
        """
        Read file content with error handling.
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            File content or None if error
        """
        try:
            # Use asyncio for non-blocking file read
            loop = asyncio.get_event_loop()
            
            def read_file():
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            
            content = await loop.run_in_executor(None, read_file)
            return content
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                def read_file_latin1():
                    with open(file_path, 'r', encoding='latin-1') as f:
                        return f.read()
                
                content = await loop.run_in_executor(None, read_file_latin1)
                return content
            except Exception as e:
                logger.warning(f"Failed to read {file_path} with fallback encoding: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get agent performance statistics"""
        cache_hit_rate = 0.0
        if self.cache_hits + self.cache_misses > 0:
            cache_hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses)
        
        avg_processing_time = 0.0
        if self.total_files_processed > 0:
            avg_processing_time = self.total_processing_time / self.total_files_processed
        
        return {
            'agent_name': self.name,
            'total_files_processed': self.total_files_processed,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': avg_processing_time,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': cache_hit_rate,
            'supported_extensions': list(self.supported_extensions),
            'analysis_types': self.analysis_types
        }
    
    async def initialize(self) -> None:
        """Initialize agent resources (override in subclasses if needed)"""
        logger.info(f"Initializing {self.name}")
    
    async def cleanup(self) -> None:
        """Clean up agent resources (override in subclasses if needed)"""
        logger.info(f"Cleaning up {self.name}")