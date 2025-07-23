"""
Supreme PRP - Core Data Models

Data models for triple-layer intelligence PRP generation with type safety
and consistency across all intelligence layers and creative cortex innovations.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Union, Any
from datetime import datetime
from enum import Enum

class IntelligenceLayer(BaseModel):
    """Base intelligence layer model with standardized metrics."""
    name: str
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    processing_time: float = Field(description="Processing time in seconds")
    output_quality: float = Field(ge=0.0, le=1.0, description="Output quality score 0-1")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    integration_status: str = Field(default="active")

class ResearchSource(BaseModel):
    """Research source with authority weighting and quality metrics."""
    url: str
    authority_score: float = Field(ge=0.0, le=1.0, description="Authority score based on source credibility")
    content_quality: float = Field(ge=0.0, le=1.0, description="Content quality assessment")
    source_type: Literal["official", "community", "security", "academic"]
    content: str
    extracted_at: datetime
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance to PRP requirements")
    bias_flags: List[str] = Field(default_factory=list)

class PRPStrategy(BaseModel):
    """Implementation strategy with complexity awareness and risk assessment."""
    name: str
    complexity: Literal["mvp", "enhanced", "future_proof"]
    confidence: float = Field(ge=0.0, le=1.0)
    risk_score: float = Field(ge=0.0, le=1.0, description="Risk assessment score")
    estimated_time: str
    prerequisites: List[str]
    success_probability: float = Field(ge=0.0, le=1.0)
    implementation_steps: List[str]
    validation_criteria: List[str]

class PRPQualityScore(BaseModel):
    """Comprehensive PRP quality assessment with 12-point scoring matrix."""
    foundation_quality: float = Field(ge=0.0, le=2.0, description="Stage 1 completeness (0-2 points)")
    intelligence_integration: float = Field(ge=0.0, le=3.0, description="Stage 2 enhancement depth (0-3 points)")
    creative_innovations: float = Field(ge=0.0, le=3.0, description="Stage 3 supremacy features (0-3 points)")
    research_comprehensiveness: float = Field(ge=0.0, le=2.0, description="Documentation depth and quality (0-2 points)")
    readiness_assessment: float = Field(ge=-2.0, le=2.0, description="Implementation readiness score (-2 to +2)")
    total_score: float = Field(ge=0.0, le=12.0, description="Total quality score")
    predicted_success_rate: float = Field(ge=0.0, le=1.0)

class CreativeCortexOutput(BaseModel):
    """Output from creative cortex innovations."""
    smart_prp_dna: Dict[str, Any] = Field(default_factory=dict)
    authority_research: Dict[str, Any] = Field(default_factory=dict)
    complexity_planning: Dict[str, Any] = Field(default_factory=dict)
    prerequisite_provisioning: Dict[str, Any] = Field(default_factory=dict)
    bias_gap_audit: Dict[str, Any] = Field(default_factory=dict)
    innovation_confidence: float = Field(ge=0.0, le=1.0)
    processing_time: float

class TripleLayerPRPResult(BaseModel):
    """Complete triple-layer PRP generation result."""
    session_id: str
    timestamp: datetime
    
    # Foundation Layer Results
    foundation_results: Dict[str, Any]
    
    # Intelligence Layer Results  
    memory_intelligence: IntelligenceLayer
    research_intelligence: IntelligenceLayer
    hybrid_rag_intelligence: IntelligenceLayer
    reasoning_intelligence: IntelligenceLayer
    tool_selection_intelligence: IntelligenceLayer
    
    # Creative Cortex Results
    creative_cortex_output: CreativeCortexOutput
    
    # Final PRP Output
    generated_prp_path: str
    research_sources: List[ResearchSource]
    implementation_strategies: List[PRPStrategy] 
    quality_assessment: PRPQualityScore
    
    # Success Metrics
    overall_confidence: float = Field(ge=0.0, le=1.0)
    predicted_success_rate: float = Field(ge=0.0, le=1.0)
    total_processing_time: float
    success: bool = True

class PRPGenerationRequest(BaseModel):
    """Input request for PRP generation with configuration options."""
    feature_description: str
    requirements: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    
    # Intelligence Layer Configuration
    intelligence_layers: List[str] = Field(default=["memory", "research", "hybrid_rag", "reasoning", "tool_selection"])
    creative_cortex: List[str] = Field(default=["smart_prp_dna", "authority_research", "complexity_planning", "prerequisite_provisioning", "bias_gap_audit"])
    
    # Research Configuration
    research_depth: Literal["quick", "standard", "comprehensive"] = "standard"
    min_research_pages: int = Field(ge=30, le=100, default=30)
    
    # Quality Thresholds
    confidence_threshold: float = Field(ge=0.7, le=0.95, default=0.85)
    quality_threshold: float = Field(ge=8.0, le=12.0, default=10.0)
    
    # Output Configuration
    output_format: Literal["standard", "enhanced", "supreme"] = "supreme"
    include_readiness_assessment: bool = True

# Helper functions for model validation and conversion

def validate_intelligence_metrics(metrics: Dict[str, Any]) -> IntelligenceLayer:
    """Validate and convert intelligence metrics to standardized format."""
    return IntelligenceLayer(**metrics)

def calculate_overall_quality(quality_scores: Dict[str, float]) -> float:
    """Calculate overall PRP quality score from component scores."""
    total = sum([
        quality_scores.get("foundation_quality", 0),
        quality_scores.get("intelligence_integration", 0), 
        quality_scores.get("creative_innovations", 0),
        quality_scores.get("research_comprehensiveness", 0),
        quality_scores.get("readiness_assessment", 0)
    ])
    return min(total, 12.0)

def predict_success_rate(quality_score: float) -> float:
    """Predict implementation success rate based on quality score."""
    success_mapping = {
        12: 0.98,    # Supreme Excellence
        11: 0.95,    # Excellent  
        10: 0.95,    # Excellent
        9: 0.85,     # Good
        8: 0.85,     # Good
        7: 0.70,     # Needs improvement
        6: 0.70,     # Needs improvement
    }
    
    # Linear interpolation for scores not in mapping
    floor_score = int(quality_score)
    if floor_score in success_mapping:
        return success_mapping[floor_score]
    elif floor_score < 6:
        return 0.50  # Below 50% for scores under 6
    else:
        return 0.85  # Default good prediction