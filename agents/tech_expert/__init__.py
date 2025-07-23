"""
Tech Stack Expert Agent Package

Provides intelligent technology stack recommendations through guided conversations
and context-aware analysis for optimal architectural decision making.
"""

from .conversation_engine import ConversationEngine
from .recommender import TechStackRecommender
from .models import ProjectRequirements, TechRecommendation, ConversationState

__all__ = [
    "ConversationEngine",
    "TechStackRecommender", 
    "ProjectRequirements",
    "TechRecommendation",
    "ConversationState"
]

__version__ = "1.0.0"