"""
Collaborative analysis modules for team-based development
"""

from .workspace_manager import WorkspaceManager
from .annotation_system import AnnotationSystem
from .knowledge_base import KnowledgeBase

__all__ = [
    'WorkspaceManager',
    'AnnotationSystem',
    'KnowledgeBase'
]