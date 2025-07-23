---
allowed-tools: [Read, Grep, Glob, Write, Edit]
description: "Create focused documentation for specific components or features"
---

# /sc:document - Focused Documentation

## Purpose
Generate precise, focused documentation for specific components, functions, or features.

## Usage
```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

## Arguments
- `target` - Specific file, function, or component to document
- `--type` - Documentation type (inline, external, api, guide)
- `--style` - Documentation style (brief, detailed)
- `--template` - Use specific documentation template

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate documentation intelligence automatically based on context.

### Supreme Documentation Mode (Enhanced)
Smart Module Loading automatically activates supreme documentation capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall successful documentation patterns and user preferences
2. **Foundation Layer** - Apply baseline documentation quality and completeness validation
3. **Hybrid RAG Layer** - Knowledge synthesis from documentation best practices and existing docs
4. **Research Layer** - Auto-research documentation standards and examples when needed
5. **Reasoning Layer** - Apply WHY analysis for documentation decisions with audience consideration
6. **Tool Selection Layer** - Intelligently choose optimal documentation tools and formats
7. **Architecture Layer** - Provide structural guidance for documentation organization

**Enhanced Documentation Process**:
1. **Intelligent Component Analysis** - Multi-dimensional code analysis with semantic understanding
2. **Smart Audience Detection** - Automatic identification of documentation consumers and requirements
3. **AI-Generated Content** - Context-aware documentation with adaptive style and depth
4. **Consistency Validation** - Cross-reference with existing documentation for coherence
5. **Quality Assurance** - Completeness scoring with gap identification and filling
6. **Learning Integration** - Capture successful documentation patterns for future use

### Standard Documentation Mode (Fallback)
When supreme documentation is not available:
1. Analyze target component and extract key information
2. Identify documentation requirements and audience
3. Generate appropriate documentation based on type and style
4. Apply consistent formatting and structure
5. Integrate with existing documentation ecosystem

### Creative Cortex Integration (Phase 3)
- **#Enhancer Mode** - Documentation improvement and clarity optimization
- **#Logic Mode** - Structured documentation validation and completeness checking
- **#Innovator Mode** - Creative documentation approaches and interactive elements
- **#Critic Mode** - Critical review of documentation quality and usability

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with DocumentationIntelligence, ContentGenerator, and QualityValidator
- **Semantic Analysis**: Enhanced Read with contextual code understanding and intent detection
- **Smart Updates**: Edit with documentation consistency and cross-reference validation
- **Intelligent Creation**: Write with template selection and adaptive content generation
- **Standards Enforcement**: Automatic style guide compliance and convention checking
- **Cross-Reference System**: Automatic linking and relationship mapping between docs
- **Learning System**: Continuous improvement through documentation usage analytics

## Intelligence Layer Auto-Triggers
```yaml
# Documentation Context Detection
if (documentation_command_detected) → ACTIVATE: [memory, foundation, tool_selection, hybrid_rag]
if (api_documentation_needed) → ENHANCE_WITH: [research, reasoning, architecture]
if (complex_component_analysis) → ENGAGE: [hybrid_rag, reasoning, architecture]
if (documentation_quality_check) → COORDINATE: [foundation, reasoning, hybrid_rag]
if (documentation_success) → LEARN_FROM: [memory, foundation]
```