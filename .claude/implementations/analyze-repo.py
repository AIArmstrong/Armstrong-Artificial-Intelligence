#!/usr/bin/env python3
"""
Enhanced Repository Analyzer Command Implementation
Implements the /analyze-repo slash command with comprehensive analysis capabilities
"""

import asyncio
import json
import logging
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add AAI to path
AAI_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(AAI_PATH))

async def run_enhanced_analysis(repository_path: str, 
                              enable_semantic: bool = True,
                              force_cache_refresh: bool = False,
                              include_performance: bool = True,
                              include_integrations: bool = True,
                              output_format: str = "markdown") -> Dict[str, Any]:
    """
    Run enhanced repository analysis with all available features.
    
    Args:
        repository_path: Path to repository to analyze
        enable_semantic: Enable semantic analysis with LLM
        force_cache_refresh: Force cache refresh
        include_performance: Include performance benchmarks
        include_integrations: Generate integration recommendations
        output_format: Output format (json, markdown)
        
    Returns:
        Analysis results dictionary
    """
    try:
        # Import Enhanced Repository Analyzer directly
        sys.path.insert(0, str(AAI_PATH / "projects" / "enhanced-repository-analyzer"))
        sys.path.insert(0, str(AAI_PATH))
        
        from brain.modules.enhanced_repository_analyzer import enhanced_analyzer
        
        # Initialize if needed
        await enhanced_analyzer._init_components()
        
        # Configure analysis types
        analysis_types = ['structure', 'patterns']
        if enable_semantic:
            analysis_types.append('semantic')
        if include_integrations:
            analysis_types.append('integration')
        
        # Set performance targets from PRP requirements
        performance_targets = {
            'max_execution_time': 60.0,
            'min_cache_hit_rate': 0.3,
            'max_memory_mb': 500.0,
            'min_files_per_second': 10.0,
            'min_semantic_accuracy': 0.85
        }
        
        logger.info(f"Starting enhanced repository analysis for: {repository_path}")
        logger.info(f"Analysis types: {analysis_types}")
        
        # Execute analysis
        start_time = time.time()
        results = await enhanced_analyzer.analyze_repository(
            repository_path=repository_path,
            analysis_types=analysis_types,
            use_semantic=enable_semantic,
            performance_targets=performance_targets
        )
        total_time = time.time() - start_time
        
        # Add execution metadata
        results['command_metadata'] = {
            'command': '/analyze-repo',
            'version': '1.0.0',
            'total_command_time': total_time,
            'arguments': {
                'repository_path': repository_path,
                'enable_semantic': enable_semantic,
                'force_cache_refresh': force_cache_refresh,
                'include_performance': include_performance,
                'include_integrations': include_integrations,
                'output_format': output_format
            }
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Enhanced repository analysis failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'command_metadata': {
                'command': '/analyze-repo',
                'version': '1.0.0',
                'total_command_time': time.time() - start_time if 'start_time' in locals() else 0
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
    integration_recs = results.get('integration_recommendations', [])
    metadata = results.get('command_metadata', {})
    
    report = f"""# Enhanced Repository Analysis Report

## Executive Summary
- **Repository**: `{results.get('repository_path', 'Unknown')}`
- **Analysis Types**: {', '.join(results.get('analysis_types', []))}
- **Session ID**: `{results.get('session_id', 'N/A')}`
- **Execution Time**: {perf_metrics.get('total_execution_time', 0):.2f}s
- **Success**: ✅ {results.get('success', False)}

## Performance Metrics
- **Files/Second**: {perf_metrics.get('files_per_second', 0):.1f}
- **Cache Hit Rate**: {perf_metrics.get('cache_hit_rate', 0):.1%}
- **Memory Efficiency**: {perf_metrics.get('memory_efficiency', 0):.2f}
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

"""
    
    # Semantic Analysis Section
    if semantic_analysis:
        report += f"""## Semantic Analysis
- **Features Detected**: {semantic_analysis.get('features_count', 0)}
- **High Confidence Features**: {semantic_analysis.get('high_confidence_features', 0)}
- **Accuracy Rate**: {(semantic_analysis.get('high_confidence_features', 0) / max(semantic_analysis.get('features_count', 1), 1)):.1%}

### Top Features
"""
        for feature in semantic_analysis.get('features', [])[:5]:
            report += f"- **{feature.get('name')}** ({feature.get('type')}) - Confidence: {feature.get('confidence', 0):.2f}\n"
            if feature.get('intent'):
                report += f"  - Intent: {feature.get('intent')[:100]}...\n"
        
        report += "\n"
    
    # Integration Recommendations
    if integration_recs:
        report += f"""## Integration Recommendations

"""
        for rec in integration_recs:
            report += f"""### {rec.get('type', 'Unknown').title()} Integration
- **Confidence**: {rec.get('confidence', 0):.1%}
- **Reason**: {rec.get('reason', 'No reason provided')}
- **Benefits**: {', '.join(rec.get('benefits', []))}

"""
    
    # Performance Validation
    validation = results.get('performance_validation', {})
    if validation:
        report += f"""## Performance Validation
"""
        for target, passed in validation.items():
            status = '✅' if passed else '❌'
            report += f"- **{target}**: {status}\n"
        report += "\n"
    
    # Command Metadata
    report += f"""## Command Information
- **Command**: `{metadata.get('command', 'N/A')}`
- **Version**: {metadata.get('version', 'N/A')}
- **Total Command Time**: {metadata.get('total_command_time', 0):.2f}s
- **Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S')}

---
*Generated by Enhanced Repository Analyzer - AAI Brain Integration*
"""
    
    return report

def format_json_output(results: Dict[str, Any]) -> str:
    """Format analysis results as JSON"""
    return json.dumps(results, indent=2, default=str)

async def main():
    """Main command entry point"""
    parser = argparse.ArgumentParser(description='Enhanced Repository Analysis')
    parser.add_argument('repository_path', nargs='?', default='.', 
                       help='Path to repository (default: current directory)')
    parser.add_argument('--semantic', action='store_true', 
                       help='Enable semantic analysis with LLM')
    parser.add_argument('--cache', action='store_true', 
                       help='Force cache refresh')
    parser.add_argument('--performance', action='store_true', 
                       help='Include detailed performance benchmarks')
    parser.add_argument('--integrations', action='store_true', 
                       help='Generate integration recommendations')
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
    print(f"📊 Analysis mode: {'Semantic + ' if args.semantic else ''}Structure + Patterns")
    
    # Run analysis
    results = await run_enhanced_analysis(
        repository_path=str(repo_path),
        enable_semantic=args.semantic,
        force_cache_refresh=args.cache,
        include_performance=args.performance,
        include_integrations=args.integrations,
        output_format=args.format
    )
    
    # Format and output results
    if args.format == 'json':
        print(format_json_output(results))
    else:
        print(format_markdown_report(results))
    
    # Exit with appropriate code
    if results.get('success', False):
        print(f"\n✅ Analysis completed successfully in {results.get('command_metadata', {}).get('total_command_time', 0):.2f}s")
        sys.exit(0)
    else:
        print(f"\n❌ Analysis failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())