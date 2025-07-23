"""
Quality Analysis Enhancement for Enhanced Repository Analyzer

This module provides multi-dimensional quality scoring capabilities.
"""

import json
import sqlite3
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class QualityAnalysisEnhancement:
    """Enhancement module for multi-dimensional quality analysis"""
    
    def __init__(self, quality_scorer, db_path):
        self.quality_scorer = quality_scorer
        self.db_path = db_path
    
    async def perform_quality_analysis(self, repo_path: Path, session_id: str) -> Dict[str, Any]:
        """
        Perform multi-dimensional quality analysis using Supreme Improve modules.
        
        Args:
            repo_path: Path to repository
            session_id: Current analysis session ID
            
        Returns:
            Quality analysis results with metrics and insights
        """
        if not self.quality_scorer:
            logger.warning("Quality scorer not available - skipping quality analysis")
            return {'error': 'Quality scorer not available', 'project_metrics': None}
        
        try:
            # Perform project-wide quality scoring
            project_results = self.quality_scorer.score_project(
                str(repo_path),
                file_patterns=["*.py", "*.js", "*.ts", "*.java", "*.go", "*.rs", "*.cpp", "*.c"]
            )
            
            # Store quality metrics in database
            await self._store_quality_metrics(session_id, project_results)
            
            # Generate quality insights
            insights = self._generate_quality_insights(project_results)
            
            return {
                'project_metrics': project_results['project_metrics'].__dict__,
                'file_count': len(project_results['file_scores']),
                'summary': project_results['summary'],
                'insights': insights,
                'recommendations': project_results['recommendations'],
                'quality_distribution': project_results['summary']['quality_distribution']
            }
            
        except Exception as e:
            logger.error(f"Quality analysis failed: {str(e)}")
            return {
                'error': str(e),
                'project_metrics': None,
                'insights': [],
                'recommendations': []
            }
    
    async def generate_improvement_recommendations(self, 
                                                repo_path: Path, 
                                                quality_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate specific improvement recommendations based on quality analysis.
        
        Args:
            repo_path: Path to repository
            quality_results: Quality analysis results
            
        Returns:
            List of actionable improvement recommendations
        """
        recommendations = []
        
        try:
            if not quality_results.get('project_metrics'):
                return recommendations
            
            project_metrics = quality_results['project_metrics']
            
            # Maintainability recommendations
            if project_metrics['maintainability_score'] < 70:
                recommendations.append({
                    'id': f"maintainability_{int(time.time())}",
                    'title': 'Improve Code Maintainability',
                    'description': 'Code maintainability score is below acceptable threshold',
                    'category': 'maintainability',
                    'priority': 'high' if project_metrics['maintainability_score'] < 60 else 'medium',
                    'effort_estimate': '4-8 hours',
                    'risk_level': 'low',
                    'breaking_change_probability': 0.1,
                    'expected_improvement': f"+{70 - project_metrics['maintainability_score']:.1f} maintainability points",
                    'code_changes': [
                        'Reduce cyclomatic complexity in large functions',
                        'Extract reusable components',
                        'Improve naming conventions'
                    ],
                    'validation_steps': [
                        'Run complexity analysis tools',
                        'Review function size metrics',
                        'Validate naming consistency'
                    ]
                })
            
            # Complexity recommendations  
            if project_metrics['complexity_score'] < 70:
                recommendations.append({
                    'id': f"complexity_{int(time.time())}",
                    'title': 'Reduce Code Complexity',
                    'description': 'Code complexity is too high for maintainable development',
                    'category': 'quality',
                    'priority': 'high' if project_metrics['complexity_score'] < 50 else 'medium',
                    'effort_estimate': '6-12 hours',
                    'risk_level': 'medium',
                    'breaking_change_probability': 0.3,
                    'expected_improvement': f"+{70 - project_metrics['complexity_score']:.1f} complexity points",
                    'code_changes': [
                        'Break down large functions into smaller ones',
                        'Reduce nesting depth',
                        'Simplify conditional logic'
                    ],
                    'validation_steps': [
                        'Measure cyclomatic complexity',
                        'Run automated tests',
                        'Verify functionality preserved'
                    ]
                })
            
            # Security recommendations
            if project_metrics['security_score'] < 80:
                recommendations.append({
                    'id': f"security_{int(time.time())}",
                    'title': 'Address Security Vulnerabilities',
                    'description': 'Security analysis found potential vulnerabilities',
                    'category': 'security',
                    'priority': 'critical' if project_metrics['security_score'] < 60 else 'high',
                    'effort_estimate': '2-4 hours',
                    'risk_level': 'low',
                    'breaking_change_probability': 0.05,
                    'expected_improvement': f"+{80 - project_metrics['security_score']:.1f} security points",
                    'code_changes': [
                        'Fix identified security patterns',
                        'Add input validation',
                        'Update dependencies with vulnerabilities'
                    ],
                    'validation_steps': [
                        'Run security scanners',
                        'Perform penetration testing',
                        'Review authentication flows'
                    ]
                })
            
            # Documentation recommendations
            if project_metrics['documentation_score'] < 60:
                recommendations.append({
                    'id': f"documentation_{int(time.time())}",
                    'title': 'Improve Code Documentation',
                    'description': 'Code documentation is insufficient for maintainability',
                    'category': 'maintainability',
                    'priority': 'medium',
                    'effort_estimate': '3-6 hours',
                    'risk_level': 'low',
                    'breaking_change_probability': 0.0,
                    'expected_improvement': f"+{60 - project_metrics['documentation_score']:.1f} documentation points",
                    'code_changes': [
                        'Add docstrings to public functions',
                        'Update README with usage examples',
                        'Add inline comments for complex logic'
                    ],
                    'validation_steps': [
                        'Check documentation coverage',
                        'Verify examples work correctly',
                        'Review API documentation'
                    ]
                })
            
            # Performance recommendations
            if project_metrics['performance_score'] < 70:
                recommendations.append({
                    'id': f"performance_{int(time.time())}",
                    'title': 'Optimize Performance',
                    'description': 'Performance analysis suggests optimization opportunities',
                    'category': 'performance',
                    'priority': 'medium',
                    'effort_estimate': '4-8 hours',
                    'risk_level': 'medium',
                    'breaking_change_probability': 0.2,
                    'expected_improvement': f"+{70 - project_metrics['performance_score']:.1f} performance points",
                    'code_changes': [
                        'Optimize database queries',
                        'Implement caching strategies',
                        'Reduce algorithmic complexity'
                    ],
                    'validation_steps': [
                        'Run performance benchmarks',
                        'Monitor resource usage',
                        'Validate output correctness'
                    ]
                })
            
            logger.info(f"Generated {len(recommendations)} improvement recommendations")
            
        except Exception as e:
            logger.error(f"Failed to generate improvement recommendations: {str(e)}")
        
        return recommendations
    
    async def _store_quality_metrics(self, session_id: str, project_results: Dict[str, Any]):
        """Store quality metrics in database for tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store project-level metrics
            project_metrics = project_results['project_metrics']
            
            cursor.execute('''
                INSERT INTO quality_metrics 
                (session_id, file_path, maintainability_score, complexity_score, 
                 readability_score, test_coverage, documentation_score, 
                 security_score, performance_score, overall_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                'PROJECT_SUMMARY',
                project_metrics.maintainability_score,
                project_metrics.complexity_score,
                project_metrics.readability_score,
                project_metrics.test_coverage,
                project_metrics.documentation_score,
                project_metrics.security_score,
                project_metrics.performance_score,
                project_metrics.overall_score,
                datetime.now().isoformat()
            ))
            
            # Store individual file metrics (sample only to avoid overwhelming DB)
            file_scores = project_results.get('file_scores', {})
            for file_path, metrics in list(file_scores.items())[:10]:  # Limit to 10 files
                cursor.execute('''
                    INSERT INTO quality_metrics 
                    (session_id, file_path, maintainability_score, complexity_score,
                     readability_score, test_coverage, documentation_score,
                     security_score, performance_score, overall_score, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    file_path,
                    metrics.maintainability_score,
                    metrics.complexity_score,
                    metrics.readability_score,
                    metrics.test_coverage,
                    metrics.documentation_score,
                    metrics.security_score,
                    metrics.performance_score,
                    metrics.overall_score,
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store quality metrics: {str(e)}")
    
    def _generate_quality_insights(self, project_results: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from quality analysis"""
        insights = []
        
        try:
            project_metrics = project_results['project_metrics']
            summary = project_results['summary']
            
            # Overall quality insight
            if project_metrics.overall_score >= 80:
                insights.append("🎉 Excellent overall code quality - well above industry standards")
            elif project_metrics.overall_score >= 70:
                insights.append("✅ Good code quality with room for targeted improvements")
            elif project_metrics.overall_score >= 60:
                insights.append("⚠️ Acceptable quality but several areas need attention")
            else:
                insights.append("🚨 Code quality needs significant improvement across multiple dimensions")
            
            # File distribution insights
            quality_dist = summary['quality_distribution']
            total_files = summary['total_files']
            
            if quality_dist['critical'] > 0:
                critical_pct = (quality_dist['critical'] / total_files) * 100
                insights.append(f"🔴 {critical_pct:.1f}% of files ({quality_dist['critical']}) have critical quality issues")
            
            if quality_dist['excellent'] > 0:
                excellent_pct = (quality_dist['excellent'] / total_files) * 100
                insights.append(f"🌟 {excellent_pct:.1f}% of files ({quality_dist['excellent']}) meet excellent quality standards")
            
            # Specific dimension insights
            if project_metrics.security_score < 70:
                insights.append("🔒 Security analysis found vulnerabilities requiring immediate attention")
            
            if project_metrics.test_coverage < 60:
                insights.append("📊 Test coverage is below recommended 60% minimum")
            
            if project_metrics.documentation_score < 50:
                insights.append("📝 Documentation is sparse - consider adding docstrings and comments")
            
            if project_metrics.performance_score > 85:
                insights.append("⚡ Code shows good performance characteristics with efficient patterns")
            
        except Exception as e:
            logger.error(f"Failed to generate quality insights: {str(e)}")
            insights.append("❓ Unable to generate insights due to analysis error")
        
        return insights