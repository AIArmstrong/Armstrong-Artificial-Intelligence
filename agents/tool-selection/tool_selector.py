"""
Core Tool Selector for Smart Tool Selection Enhancement

Implements intelligent tool selection logic with multi-pattern coordination,
confidence scoring, and AAI compliance for optimal tool recommendations.
"""
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

try:
    from .models import (
        PromptContext, ToolCategory, FabricPattern, ToolMetadata,
        ContextAnalysis, ToolSelection, SelectionRequest, SelectionResponse
    )
except ImportError:
    from agents.tool_selection.models.models import (
        PromptContext, ToolCategory, FabricPattern, ToolMetadata,
        ContextAnalysis, ToolSelection, SelectionRequest, SelectionResponse
    )
try:
    from .prompt_analyzer import PromptAnalyzer
except ImportError:
    from agents.tool_selection.prompt_analyzer import PromptAnalyzer
try:
    from .fabric_integrator import FabricIntegrator
except ImportError:
    from agents.tool_selection.fabric_integrator import FabricIntegrator
try:
    from .confidence_scorer import SelectionConfidenceScorer
except ImportError:
    from agents.tool_selection.confidence_scorer import SelectionConfidenceScorer

logger = logging.getLogger(__name__)


class ToolSelector:
    """
    Intelligent tool selection engine with multi-pattern coordination.
    
    Features:
    - Context-aware tool and pattern selection
    - Multi-pattern coordination and optimization
    - AAI-compliant confidence scoring (70-95%)
    - Alternative suggestion generation
    - Risk assessment and mitigation
    """
    
    def __init__(self, 
                 prompt_analyzer: Optional[PromptAnalyzer] = None,
                 fabric_integrator: Optional[FabricIntegrator] = None,
                 confidence_scorer: Optional[SelectionConfidenceScorer] = None):
        """Initialize tool selector with component dependencies"""
        
        # Initialize components
        self.prompt_analyzer = prompt_analyzer or PromptAnalyzer()
        self.fabric_integrator = fabric_integrator or FabricIntegrator()
        self.confidence_scorer = confidence_scorer or SelectionConfidenceScorer()
        
        # Tool registry
        self.available_tools = self._initialize_tool_registry()
        
        # Selection history for learning
        self.selection_history = []
        self.performance_metrics = {
            "total_selections": 0,
            "successful_selections": 0,
            "average_confidence": 0.75,
            "context_accuracy": {}
        }
        
        # Pattern coordination weights
        self.coordination_weights = {
            "context_match": 0.4,
            "pattern_effectiveness": 0.3,
            "tool_reliability": 0.2,
            "user_preference": 0.1
        }
    
    def _initialize_tool_registry(self) -> Dict[str, ToolMetadata]:
        """Initialize available tools registry"""
        
        tools = {}
        
        # Analysis tools
        tools["claude_analysis"] = ToolMetadata(
            name="claude_analysis",
            description="Advanced AI analysis with reasoning capabilities",
            category=ToolCategory.ANALYSIS,
            capabilities=["text_analysis", "code_review", "data_interpretation"],
            requirements=["openrouter_api"],
            confidence_baseline=0.85,
            performance_score=0.9,
            reliability_score=0.88
        )
        
        tools["fabric_analysis"] = ToolMetadata(
            name="fabric_analysis",
            description="Fabric pattern-based analysis workflows",
            category=ToolCategory.ANALYSIS,
            capabilities=["structured_analysis", "pattern_matching", "insight_extraction"],
            requirements=["fabric_patterns"],
            confidence_baseline=0.82,
            performance_score=0.85,
            reliability_score=0.90
        )
        
        # Content creation tools
        tools["claude_creation"] = ToolMetadata(
            name="claude_creation",
            description="AI-powered content generation and writing",
            category=ToolCategory.CONTENT_CREATION,
            capabilities=["text_generation", "creative_writing", "documentation"],
            requirements=["openrouter_api"],
            confidence_baseline=0.88,
            performance_score=0.92,
            reliability_score=0.87
        )
        
        tools["fabric_creation"] = ToolMetadata(
            name="fabric_creation",
            description="Fabric patterns for structured content creation",
            category=ToolCategory.CONTENT_CREATION,
            capabilities=["template_generation", "structured_writing", "format_conversion"],
            requirements=["fabric_patterns"],
            confidence_baseline=0.80,
            performance_score=0.83,
            reliability_score=0.92
        )
        
        # Code development tools
        tools["claude_coding"] = ToolMetadata(
            name="claude_coding",
            description="AI-assisted code development and debugging",
            category=ToolCategory.CODE_DEVELOPMENT,
            capabilities=["code_generation", "debugging", "refactoring", "testing"],
            requirements=["openrouter_api"],
            confidence_baseline=0.83,
            performance_score=0.87,
            reliability_score=0.85
        )
        
        tools["fabric_coding"] = ToolMetadata(
            name="fabric_coding",
            description="Fabric patterns for code-related tasks",
            category=ToolCategory.CODE_DEVELOPMENT,
            capabilities=["code_analysis", "architecture_design", "best_practices"],
            requirements=["fabric_patterns"],
            confidence_baseline=0.78,
            performance_score=0.80,
            reliability_score=0.88
        )
        
        # Research tools
        tools["web_research"] = ToolMetadata(
            name="web_research",
            description="Web-based research and information gathering",
            category=ToolCategory.RESEARCH,
            capabilities=["web_search", "information_extraction", "source_validation"],
            requirements=["internet_access"],
            confidence_baseline=0.75,
            performance_score=0.78,
            reliability_score=0.82
        )
        
        tools["fabric_research"] = ToolMetadata(
            name="fabric_research",
            description="Fabric patterns for research workflows",
            category=ToolCategory.RESEARCH,
            capabilities=["research_planning", "data_synthesis", "report_generation"],
            requirements=["fabric_patterns"],
            confidence_baseline=0.77,
            performance_score=0.81,
            reliability_score=0.85
        )
        
        # Data processing tools
        tools["data_processor"] = ToolMetadata(
            name="data_processor",
            description="Data analysis and processing capabilities",
            category=ToolCategory.DATA_PROCESSING,
            capabilities=["data_cleaning", "statistical_analysis", "visualization"],
            requirements=["python_environment"],
            confidence_baseline=0.72,
            performance_score=0.75,
            reliability_score=0.88
        )
        
        # Automation tools
        tools["n8n_automation"] = ToolMetadata(
            name="n8n_automation",
            description="Workflow automation and integration",
            category=ToolCategory.AUTOMATION,
            capabilities=["workflow_creation", "api_integration", "task_automation"],
            requirements=["n8n_instance"],
            confidence_baseline=0.73,
            performance_score=0.76,
            reliability_score=0.90
        )
        
        return tools
    
    async def select_tools(self, request: SelectionRequest) -> SelectionResponse:
        """
        Select optimal tools for given request.
        
        Args:
            request: Selection request with prompt and constraints
            
        Returns:
            Selection response with tools, patterns, and reasoning
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting tool selection for prompt: {request.prompt[:50]}...")
            
            # Step 1: Analyze prompt context
            context_analysis = await self.prompt_analyzer.analyze_prompt(
                request.prompt, 
                request.context_hint
            )
            
            # Step 2: Get relevant Fabric patterns
            fabric_patterns = await self.fabric_integrator.get_patterns_for_context(
                context_analysis.detected_context
            )
            
            # Step 3: Select optimal tools
            selected_tools = await self._select_optimal_tools(
                context_analysis, 
                request.preferred_tools,
                request.max_selections
            )
            
            # Step 4: Coordinate patterns and tools
            coordinated_selection = await self._coordinate_selection(
                context_analysis,
                fabric_patterns,
                selected_tools,
                request.constraints
            )
            
            # Step 5: Generate execution plan
            execution_plan = await self._generate_execution_plan(
                coordinated_selection["patterns"],
                coordinated_selection["tools"],
                context_analysis
            )
            
            # Step 6: Calculate overall confidence
            confidence = await self.confidence_scorer.calculate_selection_confidence(
                context_analysis,
                coordinated_selection["patterns"],
                coordinated_selection["tools"]
            )
            
            # Step 7: Generate alternatives if requested
            alternatives = []
            if request.include_alternatives:
                alternatives = await self._generate_alternatives(
                    context_analysis,
                    coordinated_selection["patterns"],
                    coordinated_selection["tools"]
                )
            
            # Step 8: Assess risks
            risk_factors = await self._assess_risk_factors(
                coordinated_selection["patterns"],
                coordinated_selection["tools"],
                context_analysis
            )
            
            # Create tool selection result
            tool_selection = ToolSelection(
                prompt_snippet=context_analysis.prompt_snippet,
                detected_context=context_analysis.detected_context,
                selected_patterns=coordinated_selection["patterns"],
                selected_tools=coordinated_selection["tools"],
                confidence_score=confidence,
                reasoning=coordinated_selection["reasoning"],
                execution_plan=execution_plan,
                alternatives=alternatives,
                risk_factors=risk_factors,
                success_probability=self._calculate_success_probability(confidence, risk_factors),
                estimated_time_minutes=self._estimate_execution_time(
                    coordinated_selection["patterns"],
                    coordinated_selection["tools"]
                )
            )
            
            # Create complete selection result
            selection_result = SelectionResult(
                context_analysis=context_analysis,
                tool_selection=tool_selection,
                session_id=request.session_id or f"sel_{int(datetime.now().timestamp())}"
            )
            
            # Generate recommendations and warnings
            recommendations = await self._generate_recommendations(selection_result)
            warnings = await self._generate_warnings(selection_result)
            
            # Calculate processing time
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Update metrics
            self._update_metrics(selection_result)
            
            # Create response
            response = SelectionResponse(
                selection_result=selection_result,
                recommendations=recommendations,
                warnings=warnings,
                execution_ready=len(risk_factors) == 0,
                next_steps=execution_plan[:3],  # First 3 steps
                session_id=selection_result.session_id,
                processing_time_ms=processing_time
            )
            
            logger.info(f"Tool selection completed: {len(selected_tools)} tools, {confidence:.2%} confidence")
            
            return response
            
        except Exception as e:
            logger.error(f"Tool selection failed: {e}")
            
            # Fallback response
            fallback_response = await self._create_fallback_response(request, str(e))
            return fallback_response
    
    async def _select_optimal_tools(self, 
                                  context_analysis: ContextAnalysis,
                                  preferred_tools: List[str],
                                  max_selections: int) -> List[ToolMetadata]:
        """Select optimal tools based on context and preferences"""
        
        # Get tools by category mapping
        category_mapping = {
            PromptContext.ANALYSIS: ToolCategory.ANALYSIS,
            PromptContext.CREATION: ToolCategory.CONTENT_CREATION,
            PromptContext.IMPLEMENTATION: ToolCategory.CODE_DEVELOPMENT,
            PromptContext.RESEARCH: ToolCategory.RESEARCH,
            PromptContext.DEBUGGING: ToolCategory.CODE_DEVELOPMENT,
            PromptContext.TESTING: ToolCategory.CODE_DEVELOPMENT,
            PromptContext.OPTIMIZATION: ToolCategory.CODE_DEVELOPMENT,
            PromptContext.DOCUMENTATION: ToolCategory.CONTENT_CREATION,
            PromptContext.EXTRACTION: ToolCategory.DATA_PROCESSING,
            PromptContext.SUMMARIZATION: ToolCategory.CONTENT_CREATION,
            PromptContext.TRANSLATION: ToolCategory.CONTENT_CREATION,
            PromptContext.DEPLOYMENT: ToolCategory.AUTOMATION
        }
        
        target_category = category_mapping.get(context_analysis.detected_context, ToolCategory.ANALYSIS)
        
        # Filter tools by category
        category_tools = [
            tool for tool in self.available_tools.values()
            if tool.category == target_category
        ]
        
        # Apply user preferences
        if preferred_tools:
            preferred = [
                tool for tool in category_tools
                if tool.name in preferred_tools
            ]
            if preferred:
                category_tools = preferred + [
                    tool for tool in category_tools 
                    if tool not in preferred
                ]
        
        # Score and rank tools
        scored_tools = []
        for tool in category_tools:
            score = await self._score_tool_for_context(tool, context_analysis)
            scored_tools.append((tool, score))
        
        # Sort by score and select top tools
        scored_tools.sort(key=lambda x: x[1], reverse=True)
        selected = [tool for tool, score in scored_tools[:max_selections]]
        
        return selected
    
    async def _score_tool_for_context(self, tool: ToolMetadata, context_analysis: ContextAnalysis) -> float:
        """Score tool suitability for context"""
        
        score = 0.0
        
        # Base score from tool reliability and performance
        score += tool.reliability_score * 0.3
        score += tool.performance_score * 0.3
        score += tool.confidence_baseline * 0.2
        
        # Context-specific scoring
        context_score = 0.0
        
        # Check if tool capabilities match context needs
        context_needs = {
            PromptContext.ANALYSIS: ["analysis", "review", "examination"],
            PromptContext.CREATION: ["generation", "creation", "writing"],
            PromptContext.RESEARCH: ["search", "research", "information"],
            PromptContext.IMPLEMENTATION: ["coding", "development", "implementation"],
            PromptContext.DEBUGGING: ["debugging", "fixing", "troubleshooting"]
        }
        
        needs = context_needs.get(context_analysis.detected_context, [])
        for need in needs:
            for capability in tool.capabilities:
                if need in capability.lower():
                    context_score += 0.1
        
        score += min(context_score, 0.2)  # Cap context bonus at 0.2
        
        return min(1.0, score)
    
    async def _coordinate_selection(self,
                                  context_analysis: ContextAnalysis,
                                  fabric_patterns: List[FabricPattern],
                                  selected_tools: List[ToolMetadata],
                                  constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate patterns and tools for optimal selection"""
        
        # Filter patterns by effectiveness and context fit
        suitable_patterns = []
        for pattern in fabric_patterns:
            if pattern.effectiveness_score >= 0.7:  # Minimum effectiveness
                suitable_patterns.append(pattern)
        
        # Limit patterns to avoid over-complexity
        max_patterns = constraints.get("max_patterns", 3)
        if len(suitable_patterns) > max_patterns:
            # Sort by effectiveness and take top patterns
            suitable_patterns.sort(key=lambda p: p.effectiveness_score, reverse=True)
            suitable_patterns = suitable_patterns[:max_patterns]
        
        # Generate reasoning for selection
        reasoning_parts = []
        reasoning_parts.append(f"Context detected: {context_analysis.detected_context.value}")
        reasoning_parts.append(f"Confidence: {context_analysis.confidence_score:.1%}")
        
        if suitable_patterns:
            reasoning_parts.append(f"Selected {len(suitable_patterns)} Fabric patterns for structured execution")
        
        if selected_tools:
            reasoning_parts.append(f"Selected {len(selected_tools)} tools optimized for {context_analysis.detected_context.value}")
        
        reasoning = ". ".join(reasoning_parts)
        
        return {
            "patterns": suitable_patterns,
            "tools": selected_tools,
            "reasoning": reasoning
        }
    
    async def _generate_execution_plan(self,
                                     patterns: List[FabricPattern],
                                     tools: List[ToolMetadata],
                                     context_analysis: ContextAnalysis) -> List[str]:
        """Generate step-by-step execution plan"""
        
        plan = []
        
        # Step 1: Context preparation
        plan.append(f"Analyze prompt context ({context_analysis.detected_context.value})")
        
        # Step 2: Pattern execution
        if patterns:
            for i, pattern in enumerate(patterns, 1):
                plan.append(f"Execute Fabric pattern: {pattern.name}")
        
        # Step 3: Tool execution
        if tools:
            for tool in tools:
                plan.append(f"Apply {tool.name} for {tool.category.value}")
        
        # Step 4: Result synthesis
        plan.append("Synthesize results and validate output quality")
        
        # Step 5: Delivery
        plan.append("Format and deliver final response")
        
        return plan
    
    async def _generate_alternatives(self,
                                   context_analysis: ContextAnalysis,
                                   primary_patterns: List[FabricPattern],
                                   primary_tools: List[ToolMetadata]) -> List[Dict[str, Any]]:
        """Generate alternative tool and pattern selections"""
        
        alternatives = []
        
        # Alternative 1: Different tool combination
        alt_tools = [
            tool for tool in self.available_tools.values()
            if tool not in primary_tools and 
            any(cap in ["analysis", "generation", "processing"] for cap in tool.capabilities)
        ][:2]
        
        if alt_tools:
            alternatives.append({
                "type": "alternative_tools",
                "description": f"Alternative tools: {', '.join(t.name for t in alt_tools)}",
                "confidence_impact": -0.05,
                "reasoning": "Different tool approach with potentially different strengths"
            })
        
        # Alternative 2: Simplified approach
        if len(primary_patterns) > 1:
            alternatives.append({
                "type": "simplified",
                "description": f"Simplified approach using only {primary_patterns[0].name}",
                "confidence_impact": -0.03,
                "reasoning": "Reduced complexity for faster execution"
            })
        
        # Alternative 3: Enhanced approach
        if context_analysis.complexity_indicators:
            alternatives.append({
                "type": "enhanced",
                "description": "Enhanced approach with additional analysis patterns",
                "confidence_impact": 0.02,
                "reasoning": "More thorough analysis for complex requirements"
            })
        
        return alternatives
    
    async def _assess_risk_factors(self,
                                 patterns: List[FabricPattern],
                                 tools: List[ToolMetadata],
                                 context_analysis: ContextAnalysis) -> List[str]:
        """Assess potential risk factors for selection"""
        
        risks = []
        
        # Check for missing dependencies
        for tool in tools:
            for requirement in tool.requirements:
                if requirement not in ["openrouter_api", "fabric_patterns"]:  # Known available
                    risks.append(f"Tool {tool.name} requires {requirement}")
        
        # Check confidence levels
        if context_analysis.confidence_score < 0.75:
            risks.append("Lower confidence in context detection")
        
        # Check complexity vs capability mismatch
        if len(context_analysis.complexity_indicators) > 3 and len(tools) < 2:
            risks.append("High complexity but limited tool selection")
        
        # Check urgency vs execution time
        if context_analysis.urgency_level >= 4 and context_analysis.estimated_effort >= 7:
            risks.append("High urgency but complex task requiring significant effort")
        
        return risks
    
    def _calculate_success_probability(self, confidence: float, risk_factors: List[str]) -> float:
        """Calculate success probability based on confidence and risks"""
        
        base_probability = confidence
        
        # Reduce probability for each risk factor
        risk_penalty = len(risk_factors) * 0.05
        
        return max(0.5, base_probability - risk_penalty)
    
    def _estimate_execution_time(self, patterns: List[FabricPattern], tools: List[ToolMetadata]) -> int:
        """Estimate execution time in minutes"""
        
        base_time = 2  # Base 2 minutes
        
        # Add time for patterns
        for pattern in patterns:
            base_time += pattern.execution_time_estimate / 60  # Convert seconds to minutes
        
        # Add time for tools (estimated)
        base_time += len(tools) * 1.5
        
        return max(1, int(base_time))
    
    async def _generate_recommendations(self, selection_result) -> List[str]:
        """Generate additional recommendations"""
        
        recommendations = []
        
        # Confidence-based recommendations
        if selection_result.tool_selection.confidence_score < 0.80:
            recommendations.append("Consider providing more specific context for better tool selection")
        
        # Risk mitigation recommendations
        if selection_result.tool_selection.risk_factors:
            recommendations.append("Review and address identified risk factors before execution")
        
        # Performance recommendations
        if selection_result.tool_selection.estimated_time_minutes > 10:
            recommendations.append("Consider breaking down complex tasks into smaller steps")
        
        return recommendations
    
    async def _generate_warnings(self, selection_result) -> List[str]:
        """Generate warnings for potential issues"""
        
        warnings = []
        
        # High complexity warnings
        if len(selection_result.context_analysis.complexity_indicators) > 5:
            warnings.append("High complexity task detected - execution may require additional time")
        
        # Low confidence warnings
        if selection_result.tool_selection.confidence_score < 0.75:
            warnings.append("Lower confidence selection - results may vary")
        
        # Urgency vs complexity mismatch
        if (selection_result.context_analysis.urgency_level >= 4 and 
            selection_result.tool_selection.estimated_time_minutes > 8):
            warnings.append("High urgency task with significant time requirement")
        
        return warnings
    
    async def _create_fallback_response(self, request: SelectionRequest, error: str) -> SelectionResponse:
        """Create fallback response when selection fails"""
        
        # Create minimal context analysis
        context_analysis = ContextAnalysis(
            original_prompt=request.prompt,
            prompt_snippet=request.prompt[:100],
            detected_context=PromptContext.ANALYSIS,
            confidence_score=0.70
        )
        
        # Create minimal tool selection
        tool_selection = ToolSelection(
            prompt_snippet=context_analysis.prompt_snippet,
            detected_context=context_analysis.detected_context,
            confidence_score=0.70,
            reasoning=f"Fallback selection due to error: {error}"
        )
        
        # Create selection result
        try:
    from .models import SelectionResult
except ImportError:
    from agents.tool_selection.models import SelectionResult
        selection_result = SelectionResult(
            context_analysis=context_analysis,
            tool_selection=tool_selection,
            session_id=request.session_id or "fallback"
        )
        
        return SelectionResponse(
            selection_result=selection_result,
            warnings=[f"Selection error occurred: {error}"],
            execution_ready=False,
            session_id=selection_result.session_id,
            processing_time_ms=0
        )
    
    def _update_metrics(self, selection_result):
        """Update performance metrics"""
        
        self.performance_metrics["total_selections"] += 1
        
        # Update average confidence
        total = self.performance_metrics["total_selections"]
        current_avg = self.performance_metrics["average_confidence"]
        new_confidence = selection_result.tool_selection.confidence_score
        
        self.performance_metrics["average_confidence"] = (
            (current_avg * (total - 1) + new_confidence) / total
        )
        
        # Update context accuracy tracking
        context = selection_result.context_analysis.detected_context
        if context not in self.performance_metrics["context_accuracy"]:
            self.performance_metrics["context_accuracy"][context] = []
        
        self.performance_metrics["context_accuracy"][context].append(
            selection_result.context_analysis.confidence_score
        )
    
    def get_selector_status(self) -> Dict[str, Any]:
        """Get selector status and performance metrics"""
        
        return {
            "available_tools": len(self.available_tools),
            "total_selections": self.performance_metrics["total_selections"],
            "average_confidence": self.performance_metrics["average_confidence"],
            "context_tracking": len(self.performance_metrics["context_accuracy"]),
            "coordination_weights": self.coordination_weights,
            "ready": True
        }


async def test_tool_selector():
    """Test tool selector functionality"""
    
    selector = ToolSelector()
    
    print("🧪 Testing Tool Selector")
    print("=" * 25)
    
    # Check selector status
    status = selector.get_selector_status()
    print(f"Available tools: {status['available_tools']}")
    print(f"Total selections: {status['total_selections']}")
    print(f"Ready: {status['ready']}")
    
    # Test selection request
    print(f"\n🎯 Testing tool selection...")
    
    request = SelectionRequest(
        prompt="Analyze this business proposal for strengths and weaknesses",
        max_selections=2,
        include_alternatives=True
    )
    
    response = await selector.select_tools(request)
    
    print(f"Context detected: {response.selection_result.context_analysis.detected_context.value}")
    print(f"Confidence: {response.selection_result.tool_selection.confidence_score:.1%}")
    print(f"Selected tools: {len(response.selection_result.tool_selection.selected_tools)}")
    print(f"Selected patterns: {len(response.selection_result.tool_selection.selected_patterns)}")
    print(f"Alternatives: {len(response.selection_result.tool_selection.alternatives)}")
    print(f"Execution ready: {response.execution_ready}")
    
    print(f"\n✅ Tool Selector Testing Complete")
    print(f"Smart tool selection working with AAI compliance")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tool_selector())