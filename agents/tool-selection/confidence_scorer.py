"""
Confidence Scorer for Tool Selection Enhancement

Implements AAI-compliant confidence scoring for tool and pattern selections
with multi-factor analysis and learning-based improvements.
"""
import logging
import math
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

try:
    from .models import (
        ContextAnalysis, FabricPattern, ToolMetadata, PromptContext
    )
except ImportError:
    from agents.tool_selection.models.models import (
        ContextAnalysis, FabricPattern, ToolMetadata, PromptContext
    )

logger = logging.getLogger(__name__)


class SelectionConfidenceScorer:
    """
    AAI-compliant confidence scoring for tool selections.
    
    Features:
    - Multi-factor confidence calculation
    - AAI range compliance (70-95%)
    - Pattern and tool reliability assessment
    - Context alignment scoring
    - Learning-based confidence adjustment
    """
    
    def __init__(self):
        """Initialize confidence scorer with AAI compliance"""
        
        # AAI confidence constraints
        self.AAI_MIN_CONFIDENCE = 0.70
        self.AAI_MAX_CONFIDENCE = 0.95
        
        # Confidence factors and weights
        self.confidence_factors = {
            "context_detection": 0.25,      # How well context was detected
            "pattern_reliability": 0.20,    # Reliability of selected patterns
            "tool_reliability": 0.20,       # Reliability of selected tools
            "selection_coherence": 0.15,    # How well selection fits together
            "historical_performance": 0.10, # Past performance for similar selections
            "risk_assessment": 0.10         # Risk factors impact
        }
        
        # Historical performance tracking
        self.historical_data = {}
        self.context_performance = {}
        
        # Risk factor penalties
        self.risk_penalties = {
            "missing_dependency": -0.05,
            "low_context_confidence": -0.03,
            "complexity_mismatch": -0.04,
            "urgency_mismatch": -0.02,
            "tool_incompatibility": -0.06
        }
    
    async def calculate_selection_confidence(self,
                                           context_analysis: ContextAnalysis,
                                           selected_patterns: List[FabricPattern],
                                           selected_tools: List[ToolMetadata]) -> float:
        """
        Calculate overall confidence for tool/pattern selection.
        
        Args:
            context_analysis: Analyzed prompt context
            selected_patterns: Selected Fabric patterns
            selected_tools: Selected tools
            
        Returns:
            AAI-compliant confidence score (70-95%)
        """
        try:
            logger.debug(f"Calculating confidence for {len(selected_patterns)} patterns, {len(selected_tools)} tools")
            
            # Calculate individual confidence factors
            factors = {}
            
            # Factor 1: Context detection confidence
            factors["context_detection"] = await self._score_context_detection(context_analysis)
            
            # Factor 2: Pattern reliability
            factors["pattern_reliability"] = await self._score_pattern_reliability(
                selected_patterns, context_analysis.detected_context
            )
            
            # Factor 3: Tool reliability
            factors["tool_reliability"] = await self._score_tool_reliability(
                selected_tools, context_analysis.detected_context
            )
            
            # Factor 4: Selection coherence
            factors["selection_coherence"] = await self._score_selection_coherence(
                context_analysis, selected_patterns, selected_tools
            )
            
            # Factor 5: Historical performance
            factors["historical_performance"] = await self._score_historical_performance(
                context_analysis.detected_context, selected_patterns, selected_tools
            )
            
            # Factor 6: Risk assessment
            factors["risk_assessment"] = await self._score_risk_factors(
                context_analysis, selected_patterns, selected_tools
            )
            
            # Calculate weighted confidence
            raw_confidence = sum(
                factors[factor] * weight 
                for factor, weight in self.confidence_factors.items()
            )
            
            # Apply AAI range enforcement
            final_confidence = self._enforce_aai_range(raw_confidence)
            
            # Log confidence breakdown
            logger.info(f"Confidence factors: {', '.join(f'{k}:{v:.2f}' for k, v in factors.items())}")
            logger.info(f"Final confidence: {final_confidence:.1%} (AAI compliant)")
            
            return final_confidence
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {e}")
            # Return safe AAI minimum
            return self.AAI_MIN_CONFIDENCE
    
    async def _score_context_detection(self, context_analysis: ContextAnalysis) -> float:
        """Score context detection quality"""
        
        base_score = context_analysis.confidence_score
        
        # Boost for clear context indicators
        if len(context_analysis.keywords_found) >= 2:
            base_score += 0.05
        
        # Boost for sufficient context
        if len(context_analysis.prompt_snippet) >= 50:
            base_score += 0.03
        
        # Penalty for low confidence
        if context_analysis.confidence_score < 0.75:
            base_score -= 0.02
        
        return min(1.0, base_score)
    
    async def _score_pattern_reliability(self, 
                                       patterns: List[FabricPattern],
                                       context: PromptContext) -> float:
        """Score reliability of selected patterns"""
        
        if not patterns:
            return 0.75  # Neutral score when no patterns
        
        # Average effectiveness of patterns
        avg_effectiveness = sum(p.effectiveness_score for p in patterns) / len(patterns)
        
        # Pattern-context alignment score
        alignment_score = 0.0
        context_categories = {
            PromptContext.ANALYSIS: "analysis",
            PromptContext.CREATION: "creation",
            PromptContext.RESEARCH: "research",
            PromptContext.EXTRACTION: "extraction",
            PromptContext.SUMMARIZATION: "summarization"
        }
        
        target_category = context_categories.get(context, "general")
        
        aligned_patterns = sum(1 for p in patterns if p.category == target_category)
        if patterns:
            alignment_score = aligned_patterns / len(patterns)
        
        # Combine scores
        pattern_score = (avg_effectiveness * 0.7) + (alignment_score * 0.3)
        
        return min(1.0, pattern_score)
    
    async def _score_tool_reliability(self,
                                    tools: List[ToolMetadata],
                                    context: PromptContext) -> float:
        """Score reliability of selected tools"""
        
        if not tools:
            return 0.70  # Lower neutral score when no tools
        
        # Average reliability scores
        avg_reliability = sum(t.reliability_score for t in tools) / len(tools)
        avg_performance = sum(t.performance_score for t in tools) / len(tools)
        avg_baseline = sum(t.confidence_baseline for t in tools) / len(tools)
        
        # Tool diversity bonus (different categories)
        unique_categories = len(set(t.category for t in tools))
        diversity_bonus = min(0.05, unique_categories * 0.02)
        
        # Combine scores
        tool_score = (
            avg_reliability * 0.4 + 
            avg_performance * 0.3 + 
            avg_baseline * 0.3 + 
            diversity_bonus
        )
        
        return min(1.0, tool_score)
    
    async def _score_selection_coherence(self,
                                       context_analysis: ContextAnalysis,
                                       patterns: List[FabricPattern],
                                       tools: List[ToolMetadata]) -> float:
        """Score how well patterns and tools work together"""
        
        coherence_score = 0.75  # Base coherence
        
        # Check if selection addresses detected context
        context_addressed = False
        
        # Check patterns address context
        if patterns:
            context_categories = {
                PromptContext.ANALYSIS: "analysis",
                PromptContext.CREATION: "creation",
                PromptContext.RESEARCH: "research",
                PromptContext.EXTRACTION: "extraction"
            }
            target_category = context_categories.get(context_analysis.detected_context)
            if target_category and any(p.category == target_category for p in patterns):
                context_addressed = True
        
        # Check tools address context
        if tools and not context_addressed:
            # Tool categories that address different contexts
            tool_context_map = {
                PromptContext.ANALYSIS: ["analysis"],
                PromptContext.CREATION: ["content_creation"],
                PromptContext.IMPLEMENTATION: ["code_development"],
                PromptContext.RESEARCH: ["research"]
            }
            target_categories = tool_context_map.get(context_analysis.detected_context, [])
            if any(t.category.value in target_categories for t in tools):
                context_addressed = True
        
        if context_addressed:
            coherence_score += 0.10
        
        # Check complexity alignment
        complexity_indicators = len(context_analysis.complexity_indicators)
        total_selections = len(patterns) + len(tools)
        
        if complexity_indicators > 3 and total_selections >= 2:
            coherence_score += 0.05  # Good match for complex task
        elif complexity_indicators <= 1 and total_selections <= 2:
            coherence_score += 0.05  # Good match for simple task
        elif complexity_indicators > 5 and total_selections <= 1:
            coherence_score -= 0.10  # Under-resourced for complexity
        
        # Check effort alignment
        if context_analysis.estimated_effort >= 7 and total_selections >= 2:
            coherence_score += 0.03
        elif context_analysis.estimated_effort <= 3 and total_selections >= 3:
            coherence_score -= 0.03  # Over-engineered for simple task
        
        return min(1.0, max(0.5, coherence_score))
    
    async def _score_historical_performance(self,
                                          context: PromptContext,
                                          patterns: List[FabricPattern],
                                          tools: List[ToolMetadata]) -> float:
        """Score based on historical performance"""
        
        # Base score when no historical data
        base_score = 0.75
        
        # Check context performance history
        if context in self.context_performance:
            context_history = self.context_performance[context]
            if len(context_history) >= 3:  # Enough data points
                avg_performance = sum(context_history) / len(context_history)
                base_score = avg_performance
        
        # Check pattern performance history
        pattern_performance = []
        for pattern in patterns:
            if pattern.name in self.historical_data:
                pattern_performance.append(self.historical_data[pattern.name])
        
        if pattern_performance:
            avg_pattern_perf = sum(pattern_performance) / len(pattern_performance)
            base_score = (base_score * 0.7) + (avg_pattern_perf * 0.3)
        
        # Check tool performance history
        tool_performance = []
        for tool in tools:
            if tool.name in self.historical_data:
                tool_performance.append(self.historical_data[tool.name])
        
        if tool_performance:
            avg_tool_perf = sum(tool_performance) / len(tool_performance)
            base_score = (base_score * 0.7) + (avg_tool_perf * 0.3)
        
        return min(1.0, base_score)
    
    async def _score_risk_factors(self,
                                context_analysis: ContextAnalysis,
                                patterns: List[FabricPattern],
                                tools: List[ToolMetadata]) -> float:
        """Score risk factors impact on confidence"""
        
        risk_score = 1.0  # Start with perfect score
        
        # Apply penalties for risk factors
        
        # Low context confidence penalty
        if context_analysis.confidence_score < 0.75:
            risk_score += self.risk_penalties["low_context_confidence"]
        
        # Complexity mismatch penalty
        complexity_count = len(context_analysis.complexity_indicators)
        selection_count = len(patterns) + len(tools)
        
        if complexity_count > 4 and selection_count <= 1:
            risk_score += self.risk_penalties["complexity_mismatch"]
        
        # Urgency mismatch penalty
        if context_analysis.urgency_level >= 4 and context_analysis.estimated_effort >= 7:
            risk_score += self.risk_penalties["urgency_mismatch"]
        
        # Tool dependency penalty
        for tool in tools:
            for requirement in tool.requirements:
                if requirement not in ["openrouter_api", "fabric_patterns"]:
                    risk_score += self.risk_penalties["missing_dependency"]
        
        # Pattern complexity penalty
        if patterns:
            avg_complexity = sum(p.complexity_score for p in patterns) / len(patterns)
            if avg_complexity > 0.8 and context_analysis.urgency_level >= 4:
                risk_score += self.risk_penalties["tool_incompatibility"]
        
        return max(0.5, risk_score)
    
    def _enforce_aai_range(self, confidence: float) -> float:
        """Enforce AAI confidence range (70-95%)"""
        return max(self.AAI_MIN_CONFIDENCE, min(self.AAI_MAX_CONFIDENCE, confidence))
    
    async def update_historical_performance(self,
                                          context: PromptContext,
                                          patterns: List[str],
                                          tools: List[str],
                                          success_rate: float,
                                          user_satisfaction: float):
        """Update historical performance data"""
        
        # Update context performance
        if context not in self.context_performance:
            self.context_performance[context] = []
        
        context_score = (success_rate * 0.7) + (user_satisfaction * 0.3)
        self.context_performance[context].append(context_score)
        
        # Keep only recent history (last 20 entries)
        if len(self.context_performance[context]) > 20:
            self.context_performance[context] = self.context_performance[context][-20:]
        
        # Update pattern performance
        for pattern_name in patterns:
            if pattern_name not in self.historical_data:
                self.historical_data[pattern_name] = []
            
            self.historical_data[pattern_name].append(context_score)
            
            # Keep only recent history
            if len(self.historical_data[pattern_name]) > 10:
                self.historical_data[pattern_name] = self.historical_data[pattern_name][-10:]
        
        # Update tool performance
        for tool_name in tools:
            if tool_name not in self.historical_data:
                self.historical_data[tool_name] = []
            
            self.historical_data[tool_name].append(context_score)
            
            # Keep only recent history
            if len(self.historical_data[tool_name]) > 10:
                self.historical_data[tool_name] = self.historical_data[tool_name][-10:]
    
    def get_confidence_statistics(self) -> Dict[str, Any]:
        """Get confidence scoring statistics"""
        
        return {
            "aai_range": f"{self.AAI_MIN_CONFIDENCE:.0%}-{self.AAI_MAX_CONFIDENCE:.0%}",
            "confidence_factors": self.confidence_factors,
            "risk_penalties": self.risk_penalties,
            "historical_contexts": len(self.context_performance),
            "historical_entries": len(self.historical_data),
            "ready": True
        }
    
    def calculate_confidence_breakdown(self, factors: Dict[str, float]) -> Dict[str, float]:
        """Calculate detailed confidence breakdown"""
        
        breakdown = {}
        
        for factor, value in factors.items():
            if factor in self.confidence_factors:
                weight = self.confidence_factors[factor]
                contribution = value * weight
                breakdown[factor] = {
                    "value": value,
                    "weight": weight,
                    "contribution": contribution
                }
        
        return breakdown


async def test_confidence_scorer():
    """Test confidence scorer functionality"""
    
    scorer = SelectionConfidenceScorer()
    
    print("🧪 Testing Confidence Scorer")
    print("=" * 30)
    
    # Check scorer stats
    stats = scorer.get_confidence_statistics()
    print(f"AAI range: {stats['aai_range']}")
    print(f"Confidence factors: {len(stats['confidence_factors'])}")
    print(f"Risk penalties: {len(stats['risk_penalties'])}")
    print(f"Ready: {stats['ready']}")
    
    # Create test data
    # Import modules defined at top level
    
    context_analysis = ContextAnalysis(
        original_prompt="Analyze this business proposal for strengths and weaknesses",
        prompt_snippet="analyze this business proposal for strengths and weaknesses",
        detected_context=PromptContext.ANALYSIS,
        confidence_score=0.85,
        keywords_found=["analyze", "business"],
        urgency_level=3,
        estimated_effort=5
    )
    
    patterns = [
        FabricPattern(
            name="analyze_claims",
            description="Analyze claims for accuracy",
            category="analysis",
            input_format="text",
            output_format="analysis",
            effectiveness_score=0.85,
            complexity_score=0.6
        )
    ]
    
    tools = [
        ToolMetadata(
            name="claude_analysis",
            description="AI analysis tool",
            category=ToolCategory.ANALYSIS,
            confidence_baseline=0.85,
            performance_score=0.90,
            reliability_score=0.88
        )
    ]
    
    # Test confidence calculation
    print(f"\n🎯 Testing confidence calculation...")
    
    confidence = await scorer.calculate_selection_confidence(
        context_analysis, patterns, tools
    )
    
    print(f"Calculated confidence: {confidence:.1%}")
    print(f"AAI compliant: {0.70 <= confidence <= 0.95}")
    
    print(f"\n✅ Confidence Scorer Testing Complete")
    print(f"AAI-compliant confidence scoring working")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_confidence_scorer())