---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-enhanced-repository-analyzer-20250719
project_name: enhanced_repository_analyzer
priority: high
auto_scaffold: true
integrations: [superclaude, openrouter, docker, tree-sitter]
estimated_effort: "3-4 weeks"
complexity: enterprise
tags: ["#performance", "#intelligence", "#architecture", "#ai-integration"]
created: 2025-07-19T00:00:00Z
author: claude-code
---

name: "Enhanced Repository Analyzer - Intelligent Code Intelligence Platform"
description: |

## Purpose
Transform the existing AAI repository analyzer from a solid analysis tool into a comprehensive **Intelligent Code Intelligence Platform** with semantic understanding, cross-repository analysis, predictive analytics, and real-time integration capabilities that multiply developer productivity exponentially.

## Core Principles
1. **Context is King**: Leverage semantic understanding beyond syntax analysis  
2. **Validation Loops**: Comprehensive testing with performance benchmarks
3. **Information Dense**: Deep integration with AAI brain modules and existing patterns
4. **Progressive Success**: Phased implementation with measurable performance improvements
5. **Global rules**: Follow all rules in CLAUDE.md and leverage existing brain modules
6. **Intelligence Integration**: Full AAI brain system integration for learning and enhancement

---

## Goal
Build a production-grade intelligent repository analyzer that provides:
- **60-80% performance improvements** through single-pass traversal and streaming I/O
- **Semantic code understanding** using hybrid LLM + Tree-sitter analysis  
- **Cross-repository intelligence** with dependency graphs and ecosystem health scoring
- **Predictive analytics** using ML models for quality forecasting and maintenance burden prediction
- **Real-time integration** with IDEs, CI/CD pipelines, and collaborative workspaces
- **Multi-language support** with 40+ languages via Tree-sitter integration

## Why
- **Developer Productivity**: 20x workflow integration through real-time IDE/CI integration
- **Predictive Intelligence**: 15x improvement through ML forecasting vs reactive analysis
- **Cross-Repository Insights**: 10x more comprehensive analysis through ecosystem-level understanding
- **Performance Gains**: 3-5x speedup on multi-core systems with intelligent caching
- **AAI Ecosystem**: Positions AAI as leader in intelligent code analysis and developer productivity

## What
An enterprise-grade code intelligence platform that transforms static repository analysis into dynamic, predictive, collaborative developer intelligence.

### Success Criteria
- [ ] **Performance**: 60-80% reduction in I/O operations through single-pass traversal
- [ ] **Intelligence**: Semantic understanding with 85%+ accuracy using hybrid LLM analysis
- [ ] **Scale**: Handle repositories >100MB through streaming and memory optimization
- [ ] **Integration**: Real-time IDE integration with <200ms response times
- [ ] **Collaboration**: Multi-user analysis sessions with role-based permissions
- [ ] **Predictive**: ML-powered quality forecasting with 80%+ accuracy
- [ ] **Cross-Repo**: Dependency analysis across 10+ repositories simultaneously

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://tree-sitter.github.io/tree-sitter/using-parsers/
  why: Multi-language AST parsing, incremental parsing, error recovery patterns
  critical: Tree-sitter provides 36x speedup and supports 165+ languages
  
- url: https://tree-sitter.github.io/tree-sitter/using-parsers/3-advanced-parsing.html
  why: Advanced parsing techniques, syntax tree manipulation, performance optimization
  critical: Incremental parsing allows real-time IDE integration

- url: https://pypi.org/project/tree-sitter-languages/
  why: Pre-built wheels for all major languages, no compilation required
  critical: Supports Python integration with simple Language.build_library() bypass

- url: https://realpython.com/async-io-python/
  why: AsyncIO patterns, concurrent programming, I/O optimization techniques
  critical: asyncio provides best performance for I/O-bound repository analysis

- url: https://realpython.com/python-concurrency/
  why: Concurrency models, when to use asyncio vs threading vs multiprocessing
  critical: "Use asyncio when you can, threading when you must" - perfect for file I/O

- url: https://python.useinstructor.com/blog/2023/11/13/learn-async/
  why: asyncio.gather vs asyncio.as_completed patterns for concurrent file processing
  critical: Performance gains from proper task orchestration and rate limiting

- url: https://realpython.com/lru-cache-python/
  why: LRU cache implementation, memory management, performance optimization
  critical: functools.lru_cache provides 5x-50x performance improvement for repeated operations

- url: https://pypi.org/project/diskcache/
  why: Persistent disk-based caching, gigabyte-scale storage, cross-session persistence
  critical: Enables caching git operations and AST parsing across analysis sessions

- url: https://medium.com/@yeqing_40735/building-a-secure-sandbox-for-langchains-create-pandas-dataframe-agent-using-docker-61c347aaec22
  why: Docker security patterns, resource constraints, container isolation for code analysis
  critical: Docker provides secure sandbox for analyzing untrusted repositories

- url: https://openrouter.ai/docs/quickstart
  why: OpenRouter API integration, LLM provider switching, structured outputs
  critical: Unified interface for LLM-powered semantic analysis with 40+ models

- url: https://openrouter.ai/docs/api-reference/overview
  why: Complete API documentation, authentication, error handling, rate limits
  critical: Proper API integration patterns for production LLM usage

- url: https://python.useinstructor.com/integrations/openrouter/
  why: Structured outputs with OpenRouter, type-safe responses, Pydantic integration
  critical: Enables reliable semantic analysis with validated LLM responses

- file: /mnt/c/Users/Brandon/AAI/brain/modules/github-analyzer.py
  why: Existing analyzer architecture, database patterns, security analysis integration
  critical: Base implementation with Docker integration and security scanning

- file: /mnt/c/Users/Brandon/AAI/projects/github-analyzer/analyzer_agents.py
  why: Multi-agent architecture, existing analysis patterns, performance bottlenecks identified
  critical: Agent-based system with CodeStructureAgent, SecurityAuditAgent, QualityAssessmentAgent

- file: /mnt/c/Users/Brandon/AAI/brain/modules/unified-analytics.py
  why: Cross-folder analytics, success tracking, template usage metrics, integration effectiveness
  critical: Pattern for AAI brain integration, SQLite database patterns, success scoring

- file: /mnt/c/Users/Brandon/AAI/brain/modules/integration-aware-prp-enhancer.py
  why: Integration detection patterns, persona recommendations, content analysis
  critical: AAI brain integration patterns, automatic enhancement suggestions
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "Tree-sitter Python multi-language parsing 2024"
    depth: 10
    target_folder: "projects/enhanced_repository_analyzer/research/tree-sitter"
    findings: "165+ languages supported, 36x speedup, incremental parsing, error recovery"
  - topic: "Python asyncio performance optimization patterns 2024"  
    depth: 10
    target_folder: "projects/enhanced_repository_analyzer/research/asyncio"
    findings: "asyncio.gather for concurrent ops, semaphores for rate limiting, best for I/O-bound"
  - topic: "Python LRU cache diskcache strategies 2024"
    depth: 8
    target_folder: "projects/enhanced_repository_analyzer/research/caching"
    findings: "functools.lru_cache + diskcache for persistence, gigabyte-scale storage"
  - topic: "Docker Python security sandboxing 2024"
    depth: 8
    target_folder: "projects/enhanced_repository_analyzer/research/docker"
    findings: "Resource limits, user namespaces, network isolation for secure analysis"
  - topic: "OpenRouter LLM integration patterns 2024"
    depth: 8
    target_folder: "projects/enhanced_repository_analyzer/research/openrouter"
    findings: "Unified API, structured outputs with Instructor, 40+ models available"
```

### Example Pattern References
```yaml
example_references:
  - brain/modules/github-analyzer.py
  - projects/github-analyzer/analyzer_agents.py
  - brain/modules/unified-analytics.py
  - brain/modules/integration-aware-prp-enhancer.py
pattern_similarity_threshold: 0.9
fallback_action: "enhance_existing_patterns"
```

### Current Codebase tree
```bash
AAI/
├── brain/
│   ├── modules/
│   │   ├── github-analyzer.py          # Main analyzer with Docker/security integration
│   │   ├── unified-analytics.py        # Cross-folder success tracking
│   │   └── integration-aware-prp-enhancer.py  # Integration detection patterns
│   └── cache/                          # Existing cache infrastructure
├── projects/
│   └── github-analyzer/
│       ├── analyzer_agents.py          # Multi-agent analysis system
│       ├── requirements.txt            # Current dependencies
│       └── test_github_analyzer.py     # Existing test patterns
├── requirements.txt                    # Core AAI dependencies
└── PRPs/                              # PRP template patterns
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
AAI/
├── brain/
│   └── modules/
│       └── enhanced-repository-analyzer.py     # Main orchestrator with AAI brain integration
├── projects/
│   └── enhanced-repository-analyzer/
│       ├── core/
│       │   ├── __init__.py                     # Package initialization
│       │   ├── streaming_walker.py             # Single-pass file traversal with type dispatch
│       │   ├── semantic_analyzer.py            # Hybrid LLM + Tree-sitter semantic analysis  
│       │   ├── cache_manager.py                # Multi-layer caching (memory + disk)
│       │   ├── pattern_registry.py             # Pre-compiled regex and AST patterns
│       │   └── performance_profiler.py         # Performance monitoring and optimization
│       ├── agents/
│       │   ├── __init__.py                     # Agent registry and base classes
│       │   ├── base_agent.py                   # Enhanced BaseAgent with streaming support
│       │   ├── structure_agent.py              # Multi-language structure analysis
│       │   ├── security_agent.py               # Enhanced security with tool orchestration
│       │   ├── quality_agent.py                # Quality assessment with ML predictions
│       │   ├── performance_agent.py            # Performance profiling and optimization
│       │   └── collaboration_agent.py          # Team analysis and workspace management
│       ├── integrations/
│       │   ├── __init__.py                     # Integration registry
│       │   ├── ide_integration.py              # Real-time IDE integration server
│       │   ├── cicd_integration.py             # CI/CD pipeline integration
│       │   ├── openrouter_integration.py       # LLM-powered semantic analysis
│       │   └── platform_integrations.py       # GitHub/GitLab/Bitbucket integration
│       ├── ml/
│       │   ├── __init__.py                     # ML model registry
│       │   ├── predictive_models.py            # Quality forecasting and risk prediction
│       │   ├── anomaly_detection.py            # Pattern anomaly and trend analysis
│       │   └── recommendation_engine.py       # Feature extraction and similarity matching
│       ├── collaborative/
│       │   ├── __init__.py                     # Collaboration framework
│       │   ├── workspace_manager.py            # Multi-user analysis sessions
│       │   ├── annotation_system.py            # Collaborative commenting and analysis
│       │   └── knowledge_base.py              # Community-driven pattern sharing
│       ├── api/
│       │   ├── __init__.py                     # FastAPI application factory
│       │   ├── main.py                         # FastAPI server with async endpoints
│       │   ├── models.py                       # Pydantic v2 models for API
│       │   ├── routes/                         # API route modules
│       │   │   ├── analysis.py                 # Repository analysis endpoints
│       │   │   ├── collaboration.py            # Collaborative analysis endpoints
│       │   │   └── monitoring.py              # Real-time monitoring endpoints
│       │   └── middleware.py                   # Rate limiting, auth, monitoring
│       ├── tests/
│       │   ├── __init__.py                     # Test configuration
│       │   ├── conftest.py                     # Pytest fixtures and configuration
│       │   ├── test_streaming_walker.py        # Single-pass traversal tests
│       │   ├── test_semantic_analyzer.py       # Semantic analysis tests
│       │   ├── test_cache_manager.py           # Caching strategy tests
│       │   ├── test_agents.py                  # Agent functionality tests
│       │   ├── test_integrations.py            # Integration tests
│       │   ├── test_performance.py             # Performance benchmark tests
│       │   └── fixtures/                       # Test repository fixtures
│       ├── config/
│       │   ├── settings.py                     # Configuration management
│       │   ├── logging.yaml                    # Logging configuration
│       │   └── docker/                         # Docker configuration files
│       ├── scripts/
│       │   ├── benchmark.py                    # Performance benchmarking
│       │   ├── migrate_data.py                 # Data migration from existing analyzer
│       │   └── setup_development.py           # Development environment setup
│       ├── requirements.txt                    # Enhanced dependencies
│       ├── Dockerfile                          # Production container
│       ├── docker-compose.yml                  # Development environment
│       └── README.md                           # Documentation and setup guide
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: AAI uses specific patterns for brain integration
# Example: All brain modules must use sqlite3 for persistence (see unified-analytics.py)
# Example: Integration detection patterns follow regex-based matching (see integration-aware-prp-enhancer.py)

# CRITICAL: Tree-sitter requires proper language installation
# Example: Use tree-sitter-languages package for pre-built wheels
# Example: Language.build_library() can be bypassed with pre-compiled languages

# CRITICAL: AsyncIO requires careful context manager usage
# Example: aiofiles for non-blocking file I/O, aiosqlite for database operations
# Example: Use asyncio.Semaphore for rate limiting to prevent resource exhaustion

# CRITICAL: Docker security patterns are essential
# Example: Always use non-root users, resource limits, and network isolation
# Example: Container should run with read-only filesystems where possible

# CRITICAL: OpenRouter API requires authentication and rate limiting
# Example: Use OPENROUTER_API_KEY environment variable
# Example: Implement exponential backoff for 429 rate limit errors

# CRITICAL: FastAPI + Pydantic v2 patterns
# Example: Use async def for all endpoints that do I/O operations
# Example: Pydantic v2 has different validation patterns than v1

# CRITICAL: AAI brain modules use specific database schema patterns
# Example: Use TEXT columns with JSON serialization for complex data
# Example: Always include created_date and last_updated timestamps
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "brain/modules/unified-analytics.py"
      reason: "Success tracking and analytics integration"
    - module: "brain/modules/integration-aware-prp-enhancer.py"  
      reason: "Integration detection and enhancement patterns"
    - prp: "PRPs/templates/prp_base.md"
      reason: "Follows AAI PRP architecture standards"
  external:
    - package: "tree-sitter ≥ 0.21.3"
      reason: "Multi-language AST parsing with 36x performance improvement"
    - package: "tree-sitter-languages ≥ 1.10.2" 
      reason: "Pre-built wheels for 165+ languages, no compilation required"
    - package: "aiosqlite ≥ 0.17.0"
      reason: "Async SQLite for non-blocking database operations"
    - package: "aiosqlitepool ≥ 1.0.0"
      reason: "High-performance connection pooling for concurrent access"
    - package: "diskcache ≥ 5.6.3"
      reason: "Persistent caching with gigabyte-scale storage capacity"
    - package: "fastapi ≥ 0.100.0"
      reason: "Async API framework with Pydantic v2 support"
    - package: "instructor ≥ 0.4.0"
      reason: "Structured LLM outputs with OpenRouter integration"
    - package: "docker ≥ 7.1.0"
      reason: "Secure sandboxing for untrusted repository analysis"
    - package: "pytest-asyncio ≥ 0.23.0"
      reason: "Async testing framework for concurrent operations"
    - package: "pytest-benchmark ≥ 4.0.0"
      reason: "Performance benchmarking and regression testing"
  conflicts:
    - issue: "Pydantic v1 vs v2 compatibility with existing AAI modules"
      mitigation: "Use Pydantic v2 throughout, add compatibility layer if needed"
    - issue: "Tree-sitter compilation requirements on some systems"
      mitigation: "Use tree-sitter-languages pre-built wheels to avoid compilation"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "brain/modules/github-analyzer.py"
    - "projects/github-analyzer/analyzer_agents.py"
    - "brain/modules/unified-analytics.py"
    - "requirements.txt"
  external_documentation_current:
    - check: "Tree-sitter documentation updated within 90 days"
    - check: "OpenRouter API documentation current"
    - check: "FastAPI + Pydantic v2 compatibility confirmed"
  example_relevance:
    - similarity_threshold: 0.9
    - fallback: "Enhance existing patterns rather than create new"
```

## 📦 Implementation Readiness Assessment

### 🔧 Auto-Generated Readiness Validation Script
```bash
# Generated script: ./scripts/validate_prp_readiness.py
# Run before implementation to identify blockers
python scripts/validate_prp_readiness.py --prp enhanced-repository-analyzer --report json
```

### 🚪 Implementation Gates

#### Infrastructure Gates
```yaml
infrastructure_gates:
  development_environment:
    - service: "Docker Desktop"
      test: "docker --version"
      expected: "Docker version 20.x or higher"
      owner: "user"
      time_to_fix: "10 minutes"
      
  memory_requirements:
    - requirement: "Available RAM ≥ 8GB"
      test: "free -h | grep Mem"
      expected: "≥ 8GB total memory"
      fallback: "Reduce concurrent analysis workers"
      owner: "user"
      
  disk_space:
    - requirement: "Available disk space ≥ 10GB"
      test: "df -h /"
      expected: "≥ 10GB available"
      fallback: "Clean up cache directories"
      owner: "user"
```

#### Credential Gates
```yaml
credential_gates:
  critical:
    - credential: "OPENROUTER_API_KEY"
      location: ".env"
      validation: "curl -H 'Authorization: Bearer $OPENROUTER_API_KEY' https://openrouter.ai/api/v1/models"
      expected: "200 OK with models list"
      owner: "user"
      setup_guide: "https://openrouter.ai/docs/quickstart"
      time_to_fix: "5 minutes"
      
  optional:
    - credential: "GITHUB_TOKEN"
      location: ".env"
      validation: "curl -H 'Authorization: token $GITHUB_TOKEN' https://api.github.com/user"
      expected: "200 OK with user data"
      fallback: "Limited to public repositories only"
      impact: "Private repository analysis unavailable"
```

#### Dependency Gates
```yaml
system_dependencies:
  python_packages:
    - package: "tree-sitter>=0.21.3"
      install: "pip install tree-sitter>=0.21.3"
      validation: "python -c 'import tree_sitter; print(tree_sitter.__version__)'"
      expected: "≥0.21.3"
      
    - package: "tree-sitter-languages>=1.10.2"
      install: "pip install tree-sitter-languages>=1.10.2"
      validation: "python -c 'from tree_sitter_languages import get_language; print(get_language(\"python\"))'"
      expected: "Language object returned"
      
    - package: "fastapi>=0.100.0"
      install: "pip install fastapi>=0.100.0"
      validation: "python -c 'import fastapi; print(fastapi.__version__)'"
      expected: "≥0.100.0"
      
  external_services:
    - service: "docker"
      validation: "docker --version"
      expected: "Docker version"
      fallback: "Skip sandboxed analysis features"
      
database_gates:
  sqlite_support:
    - test: "python -c 'import sqlite3; print(sqlite3.sqlite_version)'"
      expected: "≥3.35.0"
      fallback: "Core functionality available, advanced features disabled"
```

#### Environment Gates
```yaml
environment_validation:
  required_directories:
    - path: "projects/enhanced-repository-analyzer/"
      create_if_missing: true
    - path: "brain/cache/"
      create_if_missing: true
    - path: "logs/"
      create_if_missing: true
      
  required_files:
    - file: ".env"
      template: ".env.example"
      required_vars: ["OPENROUTER_API_KEY"]
      
  configuration_files:
    - file: "config/settings.py"
      validation: "python -c 'from config.settings import get_settings; print(get_settings())'"
      expected: "Settings object with valid configuration"
```

### 📊 Readiness Scoring & Thresholds

```yaml
readiness_scoring:
  gate_weights:
    infrastructure: 0.25    # Development environment setup
    credentials: 0.35       # API keys and authentication
    dependencies: 0.30      # Python packages and external tools
    environment: 0.10       # Files, directories, configuration
    
  phase_thresholds:
    Phase_1_Core_Development: 75%   # Can start core streaming and caching
    Phase_2_Intelligence: 85%       # Can begin semantic analysis and ML
    Phase_3_Integration: 95%        # Can add real-time and collaborative features
    
  fallback_strategies:
    90-100%: "Full implementation - all advanced features enabled"
    75-89%: "Core implementation - defer ML and collaboration features"  
    60-74%: "Basic implementation - enhanced performance only"
    <60%: "HALT - resolve critical dependencies first"
```

## Implementation Blueprint

### Data models and structure

Create the core data models, ensuring type safety and consistency with Pydantic v2 patterns.

```python
# Enhanced data models with semantic analysis support
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum

class AnalysisScope(str, Enum):
    STRUCTURE = "structure"
    SEMANTIC = "semantic" 
    SECURITY = "security"
    PERFORMANCE = "performance"
    COLLABORATION = "collaboration"

class SemanticFeature(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str = Field(..., description="Feature name extracted by semantic analysis")
    type: str = Field(..., description="Feature type: function, class, module, pattern")
    intent: str = Field(..., description="LLM-analyzed intent and purpose")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence score")
    complexity_score: float = Field(..., ge=0.0, le=1.0, description="Complexity assessment")
    file_path: str = Field(..., description="Source file location")
    line_range: tuple[int, int] = Field(..., description="Start and end line numbers")
    dependencies: List[str] = Field(default_factory=list, description="Identified dependencies")
    api_surface: Dict[str, Any] = Field(default_factory=dict, description="Public API definition")
    documentation: Optional[str] = Field(None, description="Extracted documentation")

class RepositoryMetrics(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    total_files: int = Field(..., ge=0)
    total_lines: int = Field(..., ge=0)
    language_distribution: Dict[str, float] = Field(default_factory=dict)
    complexity_metrics: Dict[str, float] = Field(default_factory=dict)
    test_coverage: Optional[float] = Field(None, ge=0.0, le=1.0)
    documentation_score: float = Field(..., ge=0.0, le=1.0)
    
class PredictiveAnalysis(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    quality_trajectory: Dict[str, float] = Field(default_factory=dict)
    maintenance_burden: float = Field(..., ge=0.0, le=1.0)
    security_risk_score: float = Field(..., ge=0.0, le=1.0)
    technical_debt_estimate: float = Field(..., ge=0.0)
    recommended_actions: List[str] = Field(default_factory=list)
    confidence_interval: tuple[float, float] = Field(..., description="Prediction confidence bounds")

class EnhancedAnalysisResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    analysis_id: str = Field(..., description="Unique analysis identifier")
    repository_url: str = Field(..., description="Repository URL or path")
    analysis_scope: List[AnalysisScope] = Field(..., description="Scopes included in analysis")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Core analysis results
    repository_metrics: RepositoryMetrics
    semantic_features: List[SemanticFeature] = Field(default_factory=list)
    predictive_analysis: Optional[PredictiveAnalysis] = None
    
    # Performance and execution data
    execution_time: float = Field(..., ge=0.0, description="Total analysis time in seconds")
    cache_hit_rate: float = Field(..., ge=0.0, le=1.0, description="Caching efficiency")
    memory_peak_mb: float = Field(..., ge=0.0, description="Peak memory usage")
    
    # Collaboration and sharing
    shared_with: List[str] = Field(default_factory=list, description="Team members with access")
    annotations: List[Dict[str, Any]] = Field(default_factory=list, description="Collaborative annotations")
    
    success: bool = Field(..., description="Analysis completion status")
    errors: List[str] = Field(default_factory=list, description="Error messages")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1: Core Infrastructure Setup
CREATE projects/enhanced-repository-analyzer/core/streaming_walker.py:
  - IMPLEMENT StreamingFileWalker class with single-pass traversal
  - MIRROR pattern from: projects/github-analyzer/analyzer_agents.py MultiAgentOrchestrator
  - ADD asyncio.Semaphore for concurrent file processing
  - PRESERVE memory efficiency with generator patterns

CREATE projects/enhanced-repository-analyzer/core/cache_manager.py:
  - IMPLEMENT multi-layer caching (LRU + diskcache)
  - MIRROR pattern from: brain/modules/unified-analytics.py database patterns
  - ADD cache invalidation and persistence strategies
  - KEEP performance optimization as primary goal

CREATE projects/enhanced-repository-analyzer/core/pattern_registry.py:
  - IMPLEMENT pre-compiled regex and AST pattern storage
  - MIRROR pattern from: brain/modules/integration-aware-prp-enhancer.py patterns
  - ADD pattern versioning and dynamic loading
  - PRESERVE existing pattern compatibility

Task 2: Enhanced Agent Architecture
MODIFY projects/enhanced-repository-analyzer/agents/base_agent.py:
  - ENHANCE BaseAnalyzerAgent from analyzer_agents.py
  - ADD streaming support and semantic analysis interface
  - INJECT caching and performance monitoring
  - PRESERVE existing agent compatibility

CREATE projects/enhanced-repository-analyzer/agents/semantic_analyzer.py:
  - IMPLEMENT hybrid LLM + Tree-sitter analysis
  - MIRROR pattern from: brain/modules/github-analyzer.py structure analysis
  - ADD OpenRouter integration with structured outputs
  - KEEP semantic understanding as core capability

ENHANCE projects/enhanced-repository-analyzer/agents/structure_agent.py:
  - EXTEND CodeStructureAgent with Tree-sitter multi-language support
  - ADD incremental parsing and error recovery
  - INJECT performance optimizations and caching
  - PRESERVE existing analysis output format

Task 3: Intelligence and ML Integration
CREATE projects/enhanced-repository-analyzer/ml/predictive_models.py:
  - IMPLEMENT quality forecasting using historical patterns
  - MIRROR pattern from: brain/modules/unified-analytics.py success patterns
  - ADD ML model training and prediction pipelines
  - KEEP AAI brain integration for learning

CREATE projects/enhanced-repository-analyzer/ml/anomaly_detection.py:
  - IMPLEMENT pattern anomaly detection using statistical methods
  - ADD trend analysis and regression detection
  - INJECT real-time monitoring capabilities
  - PRESERVE performance monitoring focus

CREATE projects/enhanced-repository-analyzer/integrations/openrouter_integration.py:
  - IMPLEMENT OpenRouter API client with rate limiting
  - MIRROR pattern from: brain/modules/integration-aware-prp-enhancer.py API patterns
  - ADD structured output parsing with Instructor
  - KEEP semantic analysis as primary use case

Task 4: API and Real-time Integration  
CREATE projects/enhanced-repository-analyzer/api/main.py:
  - IMPLEMENT FastAPI application with async endpoints
  - MIRROR pattern from: existing AAI FastAPI usage (check requirements.txt)
  - ADD WebSocket support for real-time updates
  - PRESERVE RESTful API design principles

CREATE projects/enhanced-repository-analyzer/api/routes/analysis.py:
  - IMPLEMENT analysis endpoints with streaming responses
  - ADD progress tracking and real-time updates
  - INJECT rate limiting and authentication
  - KEEP async/await patterns throughout

CREATE projects/enhanced-repository-analyzer/integrations/ide_integration.py:
  - IMPLEMENT WebSocket server for IDE communication
  - ADD incremental analysis and context-aware suggestions
  - INJECT caching for sub-200ms response times
  - PRESERVE developer workflow integration focus

Task 5: Collaborative Features
CREATE projects/enhanced-repository-analyzer/collaborative/workspace_manager.py:
  - IMPLEMENT multi-user analysis sessions
  - MIRROR pattern from: brain/modules/unified-analytics.py tracking patterns
  - ADD role-based permissions and access control
  - KEEP team productivity as primary goal

CREATE projects/enhanced-repository-analyzer/collaborative/annotation_system.py:
  - IMPLEMENT collaborative commenting on analysis results
  - ADD real-time synchronization across team members
  - INJECT version control for annotations
  - PRESERVE context and analysis correlation

Task 6: Performance Optimization and Monitoring
CREATE projects/enhanced-repository-analyzer/core/performance_profiler.py:
  - IMPLEMENT performance monitoring and bottleneck detection
  - ADD memory usage tracking and optimization suggestions
  - INJECT real-time performance metrics
  - KEEP optimization as continuous improvement focus

ENHANCE projects/enhanced-repository-analyzer/tests/test_performance.py:
  - IMPLEMENT comprehensive performance benchmarks
  - ADD regression testing for performance improvements
  - INJECT automated performance validation
  - PRESERVE performance target validation

Task 7: AAI Brain Integration
CREATE brain/modules/enhanced-repository-analyzer.py:
  - IMPLEMENT AAI brain integration module
  - MIRROR pattern from: brain/modules/unified-analytics.py integration
  - ADD success tracking and learning integration
  - PRESERVE AAI intelligence system compatibility

MODIFY brain/modules/unified-analytics.py:
  - EXTEND analytics to track enhanced analyzer usage
  - ADD performance metrics and improvement tracking
  - INJECT enhanced analyzer success patterns
  - PRESERVE existing analytics functionality

Task 8: Testing and Validation
CREATE projects/enhanced-repository-analyzer/tests/conftest.py:
  - IMPLEMENT pytest fixtures for async testing
  - MIRROR pattern from: existing test patterns in projects/github-analyzer/
  - ADD performance testing fixtures and benchmarks
  - PRESERVE test isolation and repeatability

CREATE projects/enhanced-repository-analyzer/tests/test_streaming_walker.py:
  - IMPLEMENT single-pass traversal validation tests
  - ADD performance benchmarks vs multiple traversals
  - INJECT memory usage validation
  - KEEP 60-80% I/O improvement validation

CREATE projects/enhanced-repository-analyzer/tests/test_semantic_analyzer.py:
  - IMPLEMENT semantic analysis accuracy tests
  - ADD LLM integration testing with mocked responses
  - INJECT confidence score validation
  - PRESERVE 85%+ accuracy requirement validation
```

### Per task pseudocode as needed added to each task

```python
# Task 1: StreamingFileWalker Implementation
class StreamingFileWalker:
    def __init__(self, max_concurrent: int = 4):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.agent_registry = {}  # From existing agent patterns
        
    async def walk_repository(self, repo_path: Path) -> AsyncIterator[AnalysisResult]:
        # PATTERN: Single-pass traversal like rglob but with type dispatch
        file_batches = self._group_files_by_type(repo_path)
        
        # CRITICAL: Use asyncio.TaskGroup for proper error handling (Python 3.11+)
        async with asyncio.TaskGroup() as tg:
            for file_type, files in file_batches.items():
                # PATTERN: Semaphore prevents resource exhaustion
                async with self.semaphore:
                    task = tg.create_task(self._process_file_batch(file_type, files))
                    yield await task
    
    def _group_files_by_type(self, repo_path: Path) -> Dict[str, List[Path]]:
        # GOTCHA: Use os.scandir() for better performance than pathlib.rglob()
        # PATTERN: Group by extension to minimize agent switching overhead
        batches = defaultdict(list)
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = Path(root) / file
                file_type = file_path.suffix.lower()
                batches[file_type].append(file_path)
        return batches

# Task 2: Semantic Analysis with OpenRouter
class SemanticAnalyzer:
    def __init__(self, openrouter_client):
        self.client = openrouter_client
        self.tree_sitter_parser = self._init_tree_sitter()
        
    async def analyze_intent(self, code_fragment: str, language: str) -> SemanticFeature:
        # PATTERN: Hybrid approach - Tree-sitter for structure, LLM for intent
        tree = self.tree_sitter_parser[language].parse(code_fragment.encode())
        structure = self._extract_structure(tree)
        
        # CRITICAL: Use Instructor for structured LLM outputs
        semantic_analysis = await self.client.chat.completions.create(
            model="anthropic/claude-3-haiku",
            response_model=SemanticFeature,
            messages=[{
                "role": "user", 
                "content": f"Analyze this {language} code intent: {code_fragment}"
            }]
        )
        
        # PATTERN: Merge structural and semantic analysis
        return self._merge_analysis(structure, semantic_analysis)

# Task 3: Multi-layer Caching Strategy  
class CacheManager:
    def __init__(self, memory_size: int = 1000, disk_cache_dir: Path = None):
        # PATTERN: LRU for hot data, diskcache for persistence
        self.memory_cache = LRUCache(maxsize=memory_size)
        self.disk_cache = diskcache.Cache(str(disk_cache_dir or Path('.cache')))
        
    async def cached_analysis(self, cache_key: str, analysis_func: Callable) -> Any:
        # PATTERN: Check memory first, then disk, then compute
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
            
        if cache_key in self.disk_cache:
            result = self.disk_cache[cache_key]
            self.memory_cache[cache_key] = result  # Promote to memory
            return result
            
        # CRITICAL: Only compute if not cached anywhere
        result = await analysis_func()
        self.disk_cache[cache_key] = result
        self.memory_cache[cache_key] = result
        return result

# Task 4: Real-time IDE Integration
class IDEIntegrationServer:
    def __init__(self, analyzer: EnhancedAnalyzer):
        self.analyzer = analyzer
        self.active_sessions = {}
        
    async def handle_code_change(self, websocket: WebSocket, file_path: str, content: str):
        # PATTERN: Incremental analysis for <200ms response
        session_id = websocket.headers.get("session-id")
        
        # CRITICAL: Use Tree-sitter incremental parsing
        if session_id in self.active_sessions:
            old_tree = self.active_sessions[session_id].get('tree')
            new_tree = self.parser.parse(content.encode(), old_tree)
        else:
            new_tree = self.parser.parse(content.encode())
            
        # PATTERN: Only analyze changed nodes for performance
        changed_ranges = self._get_changed_ranges(old_tree, new_tree)
        analysis = await self.analyzer.analyze_incremental(changed_ranges, content)
        
        await websocket.send_json({
            "type": "analysis_update",
            "file_path": file_path,
            "analysis": analysis.dict(),
            "response_time_ms": self._calculate_response_time()
        })

# Task 5: Performance Monitoring Integration
class PerformanceProfiler:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    async def profile_analysis(self, analysis_func: Callable) -> Tuple[Any, Dict]:
        # PATTERN: Comprehensive performance tracking
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = await analysis_func()
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss
            
            metrics = {
                "execution_time": end_time - start_time,
                "memory_delta_mb": (end_memory - start_memory) / 1024 / 1024,
                "cache_hit_rate": self._calculate_cache_hit_rate(),
                "io_operations": self._count_io_operations()
            }
            
            # CRITICAL: Track performance trends for optimization
            self._update_performance_trends(metrics)
            
            return result, metrics
            
        except Exception as e:
            # PATTERN: Don't let monitoring break analysis
            logging.error(f"Performance profiling error: {e}")
            return await analysis_func(), {}
```

### Integration Points
```yaml
DATABASE:
  - migration: "CREATE TABLE enhanced_analysis_results (...)"
  - index: "CREATE INDEX idx_analysis_performance ON enhanced_analysis_results(execution_time)"
  - pattern: "Use aiosqlite with connection pooling for concurrent access"
  
CONFIG:
  - add to: projects/enhanced-repository-analyzer/config/settings.py
  - pattern: "class Settings(BaseSettings): OPENROUTER_API_KEY: str = Field(..., env='OPENROUTER_API_KEY')"
  
ROUTES:
  - add to: projects/enhanced-repository-analyzer/api/main.py
  - pattern: "app.include_router(analysis_router, prefix='/api/v1/analysis')"
  
AAI_BRAIN:
  - integration: brain/modules/enhanced-repository-analyzer.py
  - pattern: "Follow unified-analytics.py database and tracking patterns"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check projects/enhanced-repository-analyzer/ --fix  # Auto-fix what's possible
mypy projects/enhanced-repository-analyzer/              # Type checking
black projects/enhanced-repository-analyzer/              # Code formatting

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests with Performance Benchmarks
```python
# CREATE comprehensive test suite with performance validation
@pytest.mark.asyncio
async def test_streaming_walker_performance():
    """Validate 60-80% I/O improvement vs multiple traversals"""
    test_repo = create_test_repository(files=1000, size_mb=50)
    
    # Test single-pass traversal
    walker = StreamingFileWalker()
    start_time = time.perf_counter()
    results = []
    async for result in walker.walk_repository(test_repo):
        results.append(result)
    single_pass_time = time.perf_counter() - start_time
    
    # Test multiple traversals (current approach)
    start_time = time.perf_counter()
    multiple_results = []
    for agent in [StructureAgent(), SecurityAgent(), QualityAgent()]:
        agent_results = await agent.analyze(test_repo)
        multiple_results.append(agent_results)
    multiple_pass_time = time.perf_counter() - start_time
    
    # CRITICAL: Validate 60% improvement minimum
    improvement = (multiple_pass_time - single_pass_time) / multiple_pass_time
    assert improvement >= 0.6, f"Only {improvement:.1%} improvement, need ≥60%"

@pytest.mark.asyncio 
async def test_semantic_analysis_accuracy():
    """Validate 85%+ semantic analysis accuracy"""
    test_cases = load_semantic_test_cases()  # Ground truth dataset
    analyzer = SemanticAnalyzer(mock_openrouter_client)
    
    correct_predictions = 0
    for code_sample, expected_intent in test_cases:
        result = await analyzer.analyze_intent(code_sample, "python")
        if semantic_similarity(result.intent, expected_intent) >= 0.8:
            correct_predictions += 1
    
    accuracy = correct_predictions / len(test_cases)
    assert accuracy >= 0.85, f"Accuracy {accuracy:.1%} below 85% requirement"

@pytest.mark.asyncio
async def test_cache_performance():
    """Validate caching provides expected speedup"""
    cache_manager = CacheManager()
    
    # First run - cache miss
    start_time = time.perf_counter()
    result1 = await cache_manager.cached_analysis("test_key", expensive_analysis)
    first_run_time = time.perf_counter() - start_time
    
    # Second run - cache hit
    start_time = time.perf_counter()  
    result2 = await cache_manager.cached_analysis("test_key", expensive_analysis)
    second_run_time = time.perf_counter() - start_time
    
    speedup = first_run_time / second_run_time
    assert speedup >= 10, f"Cache speedup {speedup:.1f}x below 10x expectation"
    assert result1 == result2, "Cached result differs from original"
```

```bash
# Run and iterate until passing:
pytest projects/enhanced-repository-analyzer/tests/ -v --benchmark-only
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test with Performance Validation
```bash
# Start the enhanced analyzer API
uvicorn projects.enhanced-repository-analyzer.api.main:app --reload --port 8001

# Test real repository analysis with performance tracking
curl -X POST http://localhost:8001/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "repository_url": "https://github.com/octocat/Hello-World.git",
    "analysis_scope": ["structure", "semantic", "performance"],
    "performance_targets": {
      "max_execution_time": 60,
      "max_memory_mb": 500,
      "min_cache_hit_rate": 0.3
    }
  }'

# Expected: {
#   "success": true, 
#   "analysis_id": "...",
#   "performance_metrics": {
#     "execution_time": <60,
#     "memory_peak_mb": <500,
#     "cache_hit_rate": >0.3
#   }
# }
```

### Level 4: Custom Validation Scripts
```yaml
custom_validations:
  performance:
    - script: "scripts/benchmark.py"
    - requirements: ["60%+ I/O improvement", "85%+ semantic accuracy", "sub-200ms IDE response"]
  integration:
    - script: "scripts/integration_test.py" 
    - description: "Validates AAI brain integration and success tracking"
  scalability:
    - script: "scripts/scalability_test.py"
    - requirements: ["handle 100MB+ repos", "concurrent analysis support"]
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  performance:
    - metric: "I/O Operation Reduction"
      target: "≥ 60%"
      measurement: "Compare single-pass vs multi-pass traversal"
      validation_gate: "unit_tests"
  intelligence:
    - metric: "Semantic Analysis Accuracy"  
      target: "≥ 85%"
      measurement: "Ground truth dataset validation"
      validation_gate: "integration_tests"
  scalability:
    - metric: "Repository Size Support"
      target: "≥ 100MB"
      measurement: "Memory usage monitoring during large repo analysis"
      validation_gate: "scalability_tests"
  integration:
    - metric: "IDE Response Time"
      target: "≤ 200ms"
      measurement: "WebSocket response time measurement"
      validation_gate: "real_time_tests"
  collaboration:
    - metric: "Multi-user Session Support"
      target: "≥ 10 concurrent users"
      measurement: "Load testing with simulated users"
      validation_gate: "load_tests"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md"
  success_tracker: "brain/modules/score-tracker.md" 
  auto_tag: ["#performance", "#intelligence", "#enterprise"]
  promotion_threshold: 4.8  # Auto-promote to SOP if score ≥ 4.8
```

### AAI Brain System Integration
```yaml
aai_integration:
  brain_modules:
    - "unified-analytics.py"  # For success tracking and pattern analysis
    - "integration-aware-prp-enhancer.py"  # For enhancement recommendations
    - "contradiction-check.py"  # For validation and consistency
  auto_triggers:
    - on_completion: "update_performance_metrics" 
    - on_success: "promote_to_enterprise_pattern"
    - on_failure: "log_learning_event_with_performance_data"
    - on_performance_improvement: "auto_generate_optimization_sop"
```

## Final validation Checklist
- [ ] All tests pass: `pytest projects/enhanced-repository-analyzer/tests/ -v`
- [ ] No linting errors: `ruff check projects/enhanced-repository-analyzer/`
- [ ] No type errors: `mypy projects/enhanced-repository-analyzer/`
- [ ] Performance benchmarks meet targets: `pytest --benchmark-only`
- [ ] Integration tests successful: API endpoints respond correctly
- [ ] Memory usage within limits: <500MB for 100MB repository
- [ ] Real-time features working: <200ms IDE integration response
- [ ] Collaborative features functional: Multi-user sessions supported
- [ ] AAI brain integration active: Success tracking and analytics working
- [ ] Documentation complete: Setup guide and API documentation
- [ ] Success metrics achieved: All performance targets met
- [ ] Learning events logged: Pattern promotion and SOP generation
- [ ] Example patterns updated: High-performing patterns documented

---

## Anti-Patterns to Avoid
- ❌ Don't use multiple repository traversals - implement single-pass streaming
- ❌ Don't load entire files into memory - use streaming and chunked processing
- ❌ Don't compile regex patterns repeatedly - use pre-compiled pattern registry
- ❌ Don't ignore performance monitoring - track all optimization targets
- ❌ Don't skip caching strategies - implement multi-layer caching from start
- ❌ Don't break AAI brain integration - follow existing module patterns
- ❌ Don't ignore concurrent access patterns - use proper async/await throughout
- ❌ Don't skip real-time capabilities - implement WebSocket integration early
- ❌ Don't forget collaborative features - build multi-user support from foundation
- ❌ Don't bypass semantic analysis - LLM integration is core differentiator