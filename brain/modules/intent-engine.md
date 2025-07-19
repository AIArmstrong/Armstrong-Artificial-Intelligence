# Intent Engine Module

## 🎯 Advanced Intent Clustering & Recognition

### Intent Categories & Patterns
- **Framework Shifts**: 95% success rate, 180min avg duration
- **Cache Management**: 85% success rate, 45min avg duration  
- **Naming Conflicts**: 90% success rate, 25min avg duration
- **Enhancement Workflows**: 80% success rate, 90min avg duration
- **Decision Tracking**: 95% success rate, 30min avg duration

### 🔄 Reversal Learning System
**Pattern Recognition**: Merge→Separate, Delete→Archive, New→Existing
**Active Reversals**: 3 documented, 0% repeat rate
**Learning Rules**: Modularity over consolidation, preservation over deletion

### 🧠 Semantic Embeddings (OpenRouter)
**Model**: text-embedding-ada-002 (1536 dimensions)
**Similarity Threshold**: 0.85 for pattern matching
**Storage**: brain/cache/intent-vectors.json
**Success Rate**: >90% intent recognition accuracy

### Confidence Triggers
- **< 0.70**: Request user clarification
- **0.70-0.85**: Use pattern matching from history
- **> 0.85**: Proceed with high confidence

## 🛡️ Protection Protocol Integration

### Protected File Recognition
**Critical Learning**: Always check if file is protected before any edit operation

**Protected Files List:**
- `brain/Claude.md` (master brain configuration)
- `brain/modules/superclaude-bridge.md` (bridge logic)
- Any file in `brain/Claude.md.versions/` (version history)

### Permission Protocol
```
if (target_file in PROTECTED_FILES):
    request_user_permission(f"May I modify {target_file} for {reason}?")
    wait_for_confirmation()
    if (permission_granted):
        proceed_with_edit()
        log_to_feedback_learning("protection-protocol", "Permission requested and granted")
    else:
        abort_operation()
        log_to_feedback_learning("protection-protocol", "Permission denied, operation aborted")
else:
    proceed_with_edit()
```

### Learning Integration
**Violation Logging**: Any attempt to edit protected files without permission → `brain/workflows/feedback-learning.md`
**Pattern Recognition**: 2+ violations in same session → High alert, require manual review
**Success Tracking**: Permission requests → `brain/modules/success-scoring.md`

### Intent Classification Enhancement
**New Intent Category**: `Protection-Check`
- **Trigger**: When operation involves file modification
- **Action**: Auto-check protection status before proceeding
- **Confidence**: Critical (100% accuracy required)