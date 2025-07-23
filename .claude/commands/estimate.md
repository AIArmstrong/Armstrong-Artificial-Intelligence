---
allowed-tools: [Read, Grep, Glob, Bash]
description: "Provide development estimates for tasks, features, or projects"
---

# /sc:estimate - Development Estimation

## Purpose
Generate accurate development estimates for tasks, features, or projects based on complexity analysis.

## Usage
```
/sc:estimate [target] [--type time|effort|complexity|cost] [--unit hours|days|weeks]
```

## Arguments
- `target` - Task, feature, or project to estimate
- `--type` - Estimation type (time, effort, complexity, cost)
- `--unit` - Time unit for estimates (hours, days, weeks)
- `--breakdown` - Provide detailed breakdown of estimates

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate estimation intelligence automatically based on context.

### Supreme Estimation Mode (Enhanced)
Smart Module Loading automatically activates supreme estimation capabilities when available, triggering the **8 Enhancement Layers**:

1. **Memory Layer** - Recall similar project estimates and accuracy patterns from historical data
2. **Foundation Layer** - Apply baseline estimation validation and sanity checking
3. **Hybrid RAG Layer** - Knowledge synthesis from industry estimation benchmarks and practices
4. **Research Layer** - Auto-research similar projects and complexity patterns when needed
5. **Reasoning Layer** - Apply WHY analysis for estimation decisions with 70-95% confidence scoring
6. **Tool Selection Layer** - Intelligently choose optimal estimation methodologies and frameworks
7. **Architecture Layer** - Provide technical complexity guidance and scalability considerations

**Enhanced Estimation Process**:
1. **Multi-Dimensional Scope Analysis** - Comprehensive requirement decomposition with hidden complexity detection
2. **AI-Powered Complexity Assessment** - Advanced dependency mapping with risk factor quantification
3. **Historical Data Integration** - Pattern matching with successful project outcomes and accuracy correlation
4. **Probabilistic Estimation** - Monte Carlo analysis with confidence intervals and scenario modeling
5. **Risk-Adjusted Breakdown** - Detailed task decomposition with uncertainty quantification
6. **Continuous Calibration** - Learning from estimate accuracy to improve future predictions

### Standard Estimation Mode (Fallback)
When supreme estimation is not available:
1. Analyze scope and requirements of target
2. Identify complexity factors and dependencies
3. Apply estimation methodologies and historical data
4. Generate estimates with confidence intervals
5. Present detailed breakdown with risk factors

### Creative Cortex Integration (Phase 3)
- **#Logic Mode** - Structured estimation validation and mathematical modeling
- **#Critic Mode** - Critical analysis of estimation assumptions and risk factors
- **#Enhancer Mode** - Estimation accuracy improvements and methodology optimization
- **#Innovator Mode** - Novel estimation approaches for unprecedented project types

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with EstimationIntelligence, ComplexityAnalyzer, and AccuracyTracker
- **Deep Analysis**: Enhanced Read with semantic requirement understanding and scope detection
- **Complexity Intelligence**: Glob with codebase pattern recognition and scalability assessment
- **Pattern Matching**: Grep with historical project similarity analysis and benchmark comparison
- **Accuracy Learning**: Continuous calibration through estimate vs. actual outcome tracking
- **Risk Modeling**: Advanced uncertainty quantification with scenario-based projections
- **Learning System**: Continuous improvement through estimation accuracy correlation analysis

## Intelligence Layer Auto-Triggers
```yaml
# Estimation Context Detection
if (estimation_command_detected) → ACTIVATE: [memory, foundation, tool_selection, reasoning]
if (complex_project_analysis) → ENHANCE_WITH: [hybrid_rag, research, architecture]
if (historical_data_needed) → ENGAGE: [memory, hybrid_rag, reasoning]
if (risk_assessment_required) → COORDINATE: [reasoning, architecture, hybrid_rag]
if (estimation_validation) → LEARN_FROM: [memory, foundation]
```