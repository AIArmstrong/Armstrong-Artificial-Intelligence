---
allowed-tools: [Read, Glob, Grep, TodoWrite, Task, mcp__sequential-thinking__sequentialthinking]
description: "Execute complex tasks with intelligent workflow management and cross-session persistence"
wave-enabled: true
complexity-threshold: 0.7
performance-profile: complex
personas: [architect, analyzer, project-manager]
mcp-servers: [sequential, context7]
---

# /sc:task - Enhanced Task Management

## Purpose
Execute complex tasks with intelligent workflow management, cross-session persistence, hierarchical task organization, and advanced orchestration capabilities.

## Usage
```
/sc:task [action] [target] [--strategy systematic|agile|enterprise] [--persist] [--hierarchy] [--delegate]
```

## Actions
- `create` - Create new project-level task hierarchy
- `execute` - Execute task with intelligent orchestration
- `status` - View task status across sessions
- `analytics` - Task performance and analytics dashboard
- `optimize` - Optimize task execution strategies
- `delegate` - Delegate tasks across multiple agents
- `validate` - Validate task completion with evidence

## Arguments
- `target` - Task description, project scope, or existing task ID
- `--strategy` - Execution strategy (systematic, agile, enterprise)
- `--persist` - Enable cross-session task persistence
- `--hierarchy` - Create hierarchical task breakdown
- `--delegate` - Enable multi-agent task delegation
- `--wave-mode` - Enable wave-based execution
- `--validate` - Enforce quality gates and validation
- `--mcp-routing` - Enable intelligent MCP server routing
- `overview` - Show validated, current tasks by checking claude.md and status.md


## Execution Modes

### Systematic Strategy
1. **Discovery Phase**: Comprehensive project analysis and scope definition
2. **Planning Phase**: Hierarchical task breakdown with dependency mapping
3. **Execution Phase**: Sequential execution with validation gates
4. **Validation Phase**: Evidence collection and quality assurance
5. **Optimization Phase**: Performance analysis and improvement recommendations

### Agile Strategy
1. **Sprint Planning**: Priority-based task organization
2. **Iterative Execution**: Short cycles with continuous feedback
3. **Adaptive Planning**: Dynamic task adjustment based on outcomes
4. **Continuous Integration**: Real-time validation and testing
5. **Retrospective Analysis**: Learning and process improvement

### Enterprise Strategy
1. **Stakeholder Analysis**: Multi-domain impact assessment
2. **Resource Allocation**: Optimal resource distribution across tasks
3. **Risk Management**: Comprehensive risk assessment and mitigation
4. **Compliance Validation**: Regulatory and policy compliance checks
5. **Governance Reporting**: Detailed progress and compliance reporting

## Advanced Features

### Task Hierarchy Management
- **Epic Level**: Large-scale project objectives (weeks to months)
- **Story Level**: Feature-specific implementations (days to weeks)
- **Task Level**: Specific actionable items (hours to days)
- **Subtask Level**: Granular implementation steps (minutes to hours)

### Intelligent Task Orchestration
- **Dependency Resolution**: Automatic dependency detection and sequencing
- **Parallel Execution**: Independent task parallelization
- **Resource Optimization**: Intelligent resource allocation and scheduling
- **Context Sharing**: Cross-task context and knowledge sharing

### Cross-Session Persistence
- **Task State Management**: Persistent task states across sessions
- **Context Continuity**: Preserved context and progress tracking
- **Historical Analytics**: Task execution history and learning
- **Recovery Mechanisms**: Automatic recovery from interruptions

### Quality Gates and Validation
- **Evidence Collection**: Systematic evidence gathering during execution
- **Validation Criteria**: Customizable completion criteria
- **Quality Metrics**: Comprehensive quality assessment
- **Compliance Checks**: Automated compliance validation

## Integration Points

### Wave System Integration
- **Wave Coordination**: Multi-wave task execution strategies
- **Context Accumulation**: Progressive context building across waves
- **Performance Monitoring**: Real-time performance tracking and optimization
- **Error Recovery**: Graceful error handling and recovery mechanisms

### MCP Server Coordination
- **Context7**: Framework patterns and library documentation
- **Sequential**: Complex analysis and multi-step reasoning
- **Magic**: UI component generation and design systems
- **Playwright**: End-to-end testing and performance validation

### Persona Integration
- **Architect**: System design and architectural decisions
- **Analyzer**: Code analysis and quality assessment
- **Project Manager**: Resource allocation and progress tracking
- **Domain Experts**: Specialized expertise for specific task types

## Performance Optimization

### Execution Efficiency
- **Batch Operations**: Grouped execution for related tasks
- **Parallel Processing**: Independent task parallelization
- **Context Caching**: Reusable context and analysis results
- **Resource Pooling**: Shared resource utilization

### Intelligence Features
- **Predictive Planning**: AI-driven task estimation and planning
- **Adaptive Execution**: Dynamic strategy adjustment based on progress
- **Learning Systems**: Continuous improvement from execution patterns
- **Optimization Recommendations**: Data-driven improvement suggestions

## Usage Examples

### Create Project-Level Task Hierarchy
```
/sc:task create "Implement user authentication system" --hierarchy --persist --strategy systematic
```

### Execute with Multi-Agent Delegation
```
/sc:task execute AUTH-001 --delegate --wave-mode --validate
```

### Analytics and Optimization
```
/sc:task analytics --project AUTH --optimization-recommendations
```

### Cross-Session Task Management
```
/sc:task status --all-sessions --detailed-breakdown
```
### Task Overview
...

/sc:task overview --source claude.md --validate status.md
...

## Execution Enhancement

### 🧠 ACTIVE INTELLIGENCE MODULES
```yaml
Intelligence_Layers:
  - Memory: "Recall successful task patterns, user preferences, and cross-session context"
  - Foundation: "Apply baseline task validation, quality gates, and completion criteria"
  - Hybrid RAG: "Knowledge synthesis from project management methodologies and best practices"
  - Research: "Auto-research similar projects, methodologies, and optimization techniques"
  - Reasoning: "Apply WHY analysis for task decisions with 70-95% confidence scoring"
  - Tool Selection: "Intelligently choose optimal tools and execution strategies per task type"
  - Architecture: "Provide system-wide task organization and structural optimization"
  - Orchestration: "Multi-agent coordination with intelligent delegation and resource allocation"
```

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate task intelligence automatically based on context.

### Supreme Task Management Mode (Enhanced)
Smart Module Loading automatically activates supreme task capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful task patterns, user preferences, and cross-session context
2. **Foundation Layer** - Apply baseline task validation, quality gates, and completion criteria
3. **Hybrid RAG Layer** - Knowledge synthesis from project management methodologies and best practices
4. **Research Layer** - Auto-research similar projects, methodologies, and optimization techniques
5. **Reasoning Layer** - Apply WHY analysis for task decisions with 70-95% confidence scoring
6. **Tool Selection Layer** - Intelligently choose optimal tools and execution strategies per task type
7. **Architecture Layer** - Provide system-wide task organization and structural optimization
8. **Orchestration Layer** - Multi-agent coordination with intelligent delegation and resource allocation

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured task validation and systematic execution planning
- **#Critic Mode** - Critical analysis of task quality, dependencies, and risk assessment
- **#Enhancer Mode** - Task optimization, efficiency improvements, and workflow enhancement
- **#Innovator Mode** - Novel task approaches, creative problem-solving, and breakthrough strategies

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with TaskIntelligence, WorkflowOptimizer, and QualityValidator
- **Memory-Enhanced Coordination**: Advanced TodoWrite with cross-session context and pattern learning
- **Intelligent Wave System**: Multi-stage execution with adaptive orchestration and performance optimization
- **Smart Hook System**: Real-time monitoring with predictive analytics and proactive intervention
- **Advanced MCP Coordination**: Intelligent server routing with load balancing and failover capabilities
- **Performance Intelligence**: Sub-100ms targets with comprehensive metrics and continuous optimization
- **Learning System**: Continuous improvement through task success correlation and user feedback integration

## Intelligence Layer Auto-Triggers
```yaml
# Task Context Detection
if (task_command_detected) → ACTIVATE: [memory, foundation, tool_selection, orchestration]
if (complex_project_analysis) → ENHANCE_WITH: [hybrid_rag, research, architecture]
if (cross_session_continuity_needed) → ENGAGE: [memory, reasoning, orchestration]
if (multi_agent_coordination_required) → COORDINATE: [orchestration, architecture, tool_selection]
if (quality_validation_needed) → VALIDATE_WITH: [foundation, reasoning, hybrid_rag]
if (task_optimization_opportunity) → OPTIMIZE_VIA: [reasoning, architecture, tool_selection]
if (task_success) → LEARN_FROM: [memory, foundation]
```

## Success Criteria
- **Task Completion Rate**: >95% successful task completion
- **Performance Targets**: <100ms hook execution, <5s task creation
- **Quality Metrics**: >90% validation success rate
- **Cross-Session Continuity**: 100% task state preservation
- **Intelligence Effectiveness**: >80% accurate predictive planning