"""
Pydantic models for R1 Reasoning Engine

Defines data structures for reasoning chains, confidence scoring,
and AAI-compliant response formats.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum


class ReasoningStep(BaseModel):
    """Individual step in reasoning chain"""
    step_number: int
    description: str
    reasoning: str
    confidence: float = Field(ge=0.70, le=0.95, description="AAI confidence range")
    evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class ReasoningMethod(str, Enum):
    """Types of reasoning methods"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    COMPARATIVE = "comparative"
    CAUSAL = "causal"


class ReasoningDepth(str, Enum):
    """Reasoning depth levels"""
    QUICK = "quick"
    THOROUGH = "thorough"
    EXHAUSTIVE = "exhaustive"


class ReasoningChain(BaseModel):
    """Complete reasoning chain with confidence analysis"""
    query: str
    steps: List[ReasoningStep]
    final_conclusion: str
    overall_confidence: float = Field(ge=0.70, le=0.95, description="AAI overall confidence")
    reasoning_method: ReasoningMethod = ReasoningMethod.DEDUCTIVE
    evidence_quality: float = Field(default=0.5, ge=0.0, le=1.0)
    assumption_risk: float = Field(default=0.5, ge=0.0, le=1.0)
    complexity_score: float = Field(default=0.5, ge=0.0, le=1.0)
    reasoning_time_ms: int = 0
    created_at: datetime = Field(default_factory=datetime.now)


class InferenceBackend(str, Enum):
    """Available inference backends"""
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"


class ModelInferenceConfig(BaseModel):
    """Configuration for dual-model setup"""
    reasoning_model: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    tool_model: str = "meta-llama/Llama-3.3-70B-Instruct"
    inference_backend: InferenceBackend = InferenceBackend.HUGGINGFACE
    max_tokens: int = 4096
    temperature: float = 0.1  # Low for consistent reasoning
    reasoning_temperature: float = 0.3  # Slightly higher for creativity
    timeout_seconds: int = 60
    retry_attempts: int = 3


class DocumentAnalysisRequest(BaseModel):
    """Request for document-based reasoning"""
    query: str
    user_id: str = "anonymous"
    document_limit: int = Field(default=5, le=20)
    reasoning_depth: ReasoningDepth = ReasoningDepth.THOROUGH
    confidence_threshold: float = Field(default=0.75, ge=0.70, le=0.95)
    include_reasoning_chain: bool = True
    include_alternatives: bool = True
    include_limitations: bool = True
    source_filter: Optional[str] = None
    context_window: int = Field(default=8192, le=32768)


class ConfidenceAnalysis(BaseModel):
    """Detailed confidence analysis"""
    overall: float = Field(ge=0.70, le=0.95)
    reasoning_confidence: float = Field(ge=0.70, le=0.95)
    evidence_confidence: float = Field(ge=0.0, le=1.0)
    source_reliability: float = Field(ge=0.0, le=1.0)
    assumption_certainty: float = Field(ge=0.0, le=1.0)
    reasoning_coherence: float = Field(ge=0.0, le=1.0)
    
    
class SupportingDocument(BaseModel):
    """Supporting document information"""
    filename: str
    chunk_id: str
    content_preview: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    confidence_score: float = Field(ge=0.70, le=0.95)
    source_quality: float = Field(ge=0.0, le=1.0)
    page_number: Optional[int] = None
    section: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlternativePerspective(BaseModel):
    """Alternative viewpoint or perspective"""
    perspective: str
    reasoning: str
    confidence: float = Field(ge=0.70, le=0.95)
    evidence_support: List[str] = Field(default_factory=list)
    likelihood: float = Field(ge=0.0, le=1.0)


class ReasoningLimitation(BaseModel):
    """Identified limitation in reasoning"""
    limitation_type: str
    description: str
    impact_level: str  # "low", "medium", "high"
    mitigation: Optional[str] = None


class ReasoningResponse(BaseModel):
    """Complete reasoning response with analysis"""
    answer: str
    reasoning_chain: ReasoningChain
    supporting_documents: List[SupportingDocument] = Field(default_factory=list)
    confidence_analysis: ConfidenceAnalysis
    alternative_perspectives: List[AlternativePerspective] = Field(default_factory=list)
    limitations: List[ReasoningLimitation] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)
    processing_time_ms: int
    model_used: str
    request_id: str
    created_at: datetime = Field(default_factory=datetime.now)


class VectorSearchRequest(BaseModel):
    """Request for vector-based document search"""
    query: str
    max_results: int = Field(default=10, le=50)
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    min_confidence: float = Field(default=0.70, ge=0.70, le=0.95)
    document_type_filter: Optional[str] = None
    date_range_filter: Optional[Dict[str, str]] = None


class VectorSearchResult(BaseModel):
    """Result from vector search"""
    chunk_id: str
    content: str
    filename: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    confidence_score: float = Field(ge=0.70, le=0.95)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    chunk_type: str = "text"
    page_number: Optional[int] = None


class JinaResearchRequest(BaseModel):
    """Request for Jina-based research"""
    topic: str
    max_pages: int = Field(default=5, le=20)
    quality_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    include_academic: bool = True
    include_news: bool = True
    include_documentation: bool = True
    date_filter: Optional[str] = None  # "1d", "1w", "1m", "1y"


class JinaResearchResult(BaseModel):
    """Result from Jina research"""
    url: str
    title: str
    content: str
    quality_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    source_type: str  # "academic", "news", "documentation", "blog"
    publication_date: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    """Document chunk for processing"""
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(default=0.70, ge=0.70, le=0.95)
    quality_score: float = Field(default=0.5, ge=0.0, le=1.0)
    chunk_type: str = "text"
    processing_timestamp: datetime = Field(default_factory=datetime.now)


class ReasoningVisualization(BaseModel):
    """Data for reasoning chain visualization"""
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_flow: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_mapping: Dict[str, List[str]] = Field(default_factory=dict)
    assumption_tracking: List[Dict[str, Any]] = Field(default_factory=list)


class SystemStatus(BaseModel):
    """System status information"""
    reasoning_engine_status: str
    tool_execution_status: str
    vector_store_status: str
    inference_backend_status: str
    available_models: List[str] = Field(default_factory=list)
    current_load: float = Field(ge=0.0, le=1.0)
    average_response_time_ms: float = 0.0
    success_rate: float = Field(ge=0.0, le=1.0)
    last_updated: datetime = Field(default_factory=datetime.now)


class ReasoningMetrics(BaseModel):
    """Metrics for reasoning performance"""
    total_queries: int = 0
    successful_queries: int = 0
    average_confidence: float = Field(ge=0.70, le=0.95)
    average_processing_time_ms: float = 0.0
    reasoning_accuracy: float = Field(ge=0.0, le=1.0)
    user_satisfaction: float = Field(ge=0.0, le=5.0)
    common_query_patterns: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    last_calculated: datetime = Field(default_factory=datetime.now)