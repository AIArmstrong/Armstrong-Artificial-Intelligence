"""
Interactive Interfaces for AAI

User-friendly interfaces for reasoning sessions, research integration,
and system interaction with AAI patterns and confidence visualization.
"""

__version__ = "1.0.0"

# Import interface components with fallback handling
try:
    from .r1_reasoning_interface import R1ReasoningInterface, create_r1_interface
except ImportError:
    R1ReasoningInterface = None
    create_r1_interface = None

__all__ = [
    "R1ReasoningInterface",
    "create_r1_interface"
]