---
allowed-tools: [Read, Grep, Glob, Bash]
description: "Provide clear explanations of code, concepts, or system behavior"
---

# /sc:explain - Code and Concept Explanation

## Purpose
Deliver clear, comprehensive explanations of code functionality, concepts, or system behavior.

## Usage
```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|diagram|examples]
```

## Arguments
- `target` - Code file, function, concept, or system to explain
- `--level` - Explanation complexity (basic, intermediate, advanced)
- `--format` - Output format (text, diagram, examples)
- `--context` - Additional context for explanation

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate explanation intelligence automatically based on context.

### Supreme Explanation Mode (Enhanced)
Smart Module Loading automatically activates supreme explanation capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful explanation patterns and user comprehension preferences
2. **Foundation Layer** - Apply baseline explanation quality and clarity validation
3. **Hybrid RAG Layer** - Knowledge synthesis from educational resources and documentation
4. **Research Layer** - Auto-research concept background and related information when needed
5. **Reasoning Layer** - Apply WHY analysis for concept relationships with logical flow
6. **Tool Selection Layer** - Intelligently choose optimal explanation tools and visualization methods
7. **Architecture Layer** - Provide system context and architectural understanding

**Enhanced Explanation Process**:
1. **Multi-Dimensional Analysis** - Comprehensive code/concept analysis with semantic understanding
2. **Adaptive Complexity Detection** - Automatic audience assessment and appropriate level selection
3. **Intelligent Structuring** - AI-powered explanation organization with pedagogical flow
4. **Context-Aware Examples** - Dynamic example generation based on user background and needs
5. **Interactive Clarity Validation** - Real-time comprehension assessment with adaptive refinement
6. **Learning Integration** - Capture effective explanation patterns for future use

### Standard Explanation Mode (Fallback)
When supreme explanation is not available:
1. Analyze target code or concept thoroughly
2. Identify key components and relationships
3. Structure explanation based on complexity level
4. Provide relevant examples and use cases
5. Present clear, accessible explanation with proper formatting

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured logical flow and step-by-step reasoning
- **#Enhancer Mode** - Clarity optimization and comprehension improvement
- **#Innovator Mode** - Creative explanation approaches and novel analogies
- **#Critic Mode** - Critical analysis of explanation completeness and accuracy

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with ExplanationIntelligence, ConceptMapper, and ClarityValidator
- **Semantic Analysis**: Enhanced Read with contextual understanding and intent detection
- **Pattern Intelligence**: Grep with concept relationship analysis and cross-reference discovery
- **Behavioral Analysis**: Bash with intelligent runtime exploration and example generation
- **Adaptive Communication**: Dynamic style adjustment based on complexity level and audience
- **Visualization Support**: Automatic diagram generation and interactive element creation
- **Learning System**: Continuous improvement through explanation effectiveness tracking

## Intelligence Layer Auto-Triggers
```yaml
# Explanation Context Detection
if (explanation_command_detected) → ACTIVATE: [memory, foundation, tool_selection, hybrid_rag]
if (complex_concept_analysis) → ENHANCE_WITH: [research, reasoning, architecture]
if (code_behavior_explanation) → ENGAGE: [architecture, reasoning, tool_selection]
if (educational_context_needed) → COORDINATE: [hybrid_rag, reasoning, research]
if (explanation_success) → LEARN_FROM: [memory, foundation]
```