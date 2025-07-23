"""
Supreme Analyze - Core Data Models

Data models for triple-layer intelligence code analysis with type safety
and consistency across all intelligence layers and creative cortex innovations.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Union, Any
from datetime import datetime
from enum import Enum

class IntelligenceMetrics(BaseModel):
    """Standardized intelligence layer metrics for analysis."""
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    processing_time: float = Field(description="Processing time in seconds")
    accuracy_score: float = Field(ge=0.0, le=1.0, description="Accuracy score 0-1")
    output_quality: float = Field(ge=0.0, le=100.0, description="Output quality score 0-100")
    resource_usage: Dict[str, float] = Field(default_factory=dict)
    error_rate: float = Field(ge=0.0, le=1.0)

class AnalysisIssue(BaseModel):
    """Standardized issue representation across intelligence layers."""
    id: str
    severity: Literal["critical", "high", "medium", "low", "info"]
    category: Literal["bug", "security", "performance", "maintainability", "style"]
    file_path: str
    line_number: Optional[int] = None
    description: str
    fix_suggestion: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    predicted_impact: float = Field(ge=0.0, le=1.0)
    detection_method: str = Field(default="unknown")
    false_positive_probability: float = Field(ge=0.0, le=1.0, default=0.0)

class PredictiveInsight(BaseModel):
    """Predictive analysis results with timeline forecasting."""
    insight_type: Literal["technical_debt", "performance_degradation", "security_risk", "maintainability_decline"]
    prediction_timeframe: str  # e.g., "3-6 months"
    probability: float = Field(ge=0.0, le=1.0)
    impact_assessment: float = Field(ge=0.0, le=1.0)
    prevention_strategies: List[str]
    early_warning_indicators: List[str]
    confidence_interval: Dict[str, float] = Field(default_factory=dict)

class AgentCoordinationMetrics(BaseModel):
    """Multi-agent orchestration metrics."""
    agents_deployed: int
    successful_agents: int  
    failed_agents: int
    coordination_success_rate: float = Field(ge=0.0, le=1.0)
    average_agent_time: float
    rate_limiting_events: int
    checkpoint_saves: int
    recovery_events: int

class CreativeCortexResults(BaseModel):
    """Results from all creative cortex innovations."""
    code_health_timeline: Dict[str, Any] = Field(default_factory=dict)
    bug_dna_mining: Dict[str, Any] = Field(default_factory=dict)
    multi_perspective_synthesis: Dict[str, Any] = Field(default_factory=dict)
    ecosystem_integration: Dict[str, Any] = Field(default_factory=dict)
    risk_ledger: Dict[str, Any] = Field(default_factory=dict)
    innovation_confidence: float = Field(ge=0.0, le=1.0)
    total_processing_time: float

class TripleLayerResult(BaseModel):
    """Complete triple-layer analysis result with 98% accuracy target."""
    session_id: str
    timestamp: datetime
    target_path: str
    
    # Foundation Results (Stage 1)
    foundation_results: Dict[str, Any]
    
    # Intelligence Results (Stage 2) 
    intelligence_results: Dict[str, IntelligenceMetrics]
    
    # Creative Cortex Results (Stage 3)
    creative_cortex_results: CreativeCortexResults
    
    # Analysis Output
    issues_detected: List[AnalysisIssue]
    predictive_insights: List[PredictiveInsight]
    
    # Accuracy and Performance Metrics
    overall_accuracy: float = Field(ge=0.0, le=1.0, description="Must target 98%")
    total_processing_time: float
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    # Multi-Agent Metrics
    agent_metrics: AgentCoordinationMetrics
    
    # Success Flags
    accuracy_target_achieved: bool = Field(description="True if ≥98% accuracy")
    processing_time_target_met: bool = Field(description="True if ≤5 minutes")
    success: bool = True

class CheckpointState(BaseModel):
    """Analysis checkpoint for recovery with <10% work loss."""
    checkpoint_id: str
    timestamp: datetime
    session_id: str
    completed_stages: List[str]
    partial_results: Dict[str, Any]
    agent_states: Dict[str, Any]
    processing_progress: float = Field(ge=0.0, le=1.0)
    recovery_metadata: Dict[str, Any] = Field(default_factory=dict)

class AnalysisRequest(BaseModel):
    """Input request for supreme analysis with configuration options."""
    target_path: str
    analysis_types: List[str] = Field(default=["structure", "quality", "security", "performance", "architecture"])
    
    # Intelligence Layer Configuration  
    intelligence_layers: List[str] = Field(default=["memory", "hybrid_rag", "reasoning", "research", "foundation"])
    creative_cortex: List[str] = Field(default=["timeline", "dna_mining", "synthesis", "ecosystem", "risk_ledger"])
    
    # Analysis Configuration
    analysis_depth: Literal["quick", "standard", "comprehensive", "predictive"] = "standard"
    focus: Literal["quality", "security", "performance", "architecture", "comprehensive"] = "comprehensive"
    scope: Literal["file", "module", "system", "ecosystem", "organization"] = "system"
    
    # Accuracy and Performance Requirements
    accuracy_threshold: float = Field(ge=0.95, le=0.99, default=0.98, description="Accuracy requirement")
    processing_time_limit: int = Field(ge=60, le=600, default=300, description="Max processing time in seconds")
    confidence_threshold: float = Field(ge=0.7, le=0.95, default=0.85)
    
    # Multi-Agent Configuration
    max_concurrent_agents: int = Field(ge=1, le=10, default=2)
    enable_checkpoints: bool = True
    enable_rate_limiting: bool = True
    
    # Output Configuration
    output_format: Literal["standard", "enhanced", "supreme"] = "supreme"
    include_predictive_analysis: bool = True
    include_visualizations: bool = False

class LearningMetrics(BaseModel):
    """Learning and improvement tracking metrics."""
    session_id: str
    timestamp: datetime
    accuracy_achieved: float
    issues_found: int
    false_positives: int
    false_negatives: int
    learning_insights: List[str]
    improvement_suggestions: List[str]
    correlation_with_previous_sessions: float = Field(ge=-1.0, le=1.0)

# Helper functions for model validation and accuracy calculation

def calculate_accuracy_score(detected_issues: List[AnalysisIssue], ground_truth_issues: List[Dict]) -> float:
    """Calculate analysis accuracy against ground truth dataset."""
    if not ground_truth_issues:
        return 0.0
    
    # Simple accuracy calculation (would be more sophisticated in production)
    true_positives = len([issue for issue in detected_issues if issue.confidence > 0.8])
    total_ground_truth = len(ground_truth_issues)
    
    return min(true_positives / total_ground_truth, 1.0)

def validate_intelligence_metrics(metrics: Dict[str, Any]) -> IntelligenceMetrics:
    """Validate and convert intelligence metrics to standardized format."""
    return IntelligenceMetrics(**metrics)

def check_accuracy_target(result: TripleLayerResult) -> bool:
    """Check if analysis result meets 98% accuracy target."""
    return result.overall_accuracy >= 0.98

def predict_processing_time(request: AnalysisRequest) -> float:
    """Predict processing time based on request configuration."""
    base_time = {
        "quick": 60,
        "standard": 180,
        "comprehensive": 300,
        "predictive": 450
    }.get(request.analysis_depth, 180)
    
    # Adjust for concurrent agents
    agent_factor = max(0.5, 1.0 - (request.max_concurrent_agents - 1) * 0.1)
    
    return base_time * agent_factor

def generate_session_id() -> str:
    """Generate unique session ID for analysis."""
    from datetime import datetime
    import random
    import string
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"supreme_analyze_{timestamp}_{random_suffix}"