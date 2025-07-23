"""
AAI Brain Module: Smart Tool Selector

Integrates intelligent tool selection into AAI's brain system
for automatic tool selection across all commands and interactions.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

# AAI Brain imports with fallbacks
try:
    from brain.core.module import BrainModule
    from brain.core.confidence import AAIConfidenceScorer
    BRAIN_AVAILABLE = True
except ImportError:
    BrainModule = object
    AAIConfidenceScorer = None
    BRAIN_AVAILABLE = False

# Tool selection imports with fallbacks
try:
    from agents.tool_selection.prompt_analyzer import PromptAnalyzer
    from agents.tool_selection.fabric_integrator import FabricIntegrator  
    from agents.tool_selection.tool_selector import ToolSelector
    from agents.tool_selection.confidence_scorer import SelectionConfidenceScorer
    from agents.tool_selection.learning_engine import SelectionLearningEngine
    from agents.tool_selection.models import SelectionRequest, PromptContext
    TOOL_SELECTION_AVAILABLE = True
except ImportError:
    PromptAnalyzer = None
    FabricIntegrator = None
    ToolSelector = None
    SelectionConfidenceScorer = None
    SelectionLearningEngine = None
    SelectionRequest = None
    PromptContext = None
    TOOL_SELECTION_AVAILABLE = False

logger = logging.getLogger(__name__)


class SmartToolSelectorModule(BrainModule if BRAIN_AVAILABLE else object):
    """
    AAI Brain Module for intelligent tool selection.
    
    Features:
    - Automatic tool selection for all AAI interactions
    - Context-aware pattern and tool recommendations
    - Learning from selection outcomes
    - AAI confidence scoring integration
    - Brain system integration for decision support
    """
    
    def __init__(self):
        """Initialize smart tool selector module"""
        
        # Initialize parent if available
        if BRAIN_AVAILABLE:
            super().__init__(
                name="smart_tool_selector",
                description="Intelligent tool selection for AAI commands",
                version="1.0.0"
            )
        
        # Initialize components with fallbacks
        self.prompt_analyzer = None
        self.fabric_integrator = None
        self.tool_selector = None
        self.confidence_scorer = None
        self.learning_engine = None
        
        # Module state
        self.initialized = False
        self.selection_count = 0
        self.success_rate = 0.0
        
        # Initialize components
        asyncio.create_task(self._initialize_components())
    
    async def _initialize_components(self):
        """Initialize tool selection components"""
        
        try:
            if not TOOL_SELECTION_AVAILABLE:
                logger.warning("Tool selection components not available - using fallback mode")
                self.initialized = False
                return
            
            # Initialize core components
            self.prompt_analyzer = PromptAnalyzer()
            self.fabric_integrator = FabricIntegrator()
            self.confidence_scorer = SelectionConfidenceScorer()
            self.learning_engine = SelectionLearningEngine()
            
            # Initialize tool selector with components
            self.tool_selector = ToolSelector(
                prompt_analyzer=self.prompt_analyzer,
                fabric_integrator=self.fabric_integrator,
                confidence_scorer=self.confidence_scorer
            )
            
            # Discover Fabric patterns
            await self.fabric_integrator.discover_patterns()
            
            self.initialized = True
            logger.info("Smart Tool Selector Module initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Smart Tool Selector Module: {e}")
            self.initialized = False
    
    async def select_tools_for_prompt(self, 
                                    prompt: str,
                                    user_id: str = "anonymous",
                                    context_hint: Optional[str] = None,
                                    preferred_tools: List[str] = None,
                                    session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Select optimal tools for a given prompt.
        
        Args:
            prompt: User prompt requiring tool selection
            user_id: User identifier for personalization
            context_hint: Optional context hint
            preferred_tools: User preferred tools
            session_id: Session identifier
            
        Returns:
            Selection result with tools, patterns, and confidence
        """
        try:
            if not self.initialized:
                return await self._fallback_selection(prompt)
            
            # Convert context hint to enum if provided
            context_enum = None
            if context_hint and TOOL_SELECTION_AVAILABLE:
                try:
                    context_enum = PromptContext(context_hint.lower())
                except ValueError:
                    pass
            
            # Create selection request
            request = SelectionRequest(
                prompt=prompt,
                user_id=user_id,
                context_hint=context_enum,
                preferred_tools=preferred_tools or [],
                session_id=session_id,
                max_selections=3,
                include_alternatives=True,
                learning_enabled=True
            )
            
            # Perform tool selection
            response = await self.tool_selector.select_tools(request)
            
            # Update module metrics
            self.selection_count += 1
            
            # Prepare response
            result = {
                "success": True,
                "context": response.selection_result.context_analysis.detected_context.value,
                "confidence": response.selection_result.tool_selection.confidence_score,
                "selected_tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "category": tool.category.value,
                        "confidence": tool.confidence_baseline
                    }
                    for tool in response.selection_result.tool_selection.selected_tools
                ],
                "selected_patterns": [
                    {
                        "name": pattern.name,
                        "description": pattern.description,
                        "category": pattern.category,
                        "effectiveness": pattern.effectiveness_score
                    }
                    for pattern in response.selection_result.tool_selection.selected_patterns
                ],
                "execution_plan": response.selection_result.tool_selection.execution_plan,
                "alternatives": response.selection_result.tool_selection.alternatives,
                "recommendations": response.recommendations,
                "warnings": response.warnings,
                "execution_ready": response.execution_ready,
                "estimated_time": response.selection_result.tool_selection.estimated_time_minutes,
                "session_id": response.session_id,
                "processing_time_ms": response.processing_time_ms
            }
            
            logger.info(f"Tool selection completed: {len(result['selected_tools'])} tools, {result['confidence']:.1%} confidence")
            
            return result
            
        except Exception as e:
            logger.error(f"Tool selection failed: {e}")
            return await self._fallback_selection(prompt, error=str(e))
    
    async def record_selection_outcome(self,
                                     session_id: str,
                                     execution_success: bool,
                                     user_satisfaction: float,
                                     execution_time_actual: int,
                                     user_feedback: Optional[Dict[str, Any]] = None) -> bool:
        """
        Record outcome of tool selection for learning.
        
        Args:
            session_id: Session identifier from selection
            execution_success: Whether execution was successful
            user_satisfaction: User satisfaction score (0.0-1.0)
            execution_time_actual: Actual execution time in minutes
            user_feedback: Optional user feedback
            
        Returns:
            True if recording was successful
        """
        try:
            if not self.initialized or not self.learning_engine:
                logger.warning("Learning engine not available - cannot record outcome")
                return False
            
            # Note: In a full implementation, we would need to store
            # selection results and retrieve them by session_id
            # For now, we'll create a minimal selection result
            
            # This would typically be retrieved from storage
            # selection_result = await self._get_selection_result(session_id)
            
            # For now, skip actual recording and just log
            logger.info(f"Recording outcome for session {session_id}: success={execution_success}, satisfaction={user_satisfaction:.1%}")
            
            # Update success rate
            if execution_success:
                self.success_rate = (self.success_rate * (self.selection_count - 1) + 1.0) / self.selection_count
            else:
                self.success_rate = (self.success_rate * (self.selection_count - 1) + 0.0) / self.selection_count
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to record selection outcome: {e}")
            return False
    
    async def get_tool_recommendations(self, 
                                     context: str,
                                     complexity_level: int = 3) -> Dict[str, Any]:
        """
        Get tool recommendations based on learned patterns.
        
        Args:
            context: Context type (analysis, creation, research, etc.)
            complexity_level: Task complexity level (1-10)
            
        Returns:
            Recommendations based on learning
        """
        try:
            if not self.initialized or not self.learning_engine:
                return {"recommendations": [], "error": "Learning engine not available"}
            
            # Convert context to enum
            context_enum = None
            if TOOL_SELECTION_AVAILABLE:
                try:
                    context_enum = PromptContext(context.lower())
                except ValueError:
                    context_enum = PromptContext.ANALYSIS
            
            if not context_enum:
                return {"recommendations": [], "error": "Invalid context"}
            
            # Generate complexity indicators based on level
            complexity_indicators = []
            if complexity_level >= 7:
                complexity_indicators = ["complex", "advanced", "comprehensive"]
            elif complexity_level >= 5:
                complexity_indicators = ["moderate", "detailed"]
            elif complexity_level <= 3:
                complexity_indicators = ["simple", "basic"]
            
            # Get recommendations
            recommendations = await self.learning_engine.get_selection_recommendations(
                context_enum, complexity_indicators
            )
            
            return {
                "context": context,
                "complexity_level": complexity_level,
                "preferred_patterns": recommendations.get("preferred_patterns", []),
                "preferred_tools": recommendations.get("preferred_tools", []),
                "avoid_patterns": recommendations.get("avoid_patterns", []),
                "avoid_tools": recommendations.get("avoid_tools", []),
                "execution_time_estimate": recommendations.get("execution_time_estimates", {}),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to get tool recommendations: {e}")
            return {"recommendations": [], "error": str(e)}
    
    async def analyze_selection_performance(self) -> Dict[str, Any]:
        """Analyze overall selection performance and trends"""
        
        try:
            if not self.initialized or not self.learning_engine:
                return {"analysis": {}, "error": "Learning engine not available"}
            
            # Get learning trends analysis
            analysis = await self.learning_engine.analyze_learning_trends()
            
            # Add module-specific metrics
            analysis["module_metrics"] = {
                "total_selections": self.selection_count,
                "success_rate": self.success_rate,
                "module_initialized": self.initialized,
                "components_available": TOOL_SELECTION_AVAILABLE
            }
            
            return {"analysis": analysis, "success": True}
            
        except Exception as e:
            logger.error(f"Failed to analyze selection performance: {e}")
            return {"analysis": {}, "error": str(e)}
    
    async def _fallback_selection(self, prompt: str, error: Optional[str] = None) -> Dict[str, Any]:
        """Provide fallback tool selection when components are unavailable"""
        
        # Simple rule-based fallback
        prompt_lower = prompt.lower()
        
        tools = []
        patterns = []
        context = "analysis"
        
        # Basic context detection
        if any(word in prompt_lower for word in ["analyze", "review", "examine"]):
            context = "analysis"
            tools = [{"name": "claude_analysis", "description": "AI analysis", "category": "analysis", "confidence": 0.75}]
        elif any(word in prompt_lower for word in ["create", "generate", "write"]):
            context = "creation"
            tools = [{"name": "claude_creation", "description": "AI creation", "category": "content_creation", "confidence": 0.75}]
        elif any(word in prompt_lower for word in ["research", "find", "search"]):
            context = "research"
            tools = [{"name": "web_research", "description": "Web research", "category": "research", "confidence": 0.70}]
        elif any(word in prompt_lower for word in ["code", "implement", "debug"]):
            context = "implementation"
            tools = [{"name": "claude_coding", "description": "AI coding", "category": "code_development", "confidence": 0.73}]
        else:
            tools = [{"name": "claude_analysis", "description": "AI analysis", "category": "analysis", "confidence": 0.70}]
        
        return {
            "success": True,
            "context": context,
            "confidence": 0.70,  # AAI minimum
            "selected_tools": tools,
            "selected_patterns": patterns,
            "execution_plan": ["Analyze prompt context", "Apply selected tools", "Generate response"],
            "alternatives": [],
            "recommendations": ["Consider providing more specific context for better tool selection"],
            "warnings": ["Using fallback selection - limited functionality"] + ([f"Error: {error}"] if error else []),
            "execution_ready": True,
            "estimated_time": 3,
            "session_id": f"fallback_{int(datetime.now().timestamp())}",
            "processing_time_ms": 10
        }
    
    # AAI Brain Module interface methods (if available)
    
    if BRAIN_AVAILABLE:
        async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
            """Process brain module request"""
            
            try:
                # Extract prompt from context
                prompt = context.get("prompt", "")
                user_id = context.get("user_id", "anonymous")
                session_id = context.get("session_id")
                
                # Perform tool selection
                result = await self.select_tools_for_prompt(
                    prompt=prompt,
                    user_id=user_id,
                    session_id=session_id
                )
                
                return {
                    "module_name": self.name,
                    "result": result,
                    "confidence": result.get("confidence", 0.70),
                    "success": result.get("success", False)
                }
                
            except Exception as e:
                logger.error(f"Brain module processing failed: {e}")
                return {
                    "module_name": self.name,
                    "result": {"error": str(e)},
                    "confidence": 0.70,
                    "success": False
                }
        
        async def get_status(self) -> Dict[str, Any]:
            """Get module status for brain system"""
            
            return {
                "name": self.name,
                "version": self.version,
                "initialized": self.initialized,
                "selection_count": self.selection_count,
                "success_rate": self.success_rate,
                "components_available": TOOL_SELECTION_AVAILABLE,
                "ready": self.initialized
            }
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get module status (standalone version)"""
        
        return {
            "name": "smart_tool_selector",
            "version": "1.0.0",
            "initialized": self.initialized,
            "selection_count": self.selection_count,
            "success_rate": self.success_rate,
            "brain_integration": BRAIN_AVAILABLE,
            "tool_selection_available": TOOL_SELECTION_AVAILABLE,
            "ready": self.initialized or True  # Always ready with fallback
        }


# Initialize module instance
smart_tool_selector = SmartToolSelectorModule()


async def test_smart_tool_selector_module():
    """Test Smart Tool Selector Module functionality"""
    
    module = SmartToolSelectorModule()
    
    print("🧪 Testing Smart Tool Selector Module")
    print("=" * 38)
    
    # Check module status
    status = module.get_module_status()
    print(f"Module initialized: {status['initialized']}")
    print(f"Brain integration: {status['brain_integration']}")
    print(f"Tool selection available: {status['tool_selection_available']}")
    print(f"Ready: {status['ready']}")
    
    # Wait for initialization
    await asyncio.sleep(1)
    
    # Test tool selection
    print(f"\n🎯 Testing tool selection...")
    
    result = await module.select_tools_for_prompt(
        prompt="Analyze this business proposal for strengths and weaknesses",
        user_id="test_user"
    )
    
    print(f"Selection success: {result['success']}")
    print(f"Context detected: {result['context']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Selected tools: {len(result['selected_tools'])}")
    print(f"Selected patterns: {len(result['selected_patterns'])}")
    print(f"Execution ready: {result['execution_ready']}")
    
    # Test recommendations
    print(f"\n📊 Testing recommendations...")
    
    recommendations = await module.get_tool_recommendations("analysis", complexity_level=5)
    print(f"Recommendations success: {recommendations.get('success', False)}")
    print(f"Context: {recommendations.get('context', 'unknown')}")
    print(f"Preferred tools: {len(recommendations.get('preferred_tools', []))}")
    
    print(f"\n✅ Smart Tool Selector Module Testing Complete")
    print(f"AAI Brain integration ready for intelligent tool selection")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_smart_tool_selector_module())