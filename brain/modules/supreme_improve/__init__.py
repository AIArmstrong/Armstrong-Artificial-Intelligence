"""
Supreme Improve Module - Multi-Dimensional Code Enhancement Engine

This module provides advanced code improvement capabilities with:
- Multi-dimensional quality scoring (0-100 scale)
- Risk assessment for breaking changes
- Safety mechanisms with preview and rollback
- Improvement outcome tracking and learning
"""

from .models import (
    QualityMetrics,
    ImprovementRecommendation,
    ReviewResult,
    ImprovementOutcome
)
from .risk_assessor import RiskAssessor
from .safety_mechanisms import SafetyMechanisms
from .improvement_tracker import ImprovementTracker
from .multi_dimensional_scorer import MultiDimensionalScorer

__all__ = [
    # Data Models
    'QualityMetrics',
    'ImprovementRecommendation',
    'ReviewResult',
    'ImprovementOutcome',
    
    # Core Components
    'RiskAssessor',
    'SafetyMechanisms',
    'ImprovementTracker',
    'MultiDimensionalScorer'
]

# Version and metadata
__version__ = "1.0.0"
__author__ = "AAI System"
__description__ = "Supreme code improvement with multi-dimensional analysis and safety"