#!/usr/bin/env python3
"""
AAI Memory Quality Scorer

Integrates with AAI's existing score-tracker.md patterns to assess memory quality,
usefulness, and effectiveness. Provides confidence scoring for memory operations
following AAI standards (70-95%).
"""

import os
import json
import math
import statistics
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path

# Import memory components
try:
    from ...enhancements.memory.memory_layer import MemoryItem, MemoryContext
    from ...enhancements.memory.config import MemoryConfig
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append('/mnt/c/Users/Brandon/AAI')
    from enhancements.memory.memory_layer import MemoryItem, MemoryContext
    from enhancements.memory.config import MemoryConfig


@dataclass
class MemoryQualityMetrics:
    """Memory quality assessment metrics following AAI standards"""
    memory_id: str
    content_quality: float  # 0.0 - 1.0
    relevance_accuracy: float  # 0.0 - 1.0
    usefulness_score: float  # 0.0 - 1.0
    freshness_score: float  # 0.0 - 1.0
    user_feedback_score: float  # 0.0 - 1.0
    usage_effectiveness: float  # 0.0 - 1.0
    overall_quality: float  # 0.0 - 1.0
    confidence_score: float  # AAI standard 0.70 - 0.95
    assessment_timestamp: datetime
    assessment_reason: str


@dataclass
class QualityTrend:
    """Quality trend analysis for memory items"""
    memory_id: str
    trend_direction: str  # 'improving', 'stable', 'declining'
    trend_strength: float  # 0.0 - 1.0
    quality_history: List[float]
    prediction_confidence: float
    recommendation: str


class MemoryQualityScorer:
    """
    Assesses memory quality and provides scoring following AAI patterns.
    
    Integrates with AAI's score-tracker.md methodology and provides
    confidence scoring within AAI's 70-95% range.
    """
    
    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        
        # AAI scoring thresholds (following score-tracker.md patterns)
        self.quality_thresholds = {
            'excellent': 0.85,
            'good': 0.70,
            'acceptable': 0.55,
            'poor': 0.40,
            'unusable': 0.25
        }
        
        # Confidence scoring parameters (AAI standards)
        self.confidence_params = {
            'min_confidence': self.config.min_confidence,  # 0.70
            'target_confidence': self.config.target_confidence,  # 0.85
            'max_confidence': self.config.max_confidence  # 0.95
        }
        
        # Quality assessment weights
        self.quality_weights = {
            'content_depth': 0.20,
            'technical_accuracy': 0.20,
            'user_feedback': 0.20,
            'usage_patterns': 0.15,
            'freshness': 0.10,
            'context_relevance': 0.15
        }
    
    def assess_memory_quality(self, memory_item: MemoryItem, 
                            usage_history: List[Dict] = None,
                            user_feedback: List[Dict] = None) -> MemoryQualityMetrics:
        """
        Comprehensive memory quality assessment following AAI patterns.
        
        Args:
            memory_item: Memory item to assess
            usage_history: Historical usage data
            user_feedback: User feedback data
        
        Returns:
            MemoryQualityMetrics with detailed quality scores
        """
        try:
            # Assess individual quality dimensions
            content_quality = self._assess_content_quality(memory_item)
            relevance_accuracy = self._assess_relevance_accuracy(memory_item, usage_history)
            usefulness_score = self._assess_usefulness(memory_item, usage_history, user_feedback)
            freshness_score = self._assess_freshness(memory_item)
            user_feedback_score = self._assess_user_feedback(user_feedback)
            usage_effectiveness = self._assess_usage_effectiveness(memory_item, usage_history)
            
            # Calculate overall quality using weighted average
            overall_quality = self._calculate_overall_quality({
                'content_quality': content_quality,
                'relevance_accuracy': relevance_accuracy,
                'usefulness_score': usefulness_score,
                'freshness_score': freshness_score,
                'user_feedback_score': user_feedback_score,
                'usage_effectiveness': usage_effectiveness
            })
            
            # Calculate confidence score (AAI standards)
            confidence_score = self._calculate_quality_confidence(
                overall_quality, memory_item, usage_history, user_feedback
            )
            
            # Generate assessment reason
            assessment_reason = self._generate_quality_reasoning(
                overall_quality, content_quality, usefulness_score, user_feedback_score
            )
            
            return MemoryQualityMetrics(
                memory_id=memory_item.id,
                content_quality=content_quality,
                relevance_accuracy=relevance_accuracy,
                usefulness_score=usefulness_score,
                freshness_score=freshness_score,
                user_feedback_score=user_feedback_score,
                usage_effectiveness=usage_effectiveness,
                overall_quality=overall_quality,
                confidence_score=confidence_score,
                assessment_timestamp=datetime.now(),
                assessment_reason=assessment_reason
            )
            
        except Exception as e:
            print(f"Quality assessment failed for {memory_item.id}: {e}")
            # Return minimal quality metrics
            return MemoryQualityMetrics(
                memory_id=memory_item.id,
                content_quality=0.5,
                relevance_accuracy=0.5,
                usefulness_score=0.5,
                freshness_score=0.5,
                user_feedback_score=0.5,
                usage_effectiveness=0.5,
                overall_quality=0.5,
                confidence_score=self.config.min_confidence,
                assessment_timestamp=datetime.now(),
                assessment_reason="Quality assessment failed, using default scores"
            )
    
    def _assess_content_quality(self, memory_item: MemoryItem) -> float:
        """Assess the quality of memory content"""
        quality_score = 0.0
        content = memory_item.content
        
        # Content depth and length
        if len(content) > 1000:
            quality_score += 0.30
        elif len(content) > 500:
            quality_score += 0.20
        elif len(content) > 100:
            quality_score += 0.10
        
        # Structured content indicators
        structure_indicators = ['```', 'def ', 'class ', 'function', '##', '###']
        if any(indicator in content for indicator in structure_indicators):
            quality_score += 0.20
        
        # Technical content indicators
        tech_indicators = [
            'implementation', 'pattern', 'solution', 'algorithm', 'architecture',
            'api', 'database', 'performance', 'security', 'testing'
        ]
        tech_count = sum(1 for indicator in tech_indicators if indicator.lower() in content.lower())
        quality_score += min(tech_count * 0.05, 0.25)
        
        # Code examples and technical details
        if '```' in content and any(lang in content for lang in ['python', 'javascript', 'sql', 'bash']):
            quality_score += 0.15
        
        # Metadata richness
        if memory_item.metadata and len(memory_item.metadata) > 2:
            quality_score += 0.10
        
        return min(quality_score, 1.0)
    
    def _assess_relevance_accuracy(self, memory_item: MemoryItem, usage_history: List[Dict] = None) -> float:
        """Assess how accurately the memory matches retrieval contexts"""
        if not usage_history:
            # Default based on confidence score
            return min(memory_item.confidence_score, 1.0)
        
        relevance_scores = []
        for usage in usage_history:
            if 'relevance_score' in usage:
                relevance_scores.append(usage['relevance_score'])
        
        if relevance_scores:
            return statistics.mean(relevance_scores)
        
        # Fallback: use existing confidence score
        return min(memory_item.confidence_score, 1.0)
    
    def _assess_usefulness(self, memory_item: MemoryItem, 
                          usage_history: List[Dict] = None,
                          user_feedback: List[Dict] = None) -> float:
        """Assess how useful the memory has been in practice"""
        usefulness_score = 0.5  # Default neutral score
        
        # Usage frequency indicates usefulness
        if memory_item.usage_count > 0:
            # Logarithmic scaling for usage count
            usage_factor = min(math.log(memory_item.usage_count + 1) / math.log(10), 1.0)
            usefulness_score += usage_factor * 0.3
        
        # Recency of usage
        if memory_item.last_accessed:
            days_since_access = (datetime.now() - memory_item.last_accessed).days
            if days_since_access <= 7:
                usefulness_score += 0.2
            elif days_since_access <= 30:
                usefulness_score += 0.1
        
        # User feedback on usefulness
        if user_feedback:
            helpful_feedback = [f for f in user_feedback if f.get('feedback_type') == 'helpful']
            if helpful_feedback:
                feedback_ratio = len(helpful_feedback) / len(user_feedback)
                usefulness_score += feedback_ratio * 0.3
        
        # Context type usefulness (some types are inherently more useful)
        useful_types = ['implementation', 'solution', 'pattern', 'preference', 'architecture']
        if memory_item.content_type in useful_types:
            usefulness_score += 0.1
        
        return min(usefulness_score, 1.0)
    
    def _assess_freshness(self, memory_item: MemoryItem) -> float:
        """Assess how fresh/current the memory content is"""
        if not memory_item.created_at:
            return 0.5  # Default for unknown creation time
        
        # Calculate age in days
        age_days = (datetime.now() - memory_item.created_at).days
        
        # Freshness scoring based on content type
        freshness_thresholds = {
            'technology_preference': 180,  # Tech preferences valid for ~6 months
            'implementation': 365,  # Implementation patterns valid for ~1 year
            'research': 90,  # Research findings valid for ~3 months
            'architecture': 730,  # Architecture decisions valid for ~2 years
            'preference': 365,  # User preferences valid for ~1 year
            'default': 180  # Default 6 months
        }
        
        threshold = freshness_thresholds.get(memory_item.content_type, freshness_thresholds['default'])
        
        if age_days <= threshold * 0.25:  # Very fresh (0-25% of threshold)
            return 1.0
        elif age_days <= threshold * 0.5:  # Fresh (25-50% of threshold)
            return 0.8
        elif age_days <= threshold:  # Acceptable (50-100% of threshold)
            return 0.6
        elif age_days <= threshold * 2:  # Aging (100-200% of threshold)
            return 0.4
        else:  # Stale (>200% of threshold)
            return 0.2
    
    def _assess_user_feedback(self, user_feedback: List[Dict] = None) -> float:
        """Assess user feedback on memory quality"""
        if not user_feedback:
            return 0.6  # Neutral score when no feedback available
        
        feedback_scores = []
        for feedback in user_feedback:
            feedback_type = feedback.get('feedback_type', '')
            if feedback_type == 'helpful':
                feedback_scores.append(1.0)
            elif feedback_type == 'partially_helpful':
                feedback_scores.append(0.6)
            elif feedback_type == 'not_helpful':
                feedback_scores.append(0.2)
            else:
                feedback_scores.append(0.5)  # Unknown feedback type
        
        if feedback_scores:
            return statistics.mean(feedback_scores)
        
        return 0.6  # Default when feedback exists but no valid types
    
    def _assess_usage_effectiveness(self, memory_item: MemoryItem, usage_history: List[Dict] = None) -> float:
        """Assess how effectively the memory is being used"""
        if not usage_history:
            # Base effectiveness on usage count and recency
            if memory_item.usage_count == 0:
                return 0.3  # Unused memory has low effectiveness
            
            # Factor in recency
            if memory_item.last_accessed:
                days_since_access = (datetime.now() - memory_item.last_accessed).days
                if days_since_access <= 30:
                    return 0.8
                elif days_since_access <= 90:
                    return 0.6
                else:
                    return 0.4
            
            return 0.5  # Default for used memory with unknown recency
        
        # Analyze usage patterns for effectiveness
        effectiveness_indicators = []
        
        for usage in usage_history:
            # Successful retrievals indicate effectiveness
            if usage.get('retrieval_success', False):
                effectiveness_indicators.append(0.8)
            
            # User engagement with retrieved memory
            if usage.get('user_engaged', False):
                effectiveness_indicators.append(0.9)
            
            # Context match quality
            context_match = usage.get('context_match_score', 0.5)
            effectiveness_indicators.append(context_match)
        
        if effectiveness_indicators:
            return statistics.mean(effectiveness_indicators)
        
        return 0.5  # Default when usage history exists but no clear indicators
    
    def _calculate_overall_quality(self, quality_components: Dict[str, float]) -> float:
        """Calculate overall quality using weighted average"""
        total_score = 0.0
        total_weight = 0.0
        
        # Map components to weights
        component_weights = {
            'content_quality': self.quality_weights['content_depth'],
            'relevance_accuracy': self.quality_weights['context_relevance'],
            'usefulness_score': self.quality_weights['usage_patterns'],
            'freshness_score': self.quality_weights['freshness'],
            'user_feedback_score': self.quality_weights['user_feedback'],
            'usage_effectiveness': self.quality_weights['technical_accuracy']
        }
        
        for component, score in quality_components.items():
            weight = component_weights.get(component, 0.1)  # Default weight
            total_score += score * weight
            total_weight += weight
        
        if total_weight > 0:
            return total_score / total_weight
        
        return 0.5  # Fallback score
    
    def _calculate_quality_confidence(self, overall_quality: float, 
                                    memory_item: MemoryItem,
                                    usage_history: List[Dict] = None,
                                    user_feedback: List[Dict] = None) -> float:
        """Calculate confidence in quality assessment (AAI 70-95% range)"""
        confidence = self.confidence_params['min_confidence']  # Start with 70%
        
        # Add confidence based on overall quality
        quality_factor = (overall_quality - 0.5) * 0.5  # Scale quality contribution
        confidence += max(0, quality_factor * 0.15)
        
        # Add confidence based on data availability
        if usage_history and len(usage_history) > 5:
            confidence += 0.05  # More usage data increases confidence
        
        if user_feedback and len(user_feedback) > 2:
            confidence += 0.05  # User feedback increases confidence
        
        # Add confidence based on memory age (more stable assessment for older items)
        if memory_item.created_at:
            age_days = (datetime.now() - memory_item.created_at).days
            if age_days > 30:  # Month+ old memories have more stable quality
                confidence += 0.03
        
        # Add confidence based on usage patterns
        if memory_item.usage_count > 10:
            confidence += 0.05  # Well-used memories have clearer quality signals
        
        # Add confidence based on content richness
        if len(memory_item.content) > 500 and memory_item.metadata:
            confidence += 0.02  # Rich content enables better assessment
        
        # Ensure within AAI confidence range
        return max(
            self.confidence_params['min_confidence'], 
            min(confidence, self.confidence_params['max_confidence'])
        )
    
    def _generate_quality_reasoning(self, overall_quality: float, 
                                  content_quality: float,
                                  usefulness_score: float,
                                  user_feedback_score: float) -> str:
        """Generate WHY reasoning for quality assessment (AAI pattern)"""
        reasoning_parts = []
        
        # Overall quality assessment
        if overall_quality >= self.quality_thresholds['excellent']:
            reasoning_parts.append("Excellent memory quality")
        elif overall_quality >= self.quality_thresholds['good']:
            reasoning_parts.append("Good memory quality")
        elif overall_quality >= self.quality_thresholds['acceptable']:
            reasoning_parts.append("Acceptable memory quality")
        else:
            reasoning_parts.append("Poor memory quality")
        
        # Specific strengths and weaknesses
        if content_quality >= 0.8:
            reasoning_parts.append("high content depth and technical detail")
        elif content_quality < 0.4:
            reasoning_parts.append("limited content depth")
        
        if usefulness_score >= 0.8:
            reasoning_parts.append("high practical usefulness")
        elif usefulness_score < 0.4:
            reasoning_parts.append("limited practical usefulness")
        
        if user_feedback_score >= 0.8:
            reasoning_parts.append("positive user feedback")
        elif user_feedback_score < 0.4:
            reasoning_parts.append("negative user feedback")
        
        if reasoning_parts:
            return "Quality assessment based on: " + ", ".join(reasoning_parts) + "."
        else:
            return "Quality assessment completed with standard criteria."
    
    def analyze_quality_trends(self, memory_id: str, 
                             quality_history: List[MemoryQualityMetrics]) -> QualityTrend:
        """Analyze quality trends over time"""
        if len(quality_history) < 2:
            return QualityTrend(
                memory_id=memory_id,
                trend_direction='stable',
                trend_strength=0.0,
                quality_history=[],
                prediction_confidence=self.confidence_params['min_confidence'],
                recommendation="Insufficient data for trend analysis"
            )
        
        # Extract quality scores over time
        quality_scores = [metric.overall_quality for metric in quality_history]
        
        # Calculate trend direction and strength
        if len(quality_scores) >= 3:
            # Use linear regression for trend analysis
            trend_direction, trend_strength = self._calculate_trend(quality_scores)
        else:
            # Simple comparison for limited data
            if quality_scores[-1] > quality_scores[0]:
                trend_direction = 'improving'
                trend_strength = (quality_scores[-1] - quality_scores[0]) / len(quality_scores)
            elif quality_scores[-1] < quality_scores[0]:
                trend_direction = 'declining'
                trend_strength = (quality_scores[0] - quality_scores[-1]) / len(quality_scores)
            else:
                trend_direction = 'stable'
                trend_strength = 0.0
        
        # Generate recommendation
        recommendation = self._generate_trend_recommendation(
            trend_direction, trend_strength, quality_scores[-1]
        )
        
        # Calculate prediction confidence
        prediction_confidence = self._calculate_trend_confidence(quality_scores, trend_strength)
        
        return QualityTrend(
            memory_id=memory_id,
            trend_direction=trend_direction,
            trend_strength=abs(trend_strength),
            quality_history=quality_scores,
            prediction_confidence=prediction_confidence,
            recommendation=recommendation
        )
    
    def _calculate_trend(self, values: List[float]) -> Tuple[str, float]:
        """Calculate trend direction and strength using simple linear regression"""
        n = len(values)
        if n < 2:
            return 'stable', 0.0
        
        # Simple linear regression
        x_values = list(range(n))
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return 'stable', 0.0
        
        slope = numerator / denominator
        
        # Determine trend direction
        if slope > 0.01:  # Threshold for meaningful improvement
            return 'improving', slope
        elif slope < -0.01:  # Threshold for meaningful decline
            return 'declining', slope
        else:
            return 'stable', slope
    
    def _generate_trend_recommendation(self, trend_direction: str, 
                                     trend_strength: float,
                                     current_quality: float) -> str:
        """Generate recommendation based on quality trend"""
        if trend_direction == 'improving':
            if current_quality >= self.quality_thresholds['excellent']:
                return "Maintain current usage patterns - excellent quality trajectory"
            else:
                return "Continue current usage patterns - quality is improving"
        
        elif trend_direction == 'declining':
            if current_quality <= self.quality_thresholds['poor']:
                return "Consider archiving - quality declining below useful threshold"
            else:
                return "Monitor closely - quality declining, may need refresh or retirement"
        
        else:  # stable
            if current_quality >= self.quality_thresholds['good']:
                return "Quality stable at good level - continue normal usage"
            elif current_quality >= self.quality_thresholds['acceptable']:
                return "Quality stable but could be improved - consider enhancement"
            else:
                return "Quality stable but poor - consider refresh or replacement"
    
    def _calculate_trend_confidence(self, quality_scores: List[float], trend_strength: float) -> float:
        """Calculate confidence in trend prediction"""
        confidence = self.confidence_params['min_confidence']
        
        # More data points increase confidence
        confidence += min(len(quality_scores) * 0.02, 0.15)
        
        # Stronger trends are more confident
        confidence += min(abs(trend_strength) * 0.5, 0.08)
        
        # Lower variance in scores increases confidence
        if len(quality_scores) > 2:
            variance = statistics.variance(quality_scores)
            confidence += max(0, (0.1 - variance) * 0.5)  # Lower variance = higher confidence
        
        return max(
            self.confidence_params['min_confidence'], 
            min(confidence, self.confidence_params['max_confidence'])
        )
    
    def suggest_memory_cleanup(self, quality_metrics: List[MemoryQualityMetrics]) -> List[str]:
        """Suggest memories for cleanup based on quality assessment"""
        cleanup_candidates = []
        
        for metric in quality_metrics:
            should_cleanup = False
            reason = ""
            
            # Low overall quality
            if metric.overall_quality < self.quality_thresholds['poor']:
                should_cleanup = True
                reason = f"Low overall quality ({metric.overall_quality:.2f})"
            
            # Poor user feedback
            elif metric.user_feedback_score < 0.3:
                should_cleanup = True
                reason = f"Poor user feedback ({metric.user_feedback_score:.2f})"
            
            # Unused and old
            elif metric.usefulness_score < 0.3 and metric.freshness_score < 0.3:
                should_cleanup = True
                reason = "Unused and stale content"
            
            if should_cleanup:
                cleanup_candidates.append(f"{metric.memory_id}: {reason}")
        
        return cleanup_candidates
    
    def generate_quality_report(self, quality_metrics: List[MemoryQualityMetrics]) -> Dict[str, Any]:
        """Generate comprehensive quality report following AAI patterns"""
        if not quality_metrics:
            return {'error': 'No quality metrics provided'}
        
        # Calculate summary statistics
        overall_qualities = [m.overall_quality for m in quality_metrics]
        confidence_scores = [m.confidence_score for m in quality_metrics]
        
        # Quality distribution
        excellent_count = sum(1 for q in overall_qualities if q >= self.quality_thresholds['excellent'])
        good_count = sum(1 for q in overall_qualities if q >= self.quality_thresholds['good'] and q < self.quality_thresholds['excellent'])
        acceptable_count = sum(1 for q in overall_qualities if q >= self.quality_thresholds['acceptable'] and q < self.quality_thresholds['good'])
        poor_count = sum(1 for q in overall_qualities if q < self.quality_thresholds['acceptable'])
        
        # Cleanup recommendations
        cleanup_suggestions = self.suggest_memory_cleanup(quality_metrics)
        
        return {
            'summary': {
                'total_memories_assessed': len(quality_metrics),
                'average_quality': statistics.mean(overall_qualities),
                'average_confidence': statistics.mean(confidence_scores),
                'quality_std_dev': statistics.stdev(overall_qualities) if len(overall_qualities) > 1 else 0.0
            },
            'quality_distribution': {
                'excellent': {'count': excellent_count, 'percentage': excellent_count / len(quality_metrics) * 100},
                'good': {'count': good_count, 'percentage': good_count / len(quality_metrics) * 100},
                'acceptable': {'count': acceptable_count, 'percentage': acceptable_count / len(quality_metrics) * 100},
                'poor': {'count': poor_count, 'percentage': poor_count / len(quality_metrics) * 100}
            },
            'recommendations': {
                'cleanup_candidates': cleanup_suggestions,
                'total_cleanup_suggested': len(cleanup_suggestions)
            },
            'assessment_timestamp': datetime.now().isoformat(),
            'aai_compliance': {
                'confidence_range': f"{self.confidence_params['min_confidence']:.0%} - {self.confidence_params['max_confidence']:.0%}",
                'scoring_methodology': 'AAI score-tracker.md patterns',
                'quality_thresholds': self.quality_thresholds
            }
        }


def test_memory_quality_scorer():
    """Test memory quality scoring functionality"""
    from enhancements.memory.memory_layer import MemoryItem
    from datetime import datetime, timedelta
    
    print("Testing Memory Quality Scorer")
    print("=" * 40)
    
    config = MemoryConfig.for_testing()
    scorer = MemoryQualityScorer(config)
    
    # Create test memory items
    high_quality_memory = MemoryItem(
        id="test_high_quality",
        user_id="test_user",
        content="""
        # FastAPI Authentication Implementation
        
        ```python
        from fastapi import FastAPI, Depends, HTTPException
        from fastapi.security import HTTPBearer
        
        app = FastAPI()
        security = HTTPBearer()
        
        async def authenticate_user(token: str = Depends(security)):
            # Validate JWT token
            if not validate_jwt(token.credentials):
                raise HTTPException(status_code=401, detail="Invalid token")
            return get_user_from_token(token.credentials)
        ```
        
        This implementation provides secure JWT-based authentication for FastAPI applications.
        Key benefits:
        - Stateless authentication
        - Scalable for microservices
        - Integration with standard security practices
        """,
        content_type="implementation",
        metadata={
            "technology": "FastAPI",
            "pattern": "JWT Authentication",
            "complexity": "medium",
            "tested": True
        },
        confidence_score=0.90,
        quality_score=0.0,  # Will be calculated
        usage_count=15,
        last_accessed=datetime.now() - timedelta(days=5),
        created_at=datetime.now() - timedelta(days=30),
        tags=["fastapi", "authentication", "jwt", "security"]
    )
    
    low_quality_memory = MemoryItem(
        id="test_low_quality",
        user_id="test_user",
        content="ok",
        content_type="note",
        metadata={},
        confidence_score=0.70,
        quality_score=0.0,
        usage_count=0,
        last_accessed=datetime.now() - timedelta(days=90),
        created_at=datetime.now() - timedelta(days=120),
        tags=[]
    )
    
    # Test quality assessment
    high_quality_metrics = scorer.assess_memory_quality(
        high_quality_memory,
        usage_history=[
            {'retrieval_success': True, 'user_engaged': True, 'context_match_score': 0.9},
            {'retrieval_success': True, 'user_engaged': True, 'context_match_score': 0.85},
            {'retrieval_success': True, 'user_engaged': False, 'context_match_score': 0.8}
        ],
        user_feedback=[
            {'feedback_type': 'helpful'},
            {'feedback_type': 'helpful'},
            {'feedback_type': 'partially_helpful'}
        ]
    )
    
    low_quality_metrics = scorer.assess_memory_quality(low_quality_memory)
    
    print(f"High Quality Memory Assessment:")
    print(f"  Overall Quality: {high_quality_metrics.overall_quality:.2f}")
    print(f"  Content Quality: {high_quality_metrics.content_quality:.2f}")
    print(f"  Usefulness: {high_quality_metrics.usefulness_score:.2f}")
    print(f"  User Feedback: {high_quality_metrics.user_feedback_score:.2f}")
    print(f"  Confidence: {high_quality_metrics.confidence_score:.2f}")
    print(f"  Reasoning: {high_quality_metrics.assessment_reason}")
    print()
    
    print(f"Low Quality Memory Assessment:")
    print(f"  Overall Quality: {low_quality_metrics.overall_quality:.2f}")
    print(f"  Content Quality: {low_quality_metrics.content_quality:.2f}")
    print(f"  Usefulness: {low_quality_metrics.usefulness_score:.2f}")
    print(f"  Confidence: {low_quality_metrics.confidence_score:.2f}")
    print(f"  Reasoning: {low_quality_metrics.assessment_reason}")
    print()
    
    # Test quality report
    report = scorer.generate_quality_report([high_quality_metrics, low_quality_metrics])
    print("Quality Report Summary:")
    print(f"  Total Assessed: {report['summary']['total_memories_assessed']}")
    print(f"  Average Quality: {report['summary']['average_quality']:.2f}")
    print(f"  Average Confidence: {report['summary']['average_confidence']:.2f}")
    print(f"  Cleanup Candidates: {report['recommendations']['total_cleanup_suggested']}")
    
    if report['recommendations']['cleanup_candidates']:
        print("  Cleanup Suggestions:")
        for suggestion in report['recommendations']['cleanup_candidates']:
            print(f"    - {suggestion}")


if __name__ == "__main__":
    test_memory_quality_scorer()