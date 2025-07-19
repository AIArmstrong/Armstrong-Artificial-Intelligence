# /log Command - Intelligent Context Management System

## Purpose
Intelligent logging system that auto-routes content based on tags, detects contradictions, and maintains dynamic system memory.

## Command Variants

### `/log now [--sync-tasks]`
Immediately log current context with auto-tagging and intelligent routing.
**MANDATORY**: Update `dashboards/status.md` with current task status and events.

**Task Management Features:**
- Auto-detect task completions from conversation (✅, "done", "completed")
- `--sync-tasks`: Force sync between detected tasks and dashboard state
- Verify pending tasks from previous sessions
- Auto-mark completed tasks in conversation-state.json

### `/log queue`
Show flagged contradictions and items needing user review from `brain/logs/queue.json`.
**MANDATORY**: Update `dashboards/status.md` with current task status and events.

### `/log status`
Generate comprehensive system dashboard with:
- Interactive conflict & pivot watchlist
- Phase progress tracker with visual progress bar
- Cache vs state memory heatmap
- Live decision trace graph (Mermaid)
- Recent tag trends analysis
- Last 5 actions feed
- System integrity checks
- Next review schedule
- **✅ Task Summary:** Live task state with checkboxes
  - [x] Task A — ✅ completed
  - [ ] Task B — in progress
  - [ ] Task C — pending
Output saved to `dashboards/status.md`
**MANDATORY**: Always verify and update dashboard accuracy before output.

### `/log archive-phase`
Manually trigger phase completion:
- Archive cache to `brain/logs/archives/`
- Process explain.md entries > 500 lines or marked for archival
- Move completed decisions to `brain/docs/explain-archive/`
- Update decision index and trace

### `/log summary` (optional)
Generate human-readable digest of current system state.

## Core Behavior

### 1. Auto-Tagging System
Analyze content and apply intelligent tags:
- `#intent`, `#decision`, `#feature`, `#framework`, `#pivot`, `#deprecated`
- `#state`, `#milestone`, `#task`, `#note`, `#alert`, `#review`
- `#conflict`, `#contradiction`, `#overlap`, `#flag`, `#queue`, `#context`
- `#feedback`, `#model`, `#tools`, `#persona`, `#debug`, `#refactor`
- `#task-completed`, `#task-reopened`, `#task-pending`, `#task-sync`

If too many tags apply, default to `#intent` and queue others for batch learning.

### 2. Dynamic Routing Rules

| File | Action | Notes |
|------|--------|-------|
| `conversation-state.json` | Overwrite | Living document, always current |
| `cache/config.json` | Overwrite | Active working memory |
| `logs/interactions.log` | Append | Full historical context |
| `research/_memory.md` | Version | Mark deprecated sections |
| `docs/explain.md` | Version | Track rationale evolution |
| `brain/logs/tasks-history.md` | Append | Task evolution snapshots |
| `conversation-state.json` | Update | Auto-sync task statuses |

### 3. Contradiction Detection
Use OpenRouter API (`OPENROUTER_API_KEY`) with `openai/gpt-4o-mini`:
- Analyze current session for contradictions
- Present side-by-side diff in queue
- Add to `brain/logs/queue.json` for review
- Prompt periodically: "You have unresolved items in /log queue"

### 4. Memory TTL & Archival
- Archive cache entries to `brain/logs/archives/` on phase completion
- LRU behavior: frequently accessed items persist longer
- Phase detection: Monitor `conversation-state.json` changes
- Manual trigger: `/log archive-phase`

### 5. Protected Files
NEVER modify:
- `brain/Claude.md`
- `brain/modules/superclaude-bridge.md`
- Any file in `brain/Claude.md.versions/`

Log attempts to modify protected files in `brain/logs/protected.md`.

## Implementation Steps

### Step 1: Error Introspection & Detection
```python
# Enhanced error scanning
error_events = []

# Scan conversation state for error flags
state = read_json("brain/states/conversation-state.json")
if any(flag in str(state) for flag in ["error", "failed", "unresolved"]):
    error_events.append({"type": "state_flag", "source": "conversation-state.json"})

# Scan recent conversation for error patterns
recent_messages = get_last_messages(10)
error_patterns = ["❌", "⚠️", "Fix that", "didn't work", "conflict", "error:", "mismatch"]
for msg in recent_messages:
    for pattern in error_patterns:
        if pattern.lower() in msg.lower():
            error_events.append({
                "type": "conversation_error", 
                "pattern": pattern,
                "message": msg[:100]
            })

# Log errors if found
if error_events:
    log_errors_to_files(error_events)
```

### Step 2: Analyze Current Context & Extract Task Events
```python
# Enhanced context analysis with task detection
current_context = gather_current_conversation()
intent = detect_intent(current_context)
tags = auto_generate_tags(current_context, intent)

# Task completion detection
task_events = extract_task_events(current_context)
for task, status in task_events:
    if status == "completed" and not in_conversation_state(task):
        mark_task_completed(task)
        append_log(f"[{timestamp()}] | #task-completed | {task} completed — verified from message")
    elif status == "reopened":
        reopen_task(task)
        append_log(f"[{timestamp()}] | #task-reopened | {task} reopened per message")

# Task pattern detection
task_patterns = ["✅", "❌", "done", "completed", "finished", "reopened", "undone"]
last_messages = get_last_messages(10)
for msg in last_messages:
    for pattern in task_patterns:
        if pattern.lower() in msg.lower():
            extracted_tasks = parse_task_from_message(msg, pattern)
            for task in extracted_tasks:
                update_task_status(task, derive_status_from_pattern(pattern))
```

### Step 3: Check for Contradictions
```python
# Use OpenRouter API
contradictions = check_contradictions(
    current_context,
    existing_state="brain/states/conversation-state.json",
    model="openai/gpt-4o-mini"
)
if contradictions:
    add_to_queue("brain/logs/queue.json", contradictions)
```

### Step 4: Error Logging & Learning Integration
```python
# Log each error event to dedicated files
def log_errors_to_files(error_events):
    timestamp = now()
    
    # Append to errors.md
    for event in error_events:
        append_to_file("brain/logs/errors.md", 
            f"[{timestamp}] | #error | {event['pattern']} - {event['message'][:50]}")
    
    # Update interactions.log with error count
    append_to_file("brain/logs/interactions.log",
        f"{timestamp} - Error detection: {len(error_events)} events found")
    
    # Alert if 5+ errors in single run
    if len(error_events) >= 5:
        append_to_file("brain/logs/errors.md",
            f"[ALERT] {len(error_events)} errors found in this /log cycle. Manual review recommended. #review-needed")
        
        # Update status dashboard with alert
        update_dashboard_alert("brain/logs/dashboards/status.md", 
            f"🚨 HIGH ERROR COUNT: {len(error_events)} errors detected")
    
    # Record learning events
    for event in error_events:
        append_to_file("brain/workflows/tagging-evolution.md",
            f"[{timestamp}] | #error-{event['type']} | \"{event['pattern']}\" | Learning: monitoring error patterns")
    
    # Track recurring errors in success scoring
    update_error_tracking("brain/modules/success-scoring.md", error_events)
```

### Step 5: Route Content
```python
# Based on tags and content type
if "#state" in tags or "#pivot" in tags:
    update_file("brain/states/conversation-state.json", content, mode="overwrite")
elif "#decision" in tags or "#rationale" in tags:
    update_file("brain/docs/explain.md", content, mode="version")
elif "#research" in tags:
    update_file("research/_memory.md", content, mode="version")
else:
    update_file("brain/logs/interactions.log", content, mode="append")
```

### Step 6: Proactive Regression Check
```python
# Compare current errors vs previous runs
def check_error_regression():
    current_errors = len(error_events)
    previous_alert_count = count_alerts_in_file("brain/logs/errors.md")
    
    # Check for improvement
    if current_errors < previous_alert_count:
        timestamp = now()
        # Mark learning success
        append_to_file("brain/modules/success-scoring.md",
            f"[{timestamp}] | dashboard-error-reduction | Success: {previous_alert_count} → {current_errors}")
        
        # Update learning loop dashboard
        append_to_file("brain/logs/dashboards/learning-loop.md",
            f"✔️ **Error Reduction Success**: {previous_alert_count} → {current_errors} errors")
    
    return current_errors, previous_alert_count
```

### Step 7: Sync Task Statuses & Update Dashboards
```python
# Sync detected task statuses to state and dashboard
def sync_task_statuses():
    detected_tasks = extract_task_events(last_messages)
    current_state = read_json("brain/states/conversation-state.json")
    dashboard_tasks = read_tasks_from_dashboard("dashboards/status.md")
    
    # Compare and sync mismatches
    for task, status in detected_tasks:
        if task not in current_state or current_state[task] != status:
            current_state[task] = status
            log_interaction(f"Task '{task}' auto-updated to {status}")
    
    # Update conversation state
    write_json("brain/states/conversation-state.json", current_state)
    
    # Append task history snapshot
    append_task_snapshot("brain/logs/tasks-history.md")

# Create/update status dashboard with task summary
create_dashboard("brain/logs/dashboards/status.md", {
    "memory_load": calculate_memory_usage(),
    "conflicts": count_queue_items(),
    "phase": get_current_phase(),
    "recent_logs": get_recent_entries(),
    "task_summary": generate_task_checkboxes(current_state)
})

# Pending task verification
pending_tasks = [task for task, status in current_state.items() if status == "in_progress"]
if pending_tasks:
    print(f"⚠️ Pending: {len(pending_tasks)} tasks from last session still incomplete")
    for task in pending_tasks:
        print(f"  - {task} (use '/log now --sync-tasks' to update)")
```

### Step 8: Task Confirmation & Learn from Feedback
```python
# Explicit task completion confirmation
def check_implicit_task_completion(message):
    implicit_patterns = ["that's done", "finished that", "complete", "all set"]
    for pattern in implicit_patterns:
        if pattern in message.lower():
            extracted_task = infer_task_from_context(message)
            if extracted_task and not is_explicitly_marked(extracted_task):
                return prompt_user_confirmation(f"I noticed you said '{pattern}'—should I mark '{extracted_task}' as completed and update the dashboard?")
    return False

# Task history snapshot generation
def append_task_snapshot(file_path):
    timestamp = now()
    current_tasks = get_all_tasks_from_state()
    snapshot = f"\n[{timestamp}]\n"
    for task, status in current_tasks.items():
        icon = "🗹" if status == "completed" else "☐"
        snapshot += f"- {icon} {task} – {status}\n"
    append_to_file(file_path, snapshot)

# Track tag accuracy in batch mode
if user_corrects_tag:
    log_correction("brain/workflows/tagging-evolution.md", {
        "original_tag": old_tag,
        "corrected_tag": new_tag,
        "context": snippet,
        "timestamp": now()
    })
```

## Usage Examples

### Basic Logging
```
/log now
> Context analyzed and routed to appropriate locations
> Tags applied: #decision #architecture #brain-centric
> No contradictions detected
> ✅ Task "implement user auth" auto-marked completed
> 📋 Task history snapshot saved
```

### Task Sync
```
/log now --sync-tasks
> Scanning last 10 messages for task events...
> Found: 2 completed, 1 reopened
> ✅ "database setup" marked completed
> ✅ "API endpoints" marked completed  
> 🔄 "error handling" reopened
> Dashboard updated with current task state
> ⚠️ Pending: "testing phase" still in progress from last session
```

### Reviewing Queue
```
/log queue
> 2 items pending review:
> 1. Contradiction: "Use MySQL" vs "Use Supabase" 
> 2. Direction pivot: "Archive context-base" vs "Keep context-base"
```

### System Status
```
/log status
> Memory Load: 23% (2.3MB/10MB)
> Unresolved Conflicts: 2
> Current Phase: implementation
> Recent Activity: 15 logs in past hour
>
> ### ✅ Task Summary:
> - [x] Database setup — ✅ completed
> - [x] API endpoints — ✅ completed
> - [ ] Error handling — in progress
> - [ ] Testing phase — pending
> - [ ] Documentation — pending
```

## Error Handling & Compliance
- If OpenRouter API fails, fall back to keyword-based contradiction detection
- If queue.json corrupted, create backup and start fresh
- If protected file modification attempted, log and alert user
- **File Compliance**: Error enhancement does NOT modify Claude.md or protected files
- All error data routes to: `errors.md`, `interactions.log`, `tagging-evolution.md`, `success-scoring.md`, dashboards
- **Learning Integration**: Each error automatically triggers learning event logging
- **Regression Monitoring**: Proactive comparison of error counts vs previous runs

## Task Management Integration

### Automatic Task Detection Patterns
- **Completion**: ✅, ☑️, "done", "completed", "finished", "all set"
- **Reopening**: ❌, "undone", "reopened", "needs work", "broken again"
- **Progress**: "working on", "in progress", "started", "began"

### Task State Synchronization
1. **Auto-Detection**: Scan conversation for task status changes
2. **State Update**: Sync to `conversation-state.json`
3. **Dashboard Refresh**: Update `dashboards/status.md` with current state
4. **History Tracking**: Append snapshots to `brain/logs/tasks-history.md`
5. **Conflict Resolution**: Prompt for ambiguous task references

### Task Verification Workflow
```
1. Extract task events from recent messages
2. Compare with existing conversation state
3. Auto-update confirmed completions
4. Flag ambiguous references for user confirmation
5. Update dashboard with live task checkboxes
6. Log task evolution for learning
```

## Future Enhancements
- Supabase auto-sync for distributed memory
- Advanced LLM analysis for deeper contradiction detection
- Pattern recognition for proactive suggestions
- Visual memory map generation
- **Smart Task Clustering**: Group related sub-tasks automatically
- **Progress Estimation**: ML-based completion time predictions
- **Dependency Mapping**: Visualize task relationships and blockers

---
*Intelligent logging with autonomous task management for Jarvis-grade system awareness*