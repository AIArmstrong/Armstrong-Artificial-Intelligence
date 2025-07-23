---
allowed-tools: [Read, Grep, Glob, Bash, Write]
description: "Load and analyze project context, configurations, and dependencies"
---

# /sc:load - Project Context Loading

## Purpose
Load and analyze project context, configurations, dependencies, and environment setup.

## Usage
```
/sc:load [target] [--type project|config|deps|env] [--cache]
```

## Arguments
- `target` - Project directory or specific configuration to load
- `--type` - Loading type (project, config, deps, env)
- `--cache` - Cache loaded context for faster subsequent access
- `--refresh` - Force refresh of cached context

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate loading intelligence automatically based on context.

### Supreme Loading Mode (Enhanced)
Smart Module Loading automatically activates supreme loading capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall project patterns and configuration preferences from similar projects
2. **Foundation Layer** - Apply baseline configuration validation and consistency checking
3. **Hybrid RAG Layer** - Knowledge synthesis from configuration best practices and documentation
4. **Research Layer** - Auto-research configuration standards and dependency compatibility when needed
5. **Reasoning Layer** - Apply WHY analysis for configuration decisions with dependency resolution logic
6. **Tool Selection Layer** - Intelligently choose optimal loading and validation tools
7. **Architecture Layer** - Provide project structure understanding and configuration optimization
8. **Orchestration Layer** - Coordinate complex multi-environment loading workflows

**Enhanced Loading Process**:
1. **Intelligent Discovery** - Multi-dimensional project analysis with semantic configuration detection
2. **Smart Dependency Resolution** - AI-powered dependency analysis with conflict detection and resolution
3. **Adaptive Validation** - Context-aware configuration validation with environment-specific checks
4. **Comprehensive Context Mapping** - Deep project understanding with relationship and dependency graphs
5. **Optimized Caching** - Intelligent cache management with selective refresh and version tracking
6. **Learning Integration** - Capture effective loading patterns for project-type optimization

### Standard Loading Mode (Fallback)
When supreme loading is not available:
1. Discover and analyze project structure and configuration files
2. Load dependencies, environment variables, and settings
3. Parse and validate configuration consistency
4. Create comprehensive project context map
5. Cache context for efficient future access

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured configuration validation and dependency resolution
- **#Critic Mode** - Critical analysis of configuration quality and potential issues
- **#Enhancer Mode** - Configuration optimization and performance improvement suggestions
- **#Innovator Mode** - Novel configuration approaches and environment setup strategies

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with ProjectIntelligence, ConfigurationValidator, and ContextOptimizer
- **Discovery Intelligence**: Enhanced Glob with semantic project structure analysis and priority scoring
- **Configuration Analysis**: Read with deep semantic understanding of configuration formats and relationships
- **Environment Intelligence**: Bash with environment compatibility analysis and setup optimization
- **Smart Caching**: Advanced context management with selective updates and cross-project learning
- **Dependency Intelligence**: Automatic dependency conflict detection and resolution suggestions
- **Learning System**: Continuous improvement through project loading success correlation and optimization

## Intelligence Layer Auto-Triggers
```yaml
# Loading Context Detection
if (loading_command_detected) → ACTIVATE: [memory, foundation, tool_selection, architecture]
if (configuration_analysis_needed) → ENHANCE_WITH: [hybrid_rag, reasoning, research]
if (dependency_resolution_required) → ENGAGE: [reasoning, architecture, tool_selection]
if (environment_setup_needed) → COORDINATE: [orchestration, reasoning, tool_selection]
if (loading_success) → LEARN_FROM: [memory, foundation]
```