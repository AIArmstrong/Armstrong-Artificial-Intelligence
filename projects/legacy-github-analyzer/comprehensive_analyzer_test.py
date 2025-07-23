#!/usr/bin/env python3
"""
Comprehensive GitHub Repository Analyzer Test
Tests the full analyzer system on https://github.com/penwyp/ClaudePreference.git
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# Add the current directory and AAI root to the path to import our modules
current_dir = Path(__file__).parent
aai_root = current_dir.parent.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(aai_root))

from analyzer_agents import MultiAgentOrchestrator
try:
    from brain.modules.github_analyzer import GitHubRepositoryAnalyzer
except ImportError:
    # If we can't import the brain module, we'll create a simplified version
    GitHubRepositoryAnalyzer = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/mnt/c/Users/Brandon/AAI/projects/github-analyzer/test_analysis.log')
    ]
)

logger = logging.getLogger(__name__)

async def test_multi_agent_system(repo_path: Path):
    """Test the multi-agent analyzer system"""
    logger.info("Starting multi-agent analysis...")
    
    orchestrator = MultiAgentOrchestrator()
    
    # Run all agents
    results = await orchestrator.run_analysis(repo_path)
    
    # Analyze results
    analysis_summary = {
        'timestamp': datetime.now().isoformat(),
        'repo_path': str(repo_path),
        'agents_run': list(results.keys()),
        'agent_results': {}
    }
    
    for agent_name, result in results.items():
        logger.info(f"Agent {agent_name}: Success={result.success}, Time={result.execution_time:.2f}s")
        
        analysis_summary['agent_results'][agent_name] = {
            'success': result.success,
            'execution_time': result.execution_time,
            'data_keys': list(result.data.keys()) if result.data else [],
            'errors': result.errors,
            'warnings': result.warnings
        }
        
        if result.success and result.data:
            logger.info(f"  Data keys: {list(result.data.keys())}")
            
            # Log key metrics for each agent
            if agent_name == 'structure':
                languages = result.data.get('languages', {})
                logger.info(f"  Languages found: {list(languages.keys())}")
                total_functions = sum(lang.get('functions', 0) for lang in languages.values())
                total_classes = sum(lang.get('classes', 0) for lang in languages.values())
                logger.info(f"  Total functions: {total_functions}, Total classes: {total_classes}")
                
            elif agent_name == 'security':
                vulns = result.data.get('vulnerabilities', [])
                secrets = result.data.get('secret_leaks', [])
                logger.info(f"  Vulnerabilities: {len(vulns)}, Secret leaks: {len(secrets)}")
                logger.info(f"  Security score: {result.data.get('security_score', 'N/A')}")
                
            elif agent_name == 'quality':
                test_cov = result.data.get('test_coverage', 0)
                doc_score = result.data.get('documentation_score', 0)
                overall = result.data.get('overall_score', 0)
                logger.info(f"  Test coverage: {test_cov:.2f}, Doc score: {doc_score:.2f}, Overall: {overall:.2f}")
                
            elif agent_name == 'performance':
                bottlenecks = result.data.get('bottlenecks', [])
                optimizations = result.data.get('optimization_opportunities', [])
                logger.info(f"  Bottlenecks: {len(bottlenecks)}, Optimization opportunities: {len(optimizations)}")
        
        if result.errors:
            logger.error(f"  Errors: {result.errors}")
        
        if result.warnings:
            logger.warning(f"  Warnings: {result.warnings}")
    
    return analysis_summary

async def test_main_analyzer(repo_url: str):
    """Test the main GitHub Repository Analyzer"""
    logger.info("Starting main analyzer test...")
    
    analyzer = GitHubRepositoryAnalyzer()
    
    try:
        report = await analyzer.analyze_repository(repo_url)
        
        logger.info(f"Main analysis completed: Success={report.success}")
        
        if report.success:
            logger.info(f"Repository: {report.repo_name}")
            logger.info(f"Languages: {list(report.language_distribution.keys())}")
            logger.info(f"Total files: {report.file_count}, Total lines: {report.total_lines}")
            logger.info(f"Features extracted: {len(report.features)}")
            logger.info(f"Security findings: {len(report.security_findings)}")
            logger.info(f"Security score: {report.security_score:.2f}")
            logger.info(f"Documentation score: {report.documentation_score:.2f}")
            logger.info(f"Test coverage estimate: {report.test_coverage}")
            logger.info(f"Recommended features: {report.recommended_features}")
            
            # Log top features
            if report.features and report.compatibility_scores:
                logger.info("Top features by compatibility score:")
                sorted_features = sorted(
                    zip(report.features, report.compatibility_scores),
                    key=lambda x: x[1].overall_score,
                    reverse=True
                )
                
                for i, (feature, score) in enumerate(sorted_features[:5]):
                    logger.info(f"  {i+1}. {feature.name} ({feature.type}) - Score: {score.overall_score:.2f}")
        else:
            logger.error(f"Analysis failed: {report.error_message}")
        
        return report
        
    except Exception as e:
        logger.error(f"Main analyzer test failed: {e}")
        return None

async def generate_comprehensive_report(multi_agent_results, main_analyzer_report, repo_url):
    """Generate a comprehensive analysis report"""
    logger.info("Generating comprehensive analysis report...")
    
    report = {
        'analysis_metadata': {
            'timestamp': datetime.now().isoformat(),
            'repo_url': repo_url,
            'analyzer_version': '1.0.0',
            'analysis_type': 'comprehensive_test'
        },
        'repository_overview': {},
        'multi_agent_analysis': multi_agent_results,
        'main_analyzer_results': {},
        'integration_assessment': {},
        'recommendations': {},
        'system_issues': []
    }
    
    # Extract repository overview
    if main_analyzer_report and main_analyzer_report.success:
        report['repository_overview'] = {
            'name': main_analyzer_report.repo_name,
            'language_distribution': main_analyzer_report.language_distribution,
            'total_files': main_analyzer_report.file_count,
            'total_lines': main_analyzer_report.total_lines,
            'license': main_analyzer_report.license,
            'last_commit': main_analyzer_report.last_commit
        }
        
        report['main_analyzer_results'] = {
            'features_count': len(main_analyzer_report.features),
            'security_score': main_analyzer_report.security_score,
            'documentation_score': main_analyzer_report.documentation_score,
            'test_coverage': main_analyzer_report.test_coverage,
            'code_quality_score': main_analyzer_report.code_quality_score,
            'security_findings_count': len(main_analyzer_report.security_findings),
            'recommended_features': main_analyzer_report.recommended_features
        }
        
        # Integration assessment
        if main_analyzer_report.features and main_analyzer_report.compatibility_scores:
            high_value_features = [
                {
                    'name': feature.name,
                    'type': feature.type,
                    'score': score.overall_score,
                    'rationale': score.rationale
                }
                for feature, score in zip(main_analyzer_report.features, main_analyzer_report.compatibility_scores)
                if score.overall_score >= 0.7
            ]
            
            report['integration_assessment'] = {
                'high_value_features': high_value_features,
                'integration_stubs_available': list(main_analyzer_report.integration_stubs.keys()),
                'avg_compatibility_score': sum(s.overall_score for s in main_analyzer_report.compatibility_scores) / len(main_analyzer_report.compatibility_scores)
            }
    
    # Generate recommendations
    recommendations = []
    
    # Multi-agent system recommendations
    if multi_agent_results['agent_results'].get('structure', {}).get('success'):
        structure_data = multi_agent_results['agent_results']['structure']
        if 'languages' in structure_data.get('data_keys', []):
            recommendations.append("Repository has good code structure - consider extracting reusable components")
    
    if multi_agent_results['agent_results'].get('security', {}).get('success'):
        recommendations.append("Security analysis completed - review findings before integration")
    
    if multi_agent_results['agent_results'].get('quality', {}).get('success'):
        recommendations.append("Quality metrics available - use for integration prioritization")
    
    # Main analyzer recommendations
    if main_analyzer_report and main_analyzer_report.success:
        if main_analyzer_report.security_score > 0.8:
            recommendations.append("High security score - good candidate for integration")
        elif main_analyzer_report.security_score < 0.6:
            recommendations.append("Security concerns identified - address before integration")
        
        if main_analyzer_report.documentation_score > 0.7:
            recommendations.append("Well-documented code - easier integration expected")
        
        if main_analyzer_report.test_coverage and main_analyzer_report.test_coverage > 0.5:
            recommendations.append("Good test coverage - reliable code for integration")
    
    report['recommendations'] = {
        'integration_recommendations': recommendations,
        'next_steps': [
            "Review high-value features for integration potential",
            "Address any security findings before integration",
            "Examine integration stubs for implementation guidance",
            "Consider creating AAI-specific adaptations of useful patterns"
        ]
    }
    
    # Document system issues found during testing
    system_issues = []
    
    for agent_name, result in multi_agent_results['agent_results'].items():
        if not result['success']:
            system_issues.append(f"Agent {agent_name} failed: {result['errors']}")
        if result['warnings']:
            system_issues.append(f"Agent {agent_name} warnings: {result['warnings']}")
    
    if main_analyzer_report and not main_analyzer_report.success:
        system_issues.append(f"Main analyzer failed: {main_analyzer_report.error_message}")
    
    report['system_issues'] = system_issues
    
    return report

async def main():
    """Main test execution"""
    repo_url = "https://github.com/penwyp/ClaudePreference.git"
    
    logger.info(f"Starting comprehensive analysis of {repo_url}")
    logger.info("=" * 80)
    
    start_time = time.time()
    
    # Initialize results
    multi_agent_results = None
    main_analyzer_report = None
    
    try:
        # Test 1: Multi-agent system (requires cloned repo)
        logger.info("Phase 1: Testing multi-agent system with temporary clone...")
        
        # We'll let the main analyzer handle cloning, then use its cloned repo for multi-agent test
        main_analyzer = GitHubRepositoryAnalyzer()
        
        # Clone repository for multi-agent testing
        repo_path = main_analyzer.cloner.clone_repository(repo_url)
        logger.info(f"Repository cloned to: {repo_path}")
        
        # Run multi-agent analysis
        multi_agent_results = await test_multi_agent_system(repo_path)
        
        # Test 2: Main analyzer system
        logger.info("\nPhase 2: Testing main GitHub analyzer...")
        main_analyzer_report = await test_main_analyzer(repo_url)
        
        # Cleanup cloned repo
        main_analyzer.cloner.cleanup(repo_path)
        
    except Exception as e:
        logger.error(f"Critical error during analysis: {e}")
        return
    
    # Generate comprehensive report
    logger.info("\nPhase 3: Generating comprehensive report...")
    
    try:
        comprehensive_report = await generate_comprehensive_report(
            multi_agent_results, main_analyzer_report, repo_url
        )
        
        # Save report
        report_path = Path("/mnt/c/Users/Brandon/AAI/projects/github-analyzer/comprehensive_analysis_report.json")
        with open(report_path, 'w') as f:
            json.dump(comprehensive_report, f, indent=2, default=str)
        
        logger.info(f"Comprehensive report saved to: {report_path}")
        
        # Print summary
        total_time = time.time() - start_time
        logger.info("\n" + "=" * 80)
        logger.info("ANALYSIS COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total execution time: {total_time:.2f} seconds")
        
        if main_analyzer_report and main_analyzer_report.success:
            logger.info(f"Repository: {main_analyzer_report.repo_name}")
            logger.info(f"Primary language: {max(main_analyzer_report.language_distribution.items(), key=lambda x: x[1])[0] if main_analyzer_report.language_distribution else 'Unknown'}")
            logger.info(f"Features found: {len(main_analyzer_report.features)}")
            logger.info(f"Security score: {main_analyzer_report.security_score:.2f}/1.0")
            logger.info(f"High-value features: {len([s for s in main_analyzer_report.compatibility_scores if s.overall_score >= 0.7])}")
        
        # Agent success summary
        if multi_agent_results:
            successful_agents = sum(1 for result in multi_agent_results['agent_results'].values() if result['success'])
            total_agents = len(multi_agent_results['agent_results'])
            logger.info(f"Agent success rate: {successful_agents}/{total_agents}")
        
        logger.info(f"System issues found: {len(comprehensive_report['system_issues'])}")
        logger.info(f"Report available at: {report_path}")
        
    except Exception as e:
        logger.error(f"Failed to generate comprehensive report: {e}")

if __name__ == "__main__":
    asyncio.run(main())