"""
Data Models for Tech Stack Expert Agent

Defines comprehensive data structures for project requirements,
tech recommendations, and conversation state management.
"""

from typing import Dict, List, Any, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class ApplicationType(str, Enum):
    """Types of applications for tech stack recommendations"""
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DESKTOP_APP = "desktop_app"
    AI_SERVICE = "ai_service"
    DATA_PIPELINE = "data_pipeline"
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    STATIC_SITE = "static_site"
    REAL_TIME_APP = "real_time_app"


class UserScale(str, Enum):
    """Expected user scale for the application"""
    PROTOTYPE = "prototype"  # < 100 users
    SMALL = "small"  # 100-1K users
    MEDIUM = "medium"  # 1K-10K users
    LARGE = "large"  # 10K-100K users
    ENTERPRISE = "enterprise"  # 100K+ users


class ExperienceLevel(str, Enum):
    """User experience levels with different technologies"""
    BEGINNER = "beginner"  # 0-1 years
    INTERMEDIATE = "intermediate"  # 1-3 years
    ADVANCED = "advanced"  # 3-5 years
    EXPERT = "expert"  # 5+ years


class ConversationStage(str, Enum):
    """Stages of the guided conversation"""
    WELCOME = "welcome"
    APP_TYPE = "app_type"
    SCALE_PLANNING = "scale_planning"
    AI_INTEGRATION = "ai_integration"
    EXPERIENCE_ASSESSMENT = "experience_assessment"
    CONSTRAINTS_GATHERING = "constraints_gathering"
    RECOMMENDATION_GENERATION = "recommendation_generation"
    RECOMMENDATION_REFINEMENT = "recommendation_refinement"
    FINAL_SUMMARY = "final_summary"
    COMPLETE = "complete"


class TechCategory(str, Enum):
    """Categories of technology components"""
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEPLOYMENT = "deployment"
    AI_ML = "ai_ml"
    AUTHENTICATION = "authentication"
    MONITORING = "monitoring"
    TESTING = "testing"
    CACHING = "caching"
    MESSAGE_QUEUE = "message_queue"


class ProjectRequirements(BaseModel):
    """Comprehensive project requirements for tech stack recommendations"""
    
    # Basic project info
    application_type: ApplicationType
    user_scale: UserScale
    project_timeline: Optional[str] = Field(None, description="Expected timeline (e.g., '3 months', '1 year')")
    budget_constraints: Optional[str] = Field(None, description="Budget considerations")
    
    # Technical requirements
    ai_integration: bool = Field(False, description="Requires AI/ML integration")
    real_time_features: bool = Field(False, description="Needs real-time functionality")
    mobile_support: bool = Field(False, description="Mobile app or responsive design needed")
    offline_support: bool = Field(False, description="Offline functionality required")
    
    # User experience and team
    user_experience: Dict[str, ExperienceLevel] = Field(
        default_factory=dict,
        description="Team experience with different tech categories"
    )
    team_size: Optional[int] = Field(None, ge=1, le=100, description="Development team size")
    
    # Infrastructure preferences
    cloud_preference: Optional[str] = Field(None, description="Preferred cloud provider")
    on_premise_required: bool = Field(False, description="On-premise deployment required")
    compliance_requirements: List[str] = Field(default_factory=list, description="Compliance needs (GDPR, HIPAA, etc.)")
    
    # Performance requirements
    performance_priorities: List[str] = Field(
        default_factory=list,
        description="Performance priorities (speed, scalability, cost-efficiency)"
    )
    
    # Additional context
    existing_systems: List[str] = Field(default_factory=list, description="Existing systems to integrate with")
    special_requirements: Optional[str] = Field(None, description="Any special or unique requirements")
    
    @validator('user_experience')
    def validate_experience_levels(cls, v):
        """Validate experience level values"""
        valid_levels = set(ExperienceLevel.__members__.values())
        for category, level in v.items():
            if level not in valid_levels:
                raise ValueError(f"Invalid experience level: {level}")
        return v


class TechRecommendation(BaseModel):
    """Individual technology recommendation with rationale and confidence"""
    
    component: TechCategory
    technology: str
    version: Optional[str] = None
    rationale: str = Field(..., min_length=10, description="Reasoning for this recommendation")
    confidence: float = Field(..., ge=0.70, le=0.95, description="AAI-compliant confidence score")
    
    # Additional details
    learning_curve: ExperienceLevel = Field(default=ExperienceLevel.INTERMEDIATE)
    cost_impact: Literal["low", "medium", "high"] = "medium"
    scalability_rating: float = Field(default=0.8, ge=0.0, le=1.0)
    
    # Alternatives and considerations
    alternatives: List[str] = Field(default_factory=list, description="Alternative technology options")
    pros: List[str] = Field(default_factory=list, description="Advantages of this choice")
    cons: List[str] = Field(default_factory=list, description="Potential drawbacks")
    
    # Integration info
    ecosystem_fit: float = Field(default=0.8, ge=0.0, le=1.0, description="How well it fits with other recommendations")
    migration_complexity: Literal["low", "medium", "high"] = "medium"


class TechStackRecommendationSet(BaseModel):
    """Complete set of technology recommendations for a project"""
    
    recommendations: List[TechRecommendation]
    overall_confidence: float = Field(..., ge=0.70, le=0.95)
    architecture_pattern: str = Field(..., description="Recommended overall architecture pattern")
    
    # Stack analysis
    total_cost_estimate: Optional[str] = None
    development_timeline: Optional[str] = None
    team_skill_gap: Dict[str, ExperienceLevel] = Field(default_factory=dict)
    
    # Implementation guidance
    implementation_phases: List[str] = Field(default_factory=list)
    critical_decisions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    
    # Follow-up recommendations
    next_steps: List[str] = Field(default_factory=list)
    learning_resources: Dict[str, List[str]] = Field(default_factory=dict)


class ConversationState(BaseModel):
    """Tracks the current state of a guided conversation"""
    
    session_id: str
    user_id: str
    stage: ConversationStage = ConversationStage.WELCOME
    
    # Conversation flow
    started_at: datetime = Field(default_factory=datetime.now)
    last_interaction: datetime = Field(default_factory=datetime.now)
    completed_stages: List[ConversationStage] = Field(default_factory=list)
    
    # Gathered information
    requirements: Optional[ProjectRequirements] = None
    user_responses: Dict[str, Any] = Field(default_factory=dict)
    
    # Conversation metadata
    question_count: int = 0
    clarification_requests: int = 0
    confidence_in_requirements: float = Field(default=0.7, ge=0.0, le=1.0)
    
    # Results
    recommendations: Optional[TechStackRecommendationSet] = None
    user_feedback: Dict[str, Any] = Field(default_factory=dict)
    
    def advance_stage(self) -> ConversationStage:
        """Advance to the next conversation stage"""
        stages = list(ConversationStage)
        current_index = stages.index(self.stage)
        
        if current_index < len(stages) - 1:
            self.completed_stages.append(self.stage)
            self.stage = stages[current_index + 1]
            self.last_interaction = datetime.now()
        
        return self.stage
    
    def is_complete(self) -> bool:
        """Check if conversation is complete"""
        return self.stage == ConversationStage.COMPLETE
    
    def get_progress_percentage(self) -> float:
        """Get conversation completion percentage"""
        stages = list(ConversationStage)
        current_index = stages.index(self.stage)
        return (current_index / (len(stages) - 1)) * 100


class ConversationMessage(BaseModel):
    """Represents a message in the tech expert conversation"""
    
    id: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Message content
    role: Literal["assistant", "user"] = "assistant"
    content: str
    message_type: Literal["question", "response", "clarification", "recommendation"] = "question"
    
    # Conversation context
    stage: ConversationStage
    options: List[str] = Field(default_factory=list, description="Multiple choice options if applicable")
    
    # Metadata
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    requires_response: bool = True
    
    def is_multiple_choice(self) -> bool:
        """Check if this is a multiple choice question"""
        return len(self.options) > 0


# Example instances for testing
EXAMPLE_PROJECT_REQUIREMENTS = ProjectRequirements(
    application_type=ApplicationType.WEB_APP,
    user_scale=UserScale.MEDIUM,
    ai_integration=True,
    real_time_features=False,
    mobile_support=True,
    user_experience={
        "frontend": ExperienceLevel.INTERMEDIATE,
        "backend": ExperienceLevel.BEGINNER,
        "database": ExperienceLevel.INTERMEDIATE
    },
    team_size=3,
    performance_priorities=["speed", "scalability"],
    project_timeline="6 months"
)

EXAMPLE_TECH_RECOMMENDATION = TechRecommendation(
    component=TechCategory.FRONTEND,
    technology="React.js",
    version="18.x",
    rationale="React provides excellent component reusability, large ecosystem, and strong community support. Perfect for intermediate-level developers.",
    confidence=0.85,
    learning_curve=ExperienceLevel.INTERMEDIATE,
    cost_impact="low",
    scalability_rating=0.9,
    alternatives=["Vue.js", "Angular", "Svelte"],
    pros=["Large ecosystem", "Component reusability", "Strong community"],
    cons=["Learning curve", "Rapid updates"]
)