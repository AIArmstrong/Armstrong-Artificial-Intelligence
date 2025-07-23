"""
Tool Selection Enhancement for AAI

Intelligent tool selection system that automatically selects optimal
tools based on prompt analysis with AAI patterns and confidence scoring.
"""

__version__ = "1.0.0"

# Import core components with fallback handling
try:
    from .prompt_analyzer import PromptAnalyzer, PromptContext
except ImportError:
    PromptAnalyzer = None
    PromptContext = None

try:
    from .tool_selector import ToolSelector, ToolSelection
except ImportError:
    ToolSelector = None
    ToolSelection = None

try:
    from .fabric_integrator import FabricIntegrator, FabricPattern
except ImportError:
    FabricIntegrator = None
    FabricPattern = None

try:
    from .confidence_scorer import SelectionConfidenceScorer
except ImportError:
    SelectionConfidenceScorer = None

try:
    from .learning_engine import SelectionLearningEngine
except ImportError:
    SelectionLearningEngine = None

__all__ = [
    "PromptAnalyzer",
    "PromptContext", 
    "ToolSelector",
    "ToolSelection",
    "FabricIntegrator",
    "FabricPattern",
    "SelectionConfidenceScorer",
    "SelectionLearningEngine"
]