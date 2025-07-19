---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite, Task]
description: "Analyze code quality, security, performance, and architecture with rate limiting and error handling"
---

# /analyze - Enhanced Code Analysis with Rate Limiting

## Purpose
Execute comprehensive code analysis with built-in rate limiting, error handling, and chunked output to prevent API 529 and 400 errors. Supports multi-agent orchestration with proper tool sequence management.

## Usage
```
/analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--subagents] [--resume] [--format text|json]
```

## Arguments
- `target` - Files, directories, or project to analyze (default: current directory)
- `--focus` - Analysis focus area (quality, security, performance, architecture) (default: quality)
- `--depth` - Analysis depth (quick, deep) (default: quick)
- `--format` - Output format (text, json) (default: text)
- `--subagents` - Enable subagent orchestration (default: true)
- `--resume` - Resume from previous checkpoint if available (default: false)

## New Features

### ✅ Rate Limiting & Error Handling
- **Exponential backoff**: 1s to 60s delays prevent API 529 errors
- **Retry logic**: Up to 3 attempts per failed agent
- **Tool sequence validation**: Ensures proper tool_use/tool_result pairing
- **Batch processing**: Max 2 agents concurrent to prevent overload

### ✅ Resume Functionality
- **Checkpoint system**: Saves progress automatically
- **Resume command**: `--resume` flag continues interrupted analyses
- **State recovery**: Restores failed/pending agents only

### ✅ Progress Indicators
- **Batch progress**: Shows current batch (1/3) and agent count
- **Agent status**: Individual agent progress with focus area
- **Completion stats**: Success/failure counts per batch
- **Time indicators**: Shows wait times between batches

### ✅ Enhanced Output
- **Chunked responses**: Breaks large outputs into 10KB pieces
- **Structured reporting**: Consistent format across all focus areas
- **Real analysis**: Actual file scanning and issue detection
- **Multiple formats**: Text and JSON output options

## SubAgent Testing Framework (Default Mode)

### Orchestrator-Agent Hierarchy
```
Analysis Orchestrator (Default)
├── Code Quality Agent      (SuperClaude /analyze --code --persona-qa --strict)
├── Security Analysis Agent (SuperClaude /analyze --security --owasp --persona-security)  
├── Performance Agent       (SuperClaude /analyze --profile --persona-performance --deep)
├── Architecture Agent      (SuperClaude /analyze --architecture --persona-architect)
└── Integration Test Agent  (SuperClaude /analyze --integration --seq --validate)
```

### Multi-Layer Analysis Protocol
1. **Level 1**: SuperClaude specialized analysis with personas
2. **Level 2**: AI-enhanced pattern recognition from Anthropic docs
3. **Level 3**: Cross-component integration analysis
4. **Level 4**: Quality threshold validation (95% standard)

### Focus Area Mappings
- **quality**: Deploy Code Quality + Architecture agents
- **security**: Deploy Security Analysis + Code Quality agents  
- **performance**: Deploy Performance + Architecture agents
- **architecture**: Deploy Architecture + Integration agents

## Execution (Enhanced with SubAgents)
1. **Analysis Scope Assessment**: Determine required specialized agents based on focus
2. **SubAgent Deployment**: Launch appropriate testing/analysis agents
3. **Parallel Analysis**: Multiple agents analyze different aspects simultaneously
   - **Rate Limiting**: Implements exponential backoff (1s-60s) to handle API 529 errors
   - **Batch Processing**: Processes max 2 agents concurrently to avoid overload
4. **Anthropic Documentation Integration**: Reference official docs for best practices
5. **Agent Coordination**: Orchestrate findings from multiple specialized agents
   - **Tool Sequence Handling**: Ensures every tool_use has matching tool_result
   - **Error Recovery**: Automatic retry with backoff for failed agents (max 3 retries)
6. **Quality Validation**: Apply 95% quality threshold across all findings
7. **Synthesis**: Combine agent findings into actionable insights
   - **Chunked Output**: Breaks large results into 10KB chunks for stable delivery
8. **Structured Reporting**: Present comprehensive multi-agent analysis

## Anthropic Documentation Integration
- **Tool Use Patterns**: References `/docs/official/anthropic/tool-use.md`
- **API Best Practices**: Applies prompt engineering guidelines from `/docs/official/anthropic/prompt-engineering/`
- **Model Capabilities**: Uses model documentation for agent assignment
- **Error Handling**: Follows patterns from `/docs/official/anthropic/api/errors.md`

## Claude Code Integration (Enhanced)
- Uses Glob for systematic file discovery
- Leverages Grep for pattern-based analysis with agent coordination
- Applies Read for deep code inspection with specialized agents
- References Anthropic documentation for analysis best practices
- Deploys SuperClaude testing framework for comprehensive coverage
- Maintains structured analysis reporting with agent findings
- Integrates tmux orchestrator communication patterns

## Implementation
**The `/analyze` command now executes with enhanced error handling:**

When this command is invoked, Claude will:
1. Parse the command arguments (target, focus, depth, subagents)
2. Execute analysis using the Task tool with proper rate limiting
3. Process results in batches to prevent API overload
4. Return chunked output for large responses
5. Provide checkpoint/resume functionality for interrupted analyses

**Key Features:**
- **Rate Limiting**: Exponential backoff (1s-60s) prevents API 529 errors
- **Batch Processing**: Max 2 agents concurrently to avoid overload
- **Error Recovery**: 3 retry attempts with proper tool_use/tool_result pairing
- **Chunked Output**: Breaks large responses into 10KB manageable pieces
- **Checkpoint/Resume**: Saves progress for interrupted analyses with --resume flag

## Default Behavior
**When `/sc:analyze` is run, the system automatically:**
1. Deploys SuperClaude-Enhanced Testing Framework with rate limiting
2. Launches specialized analysis agents based on focus area (batched)
3. References Anthropic documentation for analysis patterns
4. Applies quality thresholds and validation protocols
5. Provides multi-agent coordinated analysis results (chunked)

*This enhanced analysis leverages the full power of subagent orchestration with robust error handling and official Anthropic documentation for maximum analysis depth and accuracy.*