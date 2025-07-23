#!/usr/bin/env python3
"""
Performance tests for Enhanced Repository Analyzer
Validates 60-80% I/O improvement and other performance targets
"""

import asyncio
import pytest
import time
import psutil
import tempfile
from pathlib import Path
from typing import List

from core.streaming_walker import StreamingFileWalker, FileInfo
from core.cache_manager import CacheManager
from agents.structure_agent import StructureAgent

@pytest.mark.performance
@pytest.mark.asyncio
async def test_streaming_walker_performance(test_repository, performance_targets):
    """
    Validate 60-80% I/O improvement vs multiple traversals.
    This is a critical requirement from the PRP.
    """
    repo_path = test_repository
    
    # Test single-pass traversal
    walker = StreamingFileWalker(max_concurrent=4, batch_size=20)
    
    start_time = time.perf_counter()
    single_pass_results = []
    
    async for batch_result in walker.walk_repository(repo_path):
        single_pass_results.append(batch_result)
    
    single_pass_time = time.perf_counter() - start_time
    
    # Simulate traditional multiple traversals
    start_time = time.perf_counter()
    
    # First pass: count files
    file_count = 0
    for file_path in repo_path.rglob("*"):
        if file_path.is_file():
            file_count += 1
    
    # Second pass: analyze structure
    structure_files = []
    for file_path in repo_path.rglob("*.py"):
        structure_files.append(file_path)
    
    # Third pass: check patterns
    pattern_files = []
    for file_path in repo_path.rglob("*"):
        if file_path.is_file():
            pattern_files.append(file_path)
    
    multiple_pass_time = time.perf_counter() - start_time
    
    # Calculate improvement
    if multiple_pass_time > 0:
        improvement = (multiple_pass_time - single_pass_time) / multiple_pass_time
    else:
        improvement = 0
    
    print(f"Single pass time: {single_pass_time:.3f}s")
    print(f"Multiple pass time: {multiple_pass_time:.3f}s")
    print(f"Improvement: {improvement:.1%}")
    
    # Validate 60% minimum improvement
    assert improvement >= 0.6, f"Only {improvement:.1%} improvement, need ≥60%"
    
    # Validate execution time is reasonable
    assert single_pass_time <= performance_targets['max_execution_time']

@pytest.mark.performance
@pytest.mark.asyncio
async def test_cache_performance(temp_cache_dir):
    """Validate caching provides expected speedup"""
    cache_manager = CacheManager(
        memory_size=100,
        disk_cache_dir=temp_cache_dir
    )
    
    # Define expensive operation
    async def expensive_analysis(data: str) -> dict:
        await asyncio.sleep(0.1)  # Simulate processing time
        return {'processed': True, 'length': len(data), 'data': data}
    
    test_data = "This is test data for cache performance validation"
    cache_key = "test_performance_key"
    
    # First run - cache miss
    start_time = time.perf_counter()
    result1 = await cache_manager.cached_analysis(
        cache_key, expensive_analysis, test_data
    )
    first_run_time = time.perf_counter() - start_time
    
    # Second run - cache hit
    start_time = time.perf_counter()
    result2 = await cache_manager.cached_analysis(
        cache_key, expensive_analysis, test_data
    )
    second_run_time = time.perf_counter() - start_time
    
    # Calculate speedup
    speedup = first_run_time / second_run_time if second_run_time > 0 else 0
    
    print(f"First run (cache miss): {first_run_time:.3f}s")
    print(f"Second run (cache hit): {second_run_time:.3f}s")
    print(f"Cache speedup: {speedup:.1f}x")
    
    # Validate cache provides significant speedup
    assert speedup >= 10, f"Cache speedup {speedup:.1f}x below 10x expectation"
    assert result1 == result2, "Cached result differs from original"

@pytest.mark.performance
@pytest.mark.asyncio
async def test_semantic_analysis_accuracy(sample_python_code):
    """Validate 85%+ semantic analysis accuracy"""
    from core.semantic_analyzer import SemanticAnalyzer
    
    # Initialize without LLM for consistent testing
    analyzer = SemanticAnalyzer(openrouter_client=None)
    
    # Analyze the sample code
    features = await analyzer.analyze_code(sample_python_code, 'python', use_llm=False)
    
    # Validate expected features are detected
    expected_features = {
        'DataProcessor': 'class',
        'process_data': 'function',
        '_process_item': 'function'
    }
    
    detected_features = {f.name: f.type for f in features}
    
    # Calculate accuracy
    correct_detections = 0
    for name, expected_type in expected_features.items():
        if name in detected_features and detected_features[name] == expected_type:
            correct_detections += 1
    
    accuracy = correct_detections / len(expected_features)
    
    print(f"Expected features: {expected_features}")
    print(f"Detected features: {detected_features}")
    print(f"Accuracy: {accuracy:.1%}")
    
    # Validate 85%+ accuracy requirement
    assert accuracy >= 0.85, f"Accuracy {accuracy:.1%} below 85% requirement"

@pytest.mark.performance
@pytest.mark.asyncio
async def test_memory_usage_limits(test_repository, performance_targets):
    """Validate memory usage stays within limits"""
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Perform analysis
    walker = StreamingFileWalker()
    agent = StructureAgent()
    
    peak_memory = initial_memory
    
    async for batch_result in walker.walk_repository(test_repository):
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        peak_memory = max(peak_memory, current_memory)
    
    memory_used = peak_memory - initial_memory
    
    print(f"Initial memory: {initial_memory:.1f} MB")
    print(f"Peak memory: {peak_memory:.1f} MB")
    print(f"Memory used: {memory_used:.1f} MB")
    
    # Validate memory usage is reasonable
    assert memory_used <= performance_targets['max_memory_mb'], \
        f"Memory usage {memory_used:.1f}MB exceeds limit {performance_targets['max_memory_mb']}MB"

@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_concurrent_processing_scalability():
    """Test scalability with different concurrency levels"""
    # Create test repository
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create 100 test files
        for i in range(100):
            file_path = repo_path / f"test_{i}.py"
            with open(file_path, "w") as f:
                f.write(f"""
def function_{i}():
    '''Function {i}'''
    return {i}

class Class{i}:
    '''Class {i}'''
    def method(self):
        return function_{i}()
""")
        
        # Test different concurrency levels
        concurrency_levels = [1, 2, 4, 8]
        results = {}
        
        for max_concurrent in concurrency_levels:
            walker = StreamingFileWalker(max_concurrent=max_concurrent)
            
            start_time = time.perf_counter()
            batch_count = 0
            
            async for batch_result in walker.walk_repository(repo_path):
                batch_count += 1
            
            execution_time = time.perf_counter() - start_time
            results[max_concurrent] = execution_time
            
            print(f"Concurrency {max_concurrent}: {execution_time:.3f}s")
        
        # Validate that higher concurrency improves performance
        assert results[4] <= results[1], "Concurrency should improve performance"

@pytest.mark.performance
@pytest.mark.asyncio
async def test_large_repository_handling():
    """Test handling of large repositories (100MB+ simulation)"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create larger test repository
        total_size = 0
        file_count = 0
        
        # Create files until we reach ~10MB (scaled down for testing)
        while total_size < 10 * 1024 * 1024 and file_count < 500:  # 10MB, max 500 files
            file_path = repo_path / f"large_file_{file_count}.py"
            
            # Create file with substantial content
            content = f"""
# Large file {file_count}
import asyncio
import logging
from typing import Dict, List, Optional, Any

class LargeClass{file_count}:
    '''Large class for testing with substantial content'''
    
    def __init__(self):
        self.data = {{'key_{i}': f'value_{i}' for i in range(100)}}
        self.logger = logging.getLogger(__name__)
    
    async def process_large_data(self, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        '''Process large amounts of data'''
        results = {{}}
        
        for item in items:
            try:
                processed = await self._process_item(item)
                results[item.get('id', 'unknown')] = processed
            except Exception as e:
                self.logger.error(f'Processing failed: {{e}}')
                continue
        
        return results if results else None
    
    async def _process_item(self, item: Dict[str, Any]) -> Any:
        '''Process individual item with complex logic'''
        await asyncio.sleep(0.001)  # Simulate processing
        
        if 'transform' in item:
            return self._transform_data(item['transform'])
        elif 'calculate' in item:
            return self._calculate_value(item['calculate'])
        else:
            return item
    
    def _transform_data(self, data: Any) -> Any:
        '''Transform data with complex operations'''
        if isinstance(data, str):
            return data.upper().replace(' ', '_')
        elif isinstance(data, (int, float)):
            return data * 2
        elif isinstance(data, list):
            return [self._transform_data(item) for item in data]
        elif isinstance(data, dict):
            return {{k: self._transform_data(v) for k, v in data.items()}}
        return data
    
    def _calculate_value(self, expression: str) -> float:
        '''Calculate numeric value from expression'''
        try:
            # Safe evaluation of simple expressions
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                return eval(expression)  # Note: Limited safe eval for testing
        except:
            pass
        return 0.0

# Multiple function definitions
""" + "\n".join([f"def utility_function_{i}(): return {i}" for i in range(50)])
            
            with open(file_path, "w") as f:
                f.write(content)
            
            total_size += len(content.encode())
            file_count += 1
        
        print(f"Created test repository: {file_count} files, {total_size / 1024 / 1024:.1f} MB")
        
        # Test analysis performance
        walker = StreamingFileWalker(max_concurrent=4)
        
        start_time = time.perf_counter()
        total_files_processed = 0
        
        async for batch_result in walker.walk_repository(repo_path):
            total_files_processed += batch_result.files_processed
        
        execution_time = time.perf_counter() - start_time
        files_per_second = total_files_processed / execution_time if execution_time > 0 else 0
        
        print(f"Processed {total_files_processed} files in {execution_time:.3f}s")
        print(f"Rate: {files_per_second:.1f} files/second")
        
        # Validate reasonable performance for large repositories
        assert files_per_second >= 10, f"Processing rate {files_per_second:.1f} files/s too slow"
        assert execution_time <= 60, f"Processing took {execution_time:.1f}s, should be under 60s"

@pytest.mark.performance
def test_pattern_registry_performance():
    """Test pattern matching performance"""
    from core.pattern_registry import PatternRegistry
    
    registry = PatternRegistry()
    
    # Test content with various patterns
    test_content = """
import asyncio
import requests

# TODO: Fix this security issue
password = "hardcoded_secret_123"

async def fetch_data():
    # This is a synchronous call in async function
    response = requests.get("http://example.com")
    return response.json()

def long_function_with_many_parameters(param1, param2, param3, param4, param5, param6, param7, param8, param9, param10):
    # This line is way too long and exceeds the normal line length limit of 80 or 120 characters which is commonly used in many projects
    pass

class BadClass:
    def method(self):
        # FIXME: This needs to be refactored
        pass
"""
    
    # Test regex pattern matching performance
    start_time = time.perf_counter()
    
    matches = []
    for _ in range(100):  # Run multiple times to test performance
        batch_matches = registry.match_regex_patterns(test_content)
        matches.extend(batch_matches)
    
    execution_time = time.perf_counter() - start_time
    
    print(f"Pattern matching took {execution_time:.3f}s for 100 iterations")
    print(f"Found {len(matches)} total matches")
    
    # Validate performance is reasonable
    assert execution_time <= 1.0, f"Pattern matching too slow: {execution_time:.3f}s"
    
    # Validate patterns are detected
    pattern_names = {match.pattern_name for match in matches}
    expected_patterns = {'hardcoded_secret', 'todo_fixme', 'long_line', 'synchronous_io_in_async'}
    
    detected_expected = pattern_names.intersection(expected_patterns)
    print(f"Detected expected patterns: {detected_expected}")
    
    # Should detect at least some expected patterns
    assert len(detected_expected) >= 2, f"Expected to detect more patterns, got: {pattern_names}"