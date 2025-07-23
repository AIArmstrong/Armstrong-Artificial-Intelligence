---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite, Edit, MultiEdit, Write]
description: "Break complex tasks into coordinated subtasks with efficient execution"
---

# /sc:spawn - Task Orchestration

## Purpose
Decompose complex requests into manageable subtasks and coordinate their execution.

## Usage
```
/sc:spawn [task] [--sequential|--parallel] [--validate]
```

## Arguments
- `task` - Complex task or project to orchestrate
- `--sequential` - Execute tasks in dependency order (default)
- `--parallel` - Execute independent tasks concurrently
- `--validate` - Enable quality checkpoints between tasks

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate orchestration intelligence automatically based on context.

### Supreme Orchestration Mode (Enhanced)
Smart Module Loading automatically activates supreme orchestration capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful task orchestration patterns and coordination strategies
2. **Foundation Layer** - Apply baseline task validation and dependency checking
3. **Hybrid RAG Layer** - Knowledge synthesis from project management and orchestration best practices
4. **Research Layer** - Auto-research orchestration methodologies and coordination patterns when needed
5. **Reasoning Layer** - Apply WHY analysis for orchestration decisions with dependency logic
6. **Tool Selection Layer** - Intelligently choose optimal orchestration tools and execution strategies
7. **Architecture Layer** - Provide system-wide coordination guidance and workflow optimization
8. **Orchestration Layer** - Multi-agent coordination with intelligent task distribution

**Enhanced Orchestration Process**:
1. **Intelligent Task Breakdown** - Multi-dimensional analysis with semantic task decomposition
2. **Smart Dependency Mapping** - AI-powered dependency detection with conflict resolution
3. **Adaptive Execution Strategy** - Context-aware optimization of sequential vs parallel execution
4. **Coordinated Monitoring** - Real-time progress tracking with predictive bottleneck detection
5. **Intelligent Integration** - Automated result synthesis with quality validation
6. **Learning Integration** - Capture successful orchestration patterns for future optimization

### Standard Orchestration Mode (Fallback)
When supreme orchestration is not available:
1. Parse request and create hierarchical task breakdown
2. Map dependencies between subtasks
3. Choose optimal execution strategy (sequential/parallel)
4. Execute subtasks with progress monitoring
5. Integrate results and validate completion

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured orchestration validation and dependency resolution
- **#Enhancer Mode** - Workflow optimization and efficiency improvements
- **#Innovator Mode** - Novel orchestration approaches and coordination strategies
- **#Critic Mode** - Critical analysis of orchestration effectiveness and bottleneck identification

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with TaskOrchestrator, DependencyResolver, and WorkflowOptimizer
- **Intelligent Breakdown**: Enhanced TodoWrite with hierarchical task organization and dependency mapping
- **Coordinated Operations**: Advanced file operations with transaction-like batching and rollback capabilities
- **Smart Batching**: AI-powered operation grouping with efficiency optimization
- **Dependency Intelligence**: Advanced dependency analysis with conflict detection and resolution
- **Progress Intelligence**: Real-time monitoring with predictive analytics and bottleneck prevention
- **Learning System**: Continuous improvement through orchestration success correlation and pattern recognition

## Intelligence Layer Auto-Triggers
```yaml
# Orchestration Context Detection
if (spawn_command_detected) → ACTIVATE: [memory, foundation, tool_selection, orchestration]
if (complex_task_breakdown_needed) → ENHANCE_WITH: [hybrid_rag, reasoning, architecture]
if (dependency_analysis_required) → ENGAGE: [reasoning, architecture, orchestration]
if (parallel_execution_optimal) → COORDINATE: [orchestration, tool_selection, reasoning]
if (orchestration_success) → LEARN_FROM: [memory, foundation]
```