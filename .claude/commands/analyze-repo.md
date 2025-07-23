# /analyze-repo - Enhanced Repository Analysis

## Purpose
Perform comprehensive intelligent repository analysis using the Enhanced Repository Analyzer system. Provides deep code understanding, semantic analysis, performance metrics, and integration recommendations with 60-80% I/O performance improvements.

## Usage
```
/analyze-repo [repository_path] [--semantic] [--cache] [--performance] [--integrations] [--format json|markdown]
```

## Arguments
- `repository_path` - Path to repository (defaults to current directory)
- `--semantic` - Enable semantic analysis with LLM integration
- `--cache` - Force cache refresh for analysis
- `--performance` - Include detailed performance benchmarks
- `--integrations` - Generate integration recommendations  
- `--format` - Output format (json, markdown, default: markdown)

## Features

### Core Analysis
- **Single-pass file traversal** - 60-80% I/O performance improvement
- **Multi-language support** - 40+ languages via Tree-sitter
- **Pattern detection** - Security, quality, and architectural patterns
- **Structure analysis** - Dependencies, components, and relationships

### Semantic Understanding
- **Hybrid LLM + Tree-sitter** - 85%+ accuracy semantic analysis
- **Intent extraction** - Business logic and purpose identification  
- **Design pattern recognition** - Architectural pattern detection
- **Complexity scoring** - Code complexity and maintainability metrics

### Performance Optimization
- **Multi-layer caching** - LRU memory + persistent disk cache
- **Concurrent processing** - Configurable parallelism
- **Rate limiting** - API call management for LLM integration
- **Memory efficiency** - Optimized resource usage

### Integration Intelligence
- **AAI brain integration** - Learning and analytics tracking
- **Recommendation engine** - Suggested integrations and improvements
- **Performance validation** - Automated benchmark verification
- **Session tracking** - Historical analysis and trends

## Implementation

### Core Components
```python
# StreamingFileWalker - Single-pass traversal
walker = StreamingFileWalker(max_concurrent=4, batch_size=50)

# CacheManager - Multi-layer caching  
cache = CacheManager(memory_size=1000, ttl_hours=24)

# PatternRegistry - Pre-compiled patterns
patterns = PatternRegistry()  # 12+ security/quality patterns

# SemanticAnalyzer - Hybrid analysis
semantic = SemanticAnalyzer(openrouter_client)

# StructureAgent - Multi-language analysis
structure = StructureAgent(cache, patterns, semantic)
```

### Analysis Pipeline
1. **Repository discovery** - Intelligent file type detection
2. **Single-pass traversal** - Concurrent processing with batching
3. **Pattern matching** - Security, quality, architectural patterns
4. **Semantic analysis** - LLM-powered intent and design extraction
5. **Performance metrics** - Benchmark validation against targets
6. **Integration recommendations** - AAI brain-powered suggestions
7. **Report generation** - Comprehensive analysis results

### Performance Targets
- **I/O Improvement**: 60-80% vs traditional multi-pass
- **Semantic Accuracy**: 85%+ confidence on feature detection
- **Processing Rate**: 10+ files/second for large repositories
- **Cache Hit Rate**: 30%+ for repeated operations
- **Memory Usage**: <500MB for typical repositories

## Execution
1. Initialize Enhanced Repository Analyzer components
2. Configure analysis parameters based on arguments
3. Execute comprehensive repository analysis
4. Generate performance metrics and validation
5. Provide structured results with recommendations
6. Update AAI brain with learning events

## Claude Code Integration
- Uses **Bash** for system integration and validation
- Leverages **Read/Write** for repository file analysis
- Applies **TodoWrite** for progress tracking
- Maintains structured analysis workflow

## Output Format

### Markdown Report
```markdown
# Repository Analysis Report

## Executive Summary
- Repository: [path]
- Analysis Types: [structure, semantic, patterns]
- Execution Time: [time]s
- Files Processed: [count]
- Success Rate: [percentage]

## Performance Metrics
- I/O Improvement: [percentage]% vs traditional
- Files/Second: [rate]
- Cache Hit Rate: [percentage]%
- Memory Efficiency: [rating]

## Structure Analysis
- Languages Detected: [list]
- Total Files: [count]
- Code Structure: [details]
- Dependencies: [list]

## Semantic Features
- Functions Detected: [count]
- Classes Detected: [count]
- High Confidence Features: [count]
- Design Patterns: [list]

## Pattern Detection
- Security Issues: [count]
- Quality Issues: [count]
- TODO/FIXME: [count]
- Architecture Patterns: [list]

## Integration Recommendations
- Recommended Integrations: [list]
- Confidence Scores: [details]
- Benefits: [descriptions]

## AAI Brain Integration
- Session ID: [id]
- Learning Events: [count]
- Analytics Updated: [status]
```

### JSON Output
```json
{
  "session_id": "session_timestamp",
  "repository_path": "/path/to/repo",
  "analysis_types": ["structure", "semantic", "patterns"],
  "performance_metrics": {
    "total_execution_time": 2.45,
    "files_per_second": 156.3,
    "cache_hit_rate": 0.42,
    "semantic_accuracy": 0.87
  },
  "structure_analysis": {
    "success": true,
    "data": { "file_structure": {...}, "languages": [...] },
    "patterns_matched": 5,
    "cache_hit": false
  },
  "semantic_analysis": {
    "features_count": 23,
    "high_confidence_features": 20,
    "features": [...]
  },
  "integration_recommendations": [
    {
      "type": "openrouter",
      "confidence": 0.9,
      "reason": "AI/LLM integration patterns detected",
      "benefits": ["Semantic analysis", "Content generation"]
    }
  ],
  "success": true
}
```

## Error Handling
- Graceful Tree-sitter parser failures with fallback mode
- Import resolution for relative imports in modules
- Memory and timeout management for large repositories
- Comprehensive error logging and session tracking

## Dependencies
- **Core**: tree-sitter-languages, diskcache, aiosqlite
- **API**: fastapi, pydantic, instructor
- **Integration**: openrouter (optional), AAI brain modules
- **Testing**: pytest, pytest-asyncio, psutil

## Example Usage
```bash
# Basic repository analysis
/analyze-repo

# Full analysis with semantic understanding  
/analyze-repo /path/to/repo --semantic --integrations

# Performance benchmarking
/analyze-repo --performance --format json

# Cache refresh and detailed analysis
/analyze-repo --cache --semantic --performance
```

## Notes
- Automatically detects and handles Tree-sitter compatibility issues
- Integrates with existing AAI brain modules for learning
- Supports both standalone and integrated analysis modes
- Provides comprehensive validation against PRP performance targets
- Maintains backward compatibility with existing AAI patterns