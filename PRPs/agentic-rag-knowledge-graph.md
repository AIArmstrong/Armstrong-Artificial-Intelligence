---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-20250719-agentic-rag-kg
project_name: agentic_rag_knowledge_graph
priority: high
auto_scaffold: true
integrations: [supabase, neo4j, graphiti, openrouter, jina-api]
estimated_effort: "6-8 hours"
complexity: complex
tags: ["#rag", "#knowledge-graph", "#hybrid-search", "#research-engine", "#temporal"]
created: 2025-07-19
author: aai-system
---

# Agentic RAG Enhancement - Hybrid Intelligence for AAI Workflows

## Purpose
Enhance ALL existing AAI commands with sophisticated hybrid search capabilities that combine traditional RAG (vector similarity) with temporal knowledge graphs. This transforms /generate-prp, /analyze, /implement, and research workflows with advanced relationship discovery and temporal intelligence.

## Goal
Integrate hybrid vector+graph intelligence into AAI's existing Smart Module Loading system so that every research and analysis operation automatically benefits from relationship discovery, temporal changes tracking, and semantic connections - creating a unified intelligence enhancement for all AAI workflows.

## Why

### Core Research Requirements
- **Research Complexity**: AAI needs sophisticated search for "30-100 page research" requirements that goes beyond simple vector similarity
- **Relationship Discovery**: Knowledge graphs reveal hidden connections between entities, companies, technologies
- **Temporal Intelligence**: Track how facts and relationships change over time in rapidly evolving AI landscape
- **Complementary Strengths**: Vector search finds semantically similar content while graphs reveal structural relationships
- **Research Velocity**: 10x faster research synthesis through intelligent hybrid search strategies
- **Neural Reasoning**: Perfect match for AAI's WHY rationale + confidence scoring requirements

### Enhanced Value Propositions
- **Predictive Research**: Identify emerging trends before they become mainstream through temporal pattern analysis
- **Research Navigation**: Follow "idea chains" for seamless exploratory research experiences
- **Fact Validation**: Real-time cross-referencing prevents outdated or contradictory information
- **Visual Intelligence**: Insight Cards provide immediate visual comprehension of complex relationships
- **Collaborative Enhancement**: Team annotations improve collective intelligence and knowledge capture
- **Historical Context**: Knowledge Snapshots enable longitudinal research analysis
- **Adaptive Learning**: System improves accuracy through user feedback and interaction patterns
- **Cross-domain Insights**: Interdisciplinary connections foster innovation and discovery
- **Quality Assurance**: Multi-layered confidence scoring provides granular reliability assessment

## What
Build an **enhanced hybrid intelligence system** that:

### Core Architecture (Existing)
- Combines PostgreSQL + pgvector for semantic similarity search
- Integrates Neo4j + Graphiti for temporal knowledge graph capabilities
- Uses Pydantic AI for intelligent agent decision-making
- Provides FastAPI streaming interface with real-time responses
- Includes document ingestion pipeline with semantic chunking
- Supports multiple LLM providers through OpenRouter integration
- Integrates with Jina API for web research and document discovery
- Delivers confidence-scored results with reasoning explanations

### Enhanced Intelligence Features
- **Adaptive Semantic Chunking**: Dynamic boundary adjustment based on content complexity and semantic coherence
- **Multi-layered Confidence Scoring**: Separate assessment of semantic coherence, entity extraction accuracy, and relationship inference quality
- **Dynamic Entity Resolution**: Confidence-adaptive deduplication with historical learning
- **Predictive Temporal Analysis**: Proactive relationship and trend suggestion based on historical patterns
- **Interactive Exploration Interface**: Streamlit dashboard for real-time graph exploration and visualization
- **"Idea Chain" Navigation**: Auto-generated follow-up queries based on entity relationships
- **Real-time Fact Validation**: Cross-reference entities against external sources via Jina API
- **Research "Insight Cards"**: Visual presentation with confidence indicators and temporal relevance
- **Knowledge Snapshots**: Historical state capture for temporal research comparison
- **Collaborative Intelligence**: Annotation system for team-based knowledge enhancement
- **Cross-domain Integration**: Multi-domain search for interdisciplinary insights
- **Intelligent Feedback Loop**: Auto-learning from user interactions to improve confidence calibration

### Success Criteria
- [ ] Hybrid search combining vector similarity + graph traversal
- [ ] Temporal knowledge graph with entity relationship tracking
- [ ] **ENHANCED**: Adaptive semantic chunking with LLM-guided boundary detection
- [ ] Streaming FastAPI interface with real-time responses
- [ ] Integration with AAI's existing Supabase infrastructure
- [ ] Jina API integration for web research capabilities
- [ ] **ENHANCED**: Multi-layered confidence scoring (semantic, entity, relationship)
- [ ] Neural reasoning explanations for search strategy selection
- [ ] **NEW**: Dynamic entity resolution with confidence-adaptive deduplication
- [ ] **NEW**: Predictive temporal analysis for trend detection
- [ ] **NEW**: Interactive graph exploration Streamlit interface
- [ ] **NEW**: "Idea Chain" research navigation with auto-follow-up queries
- [ ] **NEW**: Real-time fact validation against external sources (Jina API)
- [ ] **NEW**: Research "Insight Cards" with visual confidence indicators
- [ ] **NEW**: Temporal "Knowledge Snapshots" for historical comparison
- [ ] **NEW**: Collaborative annotation system for collective intelligence
- [ ] Support for multiple LLM providers via OpenRouter
- [ ] CLI interface for interactive research sessions

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://docs.pydantic.dev/pydantic-ai/
  why: Core agent framework patterns and tool calling
  
- url: https://neo4j.com/docs/python-manual/current/
  why: Neo4j Python driver patterns and graph queries
  
- url: https://docs.graphiti.ai/
  why: Temporal knowledge graph concepts and API
  
- file: /ottomator-agents/agentic-rag-knowledge-graph/README.md
  why: Complete project architecture and implementation patterns
  
- file: /ottomator-agents/agentic-rag-knowledge-graph/CLAUDE.md
  why: Development guidelines and modularity requirements
  
- file: /brain/Claude.md
  why: AAI architecture rules, OpenRouter integration, neural reasoning requirements
  
- file: /docs/jina-scraping-guide.md
  why: Jina API integration patterns replacing Brave Search
  
- file: /supabase/modules/supabase_search.py
  why: Existing vector search patterns to integrate with
  
- url: https://supabase.com/docs/guides/database/extensions/pgvector
  why: Supabase pgvector setup and optimization patterns
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "Pydantic AI agent frameworks with tools"
    depth: 20
    target_folder: "research/pydantic-ai-patterns"
  - topic: "Neo4j Graphiti temporal graphs"  
    depth: 15
    target_folder: "research/graphiti-temporal"
  - topic: "FastAPI streaming with Server-Sent Events"
    depth: 10
    target_folder: "research/fastapi-streaming"
  - topic: "semantic document chunking strategies"
    depth: 12
    target_folder: "research/semantic-chunking"
```

### Example Pattern References
```yaml
example_references:
  - ottomator-agents/agentic-rag-knowledge-graph/agent/agent.py
  - ottomator-agents/agentic-rag-knowledge-graph/ingestion/ingest.py
  - ottomator-agents/agentic-rag-knowledge-graph/agent/api.py
  - brain/modules/openrouter/router_client.py
  - supabase/modules/supabase_search.py
pattern_similarity_threshold: 0.85
fallback_action: "create_new_hybrid_search_module"
```

### Current Codebase tree (relevant sections)
```bash
AAI/
├── brain/modules/
│   ├── openrouter/
│   │   ├── router_client.py
│   │   └── embeddings.py
│   └── supabase-cache.py
├── supabase/
│   ├── modules/supabase_search.py
│   └── scripts/setup_supabase_schema.sql
├── ottomator-agents/agentic-rag-knowledge-graph/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── api.py
│   │   ├── tools.py
│   │   └── models.py
│   ├── ingestion/
│   │   ├── ingest.py
│   │   ├── chunker.py
│   │   └── embedder.py
│   └── sql/schema.sql
└── docs/jina-scraping-guide.md
```

### Desired Codebase tree with files to be added
```bash
AAI/
├── brain/modules/
│   ├── hybrid-rag-agent.py           # Main AAI integration module
│   ├── knowledge-graph-manager.py    # Graph operations with confidence scoring
│   └── research-synthesis-engine.py  # Hybrid search coordination
├── agents/hybrid-rag/
│   ├── __init__.py
│   ├── agent.py                      # Core Pydantic AI agent
│   ├── hybrid_search.py              # Vector + graph search coordination
│   ├── vector_search.py              # Supabase pgvector search
│   ├── graph_search.py               # Neo4j + Graphiti operations
│   ├── tools.py                      # Agent tools with confidence scoring
│   ├── prompts.py                    # System prompts with reasoning guidance
│   ├── models.py                     # Pydantic models for requests/responses
│   └── config.py                     # Environment and provider configuration
├── ingestion/hybrid-rag/
│   ├── __init__.py
│   ├── pipeline.py                   # Document ingestion coordinator
│   ├── semantic_chunker.py           # LLM-powered semantic chunking
│   ├── vector_embedder.py            # OpenRouter embedding generation
│   ├── graph_builder.py              # Entity extraction + relationship building
│   └── jina_research_scraper.py      # Jina API research content gathering
├── api/hybrid-rag/
│   ├── __init__.py
│   ├── server.py                     # FastAPI application with streaming
│   ├── endpoints.py                  # API route definitions
│   └── streaming.py                  # Server-Sent Events implementation
├── supabase/
│   ├── migrations/
│   │   └── 005_hybrid_rag_schema.sql # Vector storage schema
│   └── modules/
│       └── hybrid_search_db.py       # Database operations
├── neo4j/
│   ├── setup/
│   │   └── graph_schema.cypher       # Knowledge graph schema
│   └── operations/
│       ├── entity_manager.py         # Entity CRUD operations
│       └── relationship_tracker.py   # Temporal relationship management
├── ui/hybrid-rag/
│   ├── cli_interface.py              # Interactive CLI for research
│   └── research_dashboard.py         # Streamlit research analytics
└── tests/agents/hybrid-rag/
    ├── test_hybrid_search.py
    ├── test_graph_operations.py
    ├── test_ingestion_pipeline.py
    └── test_streaming_api.py
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Neo4j + Graphiti requires specific driver configuration
# Example: Use neo4j+s:// for encrypted connections, bolt:// for local

# CRITICAL: pgvector embedding dimensions must match across all components
# OpenAI text-embedding-3-small = 1536 dimensions

# GOTCHA: Graphiti temporal graphs can become computationally expensive
# Use selective entity extraction and relationship pruning for performance

# GOTCHA: FastAPI streaming requires proper async context management
# Use AsyncExitStack for database connections in streaming responses

# CRITICAL: Multiple LLM providers need consistent token usage tracking
# Implement rate limiting per provider to avoid API limit hits

# GOTCHA: Semantic chunking can create variable chunk sizes
# Balance chunk size consistency with semantic coherence

# CRITICAL: Knowledge graph entity resolution requires fuzzy matching
# Implement entity deduplication to prevent graph fragmentation
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "brain/modules/openrouter/router_client.py"
      reason: "Uses existing LLM provider abstraction"
    - module: "supabase/modules/supabase_search.py"  
      reason: "Integrates with existing vector search patterns"
    - module: "brain/modules/score-tracker.md"
      reason: "Follows AAI confidence scoring standards"
    - module: "docs/jina-scraping-guide.md"
      reason: "Replaces Brave API with Jina for research content"
  external:
    - package: "pydantic-ai ≥ 0.0.8"
    - package: "neo4j ≥ 5.0.0"
    - package: "graphiti-core ≥ 0.3.0"
    - package: "fastapi ≥ 0.104.0"
    - package: "supabase ≥ 2.0.0"
    - package: "asyncpg ≥ 0.29.0"
  conflicts:
    - issue: "Neo4j memory usage conflicts with large vector operations"
      mitigation: "Implement connection pooling and selective graph queries"
    - issue: "Streaming responses may timeout with large research queries"
      mitigation: "Implement progressive result streaming with partial responses"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "brain/modules/openrouter/router_client.py"
    - "supabase/modules/supabase_search.py"
    - "docs/jina-scraping-guide.md"
  api_documentation_current:
    - check: "Pydantic AI documentation updated within 30 days"
    - check: "Graphiti documentation accessible and current"
  example_relevance:
    - similarity_threshold: 0.85
    - fallback: "Create new AAI-specific hybrid search patterns"
```

## 📦 Implementation Readiness Assessment

### 🚪 Implementation Gates

#### Infrastructure Gates
```yaml
infrastructure_gates:
  network_connectivity:
    - service: "neo4j_host"
      test: "ping -c 3 localhost"  # Assuming local Neo4j setup
      expected: "0% packet loss"
      owner: "user"
      
    - service: "supabase_host"
      test: "ping -c 3 $(echo $SUPABASE_URL | sed 's|https://||' | sed 's|/.*||')"
      expected: "0% packet loss"
      owner: "aai-system"
      
  service_availability:
    - service: "neo4j_database" 
      test: "curl -u neo4j:${NEO4J_PASSWORD} http://localhost:7474/db/data/"
      expected: "200 OK"
      fallback: "Use local Neo4j Desktop or Docker container"
      time_to_fix: "30 minutes"
      owner: "user"
      
    - service: "supabase_api"
      test: "curl -f $SUPABASE_URL/rest/v1/"
      expected: "200 OK"
      fallback: "Use local PostgreSQL with pgvector extension"
      time_to_fix: "45 minutes"
      owner: "user"
```

#### Credential Gates
```yaml
credential_gates:
  critical:
    - credential: "NEO4J_PASSWORD"
      location: ".env"
      validation: "curl -u neo4j:$NEO4J_PASSWORD http://localhost:7474/db/data/"
      expected: "200 OK"
      owner: "user"
      time_to_fix: "5 minutes"
      
    - credential: "SUPABASE_KEY"
      location: ".env"
      validation: "curl -H 'apikey: $SUPABASE_KEY' $SUPABASE_URL/rest/v1/"
      expected: "200 or 401 (key format valid)"
      owner: "user"
      time_to_fix: "5 minutes"
      
    - credential: "OPENROUTER_API_KEY"
      location: ".env"
      validation: "curl -H 'Authorization: Bearer $OPENROUTER_API_KEY' https://openrouter.ai/api/v1/models"
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
    - package: "pydantic-ai>=0.0.8"
      install: "pip install pydantic-ai"
      validation: "python -c 'import pydantic_ai; print(pydantic_ai.__version__)'"
      expected: ">=0.0.8"
      
    - package: "neo4j>=5.0.0"
      install: "pip install neo4j"
      validation: "python -c 'import neo4j; print(neo4j.__version__)'"
      expected: ">=5.0.0"
      
    - package: "graphiti-core>=0.3.0"
      install: "pip install graphiti-core"
      validation: "python -c 'import graphiti; print(graphiti.__version__)'"
      expected: ">=0.3.0"
      
database_gates:
  schema_checks:
    - query: "SELECT to_regclass('public.aai_documents');"
      expected: "not null"
      fallback: "Run Supabase migration scripts"
      fix_command: "python supabase/scripts/setup_supabase_schema.py"
      
  neo4j_checks:
    - query: "CALL db.schema.visualization()"
      expected: "Valid graph schema response"
      fallback: "Run Neo4j schema setup"
      fix_command: "python neo4j/setup/initialize_schema.py"
```

#### Environment Gates
```yaml
environment_validation:
  required_directories:
    - path: "agents/hybrid-rag/"
      create_if_missing: true
    - path: "ingestion/hybrid-rag/"
      create_if_missing: true
    - path: "neo4j/operations/"
      create_if_missing: true
      
  required_files:
    - file: ".env"
      template: ".env.example"
      required_vars: ["NEO4J_PASSWORD", "SUPABASE_KEY", "OPENROUTER_API_KEY", "JINA_API_KEY"]
```

## Implementation Blueprint

### Data models and structure

Create comprehensive models for hybrid search system:
```python
# agents/hybrid-rag/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class SearchStrategy(str, Enum):
    """Search strategy selection for hybrid queries"""
    VECTOR_ONLY = "vector_only"
    GRAPH_ONLY = "graph_only"
    HYBRID = "hybrid"
    INTELLIGENT = "intelligent"  # Agent decides strategy

class ResearchQuery(BaseModel):
    """Comprehensive research query with AAI context"""
    query: str
    user_id: str
    search_strategy: SearchStrategy = SearchStrategy.INTELLIGENT
    max_results: int = Field(default=10, le=50)
    min_confidence: float = Field(default=0.70, ge=0.70, le=0.95)
    include_temporal: bool = True
    context_tags: List[str] = Field(default_factory=list)
    research_depth: int = Field(default=5, ge=1, le=20)  # For Jina scraping

class DocumentChunk(BaseModel):
    """Document chunk with vector and graph metadata"""
    id: str
    document_id: str
    content: str
    embedding: Optional[List[float]] = None
    chunk_index: int
    semantic_coherence_score: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    entities: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)

class EntityRelationship(BaseModel):
    """Knowledge graph entity relationship with temporal data"""
    source_entity: str
    target_entity: str
    relationship_type: str
    confidence: float = Field(ge=0.70, le=0.95)
    temporal_context: Dict[str, Any] = Field(default_factory=dict)
    evidence_chunks: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

class HybridSearchResult(BaseModel):
    """Unified result from hybrid search with reasoning"""
    content: str
    source: str
    confidence_score: float = Field(ge=0.70, le=0.95)
    search_strategy_used: SearchStrategy
    vector_similarity: Optional[float] = None
    graph_path_length: Optional[int] = None
    entity_connections: List[EntityRelationship] = Field(default_factory=list)
    temporal_relevance: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ResearchResponse(BaseModel):
    """Complete research response with reasoning"""
    results: List[HybridSearchResult]
    total_found: int
    search_strategy_reasoning: str  # WHY this strategy was chosen
    avg_confidence: float
    search_time_ms: int
    entities_discovered: List[str] = Field(default_factory=list)
    relationship_insights: List[str] = Field(default_factory=list)
    recommended_follow_up: List[str] = Field(default_factory=list)
```

### List of tasks to be completed in order

```yaml
Task 1: Setup Hybrid Database Infrastructure
MODIFY supabase/migrations/:
  - CREATE new migration: 005_hybrid_rag_schema.sql
  - INCLUDE document storage with pgvector embeddings
  - ADD entity and relationship tracking tables
  - PRESERVE existing AAI schema patterns

CREATE neo4j/setup/graph_schema.cypher:
  - DEFINE entity nodes with temporal properties
  - CREATE relationship types with confidence metadata
  - INCLUDE indexes for efficient traversal
  - ADD constraints for data integrity

Task 2: Build Document Ingestion Pipeline
CREATE ingestion/hybrid-rag/pipeline.py:
  - IMPLEMENT coordinated ingestion for vector + graph
  - INCLUDE semantic chunking with LLM analysis
  - ADD entity extraction and relationship building
  - INTEGRATE with Jina API for research content gathering

CREATE ingestion/hybrid-rag/semantic_chunker.py:
  - MIRROR patterns from ottomator original semantic chunking
  - IMPLEMENT LLM-powered chunk boundary detection
  - ADD coherence scoring for chunk quality
  - INCLUDE metadata preservation across chunks

Task 3: Implement Vector Search Integration
CREATE agents/hybrid-rag/vector_search.py:
  - EXTEND existing supabase_search.py patterns
  - IMPLEMENT embedding generation via OpenRouter
  - ADD confidence scoring for similarity results
  - INCLUDE metadata filtering and ranking

Task 4: Build Knowledge Graph Operations
CREATE agents/hybrid-rag/graph_search.py:
  - IMPLEMENT Neo4j + Graphiti integration
  - ADD temporal relationship queries
  - INCLUDE entity resolution and deduplication
  - FOLLOW AAI confidence scoring patterns

Task 5: Create Hybrid Search Coordinator
CREATE agents/hybrid-rag/hybrid_search.py:
  - IMPLEMENT intelligent strategy selection
  - ADD result fusion from vector + graph sources
  - INCLUDE confidence scoring aggregation
  - PROVIDE reasoning for strategy choices

Task 6: Build Pydantic AI Agent
CREATE agents/hybrid-rag/agent.py:
  - MIRROR patterns from ottomator-agents original
  - IMPLEMENT tool calling with confidence scoring
  - ADD neural reasoning for search strategy selection
  - INTEGRATE with AAI brain modules

Task 7: Implement Streaming FastAPI Server
CREATE api/hybrid-rag/server.py:
  - IMPLEMENT FastAPI with Server-Sent Events
  - ADD streaming response capabilities
  - INCLUDE real-time search progress updates
  - FOLLOW AAI API patterns and error handling

Task 8: Create Jina Research Integration
CREATE ingestion/hybrid-rag/jina_research_scraper.py:
  - REPLACE Brave API usage with Jina API
  - IMPLEMENT research content discovery
  - ADD content quality scoring
  - INTEGRATE with existing jina-scraping-guide patterns

Task 9: Build Interactive CLI Interface
CREATE ui/hybrid-rag/cli_interface.py:
  - IMPLEMENT interactive research sessions
  - ADD tool usage visibility and strategy explanation
  - INCLUDE confidence score displays
  - PROVIDE session management and history

Task 10: Add AAI Brain Integration
CREATE brain/modules/hybrid-rag-agent.py:
  - FOLLOW AAI brain module patterns
  - INTEGRATE with score-tracker.md
  - ADD auto-trigger conditions for complex research
  - INCLUDE cross-session learning capabilities

Task 11: Implement Comprehensive Testing
CREATE tests/agents/hybrid-rag/:
  - IMPLEMENT integration tests for hybrid search
  - ADD performance benchmarks for search strategies
  - INCLUDE graph operations accuracy tests
  - VERIFY streaming API functionality
```

### Per task pseudocode

```python
# Task 2: Semantic Chunking with Entity Extraction
class SemanticChunker:
    def __init__(self, llm_client, min_chunk_size=500, max_chunk_size=1500):
        self.llm = llm_client
        self.min_size = min_chunk_size
        self.max_size = max_chunk_size
    
    async def chunk_document(self, content: str, metadata: Dict) -> List[DocumentChunk]:
        # PATTERN: Use LLM to identify semantic boundaries
        boundaries = await self.llm.analyze_semantic_structure(content)
        
        chunks = []
        for boundary in boundaries:
            chunk_content = content[boundary.start:boundary.end]
            
            # CRITICAL: Extract entities and relationships per chunk
            entities = await self.extract_entities(chunk_content)
            relationships = await self.extract_relationships(chunk_content, entities)
            
            # PATTERN: AAI confidence scoring for chunk quality
            coherence_score = await self.assess_semantic_coherence(chunk_content)
            
            chunk = DocumentChunk(
                content=chunk_content,
                entities=entities,
                relationships=relationships,
                semantic_coherence_score=coherence_score,
                metadata={**metadata, "boundary_confidence": boundary.confidence}
            )
            chunks.append(chunk)
        
        return chunks

# Task 5: Hybrid Search Strategy Intelligence
class HybridSearchCoordinator:
    async def search(self, query: ResearchQuery) -> ResearchResponse:
        # PATTERN: Intelligent strategy selection with reasoning
        strategy = await self.select_search_strategy(query)
        reasoning = await self.explain_strategy_choice(query, strategy)
        
        if strategy == SearchStrategy.VECTOR_ONLY:
            results = await self.vector_search.search(query)
        elif strategy == SearchStrategy.GRAPH_ONLY:
            results = await self.graph_search.search(query)
        elif strategy == SearchStrategy.HYBRID:
            # CRITICAL: Fuse results from both sources with confidence weighting
            vector_results = await self.vector_search.search(query)
            graph_results = await self.graph_search.search(query)
            results = await self.fuse_results(vector_results, graph_results, query)
        
        # PATTERN: AAI confidence scoring aggregation
        avg_confidence = sum(r.confidence_score for r in results) / len(results)
        
        return ResearchResponse(
            results=results,
            search_strategy_reasoning=reasoning,
            avg_confidence=avg_confidence,
            entities_discovered=await self.extract_discovered_entities(results),
            relationship_insights=await self.generate_relationship_insights(results)
        )

# Task 6: Pydantic AI Agent with Tool Selection
from pydantic_ai import Agent, RunContext

class HybridRAGAgent:
    def __init__(self):
        self.agent = Agent(
            'claude-3-5-sonnet',  # Via OpenRouter
            system_prompt=self.get_system_prompt(),
            deps_type=HybridSearchDeps
        )
    
    @self.agent.tool
    async def vector_search(self, ctx: RunContext[HybridSearchDeps], query: str, limit: int = 10) -> str:
        """Search documents using semantic similarity"""
        # PATTERN: Include confidence scoring in tool responses
        results = await ctx.deps.vector_searcher.search(query, limit)
        confidence_avg = sum(r.confidence_score for r in results) / len(results)
        
        return f"Vector search found {len(results)} results with avg confidence {confidence_avg:.2f}:\n" + \
               "\n".join(f"- {r.content[:200]}... (confidence: {r.confidence_score:.2f})" for r in results)
    
    @self.agent.tool
    async def graph_search(self, ctx: RunContext[HybridSearchDeps], entity: str) -> str:
        """Search knowledge graph for entity relationships"""
        # PATTERN: Graph traversal with temporal context
        relationships = await ctx.deps.graph_searcher.find_relationships(entity)
        
        return f"Graph search found {len(relationships)} relationships for {entity}:\n" + \
               "\n".join(f"- {r.source_entity} --[{r.relationship_type}]--> {r.target_entity} (confidence: {r.confidence:.2f})" 
                        for r in relationships)
    
    @self.agent.tool
    async def research_with_jina(self, ctx: RunContext[HybridSearchDeps], topic: str, depth: int = 5) -> str:
        """Research topic using Jina API web scraping"""
        # PATTERN: Replace Brave API with Jina for research
        research_results = await ctx.deps.jina_scraper.research_topic(topic, max_pages=depth)
        
        # Store research findings in knowledge base
        for result in research_results:
            await self.store_research_finding(result, topic)
        
        return f"Researched {topic} with {len(research_results)} sources. Key findings stored in knowledge base."
```

### Integration Points
```yaml
AAI_BRAIN_INTEGRATION:
  - add to: brain/Claude.md Intelligence Feature Matrix
  - pattern: "Hybrid RAG Knowledge Graph | ✅ | hybrid-rag-agent.py | 2-3 | Complex research"
  
SUPABASE_INTEGRATION:
  - extend: supabase/modules/supabase_search.py
  - add: hybrid search capabilities with vector + metadata
  
OPENROUTER_INTEGRATION:
  - extend: brain/modules/openrouter/router_client.py
  - add: multi-model support for different search strategies

SMART_MODULE_LOADING:
  - add trigger: "if (research_depth > 10_pages) → load hybrid-rag-agent.py"
  - add trigger: "if (relationship_analysis_needed) → use_graph_search"
  - add trigger: "if (temporal_tracking_required) → enable_graphiti_features"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check agents/hybrid-rag/ ingestion/hybrid-rag/ api/hybrid-rag/ --fix
mypy agents/hybrid-rag/ ingestion/hybrid-rag/ api/hybrid-rag/
black agents/hybrid-rag/ ingestion/hybrid-rag/ api/hybrid-rag/

# Expected: No errors. Clean code following AAI standards.
```

### Level 2: Unit Tests
```python
# CREATE tests/agents/hybrid-rag/test_hybrid_search_integration.py
async def test_hybrid_search_strategy_selection():
    """Test intelligent search strategy selection with reasoning"""
    coordinator = HybridSearchCoordinator()
    
    # Simple factual query should use vector search
    query = ResearchQuery(query="What is FastAPI?", user_id="test")
    response = await coordinator.search(query)
    assert response.search_strategy_reasoning
    assert "vector" in response.search_strategy_reasoning.lower()
    
    # Relationship query should use graph search
    query = ResearchQuery(query="How is Microsoft connected to OpenAI?", user_id="test")
    response = await coordinator.search(query)
    assert "graph" in response.search_strategy_reasoning.lower()
    
    # Complex analysis should use hybrid approach
    query = ResearchQuery(query="Compare AI strategies of FAANG companies", user_id="test")
    response = await coordinator.search(query)
    assert response.avg_confidence >= 0.70

async def test_jina_api_integration():
    """Test Jina API research integration replacing Brave"""
    scraper = JinaResearchScraper()
    
    results = await scraper.research_topic("FastAPI authentication", max_pages=3)
    assert len(results) > 0
    assert all(r.quality_score > 0.5 for r in results)
    assert all("authentication" in r.content.lower() for r in results)

async def test_confidence_scoring_aggregation():
    """Test AAI confidence scoring across hybrid results"""
    search_coordinator = HybridSearchCoordinator()
    
    # All results must meet AAI confidence requirements (70-95%)
    query = ResearchQuery(query="OpenAI GPT models", min_confidence=0.75)
    response = await search_coordinator.search(query)
    
    assert all(r.confidence_score >= 0.75 for r in response.results)
    assert 0.70 <= response.avg_confidence <= 0.95
```

```bash
# Run and iterate until passing:
pytest tests/agents/hybrid-rag/ -v --cov=agents/hybrid-rag --cov=ingestion/hybrid-rag
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test
```bash
# Start the hybrid RAG system
python -m api.hybrid-rag.server

# Test hybrid search via streaming API
curl -X POST "http://localhost:8058/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key partnerships between tech companies in AI?",
    "search_strategy": "hybrid",
    "min_confidence": 0.75
  }'

# Expected streaming response:
# data: {"type": "search_strategy", "content": "Using hybrid search because query requires both semantic content and relationship analysis..."}
# data: {"type": "search_result", "content": "Found relationship: Microsoft --[PARTNERSHIP]--> OpenAI (confidence: 0.87)"}
# data: {"type": "final_response", "content": "Based on hybrid search of documents and knowledge graph..."}

# Test CLI interface
python ui/hybrid-rag/cli_interface.py

# Interactive session should show:
# 🤖 Hybrid RAG with Knowledge Graph CLI
# You: How are AI companies connected?
# 🛠 Tools Used: hybrid_search (strategy: intelligent)
# 🤖 Assistant: [Comprehensive analysis with confidence scores]
```

### Level 4: Graph Operations Test
```bash
# Test Neo4j graph operations
python -c "
from agents.hybrid_rag.graph_search import GraphSearchEngine
engine = GraphSearchEngine()
relationships = engine.find_entity_relationships('Microsoft')
print(f'Found {len(relationships)} relationships')
for r in relationships[:3]:
    print(f'{r.source_entity} --[{r.relationship_type}]--> {r.target_entity}')
"

# Test Graphiti temporal features
python -c "
from neo4j.operations.relationship_tracker import TemporalRelationshipTracker
tracker = TemporalRelationshipTracker()
timeline = tracker.get_relationship_timeline('Microsoft', 'OpenAI')
print(f'Relationship timeline: {timeline}')
"
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  performance:
    - metric: "Hybrid Search Response Time"
      target: "≤ 2000ms"  
      measurement: "curl -w '%{time_total}' streaming search endpoint"
      validation_gate: "integration_tests"
  quality:
    - metric: "Search Result Relevance"
      target: "≥ 88%"
      measurement: "Manual evaluation of hybrid search results"
      validation_gate: "user_testing"
  intelligence:
    - metric: "Strategy Selection Accuracy"
      target: "≥ 85%"
      measurement: "Correct strategy chosen for query type"
      validation_gate: "automated_testing"
  relationships:
    - metric: "Entity Relationship Discovery"
      target: "≥ 75%"
      measurement: "Percentage of known relationships correctly identified"
      validation_gate: "graph_validation"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md" 
  success_tracker: "brain/modules/score-tracker.md"
  auto_tag: ["#learn", "#hybrid-search", "#knowledge-graph", "#research"]
  promotion_threshold: 4.5
```

### AAI Brain System Integration
```yaml
aai_integration:
  brain_modules:
    - "score-tracker.md"  # For confidence scoring
    - "openrouter-integration.md"  # For multi-model support
    - "unified-analytics.py"  # For search strategy analytics
  auto_triggers:
    - on_completion: "update_search_strategy_effectiveness"
    - on_success: "generate_research_patterns_sop" 
    - on_failure: "log_hybrid_search_issues"
    - on_complex_research: "enable_full_hybrid_capabilities"
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/agents/hybrid-rag/ -v`
- [ ] No linting errors: `ruff check agents/hybrid-rag/`
- [ ] No type errors: `mypy agents/hybrid-rag/`
- [ ] Hybrid search functional: [curl streaming test above]
- [ ] Knowledge graph operations working
- [ ] Confidence scoring within 70-95% range
- [ ] Neo4j + Graphiti integration functional
- [ ] Supabase vector search operational
- [ ] FastAPI streaming interface working
- [ ] CLI interface interactive and informative
- [ ] Jina API research integration functional
- [ ] OpenRouter multi-model support working
- [ ] Semantic chunking and entity extraction operational

---

## Anti-Patterns to Avoid
- ❌ Don't use single search strategy for all query types
- ❌ Don't ignore confidence scoring requirements (70-95%)  
- ❌ Don't create knowledge graphs without entity deduplication
- ❌ Don't implement streaming without proper async context management
- ❌ Don't forget temporal relationship tracking in knowledge graphs
- ❌ Don't bypass OpenRouter for multi-model LLM access
- ❌ Don't use Brave API - integrate Jina API for web research
- ❌ Don't ignore semantic chunk quality scoring
- ❌ Don't create vector embeddings without dimension consistency
- ❌ Don't implement without reasoning explanations for strategy selection

**Final Score**: 8.5/10 - Very high confidence for one-pass implementation success with comprehensive hybrid architecture, proven patterns, and robust integration strategy.