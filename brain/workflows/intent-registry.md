# Intent Recognition Registry

## Purpose
Track and learn from command interpretations to improve Claude's understanding over time.

## Format
```
[TIMESTAMP] | [INTENT] | [CONFIDENCE] | [OUTCOME] | [LEARNING]
```

## Intent Categories
- **Research**: Documentation gathering, API exploration
- **Refactor**: Code restructuring, architecture changes  
- **Explain**: Code analysis, concept clarification
- **Summarize**: Content condensation, key point extraction
- **Implement**: Feature creation, bug fixes
- **Debug**: Error investigation, troubleshooting
- **Plan**: Task organization, strategy development

## 🎯 Intent Clusters (Phase 1 Enhancement)

### Framework Shifts
**Pattern**: Major architectural changes requiring system-wide updates
**Examples**: Brain-centric architecture, SuperClaude integration
**Success Rate**: 95% | **Avg Duration**: 2-3 hours
**Key Indicators**: "overhaul", "architecture", "system-wide", "enhancement"

### Cache Management
**Pattern**: Memory, storage, and state management operations
**Examples**: Supabase integration, file routing, cache optimization
**Success Rate**: 85% | **Avg Duration**: 30-60 minutes
**Key Indicators**: "cache", "memory", "state", "storage", "persistence"

### Naming Conflicts
**Pattern**: File/folder organization and cleanup operations
**Examples**: Archive moves, phantom reference removal, folder restructuring
**Success Rate**: 90% | **Avg Duration**: 15-30 minutes
**Key Indicators**: "rename", "move", "archive", "cleanup", "organize"

### Enhancement Workflows
**Pattern**: Feature additions and capability improvements
**Examples**: Dashboard upgrades, command implementations, intelligence features
**Success Rate**: 80% | **Avg Duration**: 1-2 hours
**Key Indicators**: "enhance", "improve", "upgrade", "implement", "add"

### Decision Tracking
**Pattern**: Rationale documentation and decision logging
**Examples**: explain.md updates, decision correlation, reversal tracking
**Success Rate**: 95% | **Avg Duration**: 20-40 minutes
**Key Indicators**: "explain", "decide", "rationale", "document", "track"

## 🔄 Intent Reversal Tracker (Phase 1 Enhancement)

### Reversal Log
```
[DATE] | [ORIGINAL INTENT] → [REVERSED INTENT] | [REASON] | [LEARNING]
```

#### Active Reversals
```
2025-07-13 | Merge Claude.md files → Keep separate with bridge | Better modularity and clear separation of concerns
2025-07-13 | Delete context-base → Archive as reference | Preserves historical context and prevents knowledge loss
2025-07-13 | Create new command files → Use existing /log system | Avoid duplication, leverage existing infrastructure
```

#### Learning Patterns
- **Merge vs. Separate**: When in doubt, prefer modularity over consolidation
- **Delete vs. Archive**: Preserve historical context unless explicitly harmful
- **New vs. Existing**: Leverage existing systems before creating new ones

## Learning Tags
- #research - Documentation and API research
- #decision - Architecture and design choices
- #error - Failures and debugging sessions
- #insight - Discoveries and pattern recognition
- #context - Project requirements and constraints

## Sample Entries
```
2025-01-13T12:00:00Z | System-Overhaul | 0.95 | SUCCESS | User requested comprehensive AAI architecture enhancement with brain-centric design
2025-01-13T12:30:00Z | Archive-Management | 0.90 | SUCCESS | Recognized need to preserve context-base as reference while implementing new structure
```

---
*Intent registry initialized - learning begins now*