---
allowed-tools: [Bash, Read, Glob, TodoWrite, Edit]
description: "Git operations with intelligent commit messages and branch management"
---

# /sc:git - Git Operations

## Purpose
Execute Git operations with intelligent commit messages, branch management, and workflow optimization.

## Usage
```
/sc:git [operation] [args] [--smart-commit] [--branch-strategy]
```

## Arguments
- `operation` - Git operation (add, commit, push, pull, merge, branch, status)
- `args` - Operation-specific arguments
- `--smart-commit` - Generate intelligent commit messages
- `--branch-strategy` - Apply branch naming conventions
- `--interactive` - Interactive mode for complex operations

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate git intelligence automatically based on context.

### Supreme Git Mode (Enhanced)
Smart Module Loading automatically activates supreme git capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful Git workflows, commit patterns, and repository history
2. **Foundation Layer** - Apply baseline Git best practices and validation
3. **Hybrid RAG Layer** - Knowledge synthesis from Git documentation and workflow best practices
4. **Reasoning Layer** - Apply WHY analysis for Git decisions with conflict resolution logic
5. **Tool Selection Layer** - Intelligently choose optimal Git operations and command sequences
6. **Architecture Layer** - Provide repository structure guidance and branching strategy recommendations
7. **Orchestration Layer** - Coordinate complex multi-step Git workflows

**Enhanced Git Process**:
1. **Intelligent State Analysis** - Comprehensive repository analysis with change pattern recognition
2. **Smart Operation Validation** - Pre-flight checks with conflict prediction and prevention
3. **AI-Generated Commit Messages** - Semantic commit message generation with conventional format
4. **Automated Conflict Resolution** - Intelligent merge conflict analysis with resolution suggestions
5. **Workflow Optimization** - Branch strategy recommendations and Git flow enhancement
6. **Learning Integration** - Capture successful Git patterns for repository-specific optimization

### Standard Git Mode (Fallback)
When supreme git is not available:
1. Analyze current Git state and repository context
2. Execute requested Git operations with validation
3. Apply intelligent commit message generation
4. Handle merge conflicts and branch management
5. Provide clear feedback and next steps

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured Git workflow validation and optimization
- **#Enhancer Mode** - Git process improvements and efficiency optimization
- **#Critic Mode** - Critical analysis of repository health and workflow effectiveness
- **#Innovator Mode** - Novel Git workflows and automation strategies

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with GitIntelligence, ConflictResolver, and WorkflowOptimizer
- **Smart Execution**: Enhanced Bash with Git command validation and rollback capabilities
- **Repository Intelligence**: Read with semantic repository analysis and change impact assessment
- **Workflow Tracking**: TodoWrite with Git operation coordination and milestone tracking
- **Convention Enforcement**: Automatic adherence to Git best practices and team conventions
- **Conflict Intelligence**: Advanced merge conflict analysis with AI-powered resolution suggestions
- **Learning System**: Continuous improvement through Git workflow success correlation

## Intelligence Layer Auto-Triggers
```yaml
# Git Context Detection
if (git_command_detected) → ACTIVATE: [memory, foundation, tool_selection, reasoning]
if (merge_conflict_detected) → ENHANCE_WITH: [reasoning, hybrid_rag, tool_selection]
if (complex_workflow_needed) → ENGAGE: [orchestration, architecture, reasoning]
if (commit_message_generation) → COORDINATE: [memory, reasoning, hybrid_rag]
if (git_operation_success) → LEARN_FROM: [memory, foundation]
```