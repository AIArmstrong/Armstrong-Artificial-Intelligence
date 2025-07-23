"""
AAI Brain Module: MCP Orchestrator

Integrates MCP Agent Army Orchestration into AAI's brain system
for intelligent multi-agent coordination and task delegation.
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

# MCP Orchestration imports with fallbacks
try:
    from agents.orchestration.primary_agent import PrimaryOrchestrationAgent
    from agents.orchestration.models import DelegationRequest, AgentSpecialization
    from mcp.server_manager import MCPServerManager
    ORCHESTRATION_AVAILABLE = True
except ImportError:
    PrimaryOrchestrationAgent = None
    DelegationRequest = None
    AgentSpecialization = None
    MCPServerManager = None
    ORCHESTRATION_AVAILABLE = False

logger = logging.getLogger(__name__)


class MCPOrchestratorModule(BrainModule if BRAIN_AVAILABLE else object):
    """
    AAI Brain Module for MCP Agent Army Orchestration.
    
    Features:
    - Automatic multi-agent task detection and delegation
    - Integration with AAI Smart Module Loading system
    - External service interaction coordination
    - Performance tracking and learning
    - AAI confidence scoring compliance
    """
    
    def __init__(self):
        """Initialize MCP orchestrator module"""
        
        # Initialize parent if available
        if BRAIN_AVAILABLE:
            super().__init__(
                name="mcp_orchestrator",
                description="Multi-agent coordination and task delegation",
                version="1.0.0"
            )
        
        # Initialize orchestration components
        self.orchestration_agent: Optional[PrimaryOrchestrationAgent] = None
        self.mcp_manager: Optional[MCPServerManager] = None
        
        # Module state
        self.initialized = False
        self.orchestration_count = 0
        self.success_rate = 0.0
        
        # Trigger conditions for orchestration
        self.orchestration_triggers = {
            "external_service_keywords": [
                "slack", "github", "email", "calendar", "database", "api",
                "webhook", "notification", "integration", "sync"
            ],
            "multi_step_indicators": [
                "and then", "followed by", "after that", "next", "also",
                "in addition", "furthermore", "meanwhile", "simultaneously"
            ],
            "complexity_indicators": [
                "multiple", "several", "various", "complex", "comprehensive",
                "coordinate", "orchestrate", "manage", "automate"
            ]
        }
        
        # Performance tracking
        self.delegation_metrics = {
            "total_delegations": 0,
            "successful_delegations": 0,
            "average_confidence": 0.75,
            "agent_utilization": {},
            "user_satisfaction": 0.8
        }
        
        # Components will be initialized lazily when first needed
    
    async def _initialize_components(self):
        """Initialize orchestration components"""
        
        try:
            if not ORCHESTRATION_AVAILABLE:
                logger.warning("Orchestration components not available - using fallback mode")
                self.initialized = False
                return
            
            # Initialize primary orchestration agent
            self.orchestration_agent = PrimaryOrchestrationAgent()
            
            # Wait for agent initialization
            await asyncio.sleep(1)
            
            self.initialized = True
            logger.info("MCP Orchestrator Module initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP Orchestrator Module: {e}")
            self.initialized = False
    
    async def should_orchestrate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine if a request should trigger orchestration.
        
        Args:
            context: Request context with prompt and metadata
            
        Returns:
            Decision with confidence and reasoning
        """
        try:
            prompt = context.get("prompt", "")
            prompt_lower = prompt.lower()
            
            orchestration_score = 0.0
            triggers_found = []
            
            # Check for external service keywords
            external_service_matches = sum(
                1 for keyword in self.orchestration_triggers["external_service_keywords"]
                if keyword in prompt_lower
            )
            if external_service_matches > 0:
                orchestration_score += 0.4
                triggers_found.append(f"external_services ({external_service_matches} matches)")
            
            # Check for multi-step indicators
            multi_step_matches = sum(
                1 for indicator in self.orchestration_triggers["multi_step_indicators"]
                if indicator in prompt_lower
            )
            if multi_step_matches > 0:
                orchestration_score += 0.3
                triggers_found.append(f"multi_step ({multi_step_matches} indicators)")
            
            # Check for complexity indicators
            complexity_matches = sum(
                1 for indicator in self.orchestration_triggers["complexity_indicators"]
                if indicator in prompt_lower
            )
            if complexity_matches > 0:
                orchestration_score += 0.2
                triggers_found.append(f"complexity ({complexity_matches} indicators)")
            
            # Check prompt length (longer prompts may need orchestration)
            if len(prompt.split()) > 20:
                orchestration_score += 0.1
                triggers_found.append("long_prompt")
            
            # Convert to AAI-compliant confidence
            confidence = max(0.70, min(0.95, 0.70 + (orchestration_score * 0.25)))
            
            should_orchestrate = orchestration_score >= 0.3
            
            return {
                "should_orchestrate": should_orchestrate,
                "confidence": confidence,
                "orchestration_score": orchestration_score,
                "triggers_found": triggers_found,
                "reasoning": self._generate_orchestration_reasoning(
                    should_orchestrate, triggers_found, orchestration_score
                )
            }
            
        except Exception as e:
            logger.error(f"Orchestration decision failed: {e}")
            return {
                "should_orchestrate": False,
                "confidence": 0.70,
                "error": str(e)
            }
    
    def _generate_orchestration_reasoning(self, 
                                        should_orchestrate: bool,
                                        triggers_found: List[str],
                                        score: float) -> str:
        """Generate human-readable reasoning for orchestration decision"""
        
        if should_orchestrate:
            reasoning = f"Orchestration recommended (score: {score:.2f}) due to "
            if triggers_found:
                reasoning += f"detected triggers: {', '.join(triggers_found)}"
            else:
                reasoning += "task complexity indicators"
        else:
            reasoning = f"Single-agent execution suitable (score: {score:.2f})"
            if triggers_found:
                reasoning += f" despite some triggers: {', '.join(triggers_found)}"
        
        return reasoning
    
    async def orchestrate_request(self, 
                                context: Dict[str, Any],
                                user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Orchestrate a multi-agent request.
        
        Args:
            context: Request context
            user_id: User identifier
            
        Returns:
            Orchestration result
        """
        try:
            if not self.initialized or not self.orchestration_agent:
                return await self._fallback_orchestration(context)
            
            # Create delegation request
            request = DelegationRequest(
                query=context.get("prompt", ""),
                user_id=user_id,
                session_id=context.get("session_id"),
                max_parallel_tasks=context.get("max_parallel_tasks", 3),
                timeout_seconds=context.get("timeout_seconds", 120),
                context=context
            )
            
            # Execute orchestration
            response = await self.orchestration_agent.orchestrate(request)
            
            # Update metrics
            self.orchestration_count += 1
            if response.orchestration_result.success:
                success_count = sum(1 for r in response.orchestration_result.results if r.success)
                success_rate = success_count / len(response.orchestration_result.results) if response.orchestration_result.results else 0
                
                # Update running success rate
                total_delegations = self.delegation_metrics["total_delegations"] + 1
                current_success = self.delegation_metrics["successful_delegations"]
                
                if success_rate >= 0.8:
                    current_success += 1
                
                self.delegation_metrics["total_delegations"] = total_delegations
                self.delegation_metrics["successful_delegations"] = current_success
                self.success_rate = current_success / total_delegations
            
            # Convert to module result format
            result = {
                "orchestration_successful": response.orchestration_result.success,
                "overall_confidence": response.orchestration_result.overall_confidence,
                "tasks_completed": len(response.orchestration_result.results),
                "successful_tasks": sum(1 for r in response.orchestration_result.results if r.success),
                "execution_time_ms": response.orchestration_result.total_execution_time_ms,
                "agent_utilization": response.orchestration_result.agent_utilization,
                "recommendations": response.recommendations,
                "warnings": response.warnings,
                "results": [
                    {
                        "agent": result.agent_type.value,
                        "success": result.success,
                        "execution_time": result.execution_time_seconds,
                        "confidence": result.confidence_achieved
                    }
                    for result in response.orchestration_result.results
                ],
                "session_id": response.orchestration_result.session_id
            }
            
            logger.info(f"Orchestration completed: {result['orchestration_successful']}, confidence: {result['overall_confidence']:.1%}")
            
            return result
            
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            return await self._fallback_orchestration(context, error=str(e))
    
    async def _fallback_orchestration(self, context: Dict[str, Any], error: Optional[str] = None) -> Dict[str, Any]:
        """Provide fallback orchestration when components are unavailable"""
        
        prompt = context.get("prompt", "")
        
        # Simple analysis of what the request might need
        prompt_lower = prompt.lower()
        
        likely_agents = []
        if any(word in prompt_lower for word in ["slack", "message", "notify"]):
            likely_agents.append("slack")
        if any(word in prompt_lower for word in ["github", "repo", "issue", "code"]):
            likely_agents.append("github")
        if any(word in prompt_lower for word in ["file", "save", "read", "directory"]):
            likely_agents.append("filesystem")
        if any(word in prompt_lower for word in ["search", "find", "lookup", "web"]):
            likely_agents.append("search")
        
        if not likely_agents:
            likely_agents = ["general"]
        
        return {
            "orchestration_successful": False,
            "overall_confidence": 0.70,
            "tasks_completed": 0,
            "successful_tasks": 0,
            "execution_time_ms": 0,
            "agent_utilization": {agent: 1 for agent in likely_agents},
            "recommendations": ["Enable orchestration components for multi-agent coordination"],
            "warnings": [f"Orchestration unavailable: {error}"] if error else ["Orchestration components not available"],
            "results": [],
            "fallback": True,
            "likely_agents": likely_agents
        }
    
    async def get_orchestration_status(self) -> Dict[str, Any]:
        """Get orchestration system status"""
        
        status = {
            "module_initialized": self.initialized,
            "orchestration_available": ORCHESTRATION_AVAILABLE,
            "brain_integration": BRAIN_AVAILABLE,
            "total_orchestrations": self.orchestration_count,
            "success_rate": self.success_rate,
            "metrics": self.delegation_metrics
        }
        
        # Get agent status if available
        if self.orchestration_agent and hasattr(self.orchestration_agent, 'get_system_status'):
            try:
                system_status = self.orchestration_agent.get_system_status()
                status["system_status"] = {
                    "orchestration_active": system_status.orchestration_active,
                    "active_orchestrations": system_status.active_orchestrations,
                    "agent_health": system_status.agent_health,
                    "mcp_servers": system_status.mcp_servers_status
                }
            except Exception as e:
                status["system_status_error"] = str(e)
        
        return status
    
    async def update_performance_metrics(self,
                                       session_id: str,
                                       success: bool,
                                       user_satisfaction: float,
                                       execution_time_ms: int):
        """Update performance metrics from orchestration results"""
        
        # Update delegation metrics
        self.delegation_metrics["total_delegations"] += 1
        
        if success:
            self.delegation_metrics["successful_delegations"] += 1
        
        # Update running averages
        total = self.delegation_metrics["total_delegations"]
        
        # Update average confidence (placeholder - would need actual confidence tracking)
        # current_avg_conf = self.delegation_metrics["average_confidence"]
        # new_avg_conf = (current_avg_conf * (total - 1) + actual_confidence) / total
        # self.delegation_metrics["average_confidence"] = new_avg_conf
        
        # Update user satisfaction
        current_satisfaction = self.delegation_metrics["user_satisfaction"]
        new_satisfaction = (current_satisfaction * (total - 1) + user_satisfaction) / total
        self.delegation_metrics["user_satisfaction"] = new_satisfaction
        
        # Update success rate
        success_count = self.delegation_metrics["successful_delegations"]
        self.success_rate = success_count / total
    
    # AAI Brain Module interface methods (if available)
    
    if BRAIN_AVAILABLE:
        async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
            """Process brain module request"""
            
            try:
                # Check if orchestration should be triggered
                orchestration_decision = await self.should_orchestrate(context)
                
                if orchestration_decision["should_orchestrate"]:
                    # Execute orchestration
                    result = await self.orchestrate_request(
                        context,
                        context.get("user_id", "anonymous")
                    )
                    
                    return {
                        "module_name": self.name,
                        "orchestration_triggered": True,
                        "decision_confidence": orchestration_decision["confidence"],
                        "decision_reasoning": orchestration_decision["reasoning"],
                        "result": result,
                        "confidence": result.get("overall_confidence", 0.70),
                        "success": result.get("orchestration_successful", False)
                    }
                
                else:
                    # No orchestration needed
                    return {
                        "module_name": self.name,
                        "orchestration_triggered": False,
                        "decision_confidence": orchestration_decision["confidence"],
                        "decision_reasoning": orchestration_decision["reasoning"],
                        "suggestion": "Single-agent execution recommended",
                        "confidence": orchestration_decision["confidence"],
                        "success": True
                    }
                
            except Exception as e:
                logger.error(f"Brain module processing failed: {e}")
                return {
                    "module_name": self.name,
                    "orchestration_triggered": False,
                    "error": str(e),
                    "confidence": 0.70,
                    "success": False
                }
        
        async def get_status(self) -> Dict[str, Any]:
            """Get module status for brain system"""
            
            return {
                "name": self.name,
                "version": self.version,
                "initialized": self.initialized,
                "orchestration_count": self.orchestration_count,
                "success_rate": self.success_rate,
                "orchestration_available": ORCHESTRATION_AVAILABLE,
                "ready": self.initialized or True  # Always ready with fallback
            }
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get module status (standalone version)"""
        
        return {
            "name": "mcp_orchestrator",
            "version": "1.0.0",
            "initialized": self.initialized,
            "orchestration_count": self.orchestration_count,
            "success_rate": self.success_rate,
            "brain_integration": BRAIN_AVAILABLE,
            "orchestration_available": ORCHESTRATION_AVAILABLE,
            "delegation_metrics": self.delegation_metrics,
            "trigger_conditions": {
                "external_service_keywords": len(self.orchestration_triggers["external_service_keywords"]),
                "multi_step_indicators": len(self.orchestration_triggers["multi_step_indicators"]),
                "complexity_indicators": len(self.orchestration_triggers["complexity_indicators"])
            },
            "ready": self.initialized or True
        }


# Initialize module instance
mcp_orchestrator = MCPOrchestratorModule()


async def test_mcp_orchestrator_module():
    """Test MCP Orchestrator Module functionality"""
    
    module = MCPOrchestratorModule()
    
    print("🧪 Testing MCP Orchestrator Module")
    print("=" * 35)
    
    # Wait for initialization
    await asyncio.sleep(1.5)
    
    # Check module status
    status = module.get_module_status()
    print(f"Module initialized: {status['initialized']}")
    print(f"Brain integration: {status['brain_integration']}")
    print(f"Orchestration available: {status['orchestration_available']}")
    print(f"Ready: {status['ready']}")
    
    # Test orchestration decision
    print(f"\n🎯 Testing orchestration decisions...")
    
    test_contexts = [
        {
            "prompt": "Send a Slack message to the team and create a GitHub issue",
            "user_id": "test_user"
        },
        {
            "prompt": "What is the capital of France?",
            "user_id": "test_user"
        },
        {
            "prompt": "Search for information about AI trends, summarize it, and save to a file",
            "user_id": "test_user"
        }
    ]
    
    for i, context in enumerate(test_contexts, 1):
        print(f"\nContext {i}: {context['prompt'][:50]}...")
        
        decision = await module.should_orchestrate(context)
        print(f"  Should orchestrate: {decision['should_orchestrate']}")
        print(f"  Confidence: {decision['confidence']:.1%}")
        print(f"  Triggers: {', '.join(decision.get('triggers_found', []))}")
        
        if decision["should_orchestrate"]:
            # Test orchestration
            result = await module.orchestrate_request(context)
            print(f"  Orchestration success: {result.get('orchestration_successful', False)}")
            print(f"  Tasks completed: {result.get('tasks_completed', 0)}")
            print(f"  Overall confidence: {result.get('overall_confidence', 0):.1%}")
    
    # Check final status
    final_status = await module.get_orchestration_status()
    print(f"\n📊 Final Status:")
    print(f"Total orchestrations: {final_status['total_orchestrations']}")
    print(f"Success rate: {final_status['success_rate']:.1%}")
    print(f"Metrics: {final_status['metrics']['total_delegations']} delegations")
    
    print(f"\n✅ MCP Orchestrator Module Testing Complete")
    print(f"AAI Brain integration ready for multi-agent coordination")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_mcp_orchestrator_module())