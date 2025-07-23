#!/usr/bin/env python3
"""
Enhanced Repository Analyzer Command - Standalone Implementation
Direct implementation without AAI brain dependency for easier testing
"""

import asyncio
import json
import logging
import sys
import time
import argparse
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project path for imports
AAI_PATH = Path(__file__).parent.parent
PROJECT_PATH = AAI_PATH / "projects" / "enhanced-repository-analyzer"
sys.path.insert(0, str(PROJECT_PATH))
sys.path.insert(0, str(AAI_PATH))

async def run_standalone_analysis(repository_path: str, 
                                enable_semantic: bool = False,
                                include_performance: bool = True) -> Dict[str, Any]:
    """
    Run standalone enhanced repository analysis.
    
    Args:
        repository_path: Path to repository to analyze
        enable_semantic: Enable semantic analysis (limited without OpenRouter)
        include_performance: Include performance benchmarks
        
    Returns:
        Analysis results dictionary
    """
    try:
        from core.streaming_walker import StreamingFileWalker
        from core.cache_manager import CacheManager
        from core.pattern_registry import PatternRegistry
        from core.semantic_analyzer import SemanticAnalyzer
        from agents.structure_agent import StructureAgent
        
        logger.info(f"Starting standalone repository analysis for: {repository_path}")
        
        start_time = time.time()
        repo_path = Path(repository_path)
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repository_path}")
        
        # Initialize components
        cache_manager = CacheManager(memory_size=500)
        pattern_registry = PatternRegistry()
        semantic_analyzer = SemanticAnalyzer()  # No OpenRouter for standalone
        structure_agent = StructureAgent(
            cache_manager=cache_manager,
            pattern_registry=pattern_registry,
            semantic_analyzer=semantic_analyzer if enable_semantic else None
        )
        
        # Perform structure analysis
        structure_result = await structure_agent.analyze(repo_path)
        
        # Calculate basic metrics
        execution_time = time.time() - start_time
        
        # Get cache statistics
        cache_stats = await cache_manager.get_statistics()
        
        # Build results
        results = {
            'session_id': f"standalone_{int(time.time())}",
            'repository_path': str(repo_path),
            'analysis_types': ['structure', 'patterns'],
            'success': structure_result.success,
            'performance_metrics': {
                'total_execution_time': execution_time,
                'cache_hit_rate': cache_stats['performance']['overall_hit_rate'],
                'files_per_second': 0,
                'semantic_accuracy': 0.0
            },
            'structure_analysis': {
                'success': structure_result.success,
                'data': structure_result.data,
                'execution_time': structure_result.execution_time,
                'patterns_matched': len(structure_result.patterns_matched),
                'cache_hit': structure_result.cache_hit,
                'patterns_detected': [
                    {
                        'name': pattern.pattern_name,
                        'type': pattern.match_type,
                        'confidence': pattern.confidence,
                        'content': pattern.content[:100] + "..." if len(pattern.content) > 100 else pattern.content
                    }
                    for pattern in structure_result.patterns_matched[:10]  # Limit to first 10
                ]
            },
            'cache_statistics': cache_stats,
            'command_metadata': {
                'command': '/analyze-repo (standalone)',
                'version': '1.0.0',
                'total_command_time': execution_time,
                'mode': 'standalone',
                'components_initialized': {
                    'cache_manager': True,
                    'pattern_registry': True,
                    'semantic_analyzer': enable_semantic,
                    'structure_agent': True
                }
            }
        }
        
        # Calculate files per second if we have file count
        file_structure = structure_result.data.get('file_structure', {})
        total_files = file_structure.get('total_files', 0)
        if total_files > 0 and execution_time > 0:
            results['performance_metrics']['files_per_second'] = total_files / execution_time
        
        # Add semantic analysis if enabled
        if enable_semantic:
            semantic_features = []
            # Analyze a few key files for demonstration
            key_files = []
            for ext in ['.py', '.js', '.go', '.rs']:
                files = list(repo_path.rglob(f"*{ext}"))[:3]  # Limit to 3 files per type
                key_files.extend(files)
            
            for file_path in key_files[:5]:  # Max 5 files
                try:
                    features = await semantic_analyzer.analyze_file(file_path, use_llm=False)
                    semantic_features.extend(features)
                except Exception as e:
                    logger.warning(f"Semantic analysis failed for {file_path}: {e}")
            
            results['semantic_analysis'] = {
                'features_count': len(semantic_features),
                'high_confidence_features': len([f for f in semantic_features if f.confidence > 0.8]),
                'features': [
                    {
                        'name': f.name,
                        'type': f.type,
                        'confidence': f.confidence,
                        'complexity': f.complexity_score,
                        'file': f.file_path
                    }
                    for f in semantic_features[:10]  # Limit for response size
                ]
            }
            
            # Update semantic accuracy
            if semantic_features:
                high_conf = len([f for f in semantic_features if f.confidence > 0.8])
                results['performance_metrics']['semantic_accuracy'] = high_conf / len(semantic_features)
        
        return results
        
    except Exception as e:
        logger.error(f"Standalone repository analysis failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'command_metadata': {
                'command': '/analyze-repo (standalone)',
                'version': '1.0.0',
                'total_command_time': time.time() - start_time if 'start_time' in locals() else 0,
                'mode': 'standalone'
            }
        }

def format_markdown_report(results: Dict[str, Any]) -> str:
    """Format analysis results as markdown report"""
    
    if not results.get('success', False):
        return f"# Repository Analysis Failed\n\n**Error**: {results.get('error', 'Unknown error')}\n"
    
    # Extract key metrics
    perf_metrics = results.get('performance_metrics', {})
    struct_analysis = results.get('structure_analysis', {})
    semantic_analysis = results.get('semantic_analysis', {})
    cache_stats = results.get('cache_statistics', {})
    metadata = results.get('command_metadata', {})
    
    report = f"""# Enhanced Repository Analysis Report

## Executive Summary
- **Repository**: `{results.get('repository_path', 'Unknown')}`
- **Analysis Types**: {', '.join(results.get('analysis_types', []))}
- **Session ID**: `{results.get('session_id', 'N/A')}`
- **Execution Time**: {perf_metrics.get('total_execution_time', 0):.3f}s
- **Success**: ✅ {results.get('success', False)}

## Performance Metrics
- **Files/Second**: {perf_metrics.get('files_per_second', 0):.1f}
- **Cache Hit Rate**: {perf_metrics.get('cache_hit_rate', 0):.1%}
- **Semantic Accuracy**: {perf_metrics.get('semantic_accuracy', 0):.1%}

## Structure Analysis
"""
    
    if struct_analysis.get('success'):
        struct_data = struct_analysis.get('data', {})
        file_structure = struct_data.get('file_structure', {})
        
        report += f"""- **Files Processed**: {file_structure.get('total_files', 0)}
- **Languages Detected**: {len(file_structure.get('languages', []))}
- **Patterns Matched**: {struct_analysis.get('patterns_matched', 0)}
- **Cache Hit**: {'✅' if struct_analysis.get('cache_hit') else '❌'}
- **Execution Time**: {struct_analysis.get('execution_time', 0):.3f}s

### Languages Detected
{', '.join(file_structure.get('languages', []))}

### Patterns Detected
"""
        
        patterns = struct_analysis.get('patterns_detected', [])
        if patterns:
            for pattern in patterns[:5]:  # Show first 5 patterns
                report += f"- **{pattern['name']}** ({pattern['type']}) - Confidence: {pattern['confidence']:.2f}\n"
                report += f"  - Content: `{pattern['content']}`\n"
        else:
            report += "No patterns detected.\n"
        
        report += "\n"
    
    # Semantic Analysis Section
    if semantic_analysis:
        report += f"""## Semantic Analysis
- **Features Detected**: {semantic_analysis.get('features_count', 0)}
- **High Confidence Features**: {semantic_analysis.get('high_confidence_features', 0)}
- **Accuracy Rate**: {(semantic_analysis.get('high_confidence_features', 0) / max(semantic_analysis.get('features_count', 1), 1)):.1%}

### Features Detected
"""
        for feature in semantic_analysis.get('features', [])[:5]:
            report += f"- **{feature.get('name')}** ({feature.get('type')}) - Confidence: {feature.get('confidence', 0):.2f}\n"
            report += f"  - Complexity: {feature.get('complexity', 0):.2f}, File: `{Path(feature.get('file', '')).name}`\n"
        
        report += "\n"
    
    # Cache Performance
    memory_cache = cache_stats.get('memory_cache', {})
    disk_cache = cache_stats.get('disk_cache', {})
    
    report += f"""## Cache Performance
- **Memory Cache**: {memory_cache.get('size', 0)}/{memory_cache.get('maxsize', 0)} items
- **Memory Hit Rate**: {memory_cache.get('hit_rate', 0):.1%}
- **Disk Cache Size**: {disk_cache.get('size', 0)} items
- **Total Requests**: {memory_cache.get('total_requests', 0)}

## Component Status
"""
    
    components = metadata.get('components_initialized', {})
    for component, status in components.items():
        status_icon = '✅' if status else '❌'
        report += f"- **{component.replace('_', ' ').title()}**: {status_icon}\n"
    
    # Command Metadata
    report += f"""
## Command Information
- **Command**: `{metadata.get('command', 'N/A')}`
- **Version**: {metadata.get('version', 'N/A')}
- **Mode**: {metadata.get('mode', 'N/A')}
- **Total Command Time**: {metadata.get('total_command_time', 0):.3f}s
- **Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S')}

---
*Generated by Enhanced Repository Analyzer - Standalone Mode*
"""
    
    return report

def format_json_output(results: Dict[str, Any]) -> str:
    """Format analysis results as JSON"""
    return json.dumps(results, indent=2, default=str)

async def main():
    """Main command entry point"""
    parser = argparse.ArgumentParser(description='Enhanced Repository Analysis (Standalone)')
    parser.add_argument('repository_path', nargs='?', default='.', 
                       help='Path to repository (default: current directory)')
    parser.add_argument('--semantic', action='store_true', 
                       help='Enable semantic analysis (limited without OpenRouter)')
    parser.add_argument('--performance', action='store_true', 
                       help='Include detailed performance benchmarks')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress output')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Resolve repository path
    repo_path = Path(args.repository_path).resolve()
    if not repo_path.exists():
        print(f"❌ Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    print(f"🔍 Analyzing repository: {repo_path}")
    print(f"📊 Analysis mode: {'Semantic + ' if args.semantic else ''}Structure + Patterns (Standalone)")
    
    # Run analysis
    results = await run_standalone_analysis(
        repository_path=str(repo_path),
        enable_semantic=args.semantic,
        include_performance=args.performance
    )
    
    # Format and output results
    if args.format == 'json':
        print(format_json_output(results))
    else:
        print(format_markdown_report(results))
    
    # Exit with appropriate code
    if results.get('success', False):
        print(f"\n✅ Analysis completed successfully in {results.get('command_metadata', {}).get('total_command_time', 0):.3f}s")
        sys.exit(0)
    else:
        print(f"\n❌ Analysis failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())