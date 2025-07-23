#!/usr/bin/env python3
"""
Supreme Improve - Codebase Analysis Workflow

Provides comprehensive analysis workflow with multi-dimensional metrics collection
and report generation with visualization.
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add the AAI base path to Python path
aai_base_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(aai_base_path))

try:
    from brain.modules.supreme_improve import MultiDimensionalScorer, QualityMetrics
    from brain.modules.enhanced_repository_analyzer_integration import EnhancedRepositoryAnalyzer
    from brain.modules.github_analyzer import GitHubRepositoryAnalyzer
    from brain.modules.tech_stack_expert import TechStackExpertModule
    SUPREME_IMPROVE_AVAILABLE = True
except ImportError as e:
    logging.error(f"Supreme Improve modules not available: {e}")
    SUPREME_IMPROVE_AVAILABLE = False
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class CodebaseAnalyzer:
    """
    Comprehensive codebase analysis system.
    
    Integrates enhanced repository analyzer, GitHub analyzer, and multi-dimensional
    quality scoring to provide complete codebase insights.
    """
    
    def __init__(self, base_path: str = None):
        """Initialize the codebase analyzer"""
        self.base_path = Path(base_path) if base_path else aai_base_path
        
        # Initialize components
        self.quality_scorer = MultiDimensionalScorer()
        self.repository_analyzer = EnhancedRepositoryAnalyzer(str(self.base_path))
        self.github_analyzer = GitHubRepositoryAnalyzer()
        self.tech_expert = TechStackExpertModule()
        
        logger.info("Codebase analyzer initialized")
    
    async def analyze_codebase(self,
                             target_path: str,
                             analysis_types: List[str] = None,
                             output_format: str = "json",
                             include_visualization: bool = False) -> Dict[str, Any]:
        """
        Run comprehensive codebase analysis.
        
        Args:
            target_path: Path to codebase to analyze
            analysis_types: Types of analysis to perform
            output_format: Output format ('json', 'html', 'markdown')
            include_visualization: Whether to generate visualizations
            
        Returns:
            Comprehensive analysis results
        """
        logger.info(f"Starting codebase analysis for: {target_path}")
        
        target_path = Path(target_path).resolve()
        if not target_path.exists():
            raise ValueError(f"Target path does not exist: {target_path}")
        
        session_id = f"analysis_{int(datetime.now().timestamp())}"
        
        # Default analysis types if not specified
        if analysis_types is None:
            analysis_types = [
                "structure", "quality", "semantic", "integration", 
                "architecture", "security", "performance"
            ]
        
        try:
            results = {
                'session_id': session_id,
                'target_path': str(target_path),
                'analysis_types': analysis_types,
                'timestamp': datetime.now().isoformat(),
                'analysis_results': {},
                'summary': {},
                'recommendations': [],
                'success': True
            }
            
            # Phase 1: Repository Structure Analysis
            if "structure" in analysis_types:
                logger.info("Running repository structure analysis...")
                structure_results = await self._analyze_structure(target_path)
                results['analysis_results']['structure'] = structure_results
            
            # Phase 2: Multi-dimensional Quality Analysis
            if "quality" in analysis_types:
                logger.info("Running quality analysis...")
                quality_results = await self._analyze_quality(target_path)
                results['analysis_results']['quality'] = quality_results
            
            # Phase 3: Semantic Analysis
            if "semantic" in analysis_types:
                logger.info("Running semantic analysis...")
                semantic_results = await self._analyze_semantics(target_path)
                results['analysis_results']['semantic'] = semantic_results
            
            # Phase 4: Architecture Analysis
            if "architecture" in analysis_types:
                logger.info("Running architecture analysis...")
                architecture_results = await self._analyze_architecture(target_path)
                results['analysis_results']['architecture'] = architecture_results
            
            # Phase 5: Security Analysis
            if "security" in analysis_types:
                logger.info("Running security analysis...")
                security_results = await self._analyze_security(target_path)
                results['analysis_results']['security'] = security_results
            
            # Phase 6: Performance Analysis
            if "performance" in analysis_types:
                logger.info("Running performance analysis...")
                performance_results = await self._analyze_performance(target_path)
                results['analysis_results']['performance'] = performance_results
            
            # Phase 7: Integration Opportunities
            if "integration" in analysis_types:
                logger.info("Analyzing integration opportunities...")
                integration_results = await self._analyze_integrations(target_path)
                results['analysis_results']['integration'] = integration_results
            
            # Phase 8: Generate Summary and Recommendations
            logger.info("Generating summary and recommendations...")
            results['summary'] = self._generate_summary(results['analysis_results'])
            results['recommendations'] = self._generate_recommendations(results['analysis_results'])
            
            # Phase 9: Generate Visualization Data (if requested)
            if include_visualization:
                logger.info("Generating visualization data...")
                results['visualization_data'] = self._generate_visualization_data(results)
            
            logger.info(f"Codebase analysis completed successfully: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Codebase analysis failed: {str(e)}")
            return {
                'session_id': session_id,
                'target_path': str(target_path),
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _analyze_structure(self, target_path: Path) -> Dict[str, Any]:
        """Analyze repository structure"""
        try:
            # Use enhanced repository analyzer for structure analysis
            results = await self.repository_analyzer.analyze_repository(
                str(target_path),
                analysis_types=["structure"],
                use_semantic=False
            )
            
            structure_data = results.get('structure_analysis', {}).get('data', {})
            
            return {
                'file_count': structure_data.get('file_structure', {}).get('total_files', 0),
                'directory_count': structure_data.get('file_structure', {}).get('total_directories', 0),
                'file_types': structure_data.get('file_types', {}),
                'patterns_detected': results.get('structure_analysis', {}).get('patterns_matched', 0),
                'execution_time': results.get('structure_analysis', {}).get('execution_time', 0),
                'insights': self._extract_structure_insights(structure_data)
            }
            
        except Exception as e:
            logger.error(f"Structure analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_quality(self, target_path: Path) -> Dict[str, Any]:
        """Analyze code quality using multi-dimensional scorer"""
        try:
            # Use quality scorer for detailed analysis
            project_results = self.quality_scorer.score_project(
                str(target_path),
                file_patterns=["*.py", "*.js", "*.ts", "*.java", "*.go", "*.rs", "*.cpp", "*.c"]
            )
            
            return {
                'overall_score': project_results['project_metrics'].overall_score,
                'dimension_scores': {
                    'maintainability': project_results['project_metrics'].maintainability_score,
                    'complexity': project_results['project_metrics'].complexity_score,
                    'readability': project_results['project_metrics'].readability_score,
                    'test_coverage': project_results['project_metrics'].test_coverage,
                    'documentation': project_results['project_metrics'].documentation_score,
                    'security': project_results['project_metrics'].security_score,
                    'performance': project_results['project_metrics'].performance_score
                },
                'file_count': len(project_results['file_scores']),
                'quality_distribution': project_results['summary']['quality_distribution'],
                'recommendations': project_results['recommendations'],
                'top_issues': self._identify_top_quality_issues(project_results)
            }
            
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_semantics(self, target_path: Path) -> Dict[str, Any]:
        """Analyze semantic features"""
        try:
            # Use enhanced repository analyzer for semantic analysis
            results = await self.repository_analyzer.analyze_repository(
                str(target_path),
                analysis_types=["semantic"],
                use_semantic=True
            )
            
            semantic_data = results.get('semantic_analysis', {})
            
            return {
                'features_count': semantic_data.get('features_count', 0),
                'high_confidence_features': semantic_data.get('high_confidence_features', 0),
                'confidence_ratio': (
                    semantic_data.get('high_confidence_features', 0) / 
                    max(semantic_data.get('features_count', 1), 1)
                ),
                'key_features': semantic_data.get('features', [])[:10],  # Top 10 features
                'insights': self._extract_semantic_insights(semantic_data)
            }
            
        except Exception as e:
            logger.error(f"Semantic analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_architecture(self, target_path: Path) -> Dict[str, Any]:
        """Analyze architecture patterns and decisions"""
        try:
            # Use tech stack expert for architecture analysis
            architecture_insights = []
            
            # Detect technology stack
            tech_stack = await self._detect_tech_stack(target_path)
            
            # Analyze architectural patterns
            patterns = self._detect_architectural_patterns(target_path)
            
            return {
                'tech_stack': tech_stack,
                'architectural_patterns': patterns,
                'modularity_score': self._calculate_modularity_score(target_path),
                'coupling_analysis': self._analyze_coupling(target_path),
                'scalability_assessment': self._assess_scalability(target_path),
                'recommendations': self._generate_architecture_recommendations(tech_stack, patterns)
            }
            
        except Exception as e:
            logger.error(f"Architecture analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_security(self, target_path: Path) -> Dict[str, Any]:
        """Analyze security aspects"""
        try:
            security_issues = []
            
            # Basic security pattern detection
            for py_file in target_path.rglob("*.py"):
                issues = self._scan_file_for_security_issues(py_file)
                security_issues.extend(issues)
            
            return {
                'total_issues': len(security_issues),
                'issue_severity': self._categorize_security_issues(security_issues),
                'vulnerable_patterns': self._identify_vulnerable_patterns(security_issues),
                'security_score': max(0, 100 - len(security_issues) * 5),  # Simple scoring
                'recommendations': self._generate_security_recommendations(security_issues)
            }
            
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_performance(self, target_path: Path) -> Dict[str, Any]:
        """Analyze performance characteristics"""
        try:
            performance_issues = []
            
            # Basic performance pattern detection
            for py_file in target_path.rglob("*.py"):
                issues = self._scan_file_for_performance_issues(py_file)
                performance_issues.extend(issues)
            
            return {
                'total_issues': len(performance_issues),
                'issue_categories': self._categorize_performance_issues(performance_issues),
                'performance_score': max(0, 100 - len(performance_issues) * 3),  # Simple scoring
                'optimization_opportunities': self._identify_optimization_opportunities(performance_issues),
                'recommendations': self._generate_performance_recommendations(performance_issues)
            }
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_integrations(self, target_path: Path) -> Dict[str, Any]:
        """Analyze integration opportunities"""
        try:
            # Use enhanced repository analyzer for integration analysis
            results = await self.repository_analyzer.analyze_repository(
                str(target_path),
                analysis_types=["integration"],
                use_semantic=False
            )
            
            integration_data = results.get('integration_recommendations', [])
            
            return {
                'opportunities_found': len(integration_data),
                'integration_types': [rec['type'] for rec in integration_data],
                'high_confidence_opportunities': [
                    rec for rec in integration_data if rec.get('confidence', 0) > 0.8
                ],
                'recommendations': integration_data
            }
            
        except Exception as e:
            logger.error(f"Integration analysis failed: {e}")
            return {'error': str(e)}
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of analysis results"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'analysis_completed': list(analysis_results.keys()),
            'overall_health': 'unknown'
        }
        
        # Calculate overall health score
        health_scores = []
        
        if 'quality' in analysis_results and 'overall_score' in analysis_results['quality']:
            health_scores.append(analysis_results['quality']['overall_score'])
        
        if 'security' in analysis_results and 'security_score' in analysis_results['security']:
            health_scores.append(analysis_results['security']['security_score'])
        
        if 'performance' in analysis_results and 'performance_score' in analysis_results['performance']:
            health_scores.append(analysis_results['performance']['performance_score'])
        
        if health_scores:
            avg_score = sum(health_scores) / len(health_scores)
            if avg_score >= 80:
                summary['overall_health'] = 'excellent'
            elif avg_score >= 70:
                summary['overall_health'] = 'good'
            elif avg_score >= 60:
                summary['overall_health'] = 'fair'
            else:
                summary['overall_health'] = 'needs_improvement'
            
            summary['health_score'] = avg_score
        
        # Add key metrics
        if 'structure' in analysis_results:
            summary['file_count'] = analysis_results['structure'].get('file_count', 0)
            summary['patterns_detected'] = analysis_results['structure'].get('patterns_detected', 0)
        
        if 'quality' in analysis_results:
            summary['quality_score'] = analysis_results['quality'].get('overall_score', 0)
        
        if 'integration' in analysis_results:
            summary['integration_opportunities'] = analysis_results['integration'].get('opportunities_found', 0)
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive recommendations based on analysis"""
        recommendations = []
        
        # Quality recommendations
        if 'quality' in analysis_results and 'recommendations' in analysis_results['quality']:
            for rec in analysis_results['quality']['recommendations']:
                recommendations.append({
                    'type': 'quality',
                    'priority': 'high' if rec.startswith('Address') or rec.startswith('Fix') else 'medium',
                    'title': rec,
                    'category': 'Code Quality'
                })
        
        # Security recommendations
        if 'security' in analysis_results and 'recommendations' in analysis_results['security']:
            for rec in analysis_results['security']['recommendations']:
                recommendations.append({
                    'type': 'security',
                    'priority': 'critical',
                    'title': rec,
                    'category': 'Security'
                })
        
        # Performance recommendations
        if 'performance' in analysis_results and 'recommendations' in analysis_results['performance']:
            for rec in analysis_results['performance']['recommendations']:
                recommendations.append({
                    'type': 'performance',
                    'priority': 'medium',
                    'title': rec,
                    'category': 'Performance'
                })
        
        # Architecture recommendations
        if 'architecture' in analysis_results and 'recommendations' in analysis_results['architecture']:
            for rec in analysis_results['architecture']['recommendations']:
                recommendations.append({
                    'type': 'architecture',
                    'priority': 'medium',
                    'title': rec,
                    'category': 'Architecture'
                })
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations
    
    def _generate_visualization_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for visualization"""
        viz_data = {}
        
        analysis_results = results.get('analysis_results', {})
        
        # Quality radar chart data
        if 'quality' in analysis_results:
            viz_data['quality_radar'] = analysis_results['quality'].get('dimension_scores', {})
        
        # File type distribution pie chart
        if 'structure' in analysis_results:
            viz_data['file_types'] = analysis_results['structure'].get('file_types', {})
        
        # Quality distribution bar chart
        if 'quality' in analysis_results:
            viz_data['quality_distribution'] = analysis_results['quality'].get('quality_distribution', {})
        
        # Recommendation priority distribution
        recommendations = results.get('recommendations', [])
        priority_dist = {}
        for rec in recommendations:
            priority = rec.get('priority', 'unknown')
            priority_dist[priority] = priority_dist.get(priority, 0) + 1
        viz_data['priority_distribution'] = priority_dist
        
        return viz_data
    
    # Helper methods for specific analyses
    
    def _extract_structure_insights(self, structure_data: Dict[str, Any]) -> List[str]:
        """Extract insights from structure analysis"""
        insights = []
        
        file_structure = structure_data.get('file_structure', {})
        total_files = file_structure.get('total_files', 0)
        
        if total_files > 1000:
            insights.append("Large codebase with 1000+ files - consider modularization")
        elif total_files < 10:
            insights.append("Small codebase - good for rapid development")
        
        return insights
    
    def _extract_semantic_insights(self, semantic_data: Dict[str, Any]) -> List[str]:
        """Extract insights from semantic analysis"""
        insights = []
        
        confidence_ratio = semantic_data.get('confidence_ratio', 0)
        if confidence_ratio > 0.8:
            insights.append("High semantic clarity - code is well-structured")
        elif confidence_ratio < 0.5:
            insights.append("Low semantic clarity - consider improving code organization")
        
        return insights
    
    def _identify_top_quality_issues(self, project_results: Dict[str, Any]) -> List[str]:
        """Identify top quality issues from analysis"""
        issues = []
        
        metrics = project_results['project_metrics']
        
        if metrics.maintainability_score < 60:
            issues.append("Low maintainability - complex code structure")
        
        if metrics.test_coverage < 50:
            issues.append("Insufficient test coverage")
        
        if metrics.documentation_score < 40:
            issues.append("Poor documentation - missing docstrings")
        
        return issues
    
    # Simplified analysis methods (would be more sophisticated in real implementation)
    
    async def _detect_tech_stack(self, target_path: Path) -> Dict[str, Any]:
        """Detect technology stack"""
        tech_stack = {
            'languages': [],
            'frameworks': [],
            'databases': [],
            'tools': []
        }
        
        # Simple file extension detection
        if list(target_path.rglob("*.py")):
            tech_stack['languages'].append('Python')
        if list(target_path.rglob("*.js")) or list(target_path.rglob("*.ts")):
            tech_stack['languages'].append('JavaScript/TypeScript')
        if list(target_path.rglob("*.java")):
            tech_stack['languages'].append('Java')
        
        return tech_stack
    
    def _detect_architectural_patterns(self, target_path: Path) -> List[str]:
        """Detect architectural patterns"""
        patterns = []
        
        # Simple pattern detection based on directory structure
        if (target_path / "models").exists():
            patterns.append("MVC/MVP Pattern")
        if (target_path / "api").exists() or (target_path / "routes").exists():
            patterns.append("REST API Pattern")
        if (target_path / "tests").exists():
            patterns.append("Test-Driven Development")
        
        return patterns
    
    def _calculate_modularity_score(self, target_path: Path) -> float:
        """Calculate modularity score"""
        # Simple calculation based on directory structure depth
        max_depth = 0
        for path in target_path.rglob("*"):
            if path.is_file():
                depth = len(path.relative_to(target_path).parts)
                max_depth = max(max_depth, depth)
        
        # Higher depth suggests better modularity (up to a point)
        return min(100, max_depth * 20)
    
    def _analyze_coupling(self, target_path: Path) -> Dict[str, Any]:
        """Analyze coupling between modules"""
        return {
            'coupling_level': 'medium',
            'high_coupling_files': [],
            'recommendations': ['Consider reducing inter-module dependencies']
        }
    
    def _assess_scalability(self, target_path: Path) -> Dict[str, Any]:
        """Assess scalability characteristics"""
        return {
            'scalability_score': 75,
            'bottlenecks': [],
            'recommendations': ['Consider implementing caching layers']
        }
    
    def _generate_architecture_recommendations(self, tech_stack: Dict, patterns: List[str]) -> List[str]:
        """Generate architecture recommendations"""
        recommendations = []
        
        if 'Test-Driven Development' not in patterns:
            recommendations.append("Implement comprehensive testing strategy")
        
        if not tech_stack['frameworks']:
            recommendations.append("Consider adopting a framework for better structure")
        
        return recommendations
    
    def _scan_file_for_security_issues(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan file for security issues"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Simple security pattern detection
            if 'eval(' in content:
                issues.append({
                    'file': str(file_path),
                    'issue': 'Use of eval() function',
                    'severity': 'high',
                    'line': 'unknown'
                })
            
            if 'password' in content.lower() and '=' in content:
                issues.append({
                    'file': str(file_path),
                    'issue': 'Potential hardcoded password',
                    'severity': 'critical',
                    'line': 'unknown'
                })
        
        except Exception:
            pass
        
        return issues
    
    def _categorize_security_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize security issues by severity"""
        categories = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for issue in issues:
            severity = issue.get('severity', 'low')
            categories[severity] = categories.get(severity, 0) + 1
        
        return categories
    
    def _identify_vulnerable_patterns(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Identify vulnerable patterns"""
        patterns = []
        for issue in issues:
            if issue['issue'] not in patterns:
                patterns.append(issue['issue'])
        return patterns
    
    def _generate_security_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if any('eval' in issue['issue'] for issue in issues):
            recommendations.append("Replace eval() with safer alternatives")
        
        if any('password' in issue['issue'].lower() for issue in issues):
            recommendations.append("Remove hardcoded credentials and use environment variables")
        
        return recommendations
    
    def _scan_file_for_performance_issues(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan file for performance issues"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Simple performance pattern detection
            if 'for ' in content and 'append(' in content:
                issues.append({
                    'file': str(file_path),
                    'issue': 'Potential list comprehension opportunity',
                    'severity': 'low'
                })
        
        except Exception:
            pass
        
        return issues
    
    def _categorize_performance_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize performance issues"""
        categories = {'algorithmic': 0, 'memory': 0, 'io': 0, 'other': 0}
        
        for issue in issues:
            # Simple categorization
            if 'comprehension' in issue['issue']:
                categories['algorithmic'] += 1
            else:
                categories['other'] += 1
        
        return categories
    
    def _identify_optimization_opportunities(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Identify optimization opportunities"""
        opportunities = []
        for issue in issues:
            if issue['issue'] not in opportunities:
                opportunities.append(issue['issue'])
        return opportunities
    
    def _generate_performance_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if any('comprehension' in issue['issue'] for issue in issues):
            recommendations.append("Use list comprehensions instead of explicit loops where appropriate")
        
        return recommendations

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Codebase Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_codebase.py /path/to/project
  python analyze_codebase.py /path/to/project --types quality security performance
  python analyze_codebase.py /path/to/project --output analysis_report.json --visualize
        """
    )
    
    parser.add_argument(
        'target',
        help='Path to codebase to analyze'
    )
    
    parser.add_argument(
        '--types',
        nargs='+',
        choices=['structure', 'quality', 'semantic', 'integration', 'architecture', 'security', 'performance'],
        help='Types of analysis to perform'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for results (JSON format)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'html', 'markdown'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Include visualization data in output'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    async def run_analysis():
        analyzer = CodebaseAnalyzer()
        
        results = await analyzer.analyze_codebase(
            target_path=args.target,
            analysis_types=args.types,
            output_format=args.format,
            include_visualization=args.visualize
        )
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Analysis results saved to {args.output}")
        else:
            # Pretty print summary
            if results['success']:
                summary = results['summary']
                print("\n📊 CODEBASE ANALYSIS COMPLETED")
                print(f"Target: {results['target_path']}")
                print(f"Analysis Types: {', '.join(results['analysis_types'])}")
                print(f"\n🏥 OVERALL HEALTH: {summary.get('overall_health', 'unknown').upper()}")
                
                if 'health_score' in summary:
                    print(f"Health Score: {summary['health_score']:.1f}/100")
                
                if 'file_count' in summary:
                    print(f"Files Analyzed: {summary['file_count']}")
                
                if 'quality_score' in summary:
                    print(f"Quality Score: {summary['quality_score']:.1f}/100")
                
                recommendations = results.get('recommendations', [])
                if recommendations:
                    print(f"\n🎯 TOP RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations[:5], 1):
                        priority_emoji = {
                            'critical': '🚨', 'high': '⚠️', 'medium': '💡', 'low': 'ℹ️'
                        }.get(rec['priority'], '📝')
                        print(f"  {i}. {priority_emoji} {rec['title']} ({rec['category']})")
                
                if 'integration_opportunities' in summary and summary['integration_opportunities'] > 0:
                    print(f"\n🔗 Integration Opportunities: {summary['integration_opportunities']}")
            else:
                print(f"❌ ANALYSIS FAILED: {results.get('error', 'Unknown error')}")
    
    # Run the async function
    asyncio.run(run_analysis())

if __name__ == "__main__":
    main()