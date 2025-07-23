---
allowed-tools: [Read, Write, Edit, Glob, TodoWrite, Bash]
description: "Test-driven development planning with dependency mapping and tactical dashboard updates"
---

# /sc:tdd-planner - TDD Planning & Dashboard Management

## Purpose
Analyze requirements and generate structured test-driven development plans with dependency mapping, while maintaining tactical dashboard synchronization.

## Usage
```
/sc:tdd-planner [requirements] [--scope full|focused] [--update-dashboard]
```

## Arguments
- `requirements` - Requirement document(s) or target specifications
- `--scope` - Planning scope (full comprehensive analysis, focused specific features)
- `--update-dashboard` - Force tactical dashboard refresh after planning
- `--format` - Output format (markdown, json, mermaid)

## Execution

### TDD Planning Workflow
1. **Requirements Analysis**
   - Parse target documents and extract functional requirements
   - Identify technical constraints and dependencies
   - Document ambiguities and unclear specifications

2. **Test-First Strategy Design**
   - Define test architecture patterns and approach
   - Plan test structures and coverage targets
   - Outline TDD cycles and development methodology

3. **Task Decomposition with Dependencies**
   - Break down features into test-driven implementation tasks
   - Create corresponding test tasks for each feature (Red-Green-Refactor)
   - Define task types (test-write, implementation, refactor, documentation)
   - Map task prerequisites and blocking relationships

4. **Dependency Visualization**
   - Generate Mermaid diagram showing task flow and dependencies
   - Illustrate critical path and TDD milestone dependencies
   - Highlight parallel development opportunities
   - Show Red-Green-Refactor cycle relationships

5. **Dashboard Integration**
   - Update tactical HUD with planning results
   - Refresh task metrics and progress indicators
   - Synchronize planning data with brain/logs/queue.json
   - Generate planning-focused status updates

## Output Structure

### Planning Report Format
```markdown
## TDD Implementation Plan

### Overview
- High-level TDD strategy and architectural approach
- Test methodology and coverage targets
- Key technical decisions and test-first assumptions

### Test-Driven Task Breakdown
Array of TDD task objects:
```json
{
  "id": "string",
  "description": "string", 
  "type": "test-write|implement|refactor|integration-test",
  "status": "red|green|refactor|completed",
  "dependencies": ["task_id_1", "task_id_2"],
  "test_coverage_target": "percentage",
  "tdd_cycle": "red-green-refactor phase"
}
```

### Dependency Flow Diagram
Mermaid diagram illustrating:
- TDD task dependencies and Red-Green-Refactor cycles
- Critical path identification for test-first development
- Parallel testing and implementation opportunities
- Test milestone checkpoints

### Planning Clarifications
- Unclear functional requirements needing test specification
- Missing technical specifications affecting test design
- Integration and testing compatibility concerns

## Dashboard Integration Features

### Tactical HUD Updates
- **Task Metrics**: Updates active task counts from planning results
- **TDD Progress**: Shows Red-Green-Refactor cycle completion status
- **Planning Timestamp**: Refreshes dashboard generation time
- **Coverage Tracking**: Displays test coverage progress and targets

### Automatic Dashboard Refresh
```python
# Integrated dashboard update logic
import json
from datetime import datetime

# Load planning results and update queue
with open('/mnt/c/Users/Brandon/AAI/brain/logs/queue.json', 'r') as f:
    queue_data = json.load(f)
    
# Add TDD planning tasks to queue
for task in tdd_planning_tasks:
    queue_data['tasks'].append({
        'id': task['id'],
        'type': task['type'], 
        'status': task['status'],
        'tdd_cycle': task['tdd_cycle']
    })

# Update metadata
queue_data['metadata']['active_items'] = len([t for t in queue_data['tasks'] if t['status'] != 'completed'])
queue_data['metadata']['last_updated'] = datetime.now().isoformat()

# Update tactical HUD with new metrics
with open('/mnt/c/Users/Brandon/AAI/dashboards/tactical-hud.txt', 'r') as f:
    hud_content = f.read()

# Update task counts and TDD progress
hud_content = hud_content.replace('TASKS      [OLD_COUNT]', f'TASKS      [{queue_data["metadata"]["active_items"]}]')
hud_content = hud_content.replace('TDD        [OLD_STATUS]', f'TDD        [PLANNING]')

# Save updated dashboard
with open('/mnt/c/Users/Brandon/AAI/dashboards/tactical-hud.txt', 'w') as f:
    f.write(hud_content)
```

## TDD Planning Examples

### Example 1: Feature Planning
```bash
/sc:tdd-planner "Add user authentication system" --scope full
```
**Output**: Complete TDD plan with test-first approach for authentication

### Example 2: Bug Fix Planning  
```bash
/sc:tdd-planner "Fix login memory leak" --scope focused --update-dashboard
```
**Output**: Focused TDD approach for bug resolution with dashboard refresh

### Example 3: Integration Planning
```bash
/sc:tdd-planner requirements.md --format mermaid
```
**Output**: Visual TDD workflow with dependency mapping

## Claude Code Integration
- **Read**: Analyzes requirement documents and existing codebase
- **Write**: Generates comprehensive TDD planning reports
- **Glob**: Discovers related test files and implementation patterns
- **TodoWrite**: Tracks TDD planning tasks and milestones
- **Bash**: Executes dashboard update scripts and metrics collection

## Advanced Features

### Test-First Methodology Integration
- **Red Phase Planning**: Define failing test requirements
- **Green Phase Planning**: Minimal implementation strategies  
- **Refactor Phase Planning**: Code improvement and optimization cycles

### Dependency-Aware Planning
- **Parallel TDD Cycles**: Identify independent test development paths
- **Blocking Dependencies**: Critical path analysis for test-driven development
- **Integration Points**: Plan testing interfaces and contract verification

### Dashboard Intelligence
- **Automatic Sync**: Dashboard updates triggered by planning changes
- **Progress Visualization**: TDD cycle status and coverage metrics
- **Planning History**: Track planning iterations and success rates