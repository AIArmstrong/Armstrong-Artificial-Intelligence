"""
R1 Reasoning Engine for AAI

Advanced reasoning capabilities using DeepSeek R1 with dual-model architecture,
confidence scoring, and structured analysis patterns.
"""
from .models import (
    ReasoningStep,
    ReasoningChain,
    ReasoningResponse,
    DocumentAnalysisRequest,
    ConfidenceAnalysis,
    ModelInferenceConfig,
    InferenceBackend,
    ReasoningMethod,
    ReasoningDepth
)
from .config import R1ReasoningConfig

# Import core components with fallback handling
try:
    from .reasoning_engine import ReasoningEngine as R1ReasoningEngine
except ImportError:
    R1ReasoningEngine = None

try:
    from .confidence_scorer import ConfidenceScorer
except ImportError:
    ConfidenceScorer = None

try:
    from .dual_model_agent import DualModelAgent, AgentTask, AgentResult
except ImportError:
    DualModelAgent = None
    AgentTask = None
    AgentResult = None

__version__ = "1.0.0"
__author__ = "AAI System"

__all__ = [
    "ReasoningStep",
    "ReasoningChain", 
    "ReasoningResponse",
    "DocumentAnalysisRequest",
    "ConfidenceAnalysis",
    "ModelInferenceConfig",
    "InferenceBackend",
    "ReasoningMethod",
    "ReasoningDepth",
    "R1ReasoningConfig",
    "R1ReasoningEngine",
    "ConfidenceScorer",
    "DualModelAgent",
    "AgentTask",
    "AgentResult"
]