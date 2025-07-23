"""
MCP (Model Context Protocol) Management for AAI

Provides MCP server lifecycle management, connection pooling,
and health monitoring for agent orchestration.
"""

__version__ = "1.0.0"

# Import core components with fallback handling
try:
    from .server_manager import MCPServerManager
except ImportError:
    MCPServerManager = None

try:
    from .connection_pool import MCPConnectionPool
except ImportError:
    MCPConnectionPool = None

try:
    from .health_monitor import MCPHealthMonitor
except ImportError:
    MCPHealthMonitor = None

__all__ = [
    "MCPServerManager",
    "MCPConnectionPool", 
    "MCPHealthMonitor"
]