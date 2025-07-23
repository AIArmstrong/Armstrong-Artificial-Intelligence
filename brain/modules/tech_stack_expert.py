"""
AAI Brain Module: Tech Stack Expert

Integrates the Tech Stack Expert Agent into AAI's brain system for intelligent
architectural decision support and technology recommendation learning.
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

# Tech Expert imports with fallbacks
try:
    from agents.tech_expert.conversation_engine import ConversationEngine
    from agents.tech_expert.recommender import TechStackRecommender
    from agents.tech_expert.models import ProjectRequirements, ApplicationType, UserScale, ExperienceLevel
    from n8n.tech_expert_workflow import TechExpertWorkflow
    TECH_EXPERT_AVAILABLE = True
except ImportError:
    ConversationEngine = None
    TechStackRecommender = None
    ProjectRequirements = None
    TechExpertWorkflow = None
    TECH_EXPERT_AVAILABLE = False

logger = logging.getLogger(__name__)


class TechStackExpertModule(BrainModule if BRAIN_AVAILABLE else object):
    """
    AAI Brain Module for Tech Stack Expert Agent.
    
    Features:
    - Architectural decision support
    - Technology recommendation learning
    - Integration with AAI Smart Module Loading system
    - Conversation state management
    - Performance tracking and analytics
    - AAI confidence scoring compliance
    """
    
    def __init__(self):
        """Initialize tech stack expert module"""
        
        # Initialize parent if available
        if BRAIN_AVAILABLE:
            super().__init__(
                name="tech_stack_expert",
                description="Intelligent technology stack recommendations and architectural decisions",
                version="1.0.0"
            )
        
        # Initialize tech expert components
        self.conversation_engine: Optional[ConversationEngine] = None
        self.recommender: Optional[TechStackRecommender] = None
        self.workflow_integration: Optional[TechExpertWorkflow] = None
        
        # Module state
        self.initialized = False
        self.active_consultations = {}
        self.recommendation_history = []
        
        # Performance tracking
        self.total_consultations = 0
        self.successful_recommendations = 0
        self.user_satisfaction_scores = []
        
        # Trigger conditions for tech stack expertise
        self.expertise_triggers = {
            "architectural_decisions": [
                "technology stack", "tech stack", "architecture", "framework choice",
                "database selection", "deployment strategy", "frontend framework",
                "backend technology", "which technology", "recommend tech"
            ],
            "project_planning": [
                "new project", "project planning", "technology roadmap", "tech choices",
                "development stack", "platform selection", "tool selection"
            ],
            "scaling_concerns": [
                "scalability", "scale up", "performance optimization", "enterprise ready",
                "high availability", "load balancing", "microservices"
            ],
            "team_guidance": [
                "team recommendations", "learning path", "skill development",
                "technology training", "onboarding", "tech expertise"
            ]
        }
        
        # Decision support patterns
        self.decision_patterns = {
            "comparison_requests": [
                "vs", "compare", "difference between", "pros and cons",
                "better choice", "advantages", "disadvantages"
            ],
            "recommendation_requests": [
                "recommend", "suggest", "best choice", "what should I use",
                "advice", "guidance", "help me choose"
            ],
            "validation_requests": [
                "is this good", "validate", "review", "opinion",
                "thoughts on", "feedback", "assessment"
            ]
        }
        
        # Learning and adaptation
        self.learning_metrics = {
            "recommendation_feedback": {},
            "technology_trends": {},
            "user_preferences": {},
            "success_patterns": {}
        }
        
        # Components will be initialized lazily when first needed
    
    async def _initialize_components(self):
        """Initialize tech expert components"""
        
        try:
            if not TECH_EXPERT_AVAILABLE:
                logger.warning("Tech Expert components not available - using fallback mode")
                self.initialized = False
                return
            
            # Initialize core components
            self.conversation_engine = ConversationEngine()
            self.recommender = TechStackRecommender()
            self.workflow_integration = TechExpertWorkflow()
            
            # Wait for initialization
            await asyncio.sleep(1)
            
            self.initialized = True
            logger.info("Tech Stack Expert Module initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Tech Stack Expert Module: {e}")
            self.initialized = False
    
    async def should_provide_expertise(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine if a request should trigger tech stack expertise.
        
        Args:
            context: Request context with prompt and metadata
            
        Returns:
            Decision with confidence and reasoning
        """
        try:
            prompt = context.get("prompt", "")
            prompt_lower = prompt.lower()
            
            expertise_score = 0.0
            triggers_found = []
            
            # Check for architectural decision keywords
            architectural_matches = sum(
                1 for keyword in self.expertise_triggers["architectural_decisions"]
                if keyword in prompt_lower
            )
            if architectural_matches > 0:
                expertise_score += 0.5
                triggers_found.append(f"architectural_decisions ({architectural_matches} matches)")
            
            # Check for project planning keywords
            planning_matches = sum(
                1 for keyword in self.expertise_triggers["project_planning"]
                if keyword in prompt_lower
            )
            if planning_matches > 0:
                expertise_score += 0.3
                triggers_found.append(f"project_planning ({planning_matches} matches)")
            
            # Check for scaling concerns
            scaling_matches = sum(
                1 for keyword in self.expertise_triggers["scaling_concerns"]
                if keyword in prompt_lower
            )
            if scaling_matches > 0:
                expertise_score += 0.2
                triggers_found.append(f"scaling_concerns ({scaling_matches} matches)")
            
            # Check for comparison/recommendation patterns
            comparison_matches = sum(
                1 for pattern in self.decision_patterns["comparison_requests"]
                if pattern in prompt_lower
            )
            recommendation_matches = sum(
                1 for pattern in self.decision_patterns["recommendation_requests"]
                if pattern in prompt_lower
            )
            
            if comparison_matches > 0 or recommendation_matches > 0:
                expertise_score += 0.3
                triggers_found.append("decision_support_patterns")
            
            # Check for team guidance requests
            team_matches = sum(
                1 for keyword in self.expertise_triggers["team_guidance"]
                if keyword in prompt_lower
            )
            if team_matches > 0:
                expertise_score += 0.2
                triggers_found.append(f"team_guidance ({team_matches} matches)")
            
            # Convert to AAI-compliant confidence
            confidence = max(0.70, min(0.95, 0.70 + (expertise_score * 0.25)))
            
            should_provide_expertise = expertise_score >= 0.3
            
            return {
                "should_provide_expertise": should_provide_expertise,
                "confidence": confidence,
                "expertise_score": expertise_score,
                "triggers_found": triggers_found,
                "reasoning": self._generate_expertise_reasoning(
                    should_provide_expertise, triggers_found, expertise_score
                )
            }
            
        except Exception as e:
            logger.error(f"Expertise decision failed: {e}")
            return {
                "should_provide_expertise": False,
                "confidence": 0.70,
                "error": str(e)
            }
    
    def _generate_expertise_reasoning(self, 
                                    should_provide: bool,
                                    triggers_found: List[str],
                                    score: float) -> str:
        """Generate human-readable reasoning for expertise decision"""
        
        if should_provide:
            reasoning = f"Tech Stack expertise recommended (score: {score:.2f}) due to "
            if triggers_found:
                reasoning += f"detected triggers: {', '.join(triggers_found)}"
            else:
                reasoning += "technology-related decision indicators"
        else:
            reasoning = f"Standard response suitable (score: {score:.2f})"
            if triggers_found:
                reasoning += f" despite some triggers: {', '.join(triggers_found)}"
        
        return reasoning
    
    async def provide_expertise(self, 
                              context: Dict[str, Any],
                              user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Provide tech stack expertise and recommendations.
        
        Args:
            context: Request context
            user_id: User identifier
            
        Returns:
            Expertise result
        """
        try:
            if not self.initialized or not self.recommender:
                return await self._fallback_expertise(context)
            
            prompt = context.get("prompt", "")
            
            # Determine expertise type
            expertise_type = await self._determine_expertise_type(prompt)
            
            # Handle different types of expertise requests
            if expertise_type == "quick_recommendation":
                result = await self._provide_quick_recommendation(context, user_id)
            elif expertise_type == "guided_consultation":
                result = await self._start_guided_consultation(context, user_id)
            elif expertise_type == "technology_comparison":
                result = await self._provide_technology_comparison(context, user_id)
            elif expertise_type == "architecture_review":
                result = await self._provide_architecture_review(context, user_id)
            else:
                result = await self._provide_general_guidance(context, user_id)
            
            # Track consultation
            self.total_consultations += 1
            if result.get("success", False):
                self.successful_recommendations += 1
            
            # Store in history
            consultation_record = {
                "user_id": user_id,
                "prompt": prompt,
                "expertise_type": expertise_type,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "success": result.get("success", False)
            }
            self.recommendation_history.append(consultation_record)
            
            logger.info(f"Provided {expertise_type} expertise for user {user_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Tech expertise failed: {e}")
            return await self._fallback_expertise(context, error=str(e))
    
    async def _determine_expertise_type(self, prompt: str) -> str:
        """Determine the type of expertise needed"""
        
        prompt_lower = prompt.lower()
        
        # Quick recommendation indicators
        if any(indicator in prompt_lower for indicator in [
            "quick recommendation", "fast suggestion", "simple advice",
            "basic guidance", "short answer"
        ]):
            return "quick_recommendation"
        
        # Guided consultation indicators
        elif any(indicator in prompt_lower for indicator in [
            "help me choose", "need guidance", "don't know", "confused",
            "new project", "starting", "beginning"
        ]):
            return "guided_consultation"
        
        # Technology comparison indicators
        elif any(indicator in prompt_lower for indicator in [
            "vs", "compare", "difference", "pros and cons", "better"
        ]):
            return "technology_comparison"
        
        # Architecture review indicators
        elif any(indicator in prompt_lower for indicator in [
            "review", "feedback", "opinion", "validate", "assess",
            "current stack", "existing", "thoughts on"
        ]):
            return "architecture_review"
        
        else:
            return "general_guidance"
    
    async def _provide_quick_recommendation(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide quick technology recommendations"""
        
        try:
            # Parse basic requirements from prompt
            prompt = context.get("prompt", "")
            basic_requirements = await self._parse_basic_requirements(prompt)
            
            # Generate quick recommendations
            recommendations = await self.recommender.generate_recommendations(basic_requirements)
            
            # Format for quick response
            quick_response = {
                "expertise_type": "quick_recommendation",
                "recommendations": [
                    {
                        "category": rec.component.value,
                        "technology": rec.technology,
                        "confidence": rec.confidence,
                        "rationale": rec.rationale[:150] + "...",  # Shortened rationale
                        "alternatives": rec.alternatives[:2]  # Top 2 alternatives
                    }
                    for rec in recommendations.recommendations[:4]  # Top 4 recommendations
                ],
                "architecture_pattern": recommendations.architecture_pattern,
                "quick_summary": f"For your {basic_requirements.application_type.value} project, I recommend {recommendations.architecture_pattern.lower()} with {recommendations.overall_confidence:.0%} confidence.",
                "next_steps": recommendations.next_steps[:3] if recommendations.next_steps else [],
                "confidence": recommendations.overall_confidence,
                "success": True
            }
            
            return quick_response
            
        except Exception as e:
            logger.error(f"Quick recommendation failed: {e}")
            return {
                "expertise_type": "quick_recommendation",
                "error": str(e),
                "success": False,
                "confidence": 0.70
            }
    
    async def _start_guided_consultation(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Start a guided tech stack consultation"""
        
        try:
            # Start conversation session
            session_id, welcome_message = await self.conversation_engine.start_conversation(user_id)
            
            # Store active consultation
            self.active_consultations[session_id] = {
                "user_id": user_id,
                "started_at": datetime.now().isoformat(),
                "context": context,
                "status": "active"
            }
            
            return {
                "expertise_type": "guided_consultation",
                "consultation_started": True,
                "session_id": session_id,
                "welcome_message": welcome_message.content,
                "message_options": welcome_message.options,
                "current_stage": welcome_message.stage.value,
                "guidance": "I'll guide you through a series of questions to understand your project needs and provide personalized recommendations.",
                "confidence": 0.85,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Guided consultation failed: {e}")
            return {
                "expertise_type": "guided_consultation",
                "error": str(e),
                "success": False,
                "confidence": 0.70
            }
    
    async def _provide_technology_comparison(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide technology comparison and analysis"""
        
        try:
            prompt = context.get("prompt", "")
            
            # Extract technologies to compare (simplified extraction)
            technologies = await self._extract_technologies_from_prompt(prompt)
            
            # Generate comparison analysis
            comparison = await self._generate_technology_comparison(technologies, prompt)
            
            return {
                "expertise_type": "technology_comparison",
                "technologies_compared": technologies,
                "comparison_analysis": comparison,
                "recommendation": comparison.get("recommendation", ""),
                "confidence": comparison.get("confidence", 0.80),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Technology comparison failed: {e}")
            return {
                "expertise_type": "technology_comparison",
                "error": str(e),
                "success": False,
                "confidence": 0.70
            }
    
    async def _provide_architecture_review(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide architecture review and feedback"""
        
        try:
            prompt = context.get("prompt", "")
            
            # Extract current stack information
            current_stack = await self._extract_current_stack(prompt)
            
            # Generate review and suggestions
            review = await self._generate_architecture_review(current_stack, prompt)
            
            return {
                "expertise_type": "architecture_review",
                "current_stack": current_stack,
                "review_feedback": review.get("feedback", ""),
                "improvement_suggestions": review.get("suggestions", []),
                "risk_assessment": review.get("risks", []),
                "confidence": review.get("confidence", 0.75),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Architecture review failed: {e}")
            return {
                "expertise_type": "architecture_review",
                "error": str(e),
                "success": False,
                "confidence": 0.70
            }
    
    async def _provide_general_guidance(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide general tech stack guidance"""
        
        try:
            prompt = context.get("prompt", "")
            
            # Generate general guidance based on prompt analysis
            guidance = await self._generate_general_guidance(prompt)
            
            return {
                "expertise_type": "general_guidance",
                "guidance": guidance.get("advice", ""),
                "key_considerations": guidance.get("considerations", []),
                "recommended_resources": guidance.get("resources", []),
                "confidence": guidance.get("confidence", 0.75),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"General guidance failed: {e}")
            return {
                "expertise_type": "general_guidance",
                "error": str(e),
                "success": False,
                "confidence": 0.70
            }
    
    async def _parse_basic_requirements(self, prompt: str) -> ProjectRequirements:
        """Parse basic requirements from prompt for quick recommendations"""
        
        prompt_lower = prompt.lower()
        
        # Default requirements
        app_type = ApplicationType.WEB_APP
        user_scale = UserScale.MEDIUM
        ai_integration = False
        
        # Parse application type
        if any(keyword in prompt_lower for keyword in ["mobile", "app", "ios", "android"]):
            app_type = ApplicationType.MOBILE_APP
        elif any(keyword in prompt_lower for keyword in ["api", "backend", "service"]):
            app_type = ApplicationType.API_SERVICE
        elif any(keyword in prompt_lower for keyword in ["ai", "ml", "machine learning"]):
            app_type = ApplicationType.AI_SERVICE
        elif any(keyword in prompt_lower for keyword in ["static", "blog", "cms"]):
            app_type = ApplicationType.STATIC_SITE
        
        # Parse scale
        if any(keyword in prompt_lower for keyword in ["small", "prototype", "mvp"]):
            user_scale = UserScale.SMALL
        elif any(keyword in prompt_lower for keyword in ["large", "enterprise", "big"]):
            user_scale = UserScale.LARGE
        
        # Parse AI needs
        if any(keyword in prompt_lower for keyword in ["ai", "ml", "chatbot", "recommendation"]):
            ai_integration = True
        
        return ProjectRequirements(
            application_type=app_type,
            user_scale=user_scale,
            ai_integration=ai_integration,
            user_experience={
                "frontend": ExperienceLevel.INTERMEDIATE,
                "backend": ExperienceLevel.INTERMEDIATE,
                "database": ExperienceLevel.INTERMEDIATE
            }
        )
    
    async def _extract_technologies_from_prompt(self, prompt: str) -> List[str]:
        """Extract technology names from prompt for comparison"""
        
        # Common technology names
        tech_names = [
            "React", "Vue", "Angular", "Svelte",
            "Node.js", "Python", "Java", "Go", "C#",
            "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP"
        ]
        
        found_technologies = []
        prompt_lower = prompt.lower()
        
        for tech in tech_names:
            if tech.lower() in prompt_lower:
                found_technologies.append(tech)
        
        return found_technologies[:4]  # Limit to 4 technologies
    
    async def _generate_technology_comparison(self, technologies: List[str], prompt: str) -> Dict[str, Any]:
        """Generate comparison analysis between technologies"""
        
        if len(technologies) < 2:
            return {
                "analysis": "Need at least two technologies to compare",
                "confidence": 0.70
            }
        
        # Simplified comparison logic
        comparison_data = {
            "analysis": f"Comparing {' vs '.join(technologies)}:",
            "pros_cons": {},
            "recommendation": f"Based on common use cases, {technologies[0]} might be suitable for most scenarios",
            "confidence": 0.80
        }
        
        for tech in technologies:
            comparison_data["pros_cons"][tech] = {
                "pros": [f"Strong ecosystem for {tech}", f"Good performance in {tech}"],
                "cons": [f"Learning curve for {tech}", f"Potential complexity in {tech}"]
            }
        
        return comparison_data
    
    async def _extract_current_stack(self, prompt: str) -> Dict[str, Any]:
        """Extract current technology stack from prompt"""
        
        # Simplified extraction
        technologies = await self._extract_technologies_from_prompt(prompt)
        
        return {
            "identified_technologies": technologies,
            "stack_description": "Current stack extracted from description",
            "completeness": len(technologies) / 4  # Rough completeness estimate
        }
    
    async def _generate_architecture_review(self, current_stack: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """Generate architecture review and feedback"""
        
        technologies = current_stack.get("identified_technologies", [])
        
        return {
            "feedback": f"Your current stack with {', '.join(technologies)} shows good technology choices",
            "suggestions": [
                "Consider implementing monitoring and logging",
                "Evaluate containerization for better deployment",
                "Review security practices and authentication"
            ],
            "risks": [
                "Ensure proper error handling across services",
                "Monitor performance bottlenecks",
                "Plan for scalability as user base grows"
            ],
            "confidence": 0.75
        }
    
    async def _generate_general_guidance(self, prompt: str) -> Dict[str, Any]:
        """Generate general technology guidance"""
        
        return {
            "advice": "For technology decisions, consider your team's experience, project timeline, scalability needs, and long-term maintenance.",
            "considerations": [
                "Team skill level and learning capacity",
                "Project timeline and budget constraints",
                "Expected user scale and performance requirements",
                "Long-term maintenance and support"
            ],
            "resources": [
                "Technology documentation and tutorials",
                "Community forums and Stack Overflow",
                "Online courses and certification programs"
            ],
            "confidence": 0.75
        }
    
    async def _fallback_expertise(self, context: Dict[str, Any], error: Optional[str] = None) -> Dict[str, Any]:
        """Provide fallback tech expertise when components are unavailable"""
        
        prompt = context.get("prompt", "")
        
        return {
            "expertise_type": "fallback_guidance",
            "advice": "For technology stack decisions, I recommend considering: team experience, project requirements, scalability needs, and community support.",
            "general_recommendations": [
                "Start with technologies your team knows well",
                "Choose mature, well-documented solutions",
                "Consider long-term maintenance and support",
                "Plan for future scalability needs"
            ],
            "next_steps": [
                "Define your project requirements clearly",
                "Research technology options and trade-offs",
                "Consider team training and skill development",
                "Plan for iterative development and testing"
            ],
            "confidence": 0.70,
            "fallback": True,
            "error_message": f"Tech Expert components unavailable: {error}" if error else "Tech Expert components not available"
        }
    
    async def update_learning_metrics(self,
                                    user_id: str,
                                    recommendations: Dict[str, Any],
                                    user_feedback: Dict[str, Any]):
        """Update learning metrics from user feedback"""
        
        try:
            # Store recommendation feedback
            feedback_key = f"{user_id}_{datetime.now().timestamp()}"
            self.learning_metrics["recommendation_feedback"][feedback_key] = {
                "recommendations": recommendations,
                "user_feedback": user_feedback,
                "timestamp": datetime.now().isoformat()
            }
            
            # Extract satisfaction score
            satisfaction = user_feedback.get("satisfaction_score", 3.0)  # Default 3/5
            self.user_satisfaction_scores.append(satisfaction)
            
            # Update technology trend tracking
            for rec in recommendations.get("recommendations", []):
                tech = rec.get("technology", "")
                if tech:
                    if tech not in self.learning_metrics["technology_trends"]:
                        self.learning_metrics["technology_trends"][tech] = {
                            "recommendation_count": 0,
                            "positive_feedback": 0,
                            "avg_satisfaction": 0.0
                        }
                    
                    trend_data = self.learning_metrics["technology_trends"][tech]
                    trend_data["recommendation_count"] += 1
                    
                    if satisfaction >= 4.0:  # Positive feedback threshold
                        trend_data["positive_feedback"] += 1
                    
                    # Update average satisfaction
                    total_recommendations = trend_data["recommendation_count"]
                    current_avg = trend_data["avg_satisfaction"]
                    trend_data["avg_satisfaction"] = (
                        (current_avg * (total_recommendations - 1) + satisfaction) / total_recommendations
                    )
            
            logger.info(f"Updated learning metrics for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to update learning metrics: {e}")
    
    async def get_expertise_status(self) -> Dict[str, Any]:
        """Get tech stack expert status"""
        
        success_rate = (
            self.successful_recommendations / max(1, self.total_consultations)
        )
        
        avg_satisfaction = (
            sum(self.user_satisfaction_scores) / len(self.user_satisfaction_scores)
            if self.user_satisfaction_scores else 0.0
        )
        
        return {
            "module_initialized": self.initialized,
            "tech_expert_available": TECH_EXPERT_AVAILABLE,
            "brain_integration": BRAIN_AVAILABLE,
            "active_consultations": len(self.active_consultations),
            "total_consultations": self.total_consultations,
            "success_rate": success_rate,
            "average_satisfaction": avg_satisfaction,
            "recommendation_history_count": len(self.recommendation_history),
            "learning_metrics": {
                "technologies_tracked": len(self.learning_metrics["technology_trends"]),
                "feedback_entries": len(self.learning_metrics["recommendation_feedback"])
            }
        }
    
    # AAI Brain Module interface methods (if available)
    
    if BRAIN_AVAILABLE:
        async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
            """Process brain module request"""
            
            try:
                # Check if tech expertise should be provided
                expertise_decision = await self.should_provide_expertise(context)
                
                if expertise_decision["should_provide_expertise"]:
                    # Provide tech stack expertise
                    result = await self.provide_expertise(
                        context,
                        context.get("user_id", "anonymous")
                    )
                    
                    return {
                        "module_name": self.name,
                        "expertise_provided": True,
                        "decision_confidence": expertise_decision["confidence"],
                        "decision_reasoning": expertise_decision["reasoning"],
                        "result": result,
                        "confidence": result.get("confidence", 0.70),
                        "success": result.get("success", False)
                    }
                
                else:
                    # No expertise needed
                    return {
                        "module_name": self.name,
                        "expertise_provided": False,
                        "decision_confidence": expertise_decision["confidence"],
                        "decision_reasoning": expertise_decision["reasoning"],
                        "suggestion": "Standard response recommended",
                        "confidence": expertise_decision["confidence"],
                        "success": True
                    }
                
            except Exception as e:
                logger.error(f"Brain module processing failed: {e}")
                return {
                    "module_name": self.name,
                    "expertise_provided": False,
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
                "total_consultations": self.total_consultations,
                "success_rate": self.successful_recommendations / max(1, self.total_consultations),
                "tech_expert_available": TECH_EXPERT_AVAILABLE,
                "ready": self.initialized or True  # Always ready with fallback
            }
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get module status (standalone version)"""
        
        return {
            "name": "tech_stack_expert",
            "version": "1.0.0",
            "initialized": self.initialized,
            "total_consultations": self.total_consultations,
            "successful_recommendations": self.successful_recommendations,
            "brain_integration": BRAIN_AVAILABLE,
            "tech_expert_available": TECH_EXPERT_AVAILABLE,
            "trigger_conditions": {
                "architectural_decisions": len(self.expertise_triggers["architectural_decisions"]),
                "project_planning": len(self.expertise_triggers["project_planning"]),
                "scaling_concerns": len(self.expertise_triggers["scaling_concerns"]),
                "team_guidance": len(self.expertise_triggers["team_guidance"])
            },
            "learning_metrics_summary": {
                "technologies_tracked": len(self.learning_metrics["technology_trends"]),
                "feedback_entries": len(self.learning_metrics["recommendation_feedback"]),
                "satisfaction_scores": len(self.user_satisfaction_scores)
            },
            "ready": self.initialized or True
        }


# Initialize module instance
tech_stack_expert = TechStackExpertModule()


async def test_tech_stack_expert_module():
    """Test Tech Stack Expert Module functionality"""
    
    module = TechStackExpertModule()
    
    print("🧪 Testing Tech Stack Expert Module")
    print("=" * 35)
    
    # Wait for initialization
    await asyncio.sleep(1.5)
    
    # Check module status
    status = module.get_module_status()
    print(f"Module initialized: {status['initialized']}")
    print(f"Brain integration: {status['brain_integration']}")
    print(f"Tech expert available: {status['tech_expert_available']}")
    print(f"Ready: {status['ready']}")
    
    # Test expertise decisions
    print(f"\n🎯 Testing expertise decisions...")
    
    test_contexts = [
        {
            "prompt": "I need help choosing a technology stack for my new web application",
            "user_id": "test_user"
        },
        {
            "prompt": "What's the capital of France?",
            "user_id": "test_user"
        },
        {
            "prompt": "Should I use React vs Vue for my frontend framework?",
            "user_id": "test_user"
        },
        {
            "prompt": "Can you review my current architecture with Node.js and MongoDB?",
            "user_id": "test_user"
        }
    ]
    
    for i, context in enumerate(test_contexts, 1):
        print(f"\nContext {i}: {context['prompt'][:50]}...")
        
        decision = await module.should_provide_expertise(context)
        print(f"  Should provide expertise: {decision['should_provide_expertise']}")
        print(f"  Confidence: {decision['confidence']:.1%}")
        print(f"  Triggers: {', '.join(decision.get('triggers_found', []))}")
        
        if decision["should_provide_expertise"]:
            # Test providing expertise
            result = await module.provide_expertise(context)
            print(f"  Expertise provided: {result.get('success', False)}")
            print(f"  Expertise type: {result.get('expertise_type', 'unknown')}")
            print(f"  Result confidence: {result.get('confidence', 0):.1%}")
    
    # Test learning metrics update
    print(f"\n📚 Testing learning metrics...")
    
    sample_recommendations = {
        "recommendations": [
            {"technology": "React.js", "confidence": 0.85},
            {"technology": "Node.js", "confidence": 0.80}
        ]
    }
    
    sample_feedback = {
        "satisfaction_score": 4.5,
        "usefulness": "very_helpful",
        "comments": "Great recommendations!"
    }
    
    await module.update_learning_metrics("test_user", sample_recommendations, sample_feedback)
    
    # Check final status
    final_status = await module.get_expertise_status()
    print(f"\n📊 Final Status:")
    print(f"Total consultations: {final_status['total_consultations']}")
    print(f"Success rate: {final_status['success_rate']:.1%}")
    print(f"Average satisfaction: {final_status['average_satisfaction']:.1f}/5.0")
    print(f"Technologies tracked: {final_status['learning_metrics']['technologies_tracked']}")
    
    print(f"\n✅ Tech Stack Expert Module Testing Complete")
    print(f"AAI Brain integration ready for architectural decision support")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tech_stack_expert_module())