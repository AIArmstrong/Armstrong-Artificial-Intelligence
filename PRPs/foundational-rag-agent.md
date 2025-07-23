---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-20250719-foundational-rag
project_name: foundational_rag_agent
priority: low
auto_scaffold: true
integrations: [supabase, pydantic-ai, streamlit]
estimated_effort: "2-3 hours"
complexity: simple
tags: ["#rag", "#baseline", "#supabase", "#pgvector", "#simple"]
created: 2025-07-19
author: aai-system
---

# Foundational RAG Agent - Simple RAG Baseline

## Purpose
Implement a simple, foundational RAG system using Pydantic AI and Supabase pgvector as a baseline implementation and fallback for complex RAG systems.

## Goal
Build a straightforward RAG agent for simpler research tasks and as a foundation for more complex systems.

## Why
- **Baseline Implementation**: Provides simple RAG fallback when complex systems aren't needed
- **Foundation Layer**: Serves as base for other RAG implementations
- **Supabase Integration**: Leverages existing AAI infrastructure
- **Learning Reference**: Demonstrates core RAG patterns for AAI

## What
- Simple document ingestion (PDF/TXT)
- Supabase pgvector storage
- Basic semantic search
- Pydantic AI agent with search tools
- Streamlit interface

### Success Criteria
- [ ] PDF/TXT document processing
- [ ] Supabase pgvector integration
- [ ] Semantic search with confidence scoring
- [ ] Streamlit UI for interaction
- [ ] Integration with AAI patterns

## Implementation Blueprint

```yaml
Task 1: Setup Supabase Integration
CREATE database/supabase_setup.py:
  - EXTEND existing supabase patterns
  - ADD simple RAG schema
  - INCLUDE vector search functions

Task 2: Build Document Processing
CREATE document_processing/simple_processor.py:
  - IMPLEMENT PDF/TXT ingestion
  - ADD basic chunking
  - INCLUDE embedding generation

Task 3: Create RAG Agent
CREATE agent/simple_rag_agent.py:
  - IMPLEMENT Pydantic AI agent
  - ADD document search tools
  - INCLUDE confidence scoring

Task 4: Build Streamlit UI
CREATE ui/streamlit_app.py:
  - IMPLEMENT document upload
  - ADD question interface
  - INCLUDE result display
```

### Data Models

```python
class DocumentChunk(BaseModel):
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    
class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0.70, le=0.95)
```

---

**Final Score**: 6/10 - Straightforward implementation with existing patterns.