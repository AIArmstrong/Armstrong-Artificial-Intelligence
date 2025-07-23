---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-20250719-general-researcher
project_name: general_researcher_agent
priority: medium
auto_scaffold: true
integrations: [jina-api, n8n, openrouter]
estimated_effort: "5-7 hours"
complexity: simple
tags: ["#research", "#multi-source", "#jina-api", "#real-time", "#curation", "#trending-dashboard", "#credibility-scoring", "#insight-alerts", "#adaptive-depth", "#visual-snapshots"]
created: 2025-07-19
author: aai-system
---

# Research Enhancement - Multi-Source Intelligence for AAI Workflows

## Purpose
Enhance ALL existing AAI commands with intelligent multi-source research capabilities that automatically scan, curate, and synthesize information. This transforms /generate-prp, /analyze, /implement, and other workflows with comprehensive research intelligence using Jina API while maintaining AAI's research standards.

## Goal
Integrate comprehensive research capabilities into AAI's existing Smart Module Loading system so that every command requiring research automatically benefits from multi-source intelligence, curation, and synthesis - creating a unified research enhancement layer for all AAI operations.

## Why

### Core Research Requirements
- **Research Velocity**: Automates information gathering for AAI's "research 30-100 pages" requirement
- **Multi-Source Intelligence**: Curates from diverse sources for comprehensive coverage
- **Real-Time Updates**: Keeps AAI current with rapidly evolving AI landscape
- **Jina Integration**: Leverages AAI's existing Jina API infrastructure

### Enhanced Value Propositions
- **Intelligent Prioritization**: Smart ranking ensures most relevant results surface first for faster decision-making
- **Visual Intelligence**: Trending dashboard provides immediate visibility into emerging research opportunities
- **Quality Assurance**: Credibility tracking continuously improves research accuracy and reliability
- **Adaptive Intelligence**: Learning loops refine search and curation based on user behavior patterns
- **Communication Enhancement**: Visual snapshots and multi-format delivery improve knowledge transfer
- **Proactive Monitoring**: Real-time alerts ensure immediate awareness of critical developments
- **Research Flexibility**: Adaptive depth allows scaling from quick insights to comprehensive analysis
- **Trust Building**: Contextual explanations improve user confidence in content selection
- **Pattern Recognition**: Automated trend detection reveals opportunities before competitors
- **Operational Integration**: Seamless workflow delivery ensures research fits existing business processes

## What
Build **enhanced research intelligence system** that:

### Core Research Architecture (Existing)
- Uses Jina API for web content discovery and extraction
- Curates and organizes relevant articles with quality scoring
- Delivers concise summaries with confidence scores (70-95%)
- Provides real-time research updates
- Integrates with AAI brain modules for learning

### Enhanced Research Intelligence Features
- **Smart Content Prioritization**: Dynamic ranking based on user engagement, source reliability, and content freshness
- **Real-time Trending Dashboard**: Interactive Streamlit visualization of emerging topics and key insights
- **Source Credibility Tracking**: Historical accuracy scoring with real-time adjustment based on user feedback
- **Continuous Learning Integration**: User interaction data feeding AAI brain modules for search refinement
- **Visual Insights Snapshots**: Infographic-style summaries for rapid comprehension and decision-making
- **Adaptive Depth Research**: Dynamic adjustment of research breadth based on data availability and topic importance
- **Real-time Insight Alerts**: Automated notifications when significant trends emerge via multiple channels
- **Multi-format Report Delivery**: Customizable output in PDF, interactive pages, Slack messages, email digests
- **Contextual Content Explanation**: Clear rationale for source selection improving trust and interpretability
- **Automated Trend Detection**: Pattern recognition for emerging themes with significance scoring

### Success Criteria

#### Core Research Features
- [ ] Multi-source web research using Jina API
- [ ] Content curation with quality and relevance scoring
- [ ] Concise report generation with confidence scores
- [ ] Real-time research updates and monitoring
- [ ] Integration with AAI brain modules for learning
- [ ] N8N workflow integration for automated delivery

#### Enhanced Research Intelligence
- [ ] **NEW**: Smart content prioritization with dynamic ranking algorithms
- [ ] **NEW**: Real-time trending topics dashboard (Streamlit)
- [ ] **NEW**: Source credibility tracker with historical accuracy scoring
- [ ] **NEW**: Continuous learning loop with user interaction analytics
- [ ] **NEW**: Visual "Insights Snapshots" with infographic-style summaries
- [ ] **NEW**: Adaptive depth research based on topic importance
- [ ] **NEW**: Real-time insight alerts via email/Slack/N8N workflows
- [ ] **NEW**: Multi-format report delivery (PDF, Streamlit, messages)
- [ ] **NEW**: Contextual "Why" explanations for content selection
- [ ] **NEW**: Automated trend detection with significance scoring
- [ ] Real-time research monitoring and updates
- [ ] Integration with AAI memory and learning systems

## All Needed Context

### Documentation & References
```yaml
# MUST READ
- file: /ottomator-agents/general-researcher-agent/README.md
  why: Implementation approach and research patterns
- file: /docs/jina-scraping-guide.md
  why: Jina API integration patterns
- file: /brain/Claude.md
  why: AAI research standards and confidence scoring
```

### Implementation Blueprint

```yaml
Task 1: Build Jina Research Engine
CREATE agents/research/jina_researcher.py:
  - IMPLEMENT multi-source web research using Jina API
  - ADD content quality scoring and filtering
  - INCLUDE research depth control (5-100 pages)
  - FOLLOW existing jina-scraping-guide patterns

Task 2: Create Content Curation System
CREATE agents/research/content_curator.py:
  - IMPLEMENT relevance scoring and ranking
  - ADD duplicate detection and removal
  - INCLUDE source credibility assessment
  - PROVIDE content categorization

Task 3: Build Report Generator
CREATE agents/research/report_generator.py:
  - IMPLEMENT concise summary generation
  - ADD confidence scoring for research findings
  - INCLUDE key insights extraction
  - FOLLOW AAI confidence scoring standards (70-95%)

Task 4: Add Real-Time Monitoring
CREATE agents/research/monitor.py:
  - IMPLEMENT continuous research updates
  - ADD trend detection and alerting
  - INCLUDE research freshness tracking
  - PROVIDE notification systems

Task 5: Create N8N Workflow Integration
CREATE n8n/research_workflow.py:
  - IMPLEMENT automated research workflows
  - ADD scheduled research runs
  - INCLUDE result delivery systems
  - PROVIDE workflow monitoring

Task 6: Add AAI Brain Integration
CREATE brain/modules/general-researcher.py:
  - FOLLOW AAI brain module patterns
  - ADD research learning and improvement
  - INCLUDE integration with memory systems
  - PROVIDE research analytics
```

### Data Models

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ResearchSource(BaseModel):
    url: str
    title: str
    content: str
    credibility_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    freshness_score: float = Field(ge=0.0, le=1.0)

class ResearchReport(BaseModel):
    topic: str
    sources: List[ResearchSource]
    summary: str
    key_insights: List[str]
    confidence_score: float = Field(ge=0.70, le=0.95)
    research_depth: int
    timestamp: str
```

### Validation

```python
async def test_jina_research():
    """Test Jina API research functionality"""
    researcher = JinaResearcher()
    results = await researcher.research_topic("FastAPI best practices", depth=5)
    assert len(results) > 0
    assert all(r.relevance_score > 0.5 for r in results)

async def test_report_generation():
    """Test research report generation with confidence scoring"""
    generator = ReportGenerator()
    report = await generator.generate_report(research_sources)
    assert report.confidence_score >= 0.70
    assert len(report.key_insights) >= 3
```

---

**Final Score**: 7/10 - Good confidence for implementation with proven patterns and clear scope.