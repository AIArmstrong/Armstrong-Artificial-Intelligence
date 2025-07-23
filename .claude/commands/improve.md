---
allowed-tools: [Read, Grep, Glob, Edit, MultiEdit, TodoWrite]
description: "Apply systematic improvements to code quality, performance, and maintainability"
---

# /sc:improve - Code Improvement

## Purpose
Apply systematic improvements to code quality, performance, maintainability, and best practices.

## Usage
```
/sc:improve [target] [--type quality|performance|maintainability|style] [--review-type code|architecture|debate] [--safe]
```

## Arguments
- `target` - Files, directories, or project to improve
- `--type` - Improvement type (quality, performance, maintainability, style)
- `--review-type` - Advanced review mode (code, architecture, debate)
- `--safe` - Apply only safe, low-risk improvements
- `--preview` - Show improvements without applying them

## Review Types
- `code` - Comprehensive code review with quality assessment and detailed reporting
- `architecture` - Strategic architecture review focusing on high-level structure and evolution
- `debate` - Code debate analysis for implementation-level issue identification

## Execution

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate improvement intelligence automatically based on context.

### Supreme Improvement Mode (Enhanced)
Smart Module Loading automatically activates supreme improve capabilities when available, triggering advanced multi-dimensional analysis:

1. **Comprehensive Analysis Phase**
   - Multi-dimensional quality scoring (0-100 scale across 7 dimensions)
   - Repository structure analysis with pattern detection
   - Security vulnerability scanning with risk assessment
   - Performance analysis with optimization opportunities
   - Integration opportunity identification

2. **Intelligent Recommendation Generation**
   - AI-powered improvement recommendations with priority scoring
   - Risk assessment for breaking change prediction (≥90% accuracy)
   - Success probability prediction based on historical data
   - Effort estimation and validation step generation

3. **Safety-First Application**
   - Preview mode with detailed change visualization
   - Atomic file modifications with rollback capabilities
   - Real-time validation and testing integration
   - Backup creation and restoration on failures

4. **Learning and Tracking**
   - Outcome tracking for continuous improvement
   - Success correlation analysis for recommendation refinement
   - Cross-session pattern learning and adaptation
   - Developer feedback integration for model improvement

### Standard Improvement Mode (Fallback)
When supreme improve is not available, uses traditional approach:

1. Analyze code for improvement opportunities
2. Identify specific improvement patterns and techniques
3. Create improvement plan with risk assessment
4. Apply improvements with appropriate validation
5. Verify improvements and report changes

### Review Type Modes
**Code Review (`--review-type code`)**:
- Supreme Mode: Multi-dimensional analysis with 98% accuracy scoring across maintainability, complexity, readability, test coverage, documentation, security, and performance
- Standard Mode: Multi-dimensional review with functionality, security, and performance focus
- Quality assessment with detailed metrics and actionable recommendations
- Third-party library optimization with compatibility analysis

**Architecture Review (`--review-type architecture`)**:
- Supreme Mode: Architectural pattern detection with modularity assessment and scalability analysis
- Standard Mode: System-wide pattern identification and structural design issue detection
- Strategic "-ilities" evaluation with quantified impact assessment
- Technology stack optimization recommendations with migration guidance

**Debate Analysis (`--review-type debate`)**:
- Supreme Mode: Implementation-level analysis with alternative approach scoring and consensus recommendations
- Standard Mode: Implementation issue identification with coding standards compliance
- Multi-perspective analysis with trade-off evaluation
- Evidence-based decision support with confidence scoring

## Enhanced Claude Code Integration
- **Supreme Mode**: Integrates with MultiDimensionalScorer, RiskAssessor, SafetyMechanisms, and ImprovementTracker
- **Analysis Tools**: Enhanced repository analyzer with semantic understanding
- **Safety Features**: Atomic modifications, preview mode, automatic rollback on failures  
- **Learning System**: Continuous improvement through outcome tracking and pattern recognition
- **Orchestration**: Seamless workflow coordination with multi-agent intelligence
- **Validation**: Comprehensive testing integration with quality gate enforcement

## Command Usage Examples

### Basic Supreme Improvement
```bash
python scripts/supreme_improve/improve_code.py /path/to/project --mode preview
```

### Interactive High-Safety Mode
```bash  
python scripts/supreme_improve/improve_code.py /path/to/project --mode interactive --safety-level maximum --analysis comprehensive
```

### Quick Quality Assessment
```bash
python scripts/supreme_improve/analyze_codebase.py /path/to/project --types quality security --output report.json
```