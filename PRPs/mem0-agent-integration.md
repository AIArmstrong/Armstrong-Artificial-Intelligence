---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-20250719-mem0-agent
project_name: mem0_agent_integration
priority: high
auto_scaffold: true
integrations: [supabase, openrouter, jina-api]
estimated_effort: "6-8 hours"
complexity: moderate
tags: ["#memory", "#agent", "#supabase", "#cross-session", "#auto-learning"]
created: 2025-07-19
author: aai-system
---

# Mem0 Integration - AAI Workflow Memory Enhancement

## Purpose
Enhance ALL existing AAI commands with persistent, cross-session memory capabilities that eliminate repeated research and enhance learning patterns. This addresses AAI's "Auto-learning active" requirement by adding memory intelligence to /generate-prp, /implement, /analyze, and all other workflows.

## Goal
Integrate memory-powered intelligence into AAI's existing Smart Module Loading system so that every command automatically benefits from cross-session memory, research patterns, and user preferences - creating a unified memory substrate for all AAI operations.

## Why

### Core Memory Requirements
- **AAI Gap**: No cross-session memory persistence - system forgets previous research and patterns
- **Research Efficiency**: Eliminates repeated research on same topics, providing 10x faster research workflows  
- **Pattern Learning**: Captures successful implementation patterns for auto-learning enhancement
- **User Personalization**: Remembers user preferences, project contexts, and decision rationales
- **Intelligence Foundation**: Provides memory substrate for all other AAI brain modules

### Enhanced Value Propositions
- **Predictive Intelligence**: Proactive memory suggestions accelerate research initiation
- **Visual Knowledge Navigation**: Memory clusters reveal hidden connections and knowledge gaps
- **Dynamic Knowledge Curation**: Adaptive retention ensures high-value memory preservation
- **Collaborative Enhancement**: Team-based memory building improves organizational intelligence
- **Research Path Exploration**: Rewind capability enables alternative approach investigation
- **Trend Recognition**: Pattern analysis reveals user preferences and research evolution
- **Quality Assurance**: Anomaly detection prevents overlooked opportunities and errors
- **Innovation Catalyst**: Cross-domain insights foster creative problem-solving
- **Communication Enhancement**: Memory storytelling improves knowledge transfer
- **Temporal Intelligence**: Time-aware relevance improves decision timeliness
- **Continuous Learning**: Feedback loops enhance system accuracy and user satisfaction

## What
Build an **enhanced memory intelligence system** that:

### Core Memory Architecture (Existing)
- Stores conversation history and research findings in Supabase
- Retrieves relevant memories based on current queries using vector similarity
- Integrates with AAI's existing Supabase infrastructure  
- Provides both API and Streamlit interfaces
- Maintains user session contexts and project memories
- Supports confidence scoring for memory relevance (70-95% as per AAI standards)

### Enhanced Memory Intelligence Features
- **Proactive Memory Retrieval**: Real-time similarity detection that suggests relevant memories before query completion
- **Contextual Memory Tagging**: LLM-powered extraction of themes, topics, and context tags for precision filtering
- **Memory Cluster Visualization**: Interactive Streamlit interface showing memory relationships and knowledge gaps
- **Adaptive Retention Policy**: Intelligent memory lifecycle management based on retrieval frequency, relevance, and user interaction
- **Collaborative Memory System**: Multi-user memory sharing, annotation, and collective intelligence building
- **Memory "Rewind" Capability**: Session state rollback for exploring alternative research paths
- **Insight-Driven Recommendations**: Auto-generated summaries highlighting trends, patterns, and next steps
- **Anomaly Detection**: Real-time alerts when current research deviates from historical patterns
- **Cross-domain Integration**: Memory search spanning multiple projects for innovation and solution transfer
- **Interactive Storytelling**: Narrative generation from memory clusters for presentations and strategy
- **Temporal Contexting**: Time-aware memory relevance with recency and period-based significance
- **Feedback-Driven Calibration**: Continuous improvement of confidence scoring based on user interactions

### Success Criteria

#### Core Memory Features
- [ ] Cross-session memory persistence in Supabase
- [ ] Memory retrieval with vector similarity search
- [ ] Integration with AAI brain modules (scoring, tagging)
- [ ] Jina API integration for research content scraping
- [ ] Confidence scoring for memory relevance (70-95%)
- [ ] Streamlit interface for memory exploration
- [ ] API endpoints for programmatic access
- [ ] Memory quality scoring and auto-cleanup
- [ ] Integration with existing AAI workflows

#### Enhanced Memory Intelligence
- [ ] **NEW**: Proactive memory retrieval with preemptive suggestion engine
- [ ] **NEW**: Contextual tagging with LLM-based NLP extraction
- [ ] **NEW**: Memory cluster visualization for relationship navigation
- [ ] **NEW**: Adaptive memory retention policy based on relevance scoring
- [ ] **NEW**: Multi-user collaborative memory system
- [ ] **NEW**: Memory "Rewind" feature for session state rollback
- [ ] **NEW**: Memory-driven insight recommendations and trend analysis
- [ ] **NEW**: Real-time memory anomaly detection for pattern deviation
- [ ] **NEW**: Cross-domain memory integration for innovation insights
- [ ] **NEW**: Interactive memory storytelling for narrative summaries
- [ ] **NEW**: Temporal memory contexting with time-aware relevance
- [ ] **NEW**: Memory confidence calibration based on user feedback

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://docs.mem0.ai/introduction
  why: Core mem0 concepts and API patterns
  
- url: https://docs.mem0.ai/platform/quickstart
  why: Implementation setup and authentication
  
- file: /ottomator-agents/mem0-agent/README.md
  why: Project structure and Supabase integration patterns
  
- file: /brain/Claude.md
  why: AAI architecture rules, Supabase integration, neural reasoning requirements
  
- file: /docs/jina-scraping-guide.md
  why: Jina API integration patterns for research content
  
- file: /supabase/modules/supabase_search.py
  why: Existing Supabase search patterns to follow
  
- url: https://python.mem0.ai/
  why: Python library documentation and embedding patterns
  
- docfile: /brain/modules/score-tracker.md
  why: AAI confidence scoring patterns (70-95%)
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "mem0 python library integration"
    depth: 15
    target_folder: "research/mem0-integration"
  - topic: "Supabase vector storage with mem0"  
    depth: 10
    target_folder: "research/supabase-memory"
  - topic: "memory retrieval ranking algorithms"
    depth: 8
    target_folder: "research/memory-algorithms"
```

### Example Pattern References
```yaml
example_references:
  - ottomator-agents/mem0-agent/iterations/v3-streamlit-supabase-mem0.py
  - supabase/modules/supabase_search.py
  - brain/modules/supabase-cache.py
  - brain/modules/openrouter/embeddings.py
pattern_similarity_threshold: 0.85
fallback_action: "create_new_aai_memory_module"
```

### Current Codebase tree (relevant sections)
```bash
AAI/
├── brain/modules/
│   ├── supabase-cache.py
│   ├── openrouter/embeddings.py
│   └── score-tracker.md
├── supabase/
│   ├── modules/supabase_search.py
│   ├── scripts/setup_supabase_schema.sql
│   └── migrations/
├── ottomator-agents/mem0-agent/
│   ├── iterations/
│   │   ├── v1-basic-mem0.py
│   │   ├── v2-supabase-mem0.py
│   │   └── v3-streamlit-supabase-mem0.py
│   └── requirements.txt
└── docs/jina-scraping-guide.md
```

### Desired Codebase tree with files to be added
```bash
AAI/
├── brain/modules/
│   ├── mem0-memory-enhancement.md    # Smart Module Loading integration
│   ├── memory-workflow-integration.py # Memory layer for all commands
│   └── memory-quality-scorer.py     # Memory quality assessment
├── brain/workflows/
│   └── memory-enhanced-commands.md  # Integration patterns for existing commands
├── enhancements/memory/
│   ├── __init__.py
│   ├── memory_layer.py             # Core memory integration layer
│   ├── command_enhancer.py         # Enhances existing AAI commands
│   ├── memory_manager.py           # Memory CRUD operations
│   ├── workflow_memory.py          # Memory context for workflows
│   └── config.py                   # Configuration and environment handling
├── supabase/
│   ├── migrations/
│   │   └── 004_aai_memory_enhancement.sql  # Memory storage schema
│   └── modules/
│       └── memory_storage.py       # Supabase memory operations
└── tests/enhancements/memory/
    ├── test_memory_integration.py
    ├── test_command_enhancement.py
    └── test_workflow_memory.py
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: mem0 requires specific embedding models for compatibility
# Example: OpenAI text-embedding-3-small works well, others may have issues

# CRITICAL: Supabase connection pooling required for memory operations
# Use existing AAI supabase connection patterns

# GOTCHA: mem0 user_id must be consistent across sessions
# Use AAI session management or generate stable user IDs

# GOTCHA: Memory vector dimensions must match between mem0 and Supabase pgvector
# Default OpenAI embeddings are 1536 dimensions

# CRITICAL: Memory search results need confidence scoring per AAI standards
# All memory relevance must include 70-95% confidence scores

# GOTCHA: Large memory collections can slow retrieval
# Implement memory pruning and quality scoring for auto-cleanup
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "brain/modules/supabase-cache.py"
      reason: "Uses existing Supabase connection patterns"
    - module: "brain/modules/openrouter/embeddings.py"  
      reason: "Leverages existing embedding infrastructure"
    - module: "brain/modules/score-tracker.md"
      reason: "Follows AAI confidence scoring standards"
  external:
    - package: "mem0ai ≥ 1.0.0"
    - package: "supabase ≥ 2.0.0"
    - package: "streamlit ≥ 1.28.0"
    - package: "pydantic ≥ 2.0.0"
    - package: "python-dotenv"
  conflicts:
    - issue: "Memory table conflicts with existing Supabase schema"
      mitigation: "Use prefixed table names (aai_mem0_*)"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "supabase/modules/supabase_search.py"
    - "brain/modules/score-tracker.md" 
    - "docs/jina-scraping-guide.md"
  api_documentation_current:
    - check: "mem0.ai documentation updated within 30 days"
  example_relevance:
    - similarity_threshold: 0.85
    - fallback: "Create new AAI-specific memory patterns"
```

## 📦 Implementation Readiness Assessment

### 🚪 Implementation Gates

#### Infrastructure Gates
```yaml
infrastructure_gates:
  network_connectivity:
    - service: "supabase_host"
      test: "ping -c 3 $(echo $SUPABASE_URL | sed 's|https://||' | sed 's|/.*||')"
      expected: "0% packet loss"
      owner: "aai-system"
      
  service_availability:
    - service: "supabase_api" 
      test: "curl -f $SUPABASE_URL/rest/v1/"
      expected: "200 OK"
      fallback: "Use local PostgreSQL with pgvector"
      time_to_fix: "30 minutes"
      owner: "user"
```

#### Credential Gates
```yaml
credential_gates:
  critical:
    - credential: "SUPABASE_KEY"
      location: ".env"
      validation: "curl -H 'apikey: $SUPABASE_KEY' $SUPABASE_URL/rest/v1/"
      expected: "200 or 401 (key format valid)"
      owner: "user"
      time_to_fix: "5 minutes"
      
    - credential: "OPENAI_API_KEY"
      location: ".env"
      validation: "curl -H 'Authorization: Bearer $OPENAI_API_KEY' https://api.openai.com/v1/models"
      expected: "200 OK"
      owner: "user"
      time_to_fix: "5 minutes"
      
    - credential: "JINA_API_KEY"
      location: ".env"
      validation: "curl -H 'Authorization: Bearer $JINA_API_KEY' https://r.jina.ai/"
      expected: "200 or 400 (key format valid)"
      owner: "user"
      time_to_fix: "5 minutes"
```

#### Dependency Gates
```yaml
system_dependencies:
  python_packages:
    - package: "mem0ai>=1.0.0"
      install: "pip install mem0ai"
      validation: "python -c 'import mem0; print(mem0.__version__)'"
      expected: ">=1.0.0"
      
database_gates:
  schema_checks:
    - query: "SELECT to_regclass('public.aai_conversations');"
      expected: "not null"
      fallback: "Run Supabase migration scripts"
      fix_command: "python supabase/scripts/setup_supabase_schema.py"
```

#### Environment Gates
```yaml
environment_validation:
  required_directories:
    - path: "agents/mem0/"
      create_if_missing: true
    - path: "ui/memory/"
      create_if_missing: true
      
  required_files:
    - file: ".env"
      template: ".env.example"
      required_vars: ["SUPABASE_KEY", "SUPABASE_URL", "OPENAI_API_KEY", "JINA_API_KEY"]
```

## Implementation Blueprint

### Data models and structure

Create core memory models ensuring type safety and Supabase compatibility:
```python
# agents/mem0/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MemoryItem(BaseModel):
    """Core memory item with AAI metadata"""
    id: str
    user_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(ge=0.70, le=0.95)  # AAI standard
    quality_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    tags: List[str] = Field(default_factory=list)

class MemoryQuery(BaseModel):
    """Memory search query with AAI context"""
    query: str
    user_id: str
    limit: int = Field(default=10, le=50)
    min_confidence: float = Field(default=0.70, ge=0.70, le=0.95)
    context_tags: List[str] = Field(default_factory=list)
    include_metadata: bool = True

class MemoryResponse(BaseModel):
    """Memory retrieval response with confidence"""
    memories: List[MemoryItem]
    total_found: int
    avg_confidence: float
    search_time_ms: int
    reasoning: str  # WHY these memories were selected
```

### List of tasks to be completed in order

```yaml
Task 1: Create AAI Brain Module Integration
CREATE brain/modules/mem0-memory-enhancement.md:
  - DEFINE Smart Module Loading triggers for all AAI commands
  - SPECIFY when memory enhancement activates (always-on substrate)
  - INCLUDE integration patterns for /generate-prp, /implement, /analyze
  - FOLLOW existing AAI brain module patterns

Task 2: Build Command Enhancement Layer
CREATE enhancements/memory/command_enhancer.py:
  - IMPLEMENT memory enhancement for existing AAI commands
  - INTERCEPT command execution to add memory context
  - FOLLOW AAI's existing command structure in .claude/commands/
  - PRESERVE all existing command functionality while adding memory

Task 3: Create Memory Workflow Integration
CREATE enhancements/memory/memory_layer.py:
  - IMPLEMENT core memory integration layer
  - PROVIDE memory context to all AAI workflows
  - INCLUDE confidence scoring per AAI standards (70-95%)
  - INTEGRATE with existing Supabase infrastructure

Task 4: Setup Enhanced Supabase Schema
MODIFY supabase/migrations/:
  - CREATE new migration file: 004_aai_memory_enhancement.sql
  - INCLUDE memory tables with pgvector support for all workflows
  - ADD indexes for efficient cross-command memory retrieval
  - PRESERVE existing AAI schema patterns

Task 5: Build Workflow Memory Context
CREATE enhancements/memory/workflow_memory.py:
  - IMPLEMENT memory context for /generate-prp workflows
  - ADD memory enhancement for /implement workflows  
  - INCLUDE memory integration for /analyze workflows
  - PROVIDE cross-session learning for all command types

Task 6: Update Smart Module Loading
MODIFY brain/Claude.md:
  - ADD memory enhancement triggers for all commands
  - INCLUDE always-active memory substrate rules
  - UPDATE Intelligence Feature Matrix with memory enhancement
  - PRESERVE existing Smart Module Loading functionality

Task 7: Create Memory Quality Scoring
CREATE brain/modules/memory-quality-scorer.py:
  - FOLLOW AAI scoring patterns from score-tracker.md
  - IMPLEMENT memory usefulness metrics for all workflows
  - ADD auto-cleanup integrated with existing AAI cleanup
  - INCLUDE learning from command usage patterns

Task 8: Build Workflow Integration Tests
CREATE tests/enhancements/memory/:
  - TEST memory enhancement of existing commands
  - VERIFY /generate-prp memory integration
  - VALIDATE /implement memory enhancement
  - CONFIRM /analyze memory augmentation

Task 9: Document Enhanced Workflows
CREATE brain/workflows/memory-enhanced-commands.md:
  - DOCUMENT how memory enhances each existing command
  - PROVIDE examples of enhanced workflow behavior
  - INCLUDE troubleshooting for memory integration
  - FOLLOW existing AAI workflow documentation patterns
```

### Per task pseudocode

```python
# Task 1: AAI Brain Module Integration
# brain/modules/mem0-memory-enhancement.md
"""
Memory Enhancement Module for AAI Smart Module Loading

TRIGGERS:
- ALWAYS: Memory substrate active for all commands
- generate-prp: Load user's previous PRP patterns and preferences  
- implement: Load implementation patterns and user coding preferences
- analyze: Load previous analysis results and learned patterns

INTEGRATION POINTS:
- Enhances ALL existing AAI commands with memory context
- Preserves existing command functionality
- Adds cross-session learning and pattern recognition
"""

# Task 2: Command Enhancement Layer
class AAICommandEnhancer:
    def __init__(self, aai_brain_modules):
        self.memory_layer = MemoryLayer()
        self.existing_commands = aai_brain_modules
    
    async def enhance_generate_prp(self, original_command, args):
        # PATTERN: Enhance existing /generate-prp command
        memory_context = await self.memory_layer.get_prp_context(args)
        enhanced_context = {
            **original_command.context,
            'previous_prps': memory_context.similar_prps,
            'user_preferences': memory_context.coding_patterns,
            'learned_patterns': memory_context.successful_implementations
        }
        return await original_command.execute_with_memory(enhanced_context)

    async def enhance_implement(self, original_command, args):
        # PATTERN: Enhance existing /implement command  
        memory_context = await self.memory_layer.get_implementation_context(args)
        enhanced_context = {
            **original_command.context,
            'implementation_patterns': memory_context.successful_patterns,
            'user_coding_style': memory_context.preferred_approaches,
            'previous_solutions': memory_context.similar_implementations
        }
        return await original_command.execute_with_memory(enhanced_context)

# Task 3: Memory Workflow Integration
class WorkflowMemoryIntegration:
    async def integrate_with_smart_module_loading(self, command_type, context):
        # PATTERN: AAI Smart Module Loading integration
        if command_type == "generate-prp":
            return await self.enhance_prp_workflow(context)
        elif command_type == "implement":
            return await self.enhance_implementation_workflow(context)
        elif command_type == "analyze":
            return await self.enhance_analysis_workflow(context)
        
        # Always provide base memory context
        return await self.get_base_memory_context(context)
```

### Integration Points
```yaml
AAI_BRAIN_INTEGRATION:
  - add to: brain/Claude.md Intelligence Feature Matrix
  - pattern: "Memory Enhancement Layer | ✅ | mem0-memory-enhancement.md | 1-3 | Always"
  
COMMAND_ENHANCEMENT_INTEGRATION:
  - enhance: .claude/commands/generate-prp.md (add memory context)
  - enhance: .claude/commands/implement.md (add memory patterns)
  - enhance: .claude/commands/analyze.md (add memory insights)
  - preserve: ALL existing command functionality
  
SMART_MODULE_LOADING:
  - add trigger: "ALWAYS → load memory enhancement substrate"
  - add trigger: "if (generate-prp) → enhance with PRP memory context"
  - add trigger: "if (implement) → enhance with implementation memory"
  - add trigger: "if (analyze) → enhance with analysis memory"

WORKFLOW_INTEGRATION:
  - integrate: brain/workflows/ (memory-enhanced command patterns)
  - preserve: existing workflow functionality
  - enhance: cross-session learning for all workflows
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check agents/mem0/ --fix
mypy agents/mem0/
black agents/mem0/

# Expected: No errors. Clean code following AAI standards.
```

### Level 2: Unit Tests
```python
# CREATE tests/agents/mem0/test_memory_integration.py
async def test_memory_storage_and_retrieval():
    """Test complete memory lifecycle with confidence scoring"""
    memory_manager = MemoryManager(supabase_client)
    
    # Store memory with metadata
    stored = await memory_manager.store_memory(
        content="User prefers FastAPI over Flask for API development",
        user_id="test_user",
        metadata={"context": "tech_preferences", "confidence": 0.85}
    )
    assert stored.confidence_score >= 0.70
    
    # Retrieve memory with query
    query = MemoryQuery(
        query="What API framework does user prefer?",
        user_id="test_user",
        min_confidence=0.75
    )
    response = await memory_manager.search_memories(query)
    assert len(response.memories) > 0
    assert response.avg_confidence >= 0.75
    assert "FastAPI" in response.memories[0].content

async def test_memory_quality_scoring():
    """Test memory quality assessment and cleanup"""
    quality_scorer = MemoryQualityScorer()
    
    high_quality = "Detailed research finding: FastAPI with Pydantic provides excellent type safety for API development. User successfully implemented 3 projects using this stack."
    low_quality = "ok"
    
    assert quality_scorer.assess_quality(high_quality) > 0.8
    assert quality_scorer.assess_quality(low_quality) < 0.3

async def test_jina_research_memory_integration():
    """Test integration with Jina API for research content"""
    agent = Mem0Agent()
    
    # Research content should be stored as memories
    research_result = await agent.research_and_remember(
        query="FastAPI authentication patterns",
        user_id="test_user"
    )
    
    assert research_result.confidence_score >= 0.70
    assert "authentication" in research_result.content.lower()
```

```bash
# Run and iterate until passing:
pytest tests/agents/mem0/ -v --cov=agents/mem0
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test
```bash
# Start the memory system
python -m agents.mem0.agent

# Test memory storage via API
curl -X POST http://localhost:8000/memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User completed successful project using React + FastAPI",
    "user_id": "test_user",
    "metadata": {"project": "web_app", "success": true}
  }'

# Test memory retrieval
curl -X POST http://localhost:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What tech stack worked well for user?",
    "user_id": "test_user",
    "min_confidence": 0.75
  }'

# Expected: 
# {
#   "memories": [...],
#   "avg_confidence": 0.85,
#   "reasoning": "Found 2 relevant memories about successful tech stack usage..."
# }
```

### Level 4: AAI Brain Integration Test
```bash
# Test AAI brain module loading
python -c "
from brain.modules.mem0_agent import Mem0Agent
agent = Mem0Agent()
result = agent.test_integration()
print(f'Integration test: {result}')
"

# Test Streamlit memory explorer
streamlit run ui/memory/streamlit_memory_explorer.py

# Navigate to http://localhost:8501 and verify:
# - Memory search functionality
# - Confidence score displays
# - Memory quality analytics
# - AAI brain integration indicators
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  performance:
    - metric: "Memory Retrieval Time"
      target: "≤ 500ms"  
      measurement: "curl -w '%{time_total}' memory/search endpoint"
      validation_gate: "integration_tests"
  quality:
    - metric: "Memory Relevance Accuracy"
      target: "≥ 85%"
      measurement: "Manual evaluation of retrieved memories"
      validation_gate: "user_testing"
  intelligence:
    - metric: "Cross-Session Learning Rate"
      target: "≥ 75%"
      measurement: "Reduced repeated research queries"
      validation_gate: "production_usage"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md" 
  success_tracker: "brain/modules/score-tracker.md"
  auto_tag: ["#learn", "#memory", "#cross-session"]
  promotion_threshold: 4.5
```

### AAI Brain System Integration
```yaml
aai_integration:
  brain_modules:
    - "score-tracker.md"  # For confidence scoring
    - "unified-analytics.py"  # For memory usage tracking  
    - "supabase-cache.py"  # For storage patterns
  auto_triggers:
    - on_completion: "update_memory_quality_scores"
    - on_success: "generate_memory_patterns_sop" 
    - on_failure: "log_memory_retrieval_issues"
    - on_repeated_query: "retrieve_relevant_memories"
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/agents/mem0/ -v`
- [ ] No linting errors: `ruff check agents/mem0/`
- [ ] No type errors: `mypy agents/mem0/`
- [ ] Memory storage and retrieval working: [curl commands above]
- [ ] Confidence scoring within 70-95% range
- [ ] Supabase integration functional
- [ ] Streamlit interface operational
- [ ] AAI brain module integration active
- [ ] Cross-session memory persistence verified
- [ ] Jina API research content integration working
- [ ] Memory quality scoring and cleanup functional

---

## Anti-Patterns to Avoid
- ❌ Don't store memories without confidence scores
- ❌ Don't ignore AAI's 70-95% confidence scoring requirement  
- ❌ Don't bypass Supabase connection pooling
- ❌ Don't use inconsistent user_id patterns across sessions
- ❌ Don't store low-quality memories without cleanup mechanisms
- ❌ Don't ignore memory embedding dimension compatibility
- ❌ Don't skip integration with existing AAI brain modules
- ❌ Don't forget neural reasoning for memory selection explanations
- ❌ Don't implement without proper error handling and retries
- ❌ Don't neglect memory privacy and user data protection

**Final Score**: 9/10 - High confidence for one-pass implementation success with comprehensive context, validated patterns, and clear integration roadmap.