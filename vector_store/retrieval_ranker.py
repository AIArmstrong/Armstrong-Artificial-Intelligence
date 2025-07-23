"""
Retrieval Ranker for R1 Reasoning Engine

Advanced ranking system that combines similarity, confidence,
and reasoning relevance for optimal document retrieval.
"""
import logging
import math
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from agents.r1_reasoning.models import VectorSearchResult

logger = logging.getLogger(__name__)


class RankingStrategy(str, Enum):
    """Available ranking strategies"""
    SIMILARITY_ONLY = "similarity_only"
    CONFIDENCE_WEIGHTED = "confidence_weighted"
    REASONING_OPTIMIZED = "reasoning_optimized"
    BALANCED = "balanced"
    RECENCY_BOOSTED = "recency_boosted"


@dataclass
class RankingWeights:
    """Weights for different ranking factors"""
    similarity: float = 0.4
    confidence: float = 0.3
    reasoning_relevance: float = 0.2
    recency: float = 0.05
    quality: float = 0.05


@dataclass
class RankingResult:
    """Result of ranking operation"""
    original_results: List[VectorSearchResult]
    ranked_results: List[VectorSearchResult]
    ranking_strategy: RankingStrategy
    ranking_scores: List[float]
    processing_time_ms: int
    total_results: int


class RetrievalRanker:
    """
    Advanced ranking system for vector search results.
    
    Features:
    - Multiple ranking strategies
    - AAI confidence integration
    - Reasoning relevance scoring
    - Recency and quality factors
    - Configurable weight systems
    """
    
    def __init__(self, 
                 default_strategy: RankingStrategy = RankingStrategy.REASONING_OPTIMIZED,
                 default_weights: Optional[RankingWeights] = None):
        """Initialize retrieval ranker"""
        self.default_strategy = default_strategy
        self.default_weights = default_weights or RankingWeights()
        
        # Reasoning relevance keywords
        self.reasoning_keywords = self._initialize_reasoning_keywords()
        
        # Quality indicators
        self.quality_indicators = self._initialize_quality_indicators()
    
    def _initialize_reasoning_keywords(self) -> Dict[str, List[str]]:
        """Initialize keywords that indicate reasoning relevance"""
        return {
            "high_relevance": [
                "because", "therefore", "thus", "consequently", "since",
                "due to", "as a result", "leads to", "causes", "implies",
                "suggests", "indicates", "demonstrates", "proves", "shows",
                "analysis", "reasoning", "logic", "inference", "conclusion"
            ],
            "medium_relevance": [
                "explains", "describes", "discusses", "examines", "considers",
                "compares", "contrasts", "evaluates", "assesses", "determines",
                "identifies", "reveals", "illustrates", "supports", "confirms"
            ],
            "causal_indicators": [
                "effect", "impact", "influence", "result", "outcome",
                "consequence", "correlation", "relationship", "pattern"
            ],
            "analytical_terms": [
                "methodology", "approach", "framework", "model", "theory",
                "hypothesis", "evidence", "data", "findings", "research"
            ]
        }
    
    def _initialize_quality_indicators(self) -> Dict[str, List[str]]:
        """Initialize quality indicators for content assessment"""
        return {
            "high_quality": [
                "peer-reviewed", "published", "journal", "conference",
                "research", "study", "experiment", "systematic", "empirical"
            ],
            "structure_indicators": [
                "abstract", "introduction", "methodology", "results",
                "discussion", "conclusion", "references", "bibliography"
            ],
            "authority_indicators": [
                "author", "professor", "doctor", "phd", "researcher",
                "expert", "specialist", "institution", "university"
            ]
        }
    
    async def rank_results(self, 
                         results: List[VectorSearchResult],
                         strategy: Optional[RankingStrategy] = None,
                         weights: Optional[RankingWeights] = None,
                         query_context: Optional[str] = None) -> RankingResult:
        """
        Rank search results using specified strategy.
        
        Args:
            results: List of search results to rank
            strategy: Ranking strategy to use
            weights: Custom weights for ranking factors
            query_context: Optional query context for relevance scoring
            
        Returns:
            RankingResult with ranked results and metadata
        """
        start_time = datetime.now()
        
        if not results:
            return RankingResult(
                original_results=[],
                ranked_results=[],
                ranking_strategy=strategy or self.default_strategy,
                ranking_scores=[],
                processing_time_ms=0,
                total_results=0
            )
        
        strategy = strategy or self.default_strategy
        weights = weights or self.default_weights
        
        try:
            # Calculate ranking scores for each result
            ranking_scores = []
            
            for result in results:
                score = await self._calculate_ranking_score(
                    result, strategy, weights, query_context
                )
                ranking_scores.append(score)
            
            # Create tuples of (result, score) for sorting
            result_score_pairs = list(zip(results, ranking_scores))
            
            # Sort by score (highest first)
            result_score_pairs.sort(key=lambda x: x[1], reverse=True)
            
            # Extract ranked results and scores
            ranked_results = [pair[0] for pair in result_score_pairs]
            sorted_scores = [pair[1] for pair in result_score_pairs]
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return RankingResult(
                original_results=results,
                ranked_results=ranked_results,
                ranking_strategy=strategy,
                ranking_scores=sorted_scores,
                processing_time_ms=int(processing_time),
                total_results=len(results)
            )
            
        except Exception as e:
            logger.error(f"Ranking failed: {e}")
            
            # Return original results on failure
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            return RankingResult(
                original_results=results,
                ranked_results=results,  # Fallback to original order
                ranking_strategy=strategy,
                ranking_scores=[1.0] * len(results),
                processing_time_ms=int(processing_time),
                total_results=len(results)
            )
    
    async def _calculate_ranking_score(self, 
                                     result: VectorSearchResult,
                                     strategy: RankingStrategy,
                                     weights: RankingWeights,
                                     query_context: Optional[str] = None) -> float:
        """Calculate ranking score for a single result"""
        
        # Base scores
        similarity_score = result.similarity_score
        confidence_score = (result.confidence_score - 0.70) / 0.25  # Normalize to 0-1
        
        # Calculate additional factors
        reasoning_score = self._calculate_reasoning_relevance(result, query_context)
        recency_score = self._calculate_recency_score(result)
        quality_score = self._calculate_quality_score(result)
        
        # Apply strategy-specific scoring
        if strategy == RankingStrategy.SIMILARITY_ONLY:
            return similarity_score
        
        elif strategy == RankingStrategy.CONFIDENCE_WEIGHTED:
            return (
                similarity_score * 0.7 +
                confidence_score * 0.3
            )
        
        elif strategy == RankingStrategy.REASONING_OPTIMIZED:
            return (
                similarity_score * weights.similarity +
                confidence_score * weights.confidence +
                reasoning_score * weights.reasoning_relevance +
                quality_score * weights.quality +
                recency_score * weights.recency
            )
        
        elif strategy == RankingStrategy.BALANCED:
            # Equal weighting of all factors
            return (
                similarity_score * 0.25 +
                confidence_score * 0.25 +
                reasoning_score * 0.25 +
                (quality_score + recency_score) * 0.25
            )
        
        elif strategy == RankingStrategy.RECENCY_BOOSTED:
            base_score = (
                similarity_score * 0.4 +
                confidence_score * 0.3 +
                reasoning_score * 0.2
            )
            
            # Strong recency boost
            recency_boost = recency_score * 0.3
            return min(1.0, base_score + recency_boost)
        
        else:
            # Default to reasoning optimized
            return (
                similarity_score * weights.similarity +
                confidence_score * weights.confidence +
                reasoning_score * weights.reasoning_relevance +
                quality_score * weights.quality +
                recency_score * weights.recency
            )
    
    def _calculate_reasoning_relevance(self, 
                                     result: VectorSearchResult,
                                     query_context: Optional[str] = None) -> float:
        """Calculate reasoning relevance score"""
        
        content = result.content.lower()
        relevance_score = 0.0
        
        # Count reasoning keywords
        high_count = sum(1 for keyword in self.reasoning_keywords["high_relevance"] 
                        if keyword in content)
        medium_count = sum(1 for keyword in self.reasoning_keywords["medium_relevance"]
                          if keyword in content)
        causal_count = sum(1 for keyword in self.reasoning_keywords["causal_indicators"]
                          if keyword in content)
        analytical_count = sum(1 for keyword in self.reasoning_keywords["analytical_terms"]
                              if keyword in content)
        
        # Weight the counts
        relevance_score += min(0.4, high_count * 0.08)     # High impact keywords
        relevance_score += min(0.2, medium_count * 0.04)   # Medium impact keywords
        relevance_score += min(0.2, causal_count * 0.06)   # Causal reasoning
        relevance_score += min(0.2, analytical_count * 0.04)  # Analytical content
        
        # Query context matching (if provided)
        if query_context:
            context_words = set(query_context.lower().split())
            content_words = set(content.split())
            overlap = len(context_words.intersection(content_words))
            
            if context_words:
                context_score = overlap / len(context_words)
                relevance_score += context_score * 0.2
        
        return min(1.0, relevance_score)
    
    def _calculate_recency_score(self, result: VectorSearchResult) -> float:
        """Calculate recency score based on document age"""
        
        try:
            # Try to extract date from metadata
            created_at = result.metadata.get("created_at")
            if not created_at:
                return 0.5  # Neutral score for unknown dates
            
            # Parse date
            if isinstance(created_at, str):
                doc_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            else:
                doc_date = created_at
            
            # Calculate age in days
            age_days = (datetime.now() - doc_date.replace(tzinfo=None)).days
            
            # Score based on age (newer is better)
            if age_days <= 30:      # Very recent
                return 1.0
            elif age_days <= 90:    # Recent
                return 0.8
            elif age_days <= 365:   # Somewhat recent
                return 0.6
            elif age_days <= 1095:  # 3 years
                return 0.4
            else:                   # Older
                return 0.2
                
        except Exception as e:
            logger.debug(f"Recency calculation failed: {e}")
            return 0.5  # Neutral score on error
    
    def _calculate_quality_score(self, result: VectorSearchResult) -> float:
        """Calculate quality score based on content indicators"""
        
        content = result.content.lower()
        quality_score = 0.5  # Base quality
        
        # High quality indicators
        high_quality_count = sum(1 for indicator in self.quality_indicators["high_quality"]
                               if indicator in content)
        quality_score += min(0.3, high_quality_count * 0.1)
        
        # Structure indicators
        structure_count = sum(1 for indicator in self.quality_indicators["structure_indicators"]
                            if indicator in content)
        quality_score += min(0.1, structure_count * 0.02)
        
        # Authority indicators
        authority_count = sum(1 for indicator in self.quality_indicators["authority_indicators"]
                            if indicator in content)
        quality_score += min(0.1, authority_count * 0.05)
        
        # Length factor (longer content often indicates depth)
        content_length = len(result.content)
        if content_length > 1000:
            quality_score += 0.05
        if content_length > 2000:
            quality_score += 0.05
        
        # Use existing quality score from metadata if available
        metadata_quality = result.metadata.get("quality_score")
        if metadata_quality is not None:
            quality_score = (quality_score + metadata_quality) / 2
        
        return max(0.0, min(1.0, quality_score))
    
    def get_ranking_explanation(self, 
                               result: VectorSearchResult,
                               ranking_score: float,
                               strategy: RankingStrategy,
                               weights: RankingWeights) -> Dict[str, Any]:
        """Get explanation for ranking score"""
        
        similarity_score = result.similarity_score
        confidence_score = (result.confidence_score - 0.70) / 0.25
        reasoning_score = self._calculate_reasoning_relevance(result)
        recency_score = self._calculate_recency_score(result)
        quality_score = self._calculate_quality_score(result)
        
        return {
            "total_score": ranking_score,
            "components": {
                "similarity": {
                    "score": similarity_score,
                    "weight": weights.similarity,
                    "contribution": similarity_score * weights.similarity
                },
                "confidence": {
                    "score": confidence_score,
                    "weight": weights.confidence,
                    "contribution": confidence_score * weights.confidence
                },
                "reasoning_relevance": {
                    "score": reasoning_score,
                    "weight": weights.reasoning_relevance,
                    "contribution": reasoning_score * weights.reasoning_relevance
                },
                "recency": {
                    "score": recency_score,
                    "weight": weights.recency,
                    "contribution": recency_score * weights.recency
                },
                "quality": {
                    "score": quality_score,
                    "weight": weights.quality,
                    "contribution": quality_score * weights.quality
                }
            },
            "strategy": strategy.value
        }
    
    def get_ranker_status(self) -> Dict[str, Any]:
        """Get ranker status and configuration"""
        return {
            "default_strategy": self.default_strategy.value,
            "default_weights": {
                "similarity": self.default_weights.similarity,
                "confidence": self.default_weights.confidence,
                "reasoning_relevance": self.default_weights.reasoning_relevance,
                "recency": self.default_weights.recency,
                "quality": self.default_weights.quality
            },
            "available_strategies": [strategy.value for strategy in RankingStrategy],
            "reasoning_keywords_count": sum(
                len(keywords) for keywords in self.reasoning_keywords.values()
            ),
            "quality_indicators_count": sum(
                len(indicators) for indicators in self.quality_indicators.values()
            ),
            "ready": True
        }


async def test_retrieval_ranker():
    """Test retrieval ranker functionality"""
    
    ranker = RetrievalRanker()
    
    print("🧪 Testing Retrieval Ranker")
    print("=" * 35)
    
    # Check ranker status
    status = ranker.get_ranker_status()
    print(f"Default strategy: {status['default_strategy']}")
    print(f"Available strategies: {status['available_strategies']}")
    print(f"Reasoning keywords: {status['reasoning_keywords_count']}")
    print(f"Ready: {status['ready']}")
    
    # Create sample results
    sample_results = [
        VectorSearchResult(
            chunk_id="chunk_1",
            content="This analysis demonstrates how artificial intelligence reasoning systems work. Because of their logical inference capabilities, they can process complex data.",
            filename="ai_research.pdf",
            similarity_score=0.85,
            confidence_score=0.82,
            metadata={"created_at": "2024-01-15T10:00:00", "quality_score": 0.75}
        ),
        VectorSearchResult(
            chunk_id="chunk_2", 
            content="Machine learning models use statistical methods to identify patterns in large datasets.",
            filename="ml_guide.pdf",
            similarity_score=0.78,
            confidence_score=0.90,
            metadata={"created_at": "2024-06-01T14:00:00", "quality_score": 0.65}
        ),
        VectorSearchResult(
            chunk_id="chunk_3",
            content="The study shows that neural networks can effectively solve classification problems. Research indicates significant improvements in accuracy.",
            filename="neural_networks.pdf", 
            similarity_score=0.72,
            confidence_score=0.75,
            metadata={"created_at": "2024-07-10T09:00:00", "quality_score": 0.85}
        )
    ]
    
    print(f"\n📊 Testing with {len(sample_results)} sample results")
    
    # Test different ranking strategies
    strategies = [
        RankingStrategy.SIMILARITY_ONLY,
        RankingStrategy.CONFIDENCE_WEIGHTED, 
        RankingStrategy.REASONING_OPTIMIZED
    ]
    
    for strategy in strategies:
        print(f"\n🔄 Testing strategy: {strategy.value}")
        
        ranking_result = await ranker.rank_results(
            sample_results, 
            strategy=strategy,
            query_context="artificial intelligence reasoning analysis"
        )
        
        print(f"Processing time: {ranking_result.processing_time_ms}ms")
        print("Ranking order:")
        
        for i, (result, score) in enumerate(zip(ranking_result.ranked_results, ranking_result.ranking_scores)):
            print(f"  {i+1}. {result.chunk_id} - Score: {score:.3f} "
                  f"(Sim: {result.similarity_score:.3f}, Conf: {result.confidence_score:.3f})")
    
    # Test ranking explanation
    if sample_results:
        print(f"\n📋 Ranking explanation for {sample_results[0].chunk_id}:")
        explanation = ranker.get_ranking_explanation(
            sample_results[0],
            0.85,
            RankingStrategy.REASONING_OPTIMIZED,
            ranker.default_weights
        )
        
        print(f"Total score: {explanation['total_score']:.3f}")
        for component, details in explanation['components'].items():
            print(f"  {component}: {details['score']:.3f} × {details['weight']:.2f} = {details['contribution']:.3f}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_retrieval_ranker())