"""
N8N Integration for Tech Stack Expert Agent

Implements N8N workflow patterns for the tech expert conversation and recommendation
system with state management and automated workflow orchestration.
"""

import logging
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Tech Expert imports
try:
    from agents.tech_expert.conversation_engine import ConversationEngine
    from agents.tech_expert.recommender import TechStackRecommender
    from agents.tech_expert.models import ConversationState, ConversationStage, ProjectRequirements
    TECH_EXPERT_AVAILABLE = True
except ImportError:
    ConversationEngine = None
    TechStackRecommender = None
    TECH_EXPERT_AVAILABLE = False

logger = logging.getLogger(__name__)


class TechExpertWorkflow:
    """
    N8N workflow integration for Tech Stack Expert Agent.
    
    Features:
    - Webhook-based conversation triggers
    - State persistence for multi-step workflows
    - Automated recommendation generation
    - Integration with notification systems
    - Workflow status tracking and monitoring
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize N8N workflow integration"""
        
        self.name = "Tech Expert N8N Workflow"
        self.version = "1.0.0"
        self.webhook_url = webhook_url
        
        # Initialize core components
        self.conversation_engine = ConversationEngine() if TECH_EXPERT_AVAILABLE else None
        self.recommender = TechStackRecommender() if TECH_EXPERT_AVAILABLE else None
        
        # Workflow state management
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.workflow_templates = self._initialize_workflow_templates()
        
        # Performance tracking
        self.total_workflows = 0
        self.completed_workflows = 0
        self.webhook_triggers = 0
        
        # N8N integration settings
        self.n8n_settings = {
            "retry_attempts": 3,
            "timeout_seconds": 30,
            "batch_size": 10,
            "enable_logging": True
        }
        
        logger.info("Tech Expert N8N Workflow initialized")
    
    def _initialize_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize N8N workflow templates"""
        
        return {
            "tech_consultation": {
                "name": "Tech Stack Consultation Workflow",
                "description": "Complete tech stack consultation with guided conversation",
                "trigger": "webhook",
                "nodes": [
                    {
                        "id": "webhook_trigger",
                        "type": "n8n-nodes-base.webhook",
                        "name": "Tech Consultation Request",
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "tech-expert/start",
                            "responseMode": "responseNode"
                        }
                    },
                    {
                        "id": "start_conversation",
                        "type": "n8n-nodes-base.function",
                        "name": "Initialize Conversation",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').startConversationWorkflow($input.all());"
                        }
                    },
                    {
                        "id": "conversation_loop",
                        "type": "n8n-nodes-base.switch",
                        "name": "Conversation State Switch",
                        "parameters": {
                            "conditions": {
                                "boolean": [],
                                "dateTime": [],
                                "number": [],
                                "string": [
                                    {
                                        "value1": "={{$json.conversation_complete}}",
                                        "operation": "equal",
                                        "value2": "false"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "id": "generate_recommendations",
                        "type": "n8n-nodes-base.function",
                        "name": "Generate Tech Recommendations",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').generateRecommendationsWorkflow($input.all());"
                        }
                    },
                    {
                        "id": "send_notification",
                        "type": "n8n-nodes-base.slack",
                        "name": "Send Completion Notification",
                        "parameters": {
                            "channel": "#tech-recommendations",
                            "text": "={{$json.notification_message}}"
                        }
                    }
                ],
                "connections": {
                    "webhook_trigger": {"main": [["start_conversation"]]},
                    "start_conversation": {"main": [["conversation_loop"]]},
                    "conversation_loop": {
                        "main": [
                            ["generate_recommendations"],
                            ["start_conversation"]
                        ]
                    },
                    "generate_recommendations": {"main": [["send_notification"]]}
                }
            },
            
            "quick_recommendation": {
                "name": "Quick Tech Stack Recommendation",
                "description": "Fast recommendation based on minimal input",
                "trigger": "webhook",
                "nodes": [
                    {
                        "id": "webhook_trigger",
                        "type": "n8n-nodes-base.webhook",
                        "name": "Quick Recommendation Request",
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "tech-expert/quick",
                            "responseMode": "responseNode"
                        }
                    },
                    {
                        "id": "parse_requirements",
                        "type": "n8n-nodes-base.function",
                        "name": "Parse Basic Requirements",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').parseQuickRequirements($input.all());"
                        }
                    },
                    {
                        "id": "generate_quick_recs",
                        "type": "n8n-nodes-base.function", 
                        "name": "Generate Quick Recommendations",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').generateQuickRecommendations($input.all());"
                        }
                    },
                    {
                        "id": "format_response",
                        "type": "n8n-nodes-base.function",
                        "name": "Format Response",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').formatQuickResponse($input.all());"
                        }
                    }
                ],
                "connections": {
                    "webhook_trigger": {"main": [["parse_requirements"]]},
                    "parse_requirements": {"main": [["generate_quick_recs"]]},
                    "generate_quick_recs": {"main": [["format_response"]]}
                }
            },
            
            "recommendation_follow_up": {
                "name": "Recommendation Follow-up Workflow",
                "description": "Follow-up workflow for recommendation refinement",
                "trigger": "schedule",
                "nodes": [
                    {
                        "id": "schedule_trigger",
                        "type": "n8n-nodes-base.cron",
                        "name": "Weekly Follow-up Schedule",
                        "parameters": {
                            "cron": "0 10 * * 1"  # Monday 10 AM
                        }
                    },
                    {
                        "id": "check_pending_recommendations",
                        "type": "n8n-nodes-base.function",
                        "name": "Check Pending Recommendations",
                        "parameters": {
                            "functionCode": "return await $('TechExpertWorkflow').checkPendingRecommendations();"
                        }
                    },
                    {
                        "id": "send_follow_up",
                        "type": "n8n-nodes-base.email",
                        "name": "Send Follow-up Email",
                        "parameters": {
                            "subject": "Tech Stack Recommendation Follow-up",
                            "text": "={{$json.follow_up_message}}"
                        }
                    }
                ],
                "connections": {
                    "schedule_trigger": {"main": [["check_pending_recommendations"]]},
                    "check_pending_recommendations": {"main": [["send_follow_up"]]}
                }
            }
        }
    
    async def start_conversation_workflow(self, webhook_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Start a new tech consultation workflow"""
        
        try:
            if not TECH_EXPERT_AVAILABLE:
                return await self._simulate_conversation_workflow(webhook_data)
            
            # Extract user info from webhook
            user_data = webhook_data[0] if webhook_data else {}
            user_id = user_data.get("user_id", "unknown")
            trigger_source = user_data.get("source", "n8n_webhook")
            
            # Start conversation
            session_id, welcome_message = await self.conversation_engine.start_conversation(user_id)
            
            # Create workflow state
            workflow_id = f"workflow_{session_id}"
            self.active_workflows[workflow_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "workflow_type": "tech_consultation",
                "started_at": datetime.now().isoformat(),
                "status": "active",
                "trigger_source": trigger_source,
                "conversation_complete": False,
                "steps_completed": 0,
                "current_stage": welcome_message.stage.value
            }
            
            self.total_workflows += 1
            self.webhook_triggers += 1
            
            logger.info(f"Started tech consultation workflow {workflow_id} for user {user_id}")
            
            return {
                "workflow_id": workflow_id,
                "session_id": session_id,
                "conversation_complete": False,
                "current_message": welcome_message.content,
                "message_options": welcome_message.options,
                "current_stage": welcome_message.stage.value,
                "requires_response": welcome_message.requires_response,
                "webhook_response": {
                    "status": "conversation_started",
                    "next_action": "await_user_response"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to start conversation workflow: {e}")
            return {
                "error": str(e),
                "workflow_id": None,
                "conversation_complete": True,
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to start tech consultation"
                }
            }
    
    async def process_user_response_workflow(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process user response in workflow context"""
        
        try:
            if not TECH_EXPERT_AVAILABLE:
                return await self._simulate_response_workflow(workflow_data)
            
            # Extract workflow info
            request_data = workflow_data[0] if workflow_data else {}
            workflow_id = request_data.get("workflow_id")
            session_id = request_data.get("session_id")
            user_response = request_data.get("user_response", "")
            
            if not workflow_id or workflow_id not in self.active_workflows:
                raise ValueError(f"Invalid workflow ID: {workflow_id}")
            
            # Process response
            next_message = await self.conversation_engine.process_user_response(session_id, user_response)
            
            # Update workflow state
            workflow_state = self.active_workflows[workflow_id]
            workflow_state["steps_completed"] += 1
            workflow_state["current_stage"] = next_message.stage.value
            workflow_state["last_updated"] = datetime.now().isoformat()
            
            # Check if conversation is complete
            conversation_state = self.conversation_engine.get_conversation_state(session_id)
            if conversation_state and conversation_state.is_complete():
                workflow_state["conversation_complete"] = True
                workflow_state["status"] = "ready_for_recommendations"
            
            logger.info(f"Processed response in workflow {workflow_id}, stage: {next_message.stage.value}")
            
            return {
                "workflow_id": workflow_id,
                "session_id": session_id,
                "conversation_complete": workflow_state["conversation_complete"],
                "current_message": next_message.content,
                "message_options": next_message.options,
                "current_stage": next_message.stage.value,
                "requires_response": next_message.requires_response,
                "progress_percentage": conversation_state.get_progress_percentage() if conversation_state else 0,
                "webhook_response": {
                    "status": "response_processed",
                    "next_action": "generate_recommendations" if workflow_state["conversation_complete"] else "await_user_response"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process user response workflow: {e}")
            return {
                "error": str(e),
                "conversation_complete": True,
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to process response"
                }
            }
    
    async def generate_recommendations_workflow(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate tech stack recommendations in workflow context"""
        
        try:
            if not TECH_EXPERT_AVAILABLE:
                return await self._simulate_recommendations_workflow(workflow_data)
            
            # Extract workflow info
            request_data = workflow_data[0] if workflow_data else {}
            workflow_id = request_data.get("workflow_id")
            session_id = request_data.get("session_id")
            
            if not workflow_id or workflow_id not in self.active_workflows:
                raise ValueError(f"Invalid workflow ID: {workflow_id}")
            
            # Get conversation state
            conversation_state = self.conversation_engine.get_conversation_state(session_id)
            if not conversation_state or not conversation_state.requirements:
                raise ValueError("No requirements found for recommendations")
            
            # Generate recommendations
            recommendations = await self.recommender.generate_recommendations(conversation_state.requirements)
            
            # Store recommendations in conversation state
            conversation_state.recommendations = recommendations
            
            # Update workflow state
            workflow_state = self.active_workflows[workflow_id]
            workflow_state["status"] = "recommendations_generated"
            workflow_state["recommendations_generated"] = True
            workflow_state["completed_at"] = datetime.now().isoformat()
            
            self.completed_workflows += 1
            
            # Prepare notification message
            notification_message = await self._create_notification_message(
                workflow_state["user_id"], 
                recommendations,
                conversation_state.requirements
            )
            
            # Prepare summary for webhook response
            recommendation_summary = {
                "architecture_pattern": recommendations.architecture_pattern,
                "total_recommendations": len(recommendations.recommendations),
                "overall_confidence": recommendations.overall_confidence,
                "cost_estimate": recommendations.total_cost_estimate,
                "timeline": recommendations.development_timeline,
                "technologies": [
                    {
                        "category": rec.component.value,
                        "technology": rec.technology,
                        "confidence": rec.confidence,
                        "rationale": rec.rationale[:100] + "..."
                    }
                    for rec in recommendations.recommendations
                ]
            }
            
            logger.info(f"Generated recommendations for workflow {workflow_id} with {recommendations.overall_confidence:.1%} confidence")
            
            return {
                "workflow_id": workflow_id,
                "session_id": session_id,
                "recommendations_generated": True,
                "recommendation_summary": recommendation_summary,
                "notification_message": notification_message,
                "webhook_response": {
                    "status": "recommendations_complete",
                    "next_action": "send_notification"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations workflow: {e}")
            return {
                "error": str(e),
                "recommendations_generated": False,
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to generate recommendations"
                }
            }
    
    async def parse_quick_requirements(self, webhook_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse requirements for quick recommendation workflow"""
        
        try:
            # Extract quick requirements from webhook
            request_data = webhook_data[0] if webhook_data else {}
            
            # Create basic requirements from input
            app_type = request_data.get("app_type", "web_app")
            scale = request_data.get("scale", "medium")
            ai_needed = request_data.get("ai_integration", False)
            team_experience = request_data.get("team_experience", "intermediate")
            
            # Map to our enums
            from agents.tech_expert.models import ApplicationType, UserScale, ExperienceLevel
            
            app_type_mapping = {
                "web_app": ApplicationType.WEB_APP,
                "mobile_app": ApplicationType.MOBILE_APP,
                "api_service": ApplicationType.API_SERVICE,
                "ai_service": ApplicationType.AI_SERVICE
            }
            
            scale_mapping = {
                "prototype": UserScale.PROTOTYPE,
                "small": UserScale.SMALL,
                "medium": UserScale.MEDIUM,
                "large": UserScale.LARGE,
                "enterprise": UserScale.ENTERPRISE
            }
            
            experience_mapping = {
                "beginner": ExperienceLevel.BEGINNER,
                "intermediate": ExperienceLevel.INTERMEDIATE,
                "advanced": ExperienceLevel.ADVANCED,
                "expert": ExperienceLevel.EXPERT
            }
            
            # Create requirements object
            requirements = ProjectRequirements(
                application_type=app_type_mapping.get(app_type, ApplicationType.WEB_APP),
                user_scale=scale_mapping.get(scale, UserScale.MEDIUM),
                ai_integration=bool(ai_needed),
                user_experience={
                    "frontend": experience_mapping.get(team_experience, ExperienceLevel.INTERMEDIATE),
                    "backend": experience_mapping.get(team_experience, ExperienceLevel.INTERMEDIATE),
                    "database": experience_mapping.get(team_experience, ExperienceLevel.INTERMEDIATE)
                }
            )
            
            return {
                "requirements_parsed": True,
                "requirements": requirements.dict(),
                "quick_mode": True,
                "webhook_response": {
                    "status": "requirements_parsed",
                    "next_action": "generate_recommendations"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to parse quick requirements: {e}")
            return {
                "error": str(e),
                "requirements_parsed": False,
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to parse requirements"
                }
            }
    
    async def generate_quick_recommendations(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate quick recommendations from parsed requirements"""
        
        try:
            if not TECH_EXPERT_AVAILABLE:
                return await self._simulate_quick_recommendations(workflow_data)
            
            # Extract requirements
            request_data = workflow_data[0] if workflow_data else {}
            requirements_dict = request_data.get("requirements", {})
            
            # Reconstruct requirements object
            from agents.tech_expert.models import ProjectRequirements
            requirements = ProjectRequirements(**requirements_dict)
            
            # Generate recommendations
            recommendations = await self.recommender.generate_recommendations(requirements)
            
            return {
                "quick_recommendations_generated": True,
                "recommendations": recommendations.dict(),
                "webhook_response": {
                    "status": "quick_recommendations_complete",
                    "next_action": "format_response"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate quick recommendations: {e}")
            return {
                "error": str(e),
                "quick_recommendations_generated": False,
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to generate quick recommendations"
                }
            }
    
    async def format_quick_response(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format quick recommendation response"""
        
        try:
            # Extract recommendations
            request_data = workflow_data[0] if workflow_data else {}
            recommendations_dict = request_data.get("recommendations", {})
            
            # Format for API response
            formatted_response = {
                "quick_recommendation": True,
                "architecture_pattern": recommendations_dict.get("architecture_pattern"),
                "overall_confidence": recommendations_dict.get("overall_confidence"),
                "technologies": [],
                "summary": {
                    "cost_estimate": recommendations_dict.get("total_cost_estimate"),
                    "development_timeline": recommendations_dict.get("development_timeline"),
                    "next_steps": recommendations_dict.get("next_steps", [])[:3]  # Top 3 steps
                }
            }
            
            # Extract technology recommendations
            for rec in recommendations_dict.get("recommendations", []):
                formatted_response["technologies"].append({
                    "category": rec.get("component"),
                    "technology": rec.get("technology"),
                    "confidence": rec.get("confidence"),
                    "rationale": rec.get("rationale", "")[:200] + "...",  # Truncated rationale
                    "pros": rec.get("pros", [])[:2],  # Top 2 pros
                    "alternatives": rec.get("alternatives", [])[:2]  # Top 2 alternatives
                })
            
            return {
                "formatted_response": formatted_response,
                "webhook_response": {
                    "status": "success",
                    "data": formatted_response
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to format quick response: {e}")
            return {
                "error": str(e),
                "webhook_response": {
                    "status": "error",
                    "message": "Failed to format response"
                }
            }
    
    async def check_pending_recommendations(self) -> Dict[str, Any]:
        """Check for pending recommendation follow-ups"""
        
        try:
            pending_workflows = []
            
            # Check active workflows that might need follow-up
            for workflow_id, workflow_state in self.active_workflows.items():
                if workflow_state.get("status") == "recommendations_generated":
                    # Check if it's been a week since completion
                    completed_at = datetime.fromisoformat(workflow_state.get("completed_at", datetime.now().isoformat()))
                    days_since_completion = (datetime.now() - completed_at).days
                    
                    if days_since_completion >= 7:  # Follow-up after a week
                        pending_workflows.append({
                            "workflow_id": workflow_id,
                            "user_id": workflow_state["user_id"],
                            "days_since_completion": days_since_completion
                        })
            
            if pending_workflows:
                follow_up_message = f"Found {len(pending_workflows)} tech stack recommendations ready for follow-up. Users: {', '.join([w['user_id'] for w in pending_workflows])}"
            else:
                follow_up_message = "No pending tech stack recommendations require follow-up at this time."
            
            return {
                "pending_count": len(pending_workflows),
                "pending_workflows": pending_workflows,
                "follow_up_message": follow_up_message,
                "check_completed": True
            }
            
        except Exception as e:
            logger.error(f"Failed to check pending recommendations: {e}")
            return {
                "error": str(e),
                "pending_count": 0,
                "follow_up_message": "Error checking pending recommendations"
            }
    
    async def _create_notification_message(self, user_id: str, recommendations, requirements) -> str:
        """Create notification message for completed recommendations"""
        
        tech_list = ", ".join([rec.technology for rec in recommendations.recommendations])
        
        message = f"""🎯 Tech Stack Consultation Complete for {user_id}

📋 **Project:** {requirements.application_type.value} at {requirements.user_scale.value} scale
🏗️ **Architecture:** {recommendations.architecture_pattern}
🔧 **Technologies:** {tech_list}
💰 **Cost Estimate:** {recommendations.total_cost_estimate}
⏱️ **Timeline:** {recommendations.development_timeline}
🎯 **Confidence:** {recommendations.overall_confidence:.1%}

Next steps: Implementation planning and environment setup"""
        
        return message
    
    # Simulation methods for when tech expert components aren't available
    
    async def _simulate_conversation_workflow(self, webhook_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate conversation workflow for testing"""
        
        session_id = f"sim_session_{datetime.now().timestamp()}"
        workflow_id = f"workflow_{session_id}"
        
        self.active_workflows[workflow_id] = {
            "session_id": session_id,
            "user_id": "test_user",
            "workflow_type": "tech_consultation",
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "conversation_complete": False,
            "simulated": True
        }
        
        return {
            "workflow_id": workflow_id,
            "session_id": session_id,
            "conversation_complete": False,
            "current_message": "Welcome to the Tech Stack Expert! What type of application are you building?",
            "message_options": ["Web App", "Mobile App", "API Service", "AI Service"],
            "current_stage": "app_type",
            "requires_response": True,
            "simulated": True,
            "webhook_response": {
                "status": "conversation_started",
                "next_action": "await_user_response"
            }
        }
    
    async def _simulate_response_workflow(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate response processing for testing"""
        
        await asyncio.sleep(0.1)  # Simulate processing
        
        return {
            "workflow_id": "sim_workflow",
            "conversation_complete": True,
            "current_message": "Thank you! I have enough information to generate your recommendations.",
            "simulated": True,
            "webhook_response": {
                "status": "response_processed",
                "next_action": "generate_recommendations"
            }
        }
    
    async def _simulate_recommendations_workflow(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate recommendations generation for testing"""
        
        await asyncio.sleep(0.2)  # Simulate processing
        
        return {
            "workflow_id": "sim_workflow",
            "recommendations_generated": True,
            "recommendation_summary": {
                "architecture_pattern": "Modern Full-Stack Architecture",
                "total_recommendations": 4,
                "overall_confidence": 0.85,
                "technologies": [
                    {"category": "frontend", "technology": "React.js", "confidence": 0.9},
                    {"category": "backend", "technology": "Node.js", "confidence": 0.8},
                    {"category": "database", "technology": "PostgreSQL", "confidence": 0.85},
                    {"category": "deployment", "technology": "Docker", "confidence": 0.8}
                ]
            },
            "notification_message": "🎯 Tech Stack recommendations generated with 85% confidence!",
            "simulated": True,
            "webhook_response": {
                "status": "recommendations_complete",
                "next_action": "send_notification"
            }
        }
    
    async def _simulate_quick_recommendations(self, workflow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate quick recommendations for testing"""
        
        await asyncio.sleep(0.1)
        
        return {
            "quick_recommendations_generated": True,
            "recommendations": {
                "architecture_pattern": "JAMstack Architecture",
                "overall_confidence": 0.8,
                "total_cost_estimate": "$500-2000/month",
                "development_timeline": "2-3 months",
                "recommendations": [
                    {
                        "component": "frontend",
                        "technology": "React.js",
                        "confidence": 0.85,
                        "rationale": "Perfect for your web application with good scalability.",
                        "pros": ["Large ecosystem", "Component reusability"],
                        "alternatives": ["Vue.js", "Angular"]
                    }
                ]
            },
            "simulated": True,
            "webhook_response": {
                "status": "quick_recommendations_complete",
                "next_action": "format_response"
            }
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow"""
        
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow_state = self.active_workflows[workflow_id]
        
        # Calculate duration
        started_at = datetime.fromisoformat(workflow_state["started_at"])
        duration_minutes = (datetime.now() - started_at).total_seconds() / 60
        
        return {
            "workflow_id": workflow_id,
            "status": workflow_state["status"],
            "type": workflow_state["workflow_type"],
            "user_id": workflow_state["user_id"],
            "duration_minutes": duration_minutes,
            "steps_completed": workflow_state.get("steps_completed", 0),
            "conversation_complete": workflow_state.get("conversation_complete", False),
            "recommendations_generated": workflow_state.get("recommendations_generated", False)
        }
    
    def get_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available N8N workflow templates"""
        return self.workflow_templates
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get N8N integration status and metrics"""
        
        completion_rate = (
            self.completed_workflows / max(1, self.total_workflows)
        )
        
        return {
            "name": self.name,
            "version": self.version,
            "tech_expert_available": TECH_EXPERT_AVAILABLE,
            "webhook_url": self.webhook_url,
            "active_workflows": len(self.active_workflows),
            "total_workflows": self.total_workflows,
            "completed_workflows": self.completed_workflows,
            "completion_rate": completion_rate,
            "webhook_triggers": self.webhook_triggers,
            "workflow_templates": len(self.workflow_templates),
            "n8n_settings": self.n8n_settings
        }


async def test_tech_expert_workflow():
    """Test tech expert N8N workflow functionality"""
    
    workflow = TechExpertWorkflow(webhook_url="https://example.com/webhook")
    
    print("🧪 Testing Tech Expert N8N Workflow")
    print("=" * 35)
    
    # Test workflow templates
    templates = workflow.get_workflow_templates()
    print(f"Available templates: {len(templates)}")
    for name, template in templates.items():
        print(f"  - {template['name']}: {len(template['nodes'])} nodes")
    
    # Test conversation workflow
    print(f"\n🎯 Testing conversation workflow...")
    
    # Start conversation
    webhook_data = [{"user_id": "test_user", "source": "test"}]
    start_result = await workflow.start_conversation_workflow(webhook_data)
    
    print(f"Conversation started: {start_result.get('session_id')}")
    print(f"Current message: {start_result.get('current_message', '')[:50]}...")
    
    # Process response
    if start_result.get("workflow_id"):
        response_data = [{
            "workflow_id": start_result["workflow_id"],
            "session_id": start_result["session_id"],
            "user_response": "Web Application"
        }]
        response_result = await workflow.process_user_response_workflow(response_data)
        print(f"Response processed: {response_result.get('current_stage')}")
    
    # Test quick recommendation workflow
    print(f"\n⚡ Testing quick recommendation workflow...")
    
    quick_data = [{
        "app_type": "web_app",
        "scale": "medium",
        "ai_integration": True,
        "team_experience": "intermediate"
    }]
    
    # Parse requirements
    parse_result = await workflow.parse_quick_requirements(quick_data)
    print(f"Requirements parsed: {parse_result.get('requirements_parsed')}")
    
    # Generate recommendations
    if parse_result.get("requirements_parsed"):
        rec_result = await workflow.generate_quick_recommendations([parse_result])
        print(f"Quick recommendations generated: {rec_result.get('quick_recommendations_generated')}")
        
        # Format response
        if rec_result.get("quick_recommendations_generated"):
            format_result = await workflow.format_quick_response([rec_result])
            formatted = format_result.get("formatted_response", {})
            print(f"Technologies recommended: {len(formatted.get('technologies', []))}")
    
    # Check status
    status = workflow.get_integration_status()
    print(f"\n📊 Integration Status:")
    print(f"Active workflows: {status['active_workflows']}")
    print(f"Total workflows: {status['total_workflows']}")
    print(f"Completion rate: {status['completion_rate']:.1%}")
    print(f"Tech expert available: {status['tech_expert_available']}")
    
    print(f"\n✅ Tech Expert N8N Workflow Testing Complete")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tech_expert_workflow())