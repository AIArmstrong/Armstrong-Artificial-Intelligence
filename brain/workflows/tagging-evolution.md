# Tagging Evolution & Learning Log

## Purpose
Track tag accuracy improvements through user feedback to enhance auto-tagging intelligence.

## Format
```
[TIMESTAMP] | [ORIGINAL_TAG] → [CORRECTED_TAG] | [CONTEXT] | [CONFIDENCE_ADJUSTMENT]
```

## 🌳 Tag Family Trees (Phase 2 Enhancement)

### Dynamic Taxonomy Evolution
**Base Tags**: #research, #decision, #error, #insight, #context
**Auto-Generated Subtags**: Based on usage patterns and semantic clustering

### Family Tree Structure
```
#research
├── #research-api          (API documentation gathering)
├── #research-architecture (System design investigation)
├── #research-integration  (Third-party service research)
└── #research-troubleshoot (Problem diagnosis research)

#decision
├── #decision-architecture (System design choices)
├── #decision-workflow     (Process optimization choices) 
├── #decision-integration  (Tool/service selection)
└── #decision-reversal     (Decision corrections/changes)

#error
├── #error-config         (Configuration issues)
├── #error-integration    (API/service failures)
├── #error-workflow       (Process execution failures)
└── #error-reference      (Broken file/path references)

#insight
├── #insight-pattern      (Recurring behavior recognition)
├── #insight-optimization (Performance/efficiency discoveries)
├── #insight-correlation  (System relationship discoveries)
└── #insight-learning     (Meta-cognitive improvements)

#context
├── #context-requirement  (Project specifications)
├── #context-constraint   (Limitation discoveries)
├── #context-dependency   (System relationship mapping)
└── #context-evolution    (Changing project scope)
```

### Auto-Generation Rules
1. **Pattern Detection**: When tag + keyword appears >3 times, create subtag
2. **Semantic Clustering**: Use embeddings to group similar content
3. **User Confirmation**: Suggest new subtags before auto-creation
4. **Lifecycle Management**: Archive subtags with <2 uses in 30 days

### Subtag Generation Examples
- `#research + "cache"` → `#research-cache` (3+ occurrences)
- `#decision + "refactor"` → `#decision-refactor` (pattern recognition)
- `#error + "openrouter"` → `#error-openrouter` (service-specific)

## Learning Patterns
- Track which tags are frequently corrected
- Identify context patterns that lead to misclassification
- Adjust confidence thresholds based on feedback
- Batch process improvements to avoid overcorrection
- Auto-evolve taxonomy based on usage patterns
- Semantic clustering for intelligent subtag creation

## Tag Accuracy Metrics
| Tag | Uses | Corrections | Accuracy |
|-----|------|-------------|----------|
| #dashboard-sync | 1 | 1 | 0% → Learning |
| #protection | 1 | 1 | 0% → Learning |
| #status | 3 | 1 | 67% → Improving |
| #queue | 2 | 1 | 50% → Improving |
| #critical | 4 | 0 | 100% |

## Batch Learning Queue
*Corrections accumulate here until batch processing*

---
*Tag learning system initialized - accuracy will improve with usage*