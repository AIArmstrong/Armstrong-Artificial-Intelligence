"""
API Layer for AAI

RESTful API services providing programmatic access to reasoning
capabilities with authentication, rate limiting, and documentation.
"""

__version__ = "1.0.0"

# Import API components with fallback handling
try:
    from .r1_reasoning_server import R1ReasoningServer, create_r1_server
except ImportError:
    R1ReasoningServer = None
    create_r1_server = None

__all__ = [
    "R1ReasoningServer",
    "create_r1_server"
]