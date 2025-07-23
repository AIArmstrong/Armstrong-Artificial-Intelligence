"""
Data models for the Supreme Improve module
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum

class QualityMetrics(BaseModel):
    """Comprehensive code quality metrics"""
    maintainability_score: float = Field(ge=0.0, le=100.0)
    complexity_score: float = Field(ge=0.0, le=100.0)
    readability_score: float = Field(ge=0.0, le=100.0)
    test_coverage: float = Field(ge=0.0, le=100.0)
    documentation_score: float = Field(ge=0.0, le=100.0)
    security_score: float = Field(ge=0.0, le=100.0)
    performance_score: float = Field(ge=0.0, le=100.0)
    overall_score: float = Field(ge=0.0, le=100.0)

    def calculate_overall(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'maintainability_score': 0.20,
            'complexity_score': 0.15,
            'readability_score': 0.15,
            'test_coverage': 0.15,
            'documentation_score': 0.10,
            'security_score': 0.15,
            'performance_score': 0.10
        }
        
        total = sum(
            getattr(self, metric) * weight 
            for metric, weight in weights.items()
        )
        self.overall_score = round(total, 2)
        return self.overall_score

class ImprovementRecommendation(BaseModel):
    """Single improvement recommendation with risk assessment"""
    id: str
    title: str
    description: str
    category: Literal["quality", "performance", "security", "maintainability", "architecture"]
    priority: Literal["critical", "high", "medium", "low"]
    effort_estimate: str  # e.g., "2-4 hours"
    risk_level: Literal["low", "medium", "high", "critical"]
    breaking_change_probability: float = Field(ge=0.0, le=1.0)
    expected_improvement: QualityMetrics
    code_changes: List[str]  # Specific files/lines to modify
    validation_steps: List[str]
    
    def get_impact_score(self) -> float:
        """Calculate impact score based on priority and expected improvement"""
        priority_weights = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.5,
            "low": 0.3
        }
        
        priority_weight = priority_weights.get(self.priority, 0.5)
        improvement_delta = self.expected_improvement.overall_score
        risk_factor = 1.0 - (self.breaking_change_probability * 0.5)
        
        return priority_weight * improvement_delta * risk_factor
    
class ReviewResult(BaseModel):
    """Multi-dimensional review analysis result"""
    review_type: Literal["code", "architecture", "debate"]
    target_files: List[str]
    quality_before: QualityMetrics
    recommendations: List[ImprovementRecommendation]
    risk_assessment: Dict[str, float]
    estimated_total_time: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    def get_top_recommendations(self, n: int = 5) -> List[ImprovementRecommendation]:
        """Get top N recommendations by impact score"""
        sorted_recs = sorted(
            self.recommendations,
            key=lambda r: r.get_impact_score(),
            reverse=True
        )
        return sorted_recs[:n]
    
class ImprovementOutcome(BaseModel):
    """Tracking implementation outcomes for learning"""
    recommendation_id: str
    implemented: bool
    implementation_time: Optional[str] = None
    quality_after: Optional[QualityMetrics] = None
    success_metrics: Dict[str, float] = Field(default_factory=dict)
    developer_feedback: Optional[str] = None
    issues_introduced: List[str] = Field(default_factory=list)
    actual_vs_predicted_risk: float = Field(default=0.0)
    
    def calculate_success_rate(self) -> float:
        """Calculate overall success rate of the improvement"""
        if not self.implemented or not self.quality_after:
            return 0.0
            
        # Success factors:
        # - Quality improvement achieved
        # - No critical issues introduced
        # - Risk prediction accuracy
        
        quality_improved = self.quality_after.overall_score > 0
        no_critical_issues = len(self.issues_introduced) == 0
        risk_accuracy = 1.0 - abs(self.actual_vs_predicted_risk)
        
        success_rate = (
            (0.5 * (1.0 if quality_improved else 0.0)) +
            (0.3 * (1.0 if no_critical_issues else 0.5)) +
            (0.2 * risk_accuracy)
        )
        
        return round(success_rate, 2)

class AnalysisConfig(BaseModel):
    """Configuration for code analysis"""
    max_file_size: int = Field(default=1_000_000, description="Max file size in bytes")
    timeout_seconds: int = Field(default=60, description="Analysis timeout")
    parallel_workers: int = Field(default=4, description="Number of parallel workers")
    quality_thresholds: Dict[str, float] = Field(
        default_factory=lambda: {
            "critical": 60.0,
            "acceptable": 70.0,
            "good": 80.0,
            "excellent": 90.0
        }
    )
    excluded_patterns: List[str] = Field(
        default_factory=lambda: [
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "dist",
            "build"
        ]
    )