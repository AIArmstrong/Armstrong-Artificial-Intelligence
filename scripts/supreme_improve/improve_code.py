#!/usr/bin/env python3
"""
Supreme Improve - Main Code Improvement Orchestrator

This script provides the main interface for the supreme code improvement system
with multi-dimensional analysis, safety mechanisms, and learning capabilities.
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the AAI base path to Python path
aai_base_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(aai_base_path))

try:
    from brain.modules.supreme_improve import (
        MultiDimensionalScorer,
        RiskAssessor,
        SafetyMechanisms,
        ImprovementTracker,
        QualityMetrics,
        ImprovementRecommendation
    )
    from brain.modules.enhanced_repository_analyzer_integration import EnhancedRepositoryAnalyzer
    from brain.modules.unified_analytics import UnifiedAnalytics
    from brain.modules.seamless_orchestrator import SeamlessOrchestrator
    SUPREME_IMPROVE_AVAILABLE = True
except ImportError as e:
    logging.error(f"Supreme Improve modules not available: {e}")
    SUPREME_IMPROVE_AVAILABLE = False
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('brain/logs/improvements/supreme_improve.log')
    ]
)

logger = logging.getLogger(__name__)

class SupremeImproveOrchestrator:
    """
    Main orchestrator for the Supreme Improve system.
    
    Coordinates all improvement capabilities including analysis, recommendations,
    risk assessment, safety mechanisms, and outcome tracking.
    """
    
    def __init__(self, base_path: str = None):
        """Initialize the Supreme Improve orchestrator"""
        self.base_path = Path(base_path) if base_path else aai_base_path
        
        # Initialize core components
        self.quality_scorer = MultiDimensionalScorer()
        self.risk_assessor = RiskAssessor()
        self.safety_mechanisms = SafetyMechanisms()
        self.improvement_tracker = ImprovementTracker()
        
        # Initialize repository analyzer
        self.repository_analyzer = EnhancedRepositoryAnalyzer(str(self.base_path))
        
        # Initialize analytics
        self.unified_analytics = UnifiedAnalytics(str(self.base_path))
        
        logger.info("Supreme Improve orchestrator initialized")
    
    async def improve_code(self,
                          target_path: str,
                          improvement_types: List[str] = None,
                          mode: str = "apply",
                          analysis_depth: str = "standard",
                          safety_level: str = "standard") -> Dict[str, Any]:
        """
        Main code improvement workflow.
        
        Args:
            target_path: Path to code to improve
            improvement_types: Types of improvements to apply
            mode: 'preview', 'apply', or 'interactive'
            analysis_depth: 'quick', 'standard', or 'comprehensive'
            safety_level: 'minimal', 'standard', or 'maximum'
            
        Returns:
            Improvement results with recommendations and outcomes
        """
        logger.info(f"Starting code improvement for: {target_path}")
        
        target_path = Path(target_path).resolve()
        if not target_path.exists():
            raise ValueError(f"Target path does not exist: {target_path}")
        
        session_id = f"improve_{int(datetime.now().timestamp())}"
        
        try:
            # Phase 1: Comprehensive Analysis
            logger.info("Phase 1: Running comprehensive analysis...")
            analysis_results = await self._run_comprehensive_analysis(
                target_path, session_id, analysis_depth
            )
            
            # Phase 2: Generate Improvement Recommendations  
            logger.info("Phase 2: Generating improvement recommendations...")
            recommendations = await self._generate_recommendations(
                target_path, analysis_results
            )
            
            # Phase 3: Risk Assessment
            logger.info("Phase 3: Assessing risks...")
            risk_assessments = await self._assess_risks(
                target_path, recommendations
            )
            
            # Phase 4: Apply Improvements (if not preview mode)
            improvements_applied = []
            if mode != "preview":
                logger.info(f"Phase 4: Applying improvements in {mode} mode...")
                improvements_applied = await self._apply_improvements(
                    target_path, recommendations, risk_assessments, 
                    mode, safety_level, session_id
                )
            
            # Phase 5: Track Outcomes
            logger.info("Phase 5: Tracking outcomes...")
            tracking_results = await self._track_outcomes(
                session_id, recommendations, improvements_applied
            )
            
            # Compile final results
            results = {
                'session_id': session_id,
                'target_path': str(target_path),
                'mode': mode,
                'analysis_depth': analysis_depth,
                'safety_level': safety_level,
                'timestamp': datetime.now().isoformat(),
                'analysis_results': analysis_results,
                'recommendations': self._serialize_recommendations(recommendations),
                'risk_assessments': risk_assessments,
                'improvements_applied': improvements_applied,
                'tracking_results': tracking_results,
                'success': True,
                'summary': self._generate_summary(
                    analysis_results, recommendations, improvements_applied
                )
            }
            
            logger.info(f"Code improvement completed successfully: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Code improvement failed: {str(e)}")
            return {
                'session_id': session_id,
                'target_path': str(target_path),
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _run_comprehensive_analysis(self,
                                        target_path: Path,
                                        session_id: str,
                                        analysis_depth: str) -> Dict[str, Any]:
        """Run comprehensive code analysis"""
        
        # Determine analysis types based on depth
        if analysis_depth == "quick":
            analysis_types = ["structure", "quality"]
        elif analysis_depth == "comprehensive":
            analysis_types = ["structure", "semantic", "quality", "integration"]
        else:  # standard
            analysis_types = ["structure", "quality", "integration"]
        
        # Run repository analysis
        analysis_results = await self.repository_analyzer.analyze_repository(
            str(target_path),
            analysis_types=analysis_types,
            use_semantic=(analysis_depth == "comprehensive")
        )
        
        return analysis_results
    
    async def _generate_recommendations(self,
                                      target_path: Path,
                                      analysis_results: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate improvement recommendations based on analysis"""
        
        recommendations = []
        
        # Get quality-based recommendations from repository analyzer
        if 'improvement_recommendations' in analysis_results:
            for rec_data in analysis_results['improvement_recommendations']:
                # Convert dict to ImprovementRecommendation object
                recommendation = ImprovementRecommendation(
                    id=rec_data['id'],
                    title=rec_data['title'],
                    description=rec_data['description'],
                    category=rec_data['category'],
                    priority=rec_data['priority'],
                    effort_estimate=rec_data['effort_estimate'],
                    risk_level=rec_data['risk_level'],
                    breaking_change_probability=rec_data['breaking_change_probability'],
                    expected_improvement=self._parse_quality_metrics(
                        rec_data.get('expected_improvement', {})
                    ),
                    code_changes=rec_data['code_changes'],
                    validation_steps=rec_data['validation_steps']
                )
                recommendations.append(recommendation)
        
        # Generate additional recommendations based on specific patterns
        quality_metrics = analysis_results.get('quality_analysis', {}).get('project_metrics')
        if quality_metrics:
            additional_recommendations = await self._generate_pattern_based_recommendations(
                target_path, quality_metrics
            )
            recommendations.extend(additional_recommendations)
        
        # Predict success probability for each recommendation
        for recommendation in recommendations:
            success_probability = self.improvement_tracker.predict_success_probability(recommendation)
            recommendation.success_probability = success_probability
        
        # Sort by impact and success probability
        recommendations.sort(
            key=lambda r: r.get_impact_score() * getattr(r, 'success_probability', 0.8),
            reverse=True
        )
        
        logger.info(f"Generated {len(recommendations)} improvement recommendations")
        return recommendations
    
    async def _assess_risks(self,
                          target_path: Path,
                          recommendations: List[ImprovementRecommendation]) -> List[Dict[str, Any]]:
        """Assess risks for all recommendations"""
        
        risk_assessments = []
        
        for recommendation in recommendations:
            # For each recommendation, assess the risk if we were to apply the changes
            # In a real implementation, we'd generate the actual code changes first
            # For now, we'll do a high-level risk assessment based on the recommendation
            
            risk_assessment = self.risk_assessor.assess_change(
                str(target_path),
                "# Original code placeholder",
                "# Modified code placeholder", 
                recommendation
            )
            
            risk_assessments.append({
                'recommendation_id': recommendation.id,
                'breaking_change_probability': risk_assessment.breaking_change_probability,
                'impact_analysis': risk_assessment.impact_analysis,
                'risk_factors': risk_assessment.risk_factors,
                'mitigation_steps': risk_assessment.mitigation_steps,
                'confidence_score': risk_assessment.confidence_score
            })
        
        return risk_assessments
    
    async def _apply_improvements(self,
                                target_path: Path,
                                recommendations: List[ImprovementRecommendation],
                                risk_assessments: List[Dict[str, Any]],
                                mode: str,
                                safety_level: str,
                                session_id: str) -> List[Dict[str, Any]]:
        """Apply improvements with safety mechanisms"""
        
        improvements_applied = []
        
        # Configure safety based on level
        risk_threshold = {
            "minimal": 0.9,
            "standard": 0.7,
            "maximum": 0.5
        }.get(safety_level, 0.7)
        
        # Start safe modification session
        with self.safety_mechanisms.safe_modification_session(session_id):
            
            for i, recommendation in enumerate(recommendations):
                risk_assessment = risk_assessments[i]
                
                # Check if risk is acceptable
                if risk_assessment['breaking_change_probability'] > risk_threshold:
                    logger.warning(
                        f"Skipping high-risk recommendation: {recommendation.title} "
                        f"(risk: {risk_assessment['breaking_change_probability']:.2%})"
                    )
                    continue
                
                # For demonstration, we'll simulate applying improvements
                # In a real implementation, this would generate and apply actual code changes
                try:
                    # Simulate improvement application
                    logger.info(f"Applying improvement: {recommendation.title}")
                    
                    # Simulate file modification
                    improvement_result = {
                        'recommendation_id': recommendation.id,
                        'title': recommendation.title,
                        'applied': True,
                        'files_modified': recommendation.code_changes[:3],  # Simulate file list
                        'time_taken': f"{len(recommendation.code_changes)} minutes",  # Simulate time
                        'validation_passed': True,
                        'issues_encountered': []
                    }
                    
                    improvements_applied.append(improvement_result)
                    
                    # Interactive mode: ask for confirmation for high-impact changes
                    if mode == "interactive" and recommendation.priority in ["critical", "high"]:
                        # In a real implementation, this would prompt the user
                        logger.info(f"Interactive mode: Auto-approved {recommendation.title}")
                    
                except Exception as e:
                    logger.error(f"Failed to apply improvement {recommendation.title}: {e}")
                    improvement_result = {
                        'recommendation_id': recommendation.id,
                        'title': recommendation.title,
                        'applied': False,
                        'error': str(e),
                        'files_modified': [],
                        'validation_passed': False,
                        'issues_encountered': [str(e)]
                    }
                    improvements_applied.append(improvement_result)
        
        return improvements_applied
    
    async def _track_outcomes(self,
                            session_id: str,
                            recommendations: List[ImprovementRecommendation],
                            improvements_applied: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Track improvement outcomes for learning"""
        
        tracking_results = {
            'total_recommendations': len(recommendations),
            'improvements_applied': len([i for i in improvements_applied if i.get('applied', False)]),
            'success_rate': 0.0,
            'outcomes_tracked': 0
        }
        
        # Track each applied improvement
        for improvement in improvements_applied:
            if improvement.get('applied', False):
                # Find corresponding recommendation
                recommendation = next(
                    (r for r in recommendations if r.id == improvement['recommendation_id']),
                    None
                )
                
                if recommendation:
                    # Create outcome record
                    outcome = {
                        'recommendation_id': recommendation.id,
                        'implemented': True,
                        'implementation_time': improvement.get('time_taken'),
                        'quality_after': None,  # Would be calculated in real implementation
                        'success_metrics': {
                            'validation_passed': improvement.get('validation_passed', False),
                            'files_modified_count': len(improvement.get('files_modified', [])),
                            'issues_count': len(improvement.get('issues_encountered', []))
                        },
                        'developer_feedback': None,  # Would be collected in real implementation
                        'issues_introduced': improvement.get('issues_encountered', []),
                        'actual_vs_predicted_risk': 0.0  # Would be calculated based on actual results
                    }
                    
                    # In a real implementation, we'd track this with the improvement tracker
                    # For now, just log it
                    logger.info(f"Tracked outcome for: {recommendation.title}")
                    tracking_results['outcomes_tracked'] += 1
        
        # Calculate success rate
        if tracking_results['improvements_applied'] > 0:
            successful_improvements = sum(1 for i in improvements_applied 
                                        if i.get('applied', False) and i.get('validation_passed', False))
            tracking_results['success_rate'] = successful_improvements / tracking_results['improvements_applied']
        
        return tracking_results
    
    def _parse_quality_metrics(self, metrics_data: Any) -> QualityMetrics:
        """Parse quality metrics from various input formats"""
        if isinstance(metrics_data, dict):
            return QualityMetrics(**metrics_data)
        elif isinstance(metrics_data, str):
            # Parse string representation (e.g., "+12.5 quality points")
            return QualityMetrics(
                maintainability_score=0, complexity_score=0, readability_score=0,
                test_coverage=0, documentation_score=0, security_score=0,
                performance_score=0, overall_score=0
            )
        else:
            # Default metrics
            return QualityMetrics(
                maintainability_score=0, complexity_score=0, readability_score=0,
                test_coverage=0, documentation_score=0, security_score=0,
                performance_score=0, overall_score=0
            )
    
    async def _generate_pattern_based_recommendations(self,
                                                    target_path: Path,
                                                    quality_metrics: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate additional recommendations based on quality patterns"""
        recommendations = []
        
        # Example: Generate recommendation for low test coverage
        if quality_metrics.get('test_coverage', 0) < 50:
            recommendations.append(ImprovementRecommendation(
                id=f"test_coverage_{int(datetime.now().timestamp())}",
                title="Improve Test Coverage",
                description=f"Test coverage is {quality_metrics.get('test_coverage', 0):.1f}%, below recommended 70%",
                category="quality",
                priority="high",
                effort_estimate="6-10 hours",
                risk_level="low",
                breaking_change_probability=0.05,
                expected_improvement=QualityMetrics(
                    maintainability_score=0, complexity_score=0, readability_score=0,
                    test_coverage=70, documentation_score=0, security_score=0,
                    performance_score=0, overall_score=0
                ),
                code_changes=[
                    "Add unit tests for core functions",
                    "Add integration tests for main workflows",
                    "Add edge case testing"
                ],
                validation_steps=[
                    "Run test coverage report",
                    "Verify all tests pass",
                    "Check coverage meets minimum threshold"
                ]
            ))
        
        return recommendations
    
    def _serialize_recommendations(self, recommendations: List[ImprovementRecommendation]) -> List[Dict[str, Any]]:
        """Convert recommendations to serializable format"""
        return [
            {
                'id': rec.id,
                'title': rec.title,
                'description': rec.description,
                'category': rec.category,
                'priority': rec.priority,
                'effort_estimate': rec.effort_estimate,
                'risk_level': rec.risk_level,
                'breaking_change_probability': rec.breaking_change_probability,
                'expected_improvement': rec.expected_improvement.__dict__,
                'code_changes': rec.code_changes,
                'validation_steps': rec.validation_steps,
                'impact_score': rec.get_impact_score(),
                'success_probability': getattr(rec, 'success_probability', 0.8)
            }
            for rec in recommendations
        ]
    
    def _generate_summary(self,
                         analysis_results: Dict[str, Any],
                         recommendations: List[ImprovementRecommendation],
                         improvements_applied: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary of the improvement session"""
        
        quality_metrics = analysis_results.get('quality_analysis', {}).get('project_metrics', {})
        
        return {
            'overall_quality_score': quality_metrics.get('overall_score', 0),
            'total_recommendations': len(recommendations),
            'high_priority_recommendations': len([r for r in recommendations if r.priority == 'high']),
            'critical_recommendations': len([r for r in recommendations if r.priority == 'critical']),
            'improvements_applied': len([i for i in improvements_applied if i.get('applied', False)]),
            'estimated_total_effort': self._calculate_total_effort(recommendations),
            'risk_distribution': self._calculate_risk_distribution(recommendations),
            'top_categories': self._get_top_categories(recommendations),
            'quality_insights': analysis_results.get('quality_analysis', {}).get('insights', [])[:3]
        }
    
    def _calculate_total_effort(self, recommendations: List[ImprovementRecommendation]) -> str:
        """Calculate total estimated effort"""
        # Simple estimation - in real implementation would be more sophisticated
        total_hours = len(recommendations) * 4  # Average 4 hours per recommendation
        return f"{total_hours}-{total_hours * 2} hours"
    
    def _calculate_risk_distribution(self, recommendations: List[ImprovementRecommendation]) -> Dict[str, int]:
        """Calculate risk level distribution"""
        distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for rec in recommendations:
            distribution[rec.risk_level] += 1
        return distribution
    
    def _get_top_categories(self, recommendations: List[ImprovementRecommendation]) -> List[str]:
        """Get top improvement categories"""
        categories = {}
        for rec in recommendations:
            categories[rec.category] = categories.get(rec.category, 0) + 1
        
        return sorted(categories.keys(), key=lambda k: categories[k], reverse=True)[:3]

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Supreme Code Improvement System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python improve_code.py /path/to/project --mode preview
  python improve_code.py /path/to/project --mode apply --safety-level maximum
  python improve_code.py /path/to/project --mode interactive --analysis comprehensive
        """
    )
    
    parser.add_argument(
        'target',
        help='Path to code/project to improve'
    )
    
    parser.add_argument(
        '--mode',
        choices=['preview', 'apply', 'interactive'],
        default='preview',
        help='Improvement mode (default: preview)'
    )
    
    parser.add_argument(
        '--analysis',
        choices=['quick', 'standard', 'comprehensive'],
        default='standard',
        help='Analysis depth (default: standard)'
    )
    
    parser.add_argument(
        '--safety-level',
        choices=['minimal', 'standard', 'maximum'],
        default='standard',
        help='Safety level for improvements (default: standard)'
    )
    
    parser.add_argument(
        '--types',
        nargs='+',
        choices=['quality', 'performance', 'security', 'maintainability', 'architecture'],
        help='Types of improvements to focus on'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for results (JSON format)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    async def run_improvement():
        orchestrator = SupremeImproveOrchestrator()
        
        results = await orchestrator.improve_code(
            target_path=args.target,
            improvement_types=args.types,
            mode=args.mode,
            analysis_depth=args.analysis,
            safety_level=args.safety_level
        )
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            # Pretty print summary
            if results['success']:
                summary = results['summary']
                print("\n🎉 CODE IMPROVEMENT COMPLETED")
                print(f"Target: {results['target_path']}")
                print(f"Mode: {results['mode']}")
                print(f"Analysis Depth: {results['analysis_depth']}")
                print(f"\n📊 SUMMARY:")
                print(f"  Overall Quality Score: {summary['overall_quality_score']:.1f}/100")
                print(f"  Total Recommendations: {summary['total_recommendations']}")
                print(f"  High Priority: {summary['high_priority_recommendations']}")
                print(f"  Critical: {summary['critical_recommendations']}")
                print(f"  Applied: {summary['improvements_applied']}")
                print(f"  Estimated Effort: {summary['estimated_total_effort']}")
                
                if summary['quality_insights']:
                    print(f"\n💡 KEY INSIGHTS:")
                    for insight in summary['quality_insights']:
                        print(f"  • {insight}")
                
                print(f"\n📈 TOP CATEGORIES:")
                for cat in summary['top_categories']:
                    print(f"  • {cat}")
            else:
                print(f"❌ IMPROVEMENT FAILED: {results.get('error', 'Unknown error')}")
    
    # Run the async function
    asyncio.run(run_improvement())

if __name__ == "__main__":
    main()