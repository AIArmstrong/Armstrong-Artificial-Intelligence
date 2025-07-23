---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-20250719-tech-stack-expert
project_name: tech_stack_expert_agent
priority: low
auto_scaffold: true
integrations: [n8n, openrouter, supabase]
estimated_effort: "2-3 hours"
complexity: simple
tags: ["#tech-recommendations", "#conversational", "#guided-flow", "#n8n"]
created: 2025-07-19
author: aai-system
---

# Tech Stack Expert Agent - Architecture Recommendation System

## Purpose
Implement a conversational agent that provides tailored technology stack recommendations through guided conversations, helping users make informed architectural decisions.

## Goal
Build an intelligent recommendation system that conducts structured conversations to understand project needs and provides personalized tech stack guidance.

## Why
- **Architectural Intelligence**: Enhances AAI's decision-making capabilities
- **Guided Conversations**: Structured approach to requirement gathering
- **Context Awareness**: Considers user experience and project constraints
- **AAI Integration**: Supports "architectural decisions" trigger requirements

## What
- Conversational flow for requirement gathering
- Tech stack recommendation engine
- Context-aware suggestions based on user experience
- Integration with AAI decision-making systems

### Success Criteria
- [ ] Guided conversation flow for requirement gathering
- [ ] Context-aware tech stack recommendations
- [ ] Integration with AAI brain modules
- [ ] Confidence scoring for recommendations

## Implementation Blueprint

```yaml
Task 1: Build Conversation Engine
CREATE agents/tech-expert/conversation_engine.py:
  - IMPLEMENT guided conversation flow
  - ADD context gathering and analysis
  - INCLUDE user experience assessment

Task 2: Create Recommendation System
CREATE agents/tech-expert/recommender.py:
  - IMPLEMENT tech stack suggestion logic
  - ADD recommendation confidence scoring
  - INCLUDE rationale generation

Task 3: Build N8N Integration
CREATE n8n/tech_expert_workflow.py:
  - IMPLEMENT N8N workflow patterns
  - ADD conversation state management
  - INCLUDE recommendation delivery

Task 4: Add AAI Integration
CREATE brain/modules/tech-stack-expert.py:
  - FOLLOW AAI brain module patterns
  - ADD architectural decision support
  - INCLUDE recommendation learning
```

### Data Models

```python
class ProjectRequirements(BaseModel):
    application_type: str
    user_scale: str
    ai_integration: bool
    user_experience: Dict[str, int]

class TechRecommendation(BaseModel):
    component: str
    technology: str
    rationale: str
    confidence: float = Field(ge=0.70, le=0.95)
```

---

**Final Score**: 6/10 - Simple conversational agent with clear patterns.