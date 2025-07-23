"""
Data Models for Orchestration System

Pydantic models for task delegation, agent specialization, and orchestration
results with AAI confidence scoring compliance.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum


class AgentSpecialization(str, Enum):
    """Specialized agent types for different service domains"""
    SLACK = "slack"
    GITHUB = "github"
    AIRTABLE = "airtable"
    FIRECRAWL = "firecrawl"
    FILESYSTEM = "filesystem"
    JINA_SEARCH = "jina_search"
    MEMORY = "memory"
    TIME = "time"
    GENERAL = "general"


class TaskComplexity(str, Enum):
    """Task complexity levels for resource estimation"""
    SIMPLE = "simple"      # 1-3 complexity
    MODERATE = "moderate"   # 4-6 complexity
    COMPLEX = "complex"     # 7-8 complexity
    EXPERT = "expert"       # 9-10 complexity


class DelegationStatus(str, Enum):
    """Status of task delegation"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskDelegation(BaseModel):
    """Individual task delegation to specialized agent"""
    task_id: str = Field(..., description="Unique task identifier")
    task_description: str = Field(..., description="Description of task to be performed")
    assigned_agent: AgentSpecialization = Field(..., description="Agent assigned to task")
    confidence: float = Field(ge=0.70, le=0.95, description="AAI delegation confidence")
    reasoning: str = Field(..., description="Explanation for agent selection")
    estimated_complexity: int = Field(ge=1, le=10, description="Task complexity estimate")
    complexity_category: TaskComplexity = Field(default=TaskComplexity.MODERATE, description="Complexity category")
    status: DelegationStatus = Field(default=DelegationStatus.PENDING, description="Current status")
    priority: int = Field(default=5, ge=1, le=10, description="Task priority level")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    estimated_duration_seconds: int = Field(default=30, description="Estimated execution time")
    actual_duration_seconds: Optional[int] = Field(default=None, description="Actual execution time")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    started_at: Optional[datetime] = Field(default=None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")


class AgentCapability(BaseModel):
    """Capability definition for specialized agents"""
    name: str = Field(..., description="Capability name")
    description: str = Field(..., description="Capability description")
    complexity_support: List[TaskComplexity] = Field(..., description="Supported complexity levels")
    confidence_baseline: float = Field(ge=0.70, le=0.95, description="Baseline confidence for capability")
    typical_duration_seconds: int = Field(default=30, description="Typical execution duration")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies")


class AgentProfile(BaseModel):
    """Profile of specialized agent with capabilities and performance"""
    agent_type: AgentSpecialization = Field(..., description="Agent specialization type")
    name: str = Field(..., description="Agent display name")
    description: str = Field(..., description="Agent description")
    capabilities: List[AgentCapability] = Field(..., description="Agent capabilities")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    health_status: str = Field(default="healthy", description="Current health status")
    last_health_check: datetime = Field(default_factory=datetime.now, description="Last health check")
    total_tasks_completed: int = Field(default=0, description="Total completed tasks")
    success_rate: float = Field(default=1.0, ge=0.0, le=1.0, description="Task success rate")
    average_response_time: float = Field(default=1.0, description="Average response time in seconds")


class TaskResult(BaseModel):
    """Result of individual task execution"""
    task_id: str = Field(..., description="Task identifier")
    agent_type: AgentSpecialization = Field(..., description="Executing agent")
    success: bool = Field(..., description="Whether task succeeded")
    result_data: Dict[str, Any] = Field(default_factory=dict, description="Task result data")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    execution_time_seconds: float = Field(..., description="Actual execution time")
    confidence_achieved: float = Field(ge=0.0, le=1.0, description="Achieved confidence level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    completed_at: datetime = Field(default_factory=datetime.now, description="Completion timestamp")


class OrchestrationResult(BaseModel):
    """Complete result of orchestration process"""
    session_id: str = Field(..., description="Orchestration session identifier")
    original_query: str = Field(..., description="Original user query")
    delegations: List[TaskDelegation] = Field(..., description="Task delegations created")
    results: List[TaskResult] = Field(default_factory=list, description="Task execution results")
    overall_confidence: float = Field(ge=0.70, le=0.95, description="AAI overall confidence")
    success: bool = Field(..., description="Whether orchestration succeeded")
    total_execution_time_ms: int = Field(..., description="Total execution time")
    agent_utilization: Dict[str, int] = Field(default_factory=dict, description="Agent usage statistics")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")


class DelegationRequest(BaseModel):
    """Request for task delegation and orchestration"""
    query: str = Field(..., description="User query to orchestrate")
    user_id: str = Field(default="anonymous", description="User identifier")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    preferred_agents: List[AgentSpecialization] = Field(default_factory=list, description="Preferred agents")
    excluded_agents: List[AgentSpecialization] = Field(default_factory=list, description="Excluded agents")
    max_parallel_tasks: int = Field(default=3, ge=1, le=10, description="Maximum parallel tasks")
    timeout_seconds: int = Field(default=120, description="Overall timeout")
    priority: int = Field(default=5, ge=1, le=10, description="Request priority")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    require_confirmation: bool = Field(default=False, description="Require user confirmation")


class DelegationResponse(BaseModel):
    """Response from delegation system"""
    request_id: str = Field(..., description="Request identifier")
    orchestration_result: OrchestrationResult = Field(..., description="Orchestration result")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next steps")
    execution_ready: bool = Field(..., description="Ready for execution")
    estimated_cost: Optional[float] = Field(default=None, description="Estimated execution cost")
    processing_time_ms: int = Field(..., description="Processing time")


class OrchestrationMetrics(BaseModel):
    """Metrics for orchestration performance tracking"""
    total_orchestrations: int = Field(default=0, description="Total orchestrations")
    successful_orchestrations: int = Field(default=0, description="Successful orchestrations")
    average_confidence: float = Field(default=0.75, ge=0.70, le=0.95, description="Average confidence")
    average_execution_time_ms: float = Field(default=1000.0, description="Average execution time")
    agent_utilization: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Agent utilization stats")
    delegation_accuracy: float = Field(default=0.85, ge=0.0, le=1.0, description="Delegation accuracy")
    user_satisfaction: float = Field(default=0.8, ge=0.0, le=1.0, description="User satisfaction")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update time")


class SwarmCoordination(BaseModel):
    """Coordination configuration for swarm mode"""
    enabled: bool = Field(default=False, description="Whether swarm mode is enabled")
    max_swarm_size: int = Field(default=3, ge=1, le=6, description="Maximum agents in swarm")
    coordination_strategy: str = Field(default="parallel", description="Coordination strategy")
    communication_protocol: str = Field(default="shared_memory", description="Communication protocol")
    consensus_threshold: float = Field(default=0.8, ge=0.5, le=1.0, description="Consensus threshold")
    timeout_seconds: int = Field(default=180, description="Swarm coordination timeout")


class AgentOverride(BaseModel):
    """User override for agent selection"""
    task_pattern: str = Field(..., description="Task pattern to match")
    preferred_agent: AgentSpecialization = Field(..., description="Preferred agent")
    confidence_adjustment: float = Field(default=0.0, ge=-0.2, le=0.2, description="Confidence adjustment")
    reasoning: str = Field(..., description="Override reasoning")
    user_id: str = Field(..., description="User who set override")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    expires_at: Optional[datetime] = Field(default=None, description="Expiration time")


class OrchestrationConfig(BaseModel):
    """Configuration for orchestration system"""
    default_timeout_seconds: int = Field(default=120, description="Default timeout")
    max_parallel_tasks: int = Field(default=5, description="Maximum parallel tasks")
    health_check_interval: int = Field(default=30, description="Health check interval")
    confidence_threshold: float = Field(default=0.75, ge=0.70, le=0.95, description="Minimum confidence")
    enable_swarm_mode: bool = Field(default=False, description="Enable swarm coordination")
    enable_learning: bool = Field(default=True, description="Enable learning from outcomes")
    enable_user_overrides: bool = Field(default=True, description="Enable user overrides")
    performance_tracking: bool = Field(default=True, description="Enable performance tracking")
    alert_on_failures: bool = Field(default=True, description="Enable failure alerts")


class SystemStatus(BaseModel):
    """Overall system status for orchestration"""
    orchestration_active: bool = Field(..., description="Orchestration system active")
    mcp_servers_status: Dict[str, str] = Field(..., description="MCP server status")
    active_orchestrations: int = Field(default=0, description="Active orchestrations")
    agent_health: Dict[str, str] = Field(..., description="Agent health status")
    performance_metrics: OrchestrationMetrics = Field(..., description="Performance metrics")
    system_load: float = Field(default=0.0, ge=0.0, le=1.0, description="System load percentage")
    uptime_hours: float = Field(default=0.0, description="System uptime in hours")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last status update")