"""
OpenRouter Integration Package
Semantic intelligence and contradiction detection for AAI Brain
"""

from .router_client import OpenRouterClient, get_openrouter_client
from .embeddings import EmbeddingsEngine, find_similar_patterns, cache_current_intent, get_intent_recommendation
from .contradictions import ContradictionEngine, check_for_contradictions, analyze_conversation_conflicts, validate_decision_consistency

__all__ = [
    'OpenRouterClient',
    'get_openrouter_client',
    'EmbeddingsEngine', 
    'find_similar_patterns',
    'cache_current_intent',
    'get_intent_recommendation',
    'ContradictionEngine',
    'check_for_contradictions',
    'analyze_conversation_conflicts',
    'validate_decision_consistency'
]