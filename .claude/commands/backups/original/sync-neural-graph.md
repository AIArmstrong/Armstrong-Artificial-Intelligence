# Sync Neural Decision Graph

## Description
Automatically synchronizes the neural decision graph (decision-trace.mmd) with the latest entries from explain.md, incorporating confidence scoring, WHY rationale journaling, and feedback loop integration.

## Usage
```bash
python /mnt/c/Users/Brandon/AAI/brain/docs/auto-sync-graph.py
```

## What it does
1. **Extracts Decisions**: Parses explain.md for new decision entries
2. **Generates WHY Rationales**: Creates neural rationale connections showing the reasoning behind each decision
3. **Applies Confidence Scoring**: Visual thickness and opacity based on decision confidence levels
4. **Updates Graph**: Regenerates decision-trace.mmd with latest neural network visualization
5. **Logs Activity**: Tracks sync operations for learning loop integration

## Auto-Trigger Integration
This command should be automatically triggered when:
- New decisions are added to explain.md
- Decision outcomes are validated
- Confidence scores are updated
- Weekly review cycles occur

## Neural Features
- **WHY Journaling**: Each decision node includes rationale reasoning
- **Confidence Visualization**: Node thickness reflects confidence levels
- **Feedback Loops**: Outcome validation feeds back into decision scoring
- **Pattern Recognition**: Identifies successful vs failed decision patterns

## Example Output
```
🧠 Neural Decision Graph Auto-Sync Starting...
📊 Extracted 6 decisions from explain.md
✅ Neural graph updated with 6 decisions
📈 Confidence scores and WHY rationales integrated
🔄 Feedback loop system activated
```

## Integration Points
- **brain/docs/explain.md**: Source of decision data
- **brain/docs/decision-trace.mmd**: Target neural graph
- **brain/docs/sync-log.json**: Operation history
- **brain/workflows/feedback-learning.md**: Learning loop integration