---
allowed-tools: [Read, Grep, Glob, Bash, Edit, MultiEdit]
description: "Clean up code, remove dead code, and optimize project structure"
---

# /sc:cleanup - Code and Project Cleanup

## Purpose
Systematically clean up code, remove dead code, optimize imports, and improve project structure.

## Usage
```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive]
```

## Arguments
- `target` - Files, directories, or entire project to clean
- `--type` - Cleanup type (code, imports, files, all)
- `--safe` - Conservative cleanup (default)
- `--aggressive` - More thorough cleanup with higher risk
- `--dry-run` - Preview changes without applying them

## Execution

### 🧠 ACTIVE INTELLIGENCE MODULES
```yaml
Intelligence_Layers:
  - Memory: "Recall successful cleanup patterns and avoid past mistakes"
  - Foundation: "Apply baseline code quality and safety validation"
  - Hybrid RAG: "Knowledge synthesis from cleanup best practices"
  - Reasoning: "Apply WHY analysis for cleanup decisions with risk assessment"
  - Tool Selection: "Intelligently choose optimal cleanup tools and approaches"
  - Architecture: "Provide structural guidance and organization recommendations"
```

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate cleanup intelligence automatically based on context.

### Supreme Cleanup Mode (Enhanced)
Smart Module Loading automatically activates supreme cleanup capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful cleanup patterns and avoid past mistakes
2. **Foundation Layer** - Apply baseline code quality and safety validation
3. **Hybrid RAG Layer** - Knowledge synthesis from cleanup best practices
4. **Reasoning Layer** - Apply WHY analysis for cleanup decisions with risk assessment
5. **Tool Selection Layer** - Intelligently choose optimal cleanup tools and approaches
6. **Architecture Layer** - Provide structural guidance and organization recommendations

**Enhanced Cleanup Process**:
1. **Multi-Dimensional Analysis** - Comprehensive codebase analysis with pattern detection
2. **AI-Powered Detection** - Advanced dead code identification with usage analysis
3. **Intelligent Risk Assessment** - Safety scoring with breaking change prediction
4. **Coordinated Execution** - Atomic cleanup operations with automatic rollback
5. **Quality Validation** - Real-time validation with impact assessment
6. **Learning Integration** - Capture successful cleanup patterns for future operations

### Standard Cleanup Mode (Fallback)
When supreme cleanup is not available:
1. Analyze target for cleanup opportunities
2. Identify dead code, unused imports, and redundant files
3. Create cleanup plan with risk assessment
4. Execute cleanup operations with appropriate safety measures
5. Validate changes and report cleanup results

### Creative Cortex Integration (Phase 3)
- **#Critic Mode** - Critical analysis of code quality and structural issues
- **#Enhancer Mode** - Optimization opportunities and improvement suggestions
- **#Logic Mode** - Structured cleanup validation and dependency analysis
- **Innovation Mode** - Novel cleanup strategies for complex legacy systems

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with DeadCodeAnalyzer, DependencyMapper, and SafetyValidator
- **Pattern Recognition**: Enhanced Glob with semantic file analysis
- **Advanced Detection**: Grep with contextual usage analysis and cross-reference validation
- **Atomic Operations**: MultiEdit with transaction-like cleanup batches
- **Safety Mechanisms**: Automatic backup creation and intelligent rollback capabilities
- **Quality Gates**: Real-time validation with breaking change prevention
- **Learning System**: Continuous improvement through cleanup success correlation

## Intelligence Layer Auto-Triggers
```yaml
# Cleanup Context Detection
if (cleanup_command_detected) → ACTIVATE: [memory, foundation, tool_selection, reasoning]
if (dead_code_analysis_needed) → ENHANCE_WITH: [hybrid_rag, reasoning, tool_selection]
if (structural_optimization_required) → ENGAGE: [architecture, reasoning, hybrid_rag]
if (safety_validation_needed) → COORDINATE: [foundation, reasoning, tool_selection]
if (cleanup_success) → LEARN_FROM: [memory, foundation]
```