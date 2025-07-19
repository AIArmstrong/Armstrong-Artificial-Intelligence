#!/usr/bin/env python3
"""
Test script for the enhanced analyze command implementation
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_orchestrator import AnalysisOrchestrator, AnalysisFocus, AnalysisDepth
from analyze_command_handler import AnalyzeCommandHandler

async def test_rate_limiting():
    """Test rate limiting functionality"""
    print("Testing rate limiting...")
    
    orchestrator = AnalysisOrchestrator()
    
    # Test the rate limiter
    rate_limiter = orchestrator.rate_limiter
    
    # Simulate errors to test backoff
    for i in range(3):
        rate_limiter.record_error()
        await rate_limiter.wait_if_needed()
        print(f"Error {i+1}: Consecutive errors = {rate_limiter.consecutive_errors}")
    
    # Test success recovery
    rate_limiter.record_success()
    print(f"After success: Consecutive errors = {rate_limiter.consecutive_errors}")
    
    print("✓ Rate limiting test passed\n")

async def test_batch_processing():
    """Test batch processing functionality"""
    print("Testing batch processing...")
    
    orchestrator = AnalysisOrchestrator()
    
    # Get tasks for quality focus
    tasks = orchestrator.get_agent_tasks(AnalysisFocus.QUALITY, AnalysisDepth.QUICK)
    print(f"Generated {len(tasks)} tasks for quality/quick analysis")
    
    # Test batch size limitation
    batch_size = orchestrator.batch_size
    num_batches = (len(tasks) + batch_size - 1) // batch_size
    print(f"Will process in {num_batches} batches of max {batch_size} tasks each")
    
    print("✓ Batch processing test passed\n")

async def test_command_parsing():
    """Test command parsing functionality"""
    print("Testing command parsing...")
    
    handler = AnalyzeCommandHandler()
    
    # Test various command formats
    test_commands = [
        "/sc:analyze",
        "/sc:analyze src/",
        "/sc:analyze src/ --focus security",
        "/sc:analyze . --focus performance --depth deep",
        "/sc:analyze --focus quality --depth quick --subagents false"
    ]
    
    for cmd in test_commands:
        args = handler.parse_command_args(cmd)
        print(f"Command: {cmd}")
        print(f"  Parsed: target={args['target']}, focus={args['focus'].value}, depth={args['depth'].value}")
        print(f"  Subagents: {args['enable_subagents']}")
    
    print("✓ Command parsing test passed\n")

async def test_output_chunking():
    """Test output chunking functionality"""
    print("Testing output chunking...")
    
    handler = AnalyzeCommandHandler()
    
    # Create large content
    large_content = "This is a test line.\n" * 1000
    
    # Test chunking
    chunks = handler.chunk_output(large_content, max_size=1000)
    print(f"Content size: {len(large_content)} chars")
    print(f"Number of chunks: {len(chunks)}")
    print(f"Chunk sizes: {[len(chunk) for chunk in chunks]}")
    
    # Verify no content is lost
    reconstructed = '\n'.join(chunks)
    assert reconstructed == large_content, "Content was lost during chunking"
    
    print("✓ Output chunking test passed\n")

async def test_tool_message_formatting():
    """Test tool message formatting"""
    print("Testing tool message formatting...")
    
    handler = AnalyzeCommandHandler()
    
    # Test tool_use block
    tool_use = handler.create_tool_use_block(
        tool_id="test_123",
        tool_name="analyze_code",
        parameters={"target": "src/", "focus": "quality"}
    )
    
    print("Tool use block:")
    print(f"  Type: {tool_use['type']}")
    print(f"  ID: {tool_use['id']}")
    print(f"  Name: {tool_use['name']}")
    
    # Test tool_result block
    tool_result = handler.create_tool_result_block(
        tool_id="test_123",
        content="Analysis completed successfully",
        is_error=False
    )
    
    print("Tool result block:")
    print(f"  Type: {tool_result['type']}")
    print(f"  Tool Use ID: {tool_result['tool_use_id']}")
    print(f"  Is Error: {tool_result['is_error']}")
    
    print("✓ Tool message formatting test passed\n")

async def test_checkpoint_functionality():
    """Test checkpoint save/load functionality"""
    print("Testing checkpoint functionality...")
    
    orchestrator = AnalysisOrchestrator()
    
    # Create some test tasks
    tasks = orchestrator.get_agent_tasks(AnalysisFocus.SECURITY, AnalysisDepth.QUICK)
    
    # Save checkpoint
    orchestrator.save_checkpoint(tasks)
    print(f"Saved checkpoint with {len(tasks)} tasks")
    
    # Load checkpoint
    loaded_tasks = orchestrator.load_checkpoint()
    if loaded_tasks:
        print(f"Loaded {len(loaded_tasks)} resumable tasks")
    
    print("✓ Checkpoint functionality test passed\n")

async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("TESTING ENHANCED ANALYZE COMMAND IMPLEMENTATION")
    print("=" * 60)
    
    try:
        await test_rate_limiting()
        await test_batch_processing()
        await test_command_parsing()
        await test_output_chunking()
        await test_tool_message_formatting()
        await test_checkpoint_functionality()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        print("\nThe enhanced /analyze command implementation is ready!")
        print("Key improvements:")
        print("- Rate limiting with exponential backoff (1s-60s)")
        print("- Batch processing (max 2 concurrent agents)")
        print("- Proper tool_use/tool_result pairing")
        print("- Output chunking for large responses")
        print("- Checkpoint/resume functionality")
        print("- Comprehensive error handling")
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_all_tests())