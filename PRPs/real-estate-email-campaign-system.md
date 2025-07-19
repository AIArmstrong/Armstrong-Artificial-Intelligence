---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-real-estate-email-campaign-20250716
project_name: real_estate_email_campaign_system
priority: high
auto_scaffold: true
integrations: [n8n, openrouter, supabase, gmail_api]
estimated_effort: "12-16 hours"
complexity: enterprise
tags: ["#real-estate", "#email-automation", "#ai-personalization", "#n8n-workflows", "#lead-nurturing"]
created: 2025-07-16
author: claude-code
---

# Real Estate Failed Listing Email Campaign System

## Purpose
Enterprise-grade automated email campaign system targeting realtors with failed/terminated listings, offering 65% of listing price with 1.25% commission. Utilizes n8n orchestration with AI agents for email management and intelligent negotiation handling. This PRP provides comprehensive context for implementing a production-ready system that can generate working code through iterative refinement.

## Core Principles
1. **Context is King**: All necessary documentation, patterns, and implementation details included
2. **Validation Loops**: Executable tests and compliance checks throughout development
3. **Information Dense**: Leverages existing AAI codebase patterns and external best practices
4. **Progressive Success**: Modular implementation with validation at each stage
5. **Global rules**: Strict adherence to CLAUDE.md guidelines and real estate compliance laws
6. **Intelligence Integration**: Deep integration with AAI brain modules for continuous learning

---

## Goal
Build a comprehensive automated real estate email campaign system that:
- Identifies failed/terminated property listings from existing database
- Automatically generates AI-personalized email campaigns targeting listing agents
- Orchestrates multi-stage negotiation workflows through n8n automation
- Handles email responses using OpenRouter LLM integration for intelligent parsing
- Tracks engagement metrics and conversion rates through Supabase analytics
- Maintains full legal compliance with CAN-SPAM, GDPR, and real estate regulations

## Why
- **Business Impact**: Automate acquisition of distressed real estate properties at 65% market value
- **Efficiency Gains**: Replace manual outreach with intelligent automation handling 1000+ contacts daily
- **Revenue Generation**: 1.25% commission structure on successful acquisitions creates scalable income
- **Market Opportunity**: Failed listings represent undervalued opportunities for quick acquisition
- **Integration Value**: Leverages existing AAI infrastructure (n8n, OpenRouter, Supabase) for rapid deployment
- **Learning Platform**: Establishes foundation for advanced real estate automation workflows

## What
A multi-component system providing:

### User-Visible Behavior
- **Campaign Dashboard**: Web interface displaying campaign performance, response rates, and deal pipeline
- **Automated Email Sequences**: AI-generated personalized emails sent via n8n workflows
- **Response Management**: Intelligent categorization and handling of agent replies
- **Negotiation Tracking**: Real-time monitoring of offer status and counter-proposals
- **Contract Generation**: Automated creation of purchase contracts upon acceptance
- **Analytics Reporting**: Comprehensive metrics on campaign effectiveness and ROI

### Technical Requirements
- **n8n Workflow Integration**: RESTful API communication with local n8n server
- **OpenRouter AI Processing**: Multi-model LLM integration for content generation and response analysis
- **Gmail OAuth Authentication**: Secure email sending through personal Google account
- **Supabase Data Management**: Contact database, campaign analytics, and response tracking
- **Compliance Framework**: Built-in CAN-SPAM and GDPR compliance mechanisms
- **Real-time Monitoring**: WebSocket integration for live campaign status updates

### Success Criteria
- [ ] Successfully deploy n8n workflows for email automation
- [ ] Integrate OpenRouter API for AI-powered email personalization (>80% relevance score)
- [ ] Implement Gmail OAuth with 99.9% delivery rate
- [ ] Achieve <2% unsubscribe rate through quality content and targeting
- [ ] Process agent responses with 95% accuracy in intent classification
- [ ] Generate legally compliant contracts automatically upon offer acceptance
- [ ] Maintain full audit trail for compliance reporting
- [ ] Demonstrate 15%+ response rate on initial email campaigns

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window

- url: https://docs.n8n.io/
  why: Complete n8n workflow automation documentation for email campaigns
  critical: Webhook configuration, API authentication patterns

- url: https://docs.n8n.io/integrations/send-email/
  why: Email integration patterns and SMTP configuration
  critical: Gmail OAuth setup and bulk email handling

- url: https://openrouter.ai/docs/quickstart
  why: OpenRouter API integration for AI email personalization
  critical: Authentication, model selection, and cost management

- url: https://openrouter.ai/docs/api-reference/overview
  why: Complete API reference for LLM integration
  critical: Request/response formats and error handling

- url: https://developers.google.com/gmail/api/quickstart/python
  why: Gmail API Python integration patterns
  critical: OAuth2 setup and email sending capabilities

- url: https://docs.python.org/3/library/smtplib.html
  why: Python SMTP library for email automation
  critical: SMTP authentication and bulk email handling

- file: /mnt/c/Users/Brandon/AAI/brain/modules/openrouter/router_client.py
  why: Existing OpenRouter integration pattern with cost tracking
  critical: Rate limiting, model selection, and error handling patterns

- file: /mnt/c/Users/Brandon/AAI/supabase/modules/supabase_migration.py
  why: Database integration patterns for contact management
  critical: JSONB usage for flexible data storage

- file: /mnt/c/Users/Brandon/AAI/research/n8n/01_n8n_api_reference.md
  why: AAI-specific n8n integration documentation
  critical: API authentication and workflow management patterns

- docfile: /mnt/c/Users/Brandon/AAI/ideas/idea_registry.md
  why: Original feature specifications and technical requirements
  critical: Business rules, commission structure, and automation goals
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "Real estate email marketing compliance CAN-SPAM GDPR"
    depth: 15
    target_folder: "research/compliance/"
    findings: "Requires opt-out mechanisms, physical address, clear sender identification"
  
  - topic: "n8n email automation workflows API integration"
    depth: 12
    target_folder: "research/automation/"
    findings: "Supports Gmail OAuth, SMTP, webhooks, and workflow orchestration"
  
  - topic: "OpenRouter LLM email personalization examples"
    depth: 10
    target_folder: "research/ai-integration/"
    findings: "Multi-model support, cost-effective routing, and prompt engineering patterns"
  
  - topic: "Real estate lead nurturing drip campaigns"
    depth: 8
    target_folder: "research/marketing/"
    findings: "Segmentation strategies, timing optimization, and conversion tracking"
```

### Example Pattern References
```yaml
example_references:
  - brain/modules/openrouter/router_client.py
  - supabase/modules/supabase_migration.py
  - PRPs/EXAMPLE_multi_agent_prp.md
  - research/n8n/01_n8n_api_reference.md
pattern_similarity_threshold: 0.8
fallback_action: "create_new_example"
```

### Current Codebase tree
```bash
/mnt/c/Users/Brandon/AAI/
├── brain/
│   └── modules/
│       └── openrouter/
│           ├── router_client.py          # OpenRouter integration with cost tracking
│           ├── embeddings.py             # Text embedding generation
│           └── contradictions.py         # Response validation
├── supabase/
│   ├── modules/
│   │   ├── supabase_migration.py         # Database operations
│   │   ├── supabase_search.py            # Full-text search capabilities
│   │   └── supabase_auto_offload.py      # Automated data management
│   └── scripts/
│       ├── setup_supabase_schema.sql     # Database schema setup
│       └── test_connection.py            # Connection validation
├── research/
│   └── n8n/
│       └── 01_n8n_api_reference.md       # n8n API documentation
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md                   # PRP template structure
│   └── EXAMPLE_multi_agent_prp.md        # Multi-agent implementation example
└── ideas/
    └── idea_registry.md                  # Original feature specifications
```

### Desired Codebase tree with files to be added
```bash
/mnt/c/Users/Brandon/AAI/
├── projects/
│   └── real_estate_campaign/
│       ├── src/
│       │   ├── __init__.py
│       │   ├── main.py                   # Application entry point
│       │   ├── config/
│       │   │   ├── __init__.py
│       │   │   ├── settings.py           # Environment configuration
│       │   │   └── n8n_workflows.json    # n8n workflow definitions
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── contact.py            # Pydantic contact models
│       │   │   ├── campaign.py           # Campaign data models
│       │   │   ├── response.py           # Email response models
│       │   │   └── analytics.py          # Analytics data models
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   ├── n8n_client.py         # n8n API integration
│       │   │   ├── openrouter_service.py # AI content generation
│       │   │   ├── gmail_service.py      # Gmail API wrapper
│       │   │   ├── supabase_service.py   # Database operations
│       │   │   └── compliance_service.py # Legal compliance validation
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   ├── routes.py             # FastAPI route definitions
│       │   │   ├── auth.py               # Authentication middleware
│       │   │   └── webhooks.py           # n8n webhook handlers
│       │   ├── workflows/
│       │   │   ├── __init__.py
│       │   │   ├── email_campaign.py     # Campaign orchestration
│       │   │   ├── response_handler.py   # Response processing
│       │   │   └── contract_generator.py # Legal document generation
│       │   └── utils/
│       │       ├── __init__.py
│       │       ├── validators.py         # Input validation
│       │       ├── formatters.py         # Data formatting utilities
│       │       └── logger.py             # Logging configuration
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── test_services.py          # Service layer tests
│       │   ├── test_workflows.py         # Workflow logic tests
│       │   ├── test_compliance.py        # Legal compliance tests
│       │   └── test_integration.py       # End-to-end tests
│       ├── docs/
│       │   ├── api_reference.md          # API documentation
│       │   ├── deployment_guide.md       # Deployment instructions
│       │   └── compliance_checklist.md   # Legal compliance guide
│       ├── scripts/
│       │   ├── setup_database.py         # Database initialization
│       │   ├── deploy_workflows.py       # n8n workflow deployment
│       │   └── generate_test_data.py     # Test data generation
│       ├── requirements.txt              # Python dependencies
│       ├── .env.example                  # Environment variables template
│       └── README.md                     # Project documentation
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: OpenRouter rate limiting and cost management
# Pattern from brain/modules/openrouter/router_client.py
class OpenRouterClient:
    def __init__(self):
        self.requests_per_minute = 60  # Built-in rate limiting
        self.daily_cost_limit = 5.00   # $5 daily limit
        self.max_retries = 3           # Exponential backoff for failures

# CRITICAL: Supabase JSONB usage for flexible real estate data
# Pattern from supabase/modules/supabase_migration.py
contact_schema = {
    "property_preferences": "JSONB",  # Flexible property criteria storage
    "lead_score": "INTEGER",          # Scoring algorithm results
    "campaign_status": "TEXT"         # Current engagement status
}

# CRITICAL: n8n webhook authentication pattern
# n8n requires specific header authentication for webhook triggers
headers = {
    "X-N8N-API-KEY": os.getenv("N8N_API_KEY"),
    "Content-Type": "application/json"
}

# CRITICAL: Gmail API OAuth2 scopes for email sending
# Requires specific scope permissions for automated email sending
GMAIL_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify'
]

# CRITICAL: CAN-SPAM compliance requirements
# Every email must include physical address and unsubscribe link
compliance_requirements = {
    "physical_address": "Required in footer",
    "unsubscribe_link": "One-click unsubscribe mechanism",
    "sender_identification": "Clear sender name and contact info",
    "subject_line_accuracy": "Non-deceptive subject lines"
}
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "brain/modules/openrouter"
      reason: "Existing AI integration with cost tracking and rate limiting"
    - module: "supabase/modules"
      reason: "Database operations and migration patterns"
    - file: "research/n8n/01_n8n_api_reference.md"
      reason: "n8n integration documentation and patterns"
  external:
    - package: "fastapi >= 0.104.0"
      reason: "Web API framework for dashboard and webhooks"
    - package: "pydantic >= 2.5.0"
      reason: "Data validation and settings management"
    - package: "supabase >= 2.0.0"
      reason: "Database client for contact and analytics storage"
    - package: "google-auth-oauthlib >= 1.2.0"
      reason: "Gmail OAuth authentication"
    - package: "google-api-python-client >= 2.110.0"
      reason: "Gmail API integration for email sending"
    - package: "httpx >= 0.25.0"
      reason: "Async HTTP client for n8n and OpenRouter APIs"
    - package: "python-multipart >= 0.0.6"
      reason: "Form data handling for file uploads"
    - package: "uvicorn >= 0.24.0"
      reason: "ASGI server for FastAPI application"
  n8n_server:
    - service: "n8n workflow automation"
      url: "https://n8n.olympus-council.xyz"
      local_url: "http://142.93.74.22:5678"
      reason: "Remote n8n deployment for workflow orchestration"
      access: "SSH key authentication via 142.93.74.22"
      deployment: "Docker container in /root/n8n-project"
  conflicts:
    - issue: "Gmail API rate limits vs. bulk email requirements"
      mitigation: "Implement queue system with 250 emails/day limit"
    - issue: "n8n webhook timeout vs. OpenRouter API response time"
      mitigation: "Async processing with webhook acknowledgment pattern"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "brain/modules/openrouter/router_client.py"
    - "supabase/modules/supabase_migration.py"
    - "research/n8n/01_n8n_api_reference.md"
  api_documentation_current:
    - check: "OpenRouter API docs accessed within 7 days"
    - check: "Gmail API documentation current version"
    - check: "n8n API reference matches deployed version"
  environment_variables:
    - "OPENROUTER_API_KEY"
    - "N8N_API_KEY"
    - "SUPABASE_URL"
    - "SUPABASE_ANON_KEY"
    - "GMAIL_CLIENT_ID"
    - "GMAIL_CLIENT_SECRET"
```

## Implementation Blueprint

### Data Models and Structure

Create comprehensive data models ensuring type safety and real estate domain consistency:

```python
# models/contact.py - Real Estate Contact Management
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class PropertyType(str, Enum):
    HOUSE = "house"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    LAND = "land"
    COMMERCIAL = "commercial"

class ContactStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    UNSUBSCRIBED = "unsubscribed"

class RealEstateContact(BaseModel):
    id: Optional[str] = Field(None, description="UUID primary key")
    email: EmailStr = Field(..., description="Agent email address")
    name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, regex=r"^\+?1?\d{9,15}$")
    agency: Optional[str] = Field(None, max_length=200)
    license_number: Optional[str] = Field(None, max_length=50)
    
    # Property and preference data
    failed_listings: List[Dict[str, Any]] = Field(default_factory=list)
    property_preferences: Dict[str, Any] = Field(default_factory=dict)
    lead_score: int = Field(default=0, ge=0, le=100)
    
    # Campaign tracking
    campaign_status: ContactStatus = Field(default=ContactStatus.NEW)
    last_contacted: Optional[datetime] = None
    response_count: int = Field(default=0, ge=0)
    unsubscribed: bool = Field(default=False)
    
    # Compliance tracking
    consent_given: bool = Field(default=False)
    consent_date: Optional[datetime] = None
    opt_out_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# models/campaign.py - Email Campaign Management
class CampaignType(str, Enum):
    INITIAL_OUTREACH = "initial_outreach"
    FOLLOW_UP = "follow_up"
    NEGOTIATION = "negotiation"
    CONTRACT_FOLLOW_UP = "contract_follow_up"

class EmailCampaign(BaseModel):
    id: Optional[str] = Field(None, description="UUID primary key")
    name: str = Field(..., min_length=1, max_length=200)
    campaign_type: CampaignType
    
    # Campaign configuration
    target_segments: List[str] = Field(default_factory=list)
    email_template_id: str
    n8n_workflow_id: str
    
    # Offer parameters
    offer_percentage: float = Field(default=0.65, ge=0.1, le=1.0)
    commission_percentage: float = Field(default=0.0125, ge=0.001, le=0.1)
    
    # Scheduling and automation
    schedule_config: Dict[str, Any] = Field(default_factory=dict)
    automation_rules: Dict[str, Any] = Field(default_factory=dict)
    
    # Analytics and tracking
    sent_count: int = Field(default=0, ge=0)
    delivered_count: int = Field(default=0, ge=0)
    opened_count: int = Field(default=0, ge=0)
    clicked_count: int = Field(default=0, ge=0)
    responded_count: int = Field(default=0, ge=0)
    converted_count: int = Field(default=0, ge=0)
    
    # Status and lifecycle
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# models/response.py - Email Response Processing
class ResponseType(str, Enum):
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    COUNTER_OFFER = "counter_offer"
    REQUEST_INFO = "request_info"
    UNSUBSCRIBE = "unsubscribe"
    AUTO_REPLY = "auto_reply"
    SPAM_COMPLAINT = "spam_complaint"

class EmailResponse(BaseModel):
    id: Optional[str] = Field(None, description="UUID primary key")
    contact_id: str = Field(..., description="Reference to RealEstateContact")
    campaign_id: str = Field(..., description="Reference to EmailCampaign")
    
    # Email metadata
    gmail_message_id: str
    subject: str = Field(..., max_length=500)
    sender_email: EmailStr
    received_at: datetime
    
    # Content and classification
    body_text: str
    body_html: Optional[str] = None
    response_type: ResponseType
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    
    # AI analysis results
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    intent_classification: Dict[str, Any] = Field(default_factory=dict)
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    
    # Processing status
    processed: bool = Field(default=False)
    requires_human_review: bool = Field(default=False)
    follow_up_scheduled: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### List of Tasks to be Completed (In Order)

```yaml
Task 1: Environment Setup and Core Infrastructure
MODIFY requirements.txt:
  - ADD all required packages with specific versions
  - INCLUDE n8n client dependencies and OpenRouter requirements

CREATE src/config/settings.py:
  - MIRROR pattern from: brain/modules/openrouter/router_client.py
  - IMPLEMENT Pydantic Settings for environment configuration
  - INCLUDE validation for all required API keys and endpoints

CREATE src/config/n8n_workflows.json:
  - DEFINE n8n workflow templates for email automation
  - INCLUDE webhook configurations and trigger definitions
  - SPECIFY email template and response handling workflows

Task 2: Database Schema and Models Implementation
MODIFY supabase/scripts/setup_supabase_schema.sql:
  - ADD real estate campaign tables based on Pydantic models
  - INCLUDE proper indexing for email addresses and campaign tracking
  - IMPLEMENT JSONB columns for flexible property preferences storage

CREATE src/models/ directory with all Pydantic models:
  - FOLLOW pattern from: existing AAI model structure
  - IMPLEMENT comprehensive validation and type safety
  - ENSURE compliance with real estate data requirements

Task 3: OpenRouter AI Service Integration
CREATE src/services/openrouter_service.py:
  - EXTEND pattern from: brain/modules/openrouter/router_client.py
  - IMPLEMENT email personalization and response analysis
  - ADD cost tracking and rate limiting for production use

CREATE email personalization prompts and templates:
  - IMPLEMENT real estate specific prompt engineering
  - INCLUDE property valuation and negotiation language
  - ENSURE compliance with marketing communication standards

Task 4: Gmail API Service Implementation
CREATE src/services/gmail_service.py:
  - FOLLOW pattern from: research findings on Gmail OAuth integration
  - IMPLEMENT bulk email sending with rate limiting
  - ADD proper error handling and retry mechanisms

IMPLEMENT OAuth2 authentication flow:
  - CONFIGURE Google Cloud Platform credentials
  - IMPLEMENT token refresh and secure storage
  - ENSURE proper scope permissions for email sending

Task 5: n8n Workflow Integration
CREATE src/services/n8n_client.py:
  - MIRROR pattern from: research/n8n/01_n8n_api_reference.md
  - IMPLEMENT workflow deployment and execution management
  - ADD webhook handling for response processing
  - CONNECT to n8n server at https://n8n.olympus-council.xyz (port 5678)
  - USE SSH key authentication for server access via 142.93.74.22

DEPLOY n8n workflows:
  - CREATE email campaign automation workflows
  - IMPLEMENT response categorization and routing
  - CONFIGURE timing and scheduling logic
  - NOTE: n8n runs in Docker container managed by docker-compose in /root/n8n-project

Task 6: Supabase Database Service
CREATE src/services/supabase_service.py:
  - EXTEND pattern from: supabase/modules/supabase_migration.py
  - IMPLEMENT contact management and campaign analytics
  - ADD full-text search for contact and property data

IMPLEMENT data migration and seeding:
  - CREATE scripts for contact import from existing database
  - IMPLEMENT campaign analytics table structure
  - ADD compliance tracking and audit trail functionality

Task 7: Compliance and Legal Framework
CREATE src/services/compliance_service.py:
  - IMPLEMENT CAN-SPAM Act compliance validation
  - ADD GDPR consent management and data protection
  - INCLUDE unsubscribe handling and audit logging

IMPLEMENT compliance validation middleware:
  - VALIDATE all outgoing emails for legal requirements
  - ADD automated unsubscribe link generation
  - ENSURE proper sender identification and physical address

Task 8: Campaign Workflow Orchestration
CREATE src/workflows/email_campaign.py:
  - IMPLEMENT campaign lifecycle management
  - ADD segmentation and targeting logic
  - INCLUDE performance tracking and optimization

CREATE src/workflows/response_handler.py:
  - IMPLEMENT AI-powered response classification
  - ADD automatic follow-up scheduling
  - INCLUDE escalation rules for human review

Task 9: API and Web Interface
CREATE src/api/routes.py:
  - IMPLEMENT FastAPI routes for campaign management
  - ADD webhook endpoints for n8n integration
  - INCLUDE real-time analytics and monitoring

CREATE dashboard and monitoring interface:
  - IMPLEMENT campaign performance visualization
  - ADD contact management interface
  - INCLUDE compliance reporting and audit trails

Task 10: Testing and Validation Framework
CREATE comprehensive test suite:
  - IMPLEMENT unit tests for all services and workflows
  - ADD integration tests for external API interactions
  - INCLUDE compliance testing for legal requirements

IMPLEMENT end-to-end validation:
  - CREATE test campaigns with synthetic data
  - VALIDATE email delivery and response processing
  - ENSURE performance meets specified metrics
```

### Per Task Pseudocode

```python
# Task 3: OpenRouter AI Service Integration
class OpenRouterEmailService:
    def __init__(self):
        # PATTERN: Inherit from existing OpenRouter client
        self.client = OpenRouterClient()  # from brain/modules/openrouter/
        self.models = {
            "fast": "openai/gpt-4o-mini",      # Cost-effective for bulk operations
            "quality": "anthropic/claude-3-sonnet"  # High-quality for negotiations
        }
    
    async def generate_personalized_email(self, contact: RealEstateContact, 
                                        property_data: dict, 
                                        campaign_type: str) -> str:
        # PATTERN: Use existing cost tracking and rate limiting
        async with self.client.rate_limiter.acquire():
            prompt = self._build_email_prompt(contact, property_data, campaign_type)
            
            # CRITICAL: Track costs and implement fallback
            try:
                response = await self.client.chat_completion(
                    model=self.models["quality"],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                
                # GOTCHA: Always validate AI output for compliance
                email_content = self._validate_compliance(response.content)
                return email_content
                
            except CostLimitExceeded:
                # PATTERN: Fallback to cheaper model
                return await self._generate_with_fallback(prompt)
    
    def _build_email_prompt(self, contact, property_data, campaign_type):
        # CRITICAL: Include compliance requirements in every prompt
        base_prompt = f"""
        Context: You are writing a professional real estate acquisition email.
        
        Recipient: {contact.name} from {contact.agency}
        Property: {property_data['address']} - Failed listing at ${property_data['price']:,}
        Offer: 65% of listing price (${property_data['price'] * 0.65:,.0f})
        Commission: 1.25% of original listing price
        
        Requirements:
        - Professional and respectful tone
        - Reference specific property details
        - Include clear offer terms
        - Add required CAN-SPAM compliance footer
        - Maximum 200 words
        
        CRITICAL: Include unsubscribe link and physical address in footer.
        """
        return base_prompt

# Task 5: n8n Workflow Integration
class N8NWorkflowManager:
    def __init__(self):
        self.base_url = "https://n8n.olympus-council.xyz/api/v1"
        self.local_url = "http://142.93.74.22:5678/api/v1" 
        self.api_key = os.getenv("N8N_API_KEY")
        self.headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        # SSH access for server management if needed
        self.ssh_host = "142.93.74.22"
        self.ssh_key_path = "~/.ssh/droplet_key"
    
    async def deploy_campaign_workflow(self, campaign: EmailCampaign) -> str:
        # PATTERN: Use n8n API for workflow deployment
        workflow_definition = {
            "name": f"RealEstate_Campaign_{campaign.id}",
            "nodes": [
                {
                    "name": "Schedule Trigger",
                    "type": "n8n-nodes-base.cron",
                    "parameters": {"rule": campaign.schedule_config}
                },
                {
                    "name": "Fetch Contacts",
                    "type": "n8n-nodes-base.httpRequest",
                    "parameters": {
                        "url": f"http://localhost:8000/api/contacts/segment/{campaign.target_segments}",
                        "method": "GET"
                    }
                },
                {
                    "name": "Generate Email Content",
                    "type": "n8n-nodes-base.httpRequest", 
                    "parameters": {
                        "url": "http://localhost:8000/api/ai/generate-email",
                        "method": "POST"
                    }
                },
                {
                    "name": "Send Email",
                    "type": "n8n-nodes-base.gmail",
                    "parameters": {"operation": "send"}
                }
            ]
        }
        
        # CRITICAL: Handle n8n API rate limits and errors
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/workflows",
                headers=self.headers,
                json=workflow_definition,
                timeout=30.0
            )
            
        if response.status_code != 201:
            raise N8NDeploymentError(f"Failed to deploy workflow: {response.text}")
            
        workflow_id = response.json()["id"]
        return workflow_id

# Task 7: Compliance and Legal Framework
class ComplianceService:
    def __init__(self):
        self.required_elements = {
            "physical_address": "123 Main St, Your City, ST 12345",
            "unsubscribe_text": "To unsubscribe, click here:",
            "sender_identification": "From: Real Estate Acquisitions Team"
        }
    
    def validate_email_compliance(self, email_content: str, 
                                recipient_email: str) -> dict:
        """
        CRITICAL: Validate all outgoing emails for CAN-SPAM compliance
        """
        validation_results = {
            "compliant": True,
            "issues": [],
            "warnings": []
        }
        
        # PATTERN: Check for required CAN-SPAM elements
        if not self._contains_physical_address(email_content):
            validation_results["compliant"] = False
            validation_results["issues"].append("Missing physical address")
        
        if not self._contains_unsubscribe_link(email_content):
            validation_results["compliant"] = False
            validation_results["issues"].append("Missing unsubscribe mechanism")
        
        if not self._validate_subject_line_accuracy(email_content):
            validation_results["warnings"].append("Subject line may be misleading")
        
        # GOTCHA: Log all compliance checks for audit trail
        self._log_compliance_check(recipient_email, validation_results)
        
        return validation_results
    
    def generate_compliant_footer(self, recipient_email: str) -> str:
        # PATTERN: Generate standardized compliant footer
        unsubscribe_url = f"https://your-domain.com/unsubscribe?email={recipient_email}"
        
        footer = f"""
        
        ---
        {self.required_elements["sender_identification"]}
        {self.required_elements["physical_address"]}
        
        {self.required_elements["unsubscribe_text"]} {unsubscribe_url}
        
        This email was sent in compliance with CAN-SPAM regulations.
        """
        
        return footer
```

### Integration Points
```yaml
DATABASE:
  - migration: "Add real_estate_contacts, email_campaigns, campaign_analytics tables"
  - indexes: "CREATE INDEX idx_contact_email ON real_estate_contacts(email)"
  - indexes: "CREATE INDEX idx_campaign_status ON real_estate_contacts(campaign_status)"
  
CONFIG:
  - add to: src/config/settings.py
  - pattern: "N8N_API_KEY = Field(..., env='N8N_API_KEY')"
  - pattern: "OPENROUTER_API_KEY = Field(..., env='OPENROUTER_API_KEY')"
  
ROUTES:
  - add to: src/api/routes.py
  - pattern: "router.include_router(campaign_router, prefix='/campaigns')"
  - pattern: "router.include_router(webhook_router, prefix='/webhooks')"

N8N_WORKFLOWS:
  - deploy: "Email campaign automation workflow"
  - deploy: "Response processing workflow" 
  - deploy: "Follow-up scheduling workflow"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check src/ --fix                    # Auto-fix formatting and style issues
mypy src/                               # Type checking for all modules
python -m pytest tests/test_models.py  # Validate Pydantic model definitions

# Expected: No errors. If errors, READ the error message and fix systematically.
```

### Level 2: Unit Tests
```python
# CREATE test_services.py with comprehensive test coverage:

def test_openrouter_email_generation():
    """Test AI-powered email personalization"""
    service = OpenRouterEmailService()
    contact = RealEstateContact(
        email="agent@realty.com",
        name="John Smith",
        agency="Prime Realty"
    )
    property_data = {
        "address": "123 Oak Street",
        "price": 400000,
        "listing_date": "2024-01-15"
    }
    
    email = await service.generate_personalized_email(
        contact, property_data, "initial_outreach"
    )
    
    assert "John Smith" in email
    assert "123 Oak Street" in email
    assert "$260,000" in email  # 65% of $400,000
    assert "unsubscribe" in email.lower()

def test_compliance_validation():
    """Test CAN-SPAM compliance checking"""
    compliance = ComplianceService()
    
    # Test non-compliant email
    bad_email = "Hi, want to sell your house?"
    result = compliance.validate_email_compliance(bad_email, "test@example.com")
    assert not result["compliant"]
    assert "Missing physical address" in result["issues"]
    
    # Test compliant email
    good_email = compliance.add_compliance_footer(bad_email, "test@example.com")
    result = compliance.validate_email_compliance(good_email, "test@example.com")
    assert result["compliant"]

def test_n8n_workflow_deployment():
    """Test n8n integration and workflow management"""
    manager = N8NWorkflowManager()
    campaign = EmailCampaign(
        name="Test Campaign",
        campaign_type=CampaignType.INITIAL_OUTREACH,
        target_segments=["high_value_leads"]
    )
    
    workflow_id = await manager.deploy_campaign_workflow(campaign)
    assert workflow_id is not None
    assert len(workflow_id) > 0
    
    # Verify workflow is active
    status = await manager.get_workflow_status(workflow_id)
    assert status["active"] is True
```

```bash
# Run comprehensive test suite:
python -m pytest tests/ -v --cov=src --cov-report=html
# Target: >85% code coverage with all tests passing
```

### Level 3: Integration Tests
```bash
# Start all required services
docker-compose up -d supabase  # Start Supabase locally
n8n start --tunnel            # Start n8n with webhook tunneling
uvicorn src.main:app --reload  # Start FastAPI application

# Test complete workflow end-to-end
python scripts/test_campaign_flow.py

# Expected output:
# ✓ Database connection established
# ✓ n8n workflows deployed successfully  
# ✓ OpenRouter API responding
# ✓ Gmail OAuth authenticated
# ✓ Test campaign sent to synthetic contacts
# ✓ Response processing working
# ✓ Compliance validation passing
```

### Level 4: Compliance and Legal Validation
```yaml
compliance_tests:
  can_spam:
    - script: "python tests/test_can_spam_compliance.py"
    - requirements: ["physical_address_present", "unsubscribe_mechanism", "accurate_subject_lines"]
  gdpr:
    - script: "python tests/test_gdpr_compliance.py" 
    - requirements: ["consent_tracking", "data_deletion", "privacy_controls"]
  real_estate:
    - script: "python tests/test_real_estate_regulations.py"
    - requirements: ["license_validation", "fair_housing_compliance", "disclosure_requirements"]
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  technical_performance:
    - metric: "Email Delivery Rate"
      target: "≥ 99%"
      measurement: "Gmail API delivery confirmations"
      validation_gate: "integration_tests"
    - metric: "AI Response Classification Accuracy"
      target: "≥ 95%"
      measurement: "Manual validation of 100 sample responses"
      validation_gate: "ai_validation_tests"
    - metric: "n8n Workflow Execution Success"
      target: "≥ 98%"
      measurement: "n8n execution logs and error rates"
      validation_gate: "workflow_tests"
  
  business_performance:
    - metric: "Email Response Rate"
      target: "≥ 15%"
      measurement: "Responses received / Emails sent"
      validation_gate: "campaign_analytics"
    - metric: "Lead Conversion Rate"
      target: "≥ 3%"
      measurement: "Accepted offers / Total outreach"
      validation_gate: "business_analytics"
    - metric: "Compliance Adherence"
      target: "100%"
      measurement: "Zero compliance violations or penalties"
      validation_gate: "compliance_audits"
  
  operational_efficiency:
    - metric: "Cost Per Acquisition"
      target: "≤ $50"
      measurement: "(API costs + operational costs) / Properties acquired"
      validation_gate: "financial_tracking"
    - metric: "Processing Time"
      target: "≤ 5 minutes"
      measurement: "Contact import to email sent duration"
      validation_gate: "performance_tests"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md"
  success_tracker: "brain/modules/score-tracker.md" 
  auto_tag: ["#real-estate", "#email-automation", "#ai-integration"]
  promotion_threshold: 4.5  # Auto-promote to production if score ≥ 4.5
  
aai_integration:
  brain_modules:
    - "intent-engine.md"        # For response classification
    - "unified-analytics.py"    # For campaign performance tracking
    - "contradiction-check.py"  # For compliance validation
  auto_triggers:
    - on_completion: "update_real_estate_patterns"
    - on_success: "generate_automation_sop"
    - on_failure: "log_integration_issues"
```

## Final Validation Checklist
- [ ] All tests pass: `python -m pytest tests/ -v --cov=src`
- [ ] No linting errors: `ruff check src/`
- [ ] No type errors: `mypy src/`
- [ ] n8n workflows deployed and active
- [ ] OpenRouter API integration working with cost tracking
- [ ] Gmail OAuth configured and email sending functional  
- [ ] Supabase database schema created and populated
- [ ] Compliance validation passing for CAN-SPAM and GDPR
- [ ] Campaign analytics dashboard operational
- [ ] Response processing accuracy ≥95%
- [ ] End-to-end test campaign successful
- [ ] Performance metrics within target ranges
- [ ] Security audit completed for API credentials
- [ ] Documentation updated with deployment instructions

---

## Anti-Patterns to Avoid
- ❌ Don't bypass compliance validation to speed up development
- ❌ Don't hardcode API credentials or sensitive configuration
- ❌ Don't ignore n8n workflow errors or timeout issues  
- ❌ Don't send emails without proper unsubscribe mechanisms
- ❌ Don't skip rate limiting on OpenRouter API calls
- ❌ Don't process responses without confidence score validation
- ❌ Don't deploy to production without comprehensive compliance testing
- ❌ Don't ignore Gmail API quotas and rate limits
- ❌ Don't store personal data without proper consent tracking
- ❌ Don't bypass existing AAI brain module integration patterns

---

## PRP Confidence Score: 9/10

This PRP provides comprehensive context for one-pass implementation success through:
- ✅ Complete technical specifications based on existing AAI patterns
- ✅ Extensive external research integrated into implementation details  
- ✅ Detailed compliance framework for legal requirements
- ✅ Comprehensive validation gates and success metrics
- ✅ Clear integration points with existing AAI infrastructure
- ✅ Production-ready architecture with error handling and monitoring
- ✅ Detailed task breakdown with implementation order
- ✅ Realistic timelines and complexity assessment

**Confidence reduced by 1 point due to:** Complex integration requirements between multiple external services (n8n, OpenRouter, Gmail API) that may require iterative debugging and optimization.