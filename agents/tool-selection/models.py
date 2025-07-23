"""
Data Models for Tool Selection Enhancement

Pydantic models for tool selection, Fabric patterns, and confidence scoring
with AAI compliance and structured analysis.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class PromptContext(str, Enum):
    """Context types for prompt analysis"""
    ANALYSIS = "analysis"
    CREATION = "creation"
    RESEARCH = "research"
    EXTRACTION = "extraction"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    IMPLEMENTATION = "implementation"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


class ToolCategory(str, Enum):
    """Categories of tools and patterns"""
    ANALYSIS = "analysis"
    CONTENT_CREATION = "content_creation"
    CODE_DEVELOPMENT = "code_development"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    AUTOMATION = "automation"
    RESEARCH = "research"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    TESTING = "testing"


class FabricPattern(BaseModel):
    """Fabric pattern metadata and configuration"""
    name: str = Field(..., description="Pattern name")
    description: str = Field(..., description="Pattern description")
    category: str = Field(..., description="Pattern category")
    input_format: str = Field(..., description="Expected input format")
    output_format: str = Field(..., description="Expected output format")
    use_cases: List[str] = Field(default_factory=list, description="Common use cases")
    complexity_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Pattern complexity")
    effectiveness_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Historical effectiveness")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies")
    execution_time_estimate: int = Field(default=30, description="Estimated execution time in seconds")
    tags: List[str] = Field(default_factory=list, description="Pattern tags")
    
    
class ToolMetadata(BaseModel):
    """Metadata for available tools"""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    category: ToolCategory = Field(..., description="Tool category")
    capabilities: List[str] = Field(default_factory=list, description="Tool capabilities")
    requirements: List[str] = Field(default_factory=list, description="Tool requirements")
    confidence_baseline: float = Field(default=0.75, ge=0.70, le=0.95, description="AAI confidence baseline")
    performance_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Performance score")
    reliability_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Reliability score")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class ContextAnalysis(BaseModel):
    """Analysis result for prompt context"""
    original_prompt: str = Field(..., description="Original prompt text")
    prompt_snippet: str = Field(..., description="First 100 characters analyzed")
    detected_context: PromptContext = Field(..., description="Detected context type")
    confidence_score: float = Field(ge=0.70, le=0.95, description="Context detection confidence")
    keywords_found: List[str] = Field(default_factory=list, description="Context keywords found")
    complexity_indicators: List[str] = Field(default_factory=list, description="Complexity indicators")
    domain_indicators: List[str] = Field(default_factory=list, description="Domain-specific indicators")
    urgency_level: int = Field(default=1, ge=1, le=5, description="Task urgency level")
    estimated_effort: int = Field(default=1, ge=1, le=10, description="Estimated effort level")


class ToolSelection(BaseModel):
    """Tool selection result with reasoning"""
    prompt_snippet: str = Field(..., description="First 100 characters analyzed")
    detected_context: PromptContext = Field(..., description="Detected context")
    selected_patterns: List[FabricPattern] = Field(default_factory=list, description="Selected Fabric patterns")
    selected_tools: List[ToolMetadata] = Field(default_factory=list, description="Selected tools")
    confidence_score: float = Field(ge=0.70, le=0.95, description="AAI selection confidence")
    reasoning: str = Field(..., description="Selection reasoning")
    execution_plan: List[str] = Field(default_factory=list, description="Execution plan steps")
    alternatives: List[Dict[str, Any]] = Field(default_factory=list, description="Alternative selections")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    success_probability: float = Field(default=0.8, ge=0.0, le=1.0, description="Success probability")
    estimated_time_minutes: int = Field(default=5, description="Estimated execution time")
    created_at: datetime = Field(default_factory=datetime.now, description="Selection timestamp")


class SelectionResult(BaseModel):
    """Complete selection process result"""
    context_analysis: ContextAnalysis = Field(..., description="Context analysis result")
    tool_selection: ToolSelection = Field(..., description="Tool selection result")
    execution_results: List[Dict[str, Any]] = Field(default_factory=list, description="Execution results")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Execution success rate")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    learning_feedback: Dict[str, Any] = Field(default_factory=dict, description="Learning feedback")
    session_id: str = Field(..., description="Session identifier")
    user_feedback: Optional[Dict[str, Any]] = Field(default=None, description="User feedback")


class LearningRecord(BaseModel):
    """Record for learning from selection results"""
    selection_id: str = Field(..., description="Selection identifier")
    prompt_context: PromptContext = Field(..., description="Original context")
    tools_selected: List[str] = Field(..., description="Selected tool names")
    patterns_selected: List[str] = Field(..., description="Selected pattern names")
    execution_success: bool = Field(..., description="Execution success")
    user_satisfaction: float = Field(ge=0.0, le=1.0, description="User satisfaction score")
    execution_time_actual: int = Field(..., description="Actual execution time")
    confidence_accuracy: float = Field(ge=0.0, le=1.0, description="Confidence prediction accuracy")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    created_at: datetime = Field(default_factory=datetime.now, description="Learning record timestamp")


class SelectionMetrics(BaseModel):
    """Metrics for selection performance tracking"""
    total_selections: int = Field(default=0, description="Total selections made")
    successful_selections: int = Field(default=0, description="Successful selections")
    average_confidence: float = Field(default=0.75, ge=0.70, le=0.95, description="Average confidence score")
    average_execution_time: float = Field(default=5.0, description="Average execution time")
    context_accuracy: Dict[str, float] = Field(default_factory=dict, description="Context detection accuracy")
    pattern_effectiveness: Dict[str, float] = Field(default_factory=dict, description="Pattern effectiveness scores")
    user_satisfaction_avg: float = Field(default=0.8, ge=0.0, le=1.0, description="Average user satisfaction")
    improvement_rate: float = Field(default=0.0, description="Selection improvement rate")
    last_updated: datetime = Field(default_factory=datetime.now, description="Metrics last updated")


class SelectionRequest(BaseModel):
    """Request for tool selection"""
    prompt: str = Field(..., description="User prompt requiring tool selection")
    user_id: str = Field(default="anonymous", description="User identifier")
    context_hint: Optional[PromptContext] = Field(default=None, description="Optional context hint")
    preferred_tools: List[str] = Field(default_factory=list, description="User preferred tools")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Selection constraints")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    max_selections: int = Field(default=3, ge=1, le=10, description="Maximum tool selections")
    confidence_threshold: float = Field(default=0.75, ge=0.70, le=0.95, description="Minimum confidence")
    include_alternatives: bool = Field(default=True, description="Include alternative suggestions")
    learning_enabled: bool = Field(default=True, description="Enable learning from selection")


class SelectionResponse(BaseModel):
    """Response from tool selection service"""
    selection_result: SelectionResult = Field(..., description="Selection result")
    recommendations: List[str] = Field(default_factory=list, description="Additional recommendations")
    warnings: List[str] = Field(default_factory=list, description="Selection warnings")
    execution_ready: bool = Field(default=True, description="Ready for execution")
    estimated_cost: Optional[float] = Field(default=None, description="Estimated execution cost")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next steps")
    help_resources: List[str] = Field(default_factory=list, description="Help resources")
    session_id: str = Field(..., description="Session identifier")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class SystemStatus(BaseModel):
    """System status for tool selection service"""
    service_status: str = Field(..., description="Service status")
    fabric_integration_status: str = Field(..., description="Fabric integration status")  
    available_patterns: int = Field(default=0, description="Number of available patterns")
    available_tools: int = Field(default=0, description="Number of available tools")
    active_sessions: int = Field(default=0, description="Number of active sessions")
    total_selections_today: int = Field(default=0, description="Total selections today")
    average_response_time_ms: float = Field(default=0.0, description="Average response time")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Selection success rate")
    learning_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Learning accuracy")
    last_updated: datetime = Field(default_factory=datetime.now, description="Status last updated")