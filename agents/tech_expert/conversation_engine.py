"""
Conversation Engine for Tech Stack Expert Agent

Implements guided conversation flow for requirement gathering
and context analysis to support intelligent tech stack recommendations.
"""

import logging
import asyncio
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

try:
    from .models import (
        ConversationState, ConversationStage, ConversationMessage,
        ProjectRequirements, ApplicationType, UserScale, ExperienceLevel,
        TechCategory
    )
except ImportError:
    from agents.tech_expert.models import (
        ConversationState, ConversationStage, ConversationMessage,
        ProjectRequirements, ApplicationType, UserScale, ExperienceLevel,
        TechCategory
    )

logger = logging.getLogger(__name__)


class ConversationEngine:
    """
    Manages guided conversations for tech stack requirement gathering.
    
    Features:
    - Stage-based conversation flow
    - Context-aware question generation
    - User experience assessment
    - Requirement validation and refinement
    - AAI-compliant confidence scoring
    """
    
    def __init__(self):
        """Initialize conversation engine"""
        
        self.name = "Tech Stack Conversation Engine"
        self.version = "1.0.0"
        
        # Active conversation sessions
        self.active_sessions: Dict[str, ConversationState] = {}
        
        # Conversation templates and questions
        self.stage_questions = self._initialize_question_templates()
        
        # Performance tracking
        self.total_conversations = 0
        self.completed_conversations = 0
        self.average_session_length = 0.0
        
        logger.info("Tech Stack Conversation Engine initialized")
    
    def _initialize_question_templates(self) -> Dict[ConversationStage, Dict[str, Any]]:
        """Initialize question templates for each conversation stage"""
        
        return {
            ConversationStage.WELCOME: {
                "message": "👋 Welcome! I'm your Tech Stack Expert Agent. I'll help you choose the perfect technology stack for your project through a guided conversation. Let's start by understanding what you're building!",
                "options": ["Let's begin!", "Tell me more about the process"],
                "requires_response": True
            },
            
            ConversationStage.APP_TYPE: {
                "message": "What type of application are you planning to build?",
                "options": [
                    "Web Application (browser-based)",
                    "Mobile Application (iOS/Android)",
                    "API Service (backend/microservice)",
                    "Desktop Application",
                    "AI/ML Service",
                    "Data Pipeline/ETL",
                    "Real-time Application (chat, gaming)",
                    "Static Website/Blog"
                ],
                "context": "Understanding the application type helps determine the core technologies and architecture patterns.",
                "requires_response": True
            },
            
            ConversationStage.SCALE_PLANNING: {
                "message": "How many users do you expect to support initially and at peak?",
                "options": [
                    "Prototype/MVP (< 100 users)",
                    "Small scale (100-1,000 users)",
                    "Medium scale (1,000-10,000 users)", 
                    "Large scale (10,000-100,000 users)",
                    "Enterprise scale (100,000+ users)"
                ],
                "context": "User scale significantly impacts technology choices, especially for databases, caching, and deployment strategies.",
                "requires_response": True
            },
            
            ConversationStage.AI_INTEGRATION: {
                "message": "Will your application include AI/ML features?",
                "options": [
                    "Yes - Core AI functionality (LLMs, computer vision, etc.)",
                    "Yes - Simple AI features (recommendations, basic ML)",
                    "Maybe - Considering it for future",
                    "No - Traditional application only"
                ],
                "context": "AI integration affects technology choices for data processing, model serving, and infrastructure requirements.",
                "requires_response": True
            },
            
            ConversationStage.EXPERIENCE_ASSESSMENT: {
                "message": "Let's assess your team's experience with different technology areas. This helps me recommend technologies that match your current skills.",
                "context": "I'll ask about experience in key areas like frontend, backend, databases, and deployment.",
                "requires_response": True
            },
            
            ConversationStage.CONSTRAINTS_GATHERING: {
                "message": "Are there any specific constraints or requirements I should know about?",
                "context": "Examples: budget limitations, compliance requirements, existing systems to integrate with, deployment preferences.",
                "requires_response": True
            },
            
            ConversationStage.RECOMMENDATION_GENERATION: {
                "message": "Perfect! I have enough information to generate your personalized tech stack recommendations. Let me analyze your requirements...",
                "requires_response": False
            },
            
            ConversationStage.RECOMMENDATION_REFINEMENT: {
                "message": "Here are my recommendations! Would you like me to explain any choices or explore alternatives for specific components?",
                "requires_response": True
            },
            
            ConversationStage.FINAL_SUMMARY: {
                "message": "Here's your complete tech stack recommendation with implementation guidance. Would you like me to save this or provide additional resources?",
                "requires_response": True
            }
        }
    
    async def start_conversation(self, user_id: str) -> Tuple[str, ConversationMessage]:
        """
        Start a new tech stack consultation conversation.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Tuple of (session_id, welcome_message)
        """
        
        session_id = str(uuid.uuid4())
        
        # Create new conversation state
        conversation = ConversationState(
            session_id=session_id,
            user_id=user_id,
            stage=ConversationStage.WELCOME
        )
        
        self.active_sessions[session_id] = conversation
        self.total_conversations += 1
        
        # Generate welcome message
        welcome_message = await self._generate_stage_message(conversation)
        
        logger.info(f"Started tech stack conversation for user {user_id}, session {session_id}")
        
        return session_id, welcome_message
    
    async def process_user_response(self, session_id: str, user_input: str) -> ConversationMessage:
        """
        Process user response and advance conversation.
        
        Args:
            session_id: Session identifier
            user_input: User's response
            
        Returns:
            Next conversation message
        """
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        conversation = self.active_sessions[session_id]
        conversation.last_interaction = datetime.now()
        conversation.question_count += 1
        
        # Store user response
        stage_key = conversation.stage.value
        conversation.user_responses[stage_key] = user_input
        
        # Process response based on current stage
        await self._process_stage_response(conversation, user_input)
        
        # Generate next message
        next_message = await self._generate_next_message(conversation)
        
        logger.info(f"Processed response in session {session_id}, stage: {conversation.stage}")
        
        return next_message
    
    async def _process_stage_response(self, conversation: ConversationState, user_input: str):
        """Process user response for the current conversation stage"""
        
        stage = conversation.stage
        
        if stage == ConversationStage.WELCOME:
            # User confirmed they want to start
            conversation.advance_stage()
        
        elif stage == ConversationStage.APP_TYPE:
            # Parse application type from user response
            app_type = await self._parse_application_type(user_input)
            if not conversation.requirements:
                conversation.requirements = ProjectRequirements(
                    application_type=app_type,
                    user_scale=UserScale.MEDIUM  # Default, will be updated
                )
            else:
                conversation.requirements.application_type = app_type
            conversation.advance_stage()
        
        elif stage == ConversationStage.SCALE_PLANNING:
            # Parse user scale from response
            user_scale = await self._parse_user_scale(user_input)
            if conversation.requirements:
                conversation.requirements.user_scale = user_scale
            conversation.advance_stage()
        
        elif stage == ConversationStage.AI_INTEGRATION:
            # Parse AI integration requirements
            ai_integration = await self._parse_ai_integration(user_input)
            if conversation.requirements:
                conversation.requirements.ai_integration = ai_integration
            conversation.advance_stage()
        
        elif stage == ConversationStage.EXPERIENCE_ASSESSMENT:
            # This stage may involve multiple questions
            if not hasattr(conversation, '_experience_questions_asked'):
                conversation._experience_questions_asked = 0
            
            await self._process_experience_question(conversation, user_input)
        
        elif stage == ConversationStage.CONSTRAINTS_GATHERING:
            # Parse additional constraints
            await self._parse_constraints(conversation, user_input)
            conversation.advance_stage()
        
        elif stage == ConversationStage.RECOMMENDATION_GENERATION:
            # This stage doesn't require user input
            conversation.advance_stage()
        
        elif stage == ConversationStage.RECOMMENDATION_REFINEMENT:
            # Handle refinement requests
            await self._process_refinement_request(conversation, user_input)
            
        elif stage == ConversationStage.FINAL_SUMMARY:
            # Handle final requests
            await self._process_final_request(conversation, user_input)
            conversation.advance_stage()  # Move to COMPLETE
    
    async def _generate_stage_message(self, conversation: ConversationState) -> ConversationMessage:
        """Generate message for current conversation stage"""
        
        stage = conversation.stage
        template = self.stage_questions.get(stage, {})
        
        message_id = str(uuid.uuid4())
        
        if stage == ConversationStage.EXPERIENCE_ASSESSMENT:
            # Handle multi-question experience assessment
            return await self._generate_experience_question(conversation, message_id)
        
        return ConversationMessage(
            id=message_id,
            session_id=conversation.session_id,
            role="assistant",
            content=template.get("message", "How can I help you?"),
            message_type="question",
            stage=stage,
            options=template.get("options", []),
            requires_response=template.get("requires_response", True)
        )
    
    async def _generate_next_message(self, conversation: ConversationState) -> ConversationMessage:
        """Generate the next message in the conversation"""
        
        if conversation.stage == ConversationStage.COMPLETE:
            return ConversationMessage(
                id=str(uuid.uuid4()),
                session_id=conversation.session_id,
                role="assistant",
                content="Thank you for using the Tech Stack Expert! Your recommendations have been generated. Feel free to start a new conversation anytime you need architectural guidance.",
                message_type="response",
                stage=conversation.stage,
                requires_response=False
            )
        
        return await self._generate_stage_message(conversation)
    
    async def _generate_experience_question(self, conversation: ConversationState, message_id: str) -> ConversationMessage:
        """Generate experience assessment question"""
        
        tech_categories = [
            ("frontend", "Frontend Development (React, Vue, Angular, etc.)"),
            ("backend", "Backend Development (Node.js, Python, Java, etc.)"),
            ("database", "Database Management (SQL, NoSQL, etc.)"),
            ("deployment", "Deployment & DevOps (Docker, AWS, CI/CD)"),
            ("ai_ml", "AI/ML Technologies (if applicable)")
        ]
        
        if not hasattr(conversation, '_experience_questions_asked'):
            conversation._experience_questions_asked = 0
        
        if conversation._experience_questions_asked < len(tech_categories):
            category, description = tech_categories[conversation._experience_questions_asked]
            
            return ConversationMessage(
                id=message_id,
                session_id=conversation.session_id,
                role="assistant",
                content=f"What's your team's experience level with {description}?",
                message_type="question",
                stage=conversation.stage,
                options=["Beginner (0-1 years)", "Intermediate (1-3 years)", "Advanced (3-5 years)", "Expert (5+ years)"],
                requires_response=True
            )
        else:
            # Done with experience questions
            conversation.advance_stage()
            return await self._generate_stage_message(conversation)
    
    async def _process_experience_question(self, conversation: ConversationState, user_input: str):
        """Process experience level response"""
        
        tech_categories = ["frontend", "backend", "database", "deployment", "ai_ml"]
        
        if not hasattr(conversation, '_experience_questions_asked'):
            conversation._experience_questions_asked = 0
        
        # Parse experience level
        experience_level = await self._parse_experience_level(user_input)
        
        # Store in requirements
        if conversation.requirements:
            if not conversation.requirements.user_experience:
                conversation.requirements.user_experience = {}
            
            category = tech_categories[conversation._experience_questions_asked]
            conversation.requirements.user_experience[category] = experience_level
        
        conversation._experience_questions_asked += 1
    
    async def _parse_application_type(self, user_input: str) -> ApplicationType:
        """Parse application type from user input"""
        
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["web", "browser", "website"]):
            return ApplicationType.WEB_APP
        elif any(keyword in input_lower for keyword in ["mobile", "ios", "android", "app"]):
            return ApplicationType.MOBILE_APP
        elif any(keyword in input_lower for keyword in ["api", "service", "backend", "microservice"]):
            return ApplicationType.API_SERVICE
        elif any(keyword in input_lower for keyword in ["desktop", "electron"]):
            return ApplicationType.DESKTOP_APP
        elif any(keyword in input_lower for keyword in ["ai", "ml", "machine learning", "artificial intelligence"]):
            return ApplicationType.AI_SERVICE
        elif any(keyword in input_lower for keyword in ["data", "pipeline", "etl"]):
            return ApplicationType.DATA_PIPELINE
        elif any(keyword in input_lower for keyword in ["real-time", "chat", "gaming", "live"]):
            return ApplicationType.REAL_TIME_APP
        elif any(keyword in input_lower for keyword in ["static", "blog", "cms"]):
            return ApplicationType.STATIC_SITE
        else:
            return ApplicationType.WEB_APP  # Default fallback
    
    async def _parse_user_scale(self, user_input: str) -> UserScale:
        """Parse user scale from user input"""
        
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["prototype", "mvp", "100", "few"]):
            return UserScale.PROTOTYPE
        elif any(keyword in input_lower for keyword in ["small", "1000", "thousand"]):
            return UserScale.SMALL
        elif any(keyword in input_lower for keyword in ["medium", "10000", "10k"]):
            return UserScale.MEDIUM
        elif any(keyword in input_lower for keyword in ["large", "100000", "100k"]):
            return UserScale.LARGE
        elif any(keyword in input_lower for keyword in ["enterprise", "million", "massive"]):
            return UserScale.ENTERPRISE
        else:
            return UserScale.MEDIUM  # Default fallback
    
    async def _parse_ai_integration(self, user_input: str) -> bool:
        """Parse AI integration requirement from user input"""
        
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["yes", "core", "definitely", "need"]):
            return True
        elif any(keyword in input_lower for keyword in ["no", "traditional", "not"]):
            return False
        else:
            return "maybe" in input_lower  # Return True for "maybe" cases
    
    async def _parse_experience_level(self, user_input: str) -> ExperienceLevel:
        """Parse experience level from user input"""
        
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["beginner", "0-1", "new", "learning"]):
            return ExperienceLevel.BEGINNER
        elif any(keyword in input_lower for keyword in ["intermediate", "1-3", "some experience"]):
            return ExperienceLevel.INTERMEDIATE
        elif any(keyword in input_lower for keyword in ["advanced", "3-5", "experienced"]):
            return ExperienceLevel.ADVANCED
        elif any(keyword in input_lower for keyword in ["expert", "5+", "senior", "master"]):
            return ExperienceLevel.EXPERT
        else:
            return ExperienceLevel.INTERMEDIATE  # Default fallback
    
    async def _parse_constraints(self, conversation: ConversationState, user_input: str):
        """Parse additional constraints from user input"""
        
        if not conversation.requirements:
            return
        
        input_lower = user_input.lower()
        
        # Parse various constraint types
        if "budget" in input_lower or "cost" in input_lower:
            conversation.requirements.budget_constraints = user_input
        
        if any(keyword in input_lower for keyword in ["compliance", "gdpr", "hipaa", "sox"]):
            compliance_found = []
            if "gdpr" in input_lower:
                compliance_found.append("GDPR")
            if "hipaa" in input_lower:
                compliance_found.append("HIPAA")
            if "sox" in input_lower:
                compliance_found.append("SOX")
            conversation.requirements.compliance_requirements = compliance_found
        
        if "on-premise" in input_lower or "on premise" in input_lower:
            conversation.requirements.on_premise_required = True
        
        if any(keyword in input_lower for keyword in ["aws", "azure", "gcp", "google cloud"]):
            if "aws" in input_lower:
                conversation.requirements.cloud_preference = "AWS"
            elif "azure" in input_lower:
                conversation.requirements.cloud_preference = "Azure"
            elif "gcp" in input_lower or "google" in input_lower:
                conversation.requirements.cloud_preference = "Google Cloud"
    
    async def _process_refinement_request(self, conversation: ConversationState, user_input: str):
        """Process recommendation refinement requests"""
        
        # Store refinement feedback
        if 'refinement_requests' not in conversation.user_feedback:
            conversation.user_feedback['refinement_requests'] = []
        
        conversation.user_feedback['refinement_requests'].append({
            'request': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check if user wants to move to final summary
        input_lower = user_input.lower()
        if any(keyword in input_lower for keyword in ["done", "finished", "final", "complete", "satisfied"]):
            conversation.advance_stage()
    
    async def _process_final_request(self, conversation: ConversationState, user_input: str):
        """Process final stage requests"""
        
        input_lower = user_input.lower()
        
        # Store final feedback
        conversation.user_feedback['final_feedback'] = user_input
        
        if any(keyword in input_lower for keyword in ["save", "export", "download"]):
            conversation.user_feedback['wants_export'] = True
        
        if any(keyword in input_lower for keyword in ["resources", "learning", "tutorial"]):
            conversation.user_feedback['wants_resources'] = True
    
    def get_conversation_state(self, session_id: str) -> Optional[ConversationState]:
        """Get current conversation state"""
        return self.active_sessions.get(session_id)
    
    def get_conversation_progress(self, session_id: str) -> Dict[str, Any]:
        """Get conversation progress information"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        conversation = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "current_stage": conversation.stage.value,
            "progress_percentage": conversation.get_progress_percentage(),
            "questions_answered": len(conversation.user_responses),
            "requirements_gathered": conversation.requirements is not None,
            "confidence_level": conversation.confidence_in_requirements
        }
    
    def end_conversation(self, session_id: str) -> Dict[str, Any]:
        """End conversation and clean up resources"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        conversation = self.active_sessions[session_id]
        
        # Mark as complete if not already
        if not conversation.is_complete():
            conversation.stage = ConversationStage.COMPLETE
        
        # Update statistics
        if conversation.is_complete():
            self.completed_conversations += 1
            session_duration = (datetime.now() - conversation.started_at).total_seconds() / 60
            
            # Update average session length
            total_completed = self.completed_conversations
            current_avg = self.average_session_length
            self.average_session_length = ((current_avg * (total_completed - 1)) + session_duration) / total_completed
        
        # Remove from active sessions
        conversation_data = self.active_sessions.pop(session_id)
        
        logger.info(f"Ended conversation session {session_id}")
        
        return {
            "session_ended": True,
            "conversation_complete": conversation.is_complete(),
            "requirements_gathered": conversation.requirements is not None,
            "total_questions": conversation.question_count,
            "session_duration_minutes": (datetime.now() - conversation.started_at).total_seconds() / 60
        }
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get conversation engine status and metrics"""
        
        completion_rate = (
            self.completed_conversations / max(1, self.total_conversations)
        )
        
        return {
            "name": self.name,
            "version": self.version,
            "active_sessions": len(self.active_sessions),
            "total_conversations": self.total_conversations,
            "completed_conversations": self.completed_conversations,
            "completion_rate": completion_rate,
            "average_session_length_minutes": self.average_session_length,
            "supported_stages": len(self.stage_questions)
        }


async def test_conversation_engine():
    """Test conversation engine functionality"""
    
    engine = ConversationEngine()
    
    print("🧪 Testing Tech Stack Conversation Engine")
    print("=" * 41)
    
    # Test conversation flow
    session_id, welcome_msg = await engine.start_conversation("test_user")
    print(f"Started session: {session_id}")
    print(f"Welcome message: {welcome_msg.content[:100]}...")
    
    # Simulate user responses
    test_responses = [
        "Let's begin!",
        "Web Application",
        "Medium scale (1,000-10,000 users)",
        "Yes - Core AI functionality",
        "Intermediate (1-3 years)",  # Frontend
        "Beginner (0-1 years)",     # Backend
        "Intermediate (1-3 years)",  # Database
        "Beginner (0-1 years)",     # Deployment
        "Beginner (0-1 years)",     # AI/ML
        "No specific constraints",
        "These look good",
        "Save the recommendations"
    ]
    
    for i, response in enumerate(test_responses):
        try:
            next_msg = await engine.process_user_response(session_id, response)
            print(f"\nStep {i+1}: User: '{response}'")
            print(f"Assistant: {next_msg.content[:100]}...")
            print(f"Stage: {next_msg.stage.value}")
            
            # Check progress
            progress = engine.get_conversation_progress(session_id)
            print(f"Progress: {progress['progress_percentage']:.1f}%")
            
        except Exception as e:
            print(f"Error at step {i+1}: {e}")
            break
    
    # Get final status
    final_status = engine.get_engine_status()
    print(f"\n📊 Final Status:")
    print(f"Active sessions: {final_status['active_sessions']}")
    print(f"Completion rate: {final_status['completion_rate']:.1%}")
    
    # End conversation
    end_result = engine.end_conversation(session_id)
    print(f"\nConversation ended: {end_result['session_ended']}")
    
    print(f"\n✅ Conversation Engine Testing Complete")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_conversation_engine())