# Subagent Invocation Log

## Purpose
Track when and why research subagents (Claude-native, OpenRouter, MCP) are invoked for research tasks.

## Format
```
[TIMESTAMP] | [AGENT_TYPE] | [RESEARCH_SCOPE] | [RATIONALE] | [OUTCOME]
```

## Agent Types
- **claude-general**: Claude-native GeneralResearcher for general knowledge
- **claude-project**: Claude-native ProjectResearcher for project-specific research
- **openrouter-specialist**: OpenRouter LLM for advanced analysis
- **mcp-external**: MCP server delegation for complex scraping

## Invocation Log

### Initial Setup
*No subagents invoked yet - this file will track research agent usage and effectiveness.*

## Delegation Rules
- **404 errors > 3**: Delegate to MCP for deep scraping
- **Research complexity > 0.8**: Parallel MCP assistance
- **Contradiction detection needed**: OpenRouter specialist
- **General knowledge acquisition**: Claude-native GeneralResearcher
- **Project-specific research**: Claude-native ProjectResearcher

## Performance Metrics
- **Success Rate**: Percentage of successful research completions
- **Average Score**: Research quality scores by agent type
- **Time Efficiency**: Research completion time by agent

---
*Subagent coordination for intelligent research delegation*