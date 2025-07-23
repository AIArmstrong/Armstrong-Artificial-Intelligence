"""
Orchestration Agents for AAI

Provides intelligent task delegation and coordination across multiple
specialized agents using MCP (Model Context Protocol) infrastructure.
"""

__version__ = "1.0.0"

# Import core components with fallback handling
try:
    from .primary_agent import PrimaryOrchestrationAgent
except ImportError:
    PrimaryOrchestrationAgent = None

try:
    from .delegation_engine import DelegationEngine, TaskDelegation
except ImportError:
    DelegationEngine = None
    TaskDelegation = None

try:
    from .resource_manager import ResourceManager
except ImportError:
    ResourceManager = None

try:
    from .confidence_scorer import OrchestrationConfidenceScorer
except ImportError:
    OrchestrationConfidenceScorer = None

try:
    from .models import AgentSpecialization, OrchestrationResult
except ImportError:
    AgentSpecialization = None
    OrchestrationResult = None

__all__ = [
    "PrimaryOrchestrationAgent",
    "DelegationEngine",
    "TaskDelegation",
    "ResourceManager", 
    "OrchestrationConfidenceScorer",
    "AgentSpecialization",
    "OrchestrationResult"
]