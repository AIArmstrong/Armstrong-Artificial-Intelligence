"""
AAI Memory Enhancement Package

Provides persistent, cross-session memory capabilities for ALL AAI commands.
Enhances existing commands without modifying their core functionality.
"""

from .command_enhancer import AAICommandEnhancer, enhance_aai_command, get_memory_enhanced_args
from .memory_layer import MemoryLayer, MemoryContext, MemoryItem
from .workflow_memory import WorkflowMemoryManager
from .config import MemoryConfig

__version__ = "1.0.0"
__all__ = [
    "AAICommandEnhancer", 
    "enhance_aai_command", 
    "get_memory_enhanced_args",
    "MemoryLayer", 
    "MemoryContext", 
    "MemoryItem",
    "WorkflowMemoryManager",
    "MemoryConfig"
]