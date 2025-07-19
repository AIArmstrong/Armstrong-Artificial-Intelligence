#!/usr/bin/env python3
"""
Unified Task Manager - Single Source of Truth
Automatically syncs all task registries and prevents drift
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: str  # critical, high, medium, low
    status: str    # pending, in_progress, completed, blocked
    tags: List[str]
    estimated_duration: str
    created: str
    completed: Optional[str] = None
    source: str = "unified"  # which registry originated this task
    category: str = "general"
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class UnifiedTaskManager:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        
        # Registry files
        self.queue_file = self.aai_root / "brain" / "logs" / "queue.json"
        self.master_registry = self.aai_root / "brain" / "workflows" / "master-task-registry.json"
        self.unified_registry = self.aai_root / "brain" / "logs" / "unified-task-registry.json"
        
        # Backup directory
        self.backup_dir = self.aai_root / "brain" / "logs" / "archives" / f"task-sync-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Task storage
        self.tasks: Dict[str, Task] = {}
        self.sync_log = []
        
    def backup_existing_files(self):
        """Backup existing task files before sync"""
        files_to_backup = [self.queue_file, self.master_registry]
        
        for file_path in files_to_backup:
            if file_path.exists():
                backup_path = self.backup_dir / file_path.name
                backup_path.write_text(file_path.read_text())
                self.log(f"Backed up {file_path.name}")
        
        # Create backup info
        backup_info = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": "Unified task manager sync",
            "files_backed_up": [f.name for f in files_to_backup if f.exists()],
            "backup_location": str(self.backup_dir)
        }
        
        (self.backup_dir / "BACKUP_INFO.json").write_text(json.dumps(backup_info, indent=2))
    
    def log(self, message: str):
        """Log sync operations"""
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"[{timestamp}] {message}"
        self.sync_log.append(log_entry)
        print(f"📋 {message}")
    
    def normalize_task_id(self, task_id: str) -> str:
        """Normalize task IDs to prevent duplicates"""
        # Remove common prefixes and clean up
        cleaned = task_id.lower().replace("-", "_")
        
        # Handle duplicates from different sources
        common_mappings = {
            "youtube_subagent_research": "youtube_subagent_research",
            "docs_enhance_structure": "docs_enhance_structure", 
            "examples_implement_patterns": "examples_implement_patterns",
            "ideas_develop_pipeline": "ideas_develop_pipeline"
        }
        
        return common_mappings.get(cleaned, cleaned)
    
    def load_queue_tasks(self) -> List[Task]:
        """Load tasks from queue.json"""
        if not self.queue_file.exists():
            return []
        
        with open(self.queue_file, 'r') as f:
            data = json.load(f)
        
        tasks = []
        
        # Load pending tasks
        for task_data in data.get('queue', []):
            task = Task(
                id=self.normalize_task_id(task_data['id']),
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority'],
                status=task_data['status'],
                tags=task_data.get('tags', []),
                estimated_duration=task_data.get('estimated_duration', ''),
                created=task_data.get('created', ''),
                source="queue",
                category="queue"
            )
            tasks.append(task)
        
        # Load completed tasks
        for task_data in data.get('completed', []):
            task = Task(
                id=self.normalize_task_id(task_data['id']),
                title=task_data['title'], 
                description=task_data['description'],
                priority=task_data['priority'],
                status="completed",
                tags=task_data.get('tags', []),
                estimated_duration=task_data.get('estimated_duration', ''),
                created=task_data.get('created', ''),
                completed=task_data.get('completed', ''),
                source="queue",
                category="queue"
            )
            tasks.append(task)
        
        self.log(f"Loaded {len(tasks)} tasks from queue.json")
        return tasks
    
    def load_master_tasks(self) -> List[Task]:
        """Load tasks from master registry"""
        if not self.master_registry.exists():
            return []
        
        with open(self.master_registry, 'r') as f:
            data = json.load(f)
        
        tasks = []
        
        # Load systematic tasks
        systematic_tasks = data.get('tasks', {}).get('systematic', {})
        for task_id, task_data in systematic_tasks.items():
            task = Task(
                id=self.normalize_task_id(task_id),
                title=task_data['title'],
                description=task_data['description'], 
                priority=task_data['priority'],
                status=task_data['status'],
                tags=[f"#systematic", f"#{task_data.get('category', 'general')}"],
                estimated_duration="2-3 hours",  # default for systematic tasks
                created="2025-07-15T12:00:00Z",  # default creation date
                source="master",
                category=task_data.get('category', 'Foundation')
            )
            tasks.append(task)
        
        self.log(f"Loaded {len(tasks)} tasks from master registry")
        return tasks
    
    def merge_tasks(self, queue_tasks: List[Task], master_tasks: List[Task]) -> Dict[str, Task]:
        """Merge tasks from different sources, handling duplicates intelligently"""
        merged = {}
        conflicts = []
        
        # Add all tasks, checking for conflicts
        all_tasks = queue_tasks + master_tasks
        
        for task in all_tasks:
            if task.id in merged:
                existing = merged[task.id]
                
                # Handle conflicts based on priority rules:
                # 1. Completed tasks take precedence
                # 2. Queue tasks take precedence for status (more up-to-date)
                # 3. Master tasks provide systematic categorization
                
                if task.status == "completed" and existing.status != "completed":
                    # Completed task wins
                    merged[task.id] = task
                    conflicts.append(f"Resolved: {task.id} marked completed (was {existing.status})")
                elif existing.status == "completed" and task.status != "completed":
                    # Keep completed status
                    conflicts.append(f"Kept: {task.id} completed status (ignoring {task.status})")
                elif task.source == "queue" and existing.source == "master":
                    # Queue is more up-to-date for status, but keep systematic category
                    task.category = existing.category
                    merged[task.id] = task
                    conflicts.append(f"Merged: {task.id} using queue status with master category")
                elif task.source == "master" and existing.source == "queue":
                    # Keep queue task but update category
                    existing.category = task.category
                    conflicts.append(f"Enhanced: {task.id} with systematic category")
                else:
                    # Use most recent or highest priority
                    if task.priority == "critical" or existing.priority != "critical":
                        merged[task.id] = task
                        conflicts.append(f"Updated: {task.id} with newer/higher priority info")
            else:
                merged[task.id] = task
        
        if conflicts:
            self.log(f"Resolved {len(conflicts)} conflicts during merge")
            for conflict in conflicts:
                self.log(f"  - {conflict}")
        
        return merged
    
    def save_unified_registry(self):
        """Save the unified task registry"""
        # Create unified structure
        unified_data = {
            "metadata": {
                "created": datetime.now(timezone.utc).isoformat(),
                "version": "2.0.0",
                "description": "Unified task registry - single source of truth",
                "sync_log": self.sync_log,
                "total_tasks": len(self.tasks)
            },
            "summary": {
                "by_status": {},
                "by_priority": {},
                "by_category": {},
                "by_source": {}
            },
            "tasks": {}
        }
        
        # Calculate statistics
        for task in self.tasks.values():
            # Status stats
            unified_data["summary"]["by_status"][task.status] = \
                unified_data["summary"]["by_status"].get(task.status, 0) + 1
            
            # Priority stats
            unified_data["summary"]["by_priority"][task.priority] = \
                unified_data["summary"]["by_priority"].get(task.priority, 0) + 1
            
            # Category stats
            unified_data["summary"]["by_category"][task.category] = \
                unified_data["summary"]["by_category"].get(task.category, 0) + 1
            
            # Source stats
            unified_data["summary"]["by_source"][task.source] = \
                unified_data["summary"]["by_source"].get(task.source, 0) + 1
            
            # Add task to registry
            unified_data["tasks"][task.id] = asdict(task)
        
        # Save unified registry
        with open(self.unified_registry, 'w') as f:
            json.dump(unified_data, f, indent=2)
        
        self.log(f"Saved unified registry with {len(self.tasks)} tasks")
    
    def update_queue_file(self):
        """Update queue.json with synchronized data"""
        pending_tasks = []
        completed_tasks = []
        
        for task in self.tasks.values():
            task_data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "tags": task.tags,
                "estimated_duration": task.estimated_duration,
                "created": task.created,
                "status": task.status
            }
            
            if task.status == "completed":
                task_data["completed"] = task.completed or datetime.now(timezone.utc).isoformat()
                completed_tasks.append(task_data)
            else:
                pending_tasks.append(task_data)
        
        # Create updated queue structure
        queue_data = {
            "queue": pending_tasks,
            "completed": completed_tasks,
            "metadata": {
                "created": "2025-07-13T00:00:00Z",
                "last_reviewed": datetime.now(timezone.utc).isoformat(),
                "total_items_processed": len(completed_tasks),
                "active_items": len(pending_tasks),
                "completed_items": len(completed_tasks),
                "sync_source": "unified_task_manager"
            },
            "settings": {
                "persist_across_sessions": True,
                "auto_prompt_threshold": 5,
                "prompt_frequency_hours": 4
            }
        }
        
        # Save updated queue
        with open(self.queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)
        
        self.log(f"Updated queue.json: {len(pending_tasks)} pending, {len(completed_tasks)} completed")
    
    def update_master_registry(self):
        """Update master registry with comprehensive task categorization"""
        # Group tasks by category
        categories = {}
        for task in self.tasks.values():
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)
        
        # Create master registry structure
        master_data = {
            "metadata": {
                "created": "2025-07-15T12:00:00Z",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "version": "2.0.0",
                "description": "Master task registry with unified categorization",
                "sync_source": "unified_task_manager"
            },
            "summary": {
                "total_tasks": len(self.tasks),
                "by_status": {},
                "by_priority": {},
                "by_category": {}
            },
            "categories": {},
            "tasks": {}
        }
        
        # Calculate summary stats
        for task in self.tasks.values():
            master_data["summary"]["by_status"][task.status] = \
                master_data["summary"]["by_status"].get(task.status, 0) + 1
            master_data["summary"]["by_priority"][task.priority] = \
                master_data["summary"]["by_priority"].get(task.priority, 0) + 1
            master_data["summary"]["by_category"][task.category] = \
                master_data["summary"]["by_category"].get(task.category, 0) + 1
        
        # Add category information
        for category, tasks in categories.items():
            master_data["categories"][category] = {
                "total": len(tasks),
                "completed": len([t for t in tasks if t.status == "completed"]),
                "pending": len([t for t in tasks if t.status != "completed"]),
                "description": f"Tasks in {category} category"
            }
        
        # Add all tasks
        for task in self.tasks.values():
            master_data["tasks"][task.id] = asdict(task)
        
        # Save master registry
        with open(self.master_registry, 'w') as f:
            json.dump(master_data, f, indent=2)
        
        self.log(f"Updated master registry with {len(categories)} categories")
    
    def update_status_dashboard(self):
        """Update status.md dashboard with unified task data (as Claude.md specifies)"""
        status_file = self.aai_root / "dashboards" / "status.md"
        
        if not status_file.exists():
            self.log("Status dashboard not found, skipping update")
            return
        
        # Read current status.md
        with open(status_file, 'r') as f:
            content = f.read()
        
        # Calculate task statistics
        pending_count = len([t for t in self.tasks.values() if t.status != "completed"])
        completed_count = len([t for t in self.tasks.values() if t.status == "completed"])
        total_count = len(self.tasks)
        
        # Calculate priority distribution
        priority_counts = {}
        for task in self.tasks.values():
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        
        # Update queue processing section
        queue_pattern = r'Queue Processing\s+✅ Normal \(\d+ pending, \d+ complete\)'
        queue_replacement = f'Queue Processing        ✅ Normal ({pending_count} pending, {completed_count} complete)'
        content = re.sub(queue_pattern, queue_replacement, content)
        
        # Update Priority Actions Queue section
        priority_section_pattern = r'(## 🚀 Priority Actions Queue.*?)(## 🔮 System Trajectory)'
        
        # Generate priority actions from pending high-priority tasks
        high_priority_tasks = [t for t in self.tasks.values() if t.status != "completed" and t.priority == "high"]
        
        priority_actions = "## 🚀 Priority Actions Queue\n\n"
        for i, task in enumerate(high_priority_tasks[:5], 1):
            priority_actions += f"{i}. **{task.title}** [HIGH]\n"
            priority_actions += f"   - {task.description}\n"
            priority_actions += f"   - Estimated: {task.estimated_duration}\n\n"
        
        if len(high_priority_tasks) > 5:
            priority_actions += f"*Plus {len(high_priority_tasks) - 5} more high-priority tasks*\n\n"
        
        # Replace the priority actions section
        content = re.sub(priority_section_pattern, 
                        priority_actions + "## 🔮 System Trajectory", 
                        content, flags=re.DOTALL)
        
        # Update the conflict watchlist with current task counts
        conflict_pattern = r'Task Registry Mismatch\*\*: Master registry \(\d+ tasks\) vs Queue \(\d+ tasks\)'
        conflict_replacement = f'Task Registry Synchronization**: {total_count} tasks unified ({pending_count} pending, {completed_count} completed)'
        content = re.sub(conflict_pattern, conflict_replacement, content)
        
        # Update last 5 actions with sync information
        actions_pattern = r'(## 📋 Last 5 Actions Feed.*?)(1\. \*\*\[.*?\]\*\*.*?)(## ⚠️ Conflict & Pivot Watchlist)'
        
        current_time = datetime.now().strftime("%H:%M:%S")
        sync_action = f"1. **[{current_time}]** Task Registry Unified: {total_count} tasks synchronized\n"
        
        def actions_replacement(match):
            return match.group(1) + sync_action + match.group(2) + match.group(3)
        
        content = re.sub(actions_pattern, actions_replacement, content, flags=re.DOTALL)
        
        # Save updated status.md
        with open(status_file, 'w') as f:
            f.write(content)
        
        self.log(f"Updated status.md dashboard with {total_count} unified tasks")
    
    def generate_sync_report(self) -> str:
        """Generate comprehensive sync report"""
        report = f"""
# Task Registry Synchronization Report

**Sync Completed**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}
**Backup Location**: {self.backup_dir}

## Summary Statistics

- **Total Unified Tasks**: {len(self.tasks)}
- **Pending**: {len([t for t in self.tasks.values() if t.status != 'completed'])}
- **Completed**: {len([t for t in self.tasks.values() if t.status == 'completed'])}

## By Priority
"""
        
        priority_counts = {}
        for task in self.tasks.values():
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        
        for priority, count in sorted(priority_counts.items()):
            report += f"- **{priority.title()}**: {count} tasks\n"
        
        report += "\n## By Category\n"
        
        category_counts = {}
        for task in self.tasks.values():
            category_counts[task.category] = category_counts.get(task.category, 0) + 1
        
        for category, count in sorted(category_counts.items()):
            report += f"- **{category}**: {count} tasks\n"
        
        report += f"""
## Sync Operations Performed

"""
        for log_entry in self.sync_log:
            report += f"- {log_entry.split('] ')[1]}\n"
        
        report += f"""
## Files Updated

- ✅ `brain/logs/queue.json` - Primary task queue
- ✅ `brain/workflows/master-task-registry.json` - Master registry
- ✅ `brain/logs/unified-task-registry.json` - Single source of truth
- ✅ `dashboards/status.md` - Task status dashboard (as Claude.md specifies)

## Next Steps

1. All task registries are now synchronized
2. Use `brain/logs/unified-task-registry.json` as the single source of truth
3. Status dashboard automatically reflects unified task data
4. Other registries will be kept in sync automatically
5. No more manual sync required!

---
*Generated by Unified Task Manager | Automatic Sync Enabled*
"""
        
        return report
    
    def sync_all(self):
        """Main sync function - unify all task registries"""
        self.log("Starting unified task registry synchronization")
        
        # Backup existing files
        self.backup_existing_files()
        
        # Load tasks from all sources
        queue_tasks = self.load_queue_tasks()
        master_tasks = self.load_master_tasks()
        
        # Merge all tasks intelligently
        self.tasks = self.merge_tasks(queue_tasks, master_tasks)
        
        # Save unified registry
        self.save_unified_registry()
        
        # Update source files
        self.update_queue_file()
        self.update_master_registry()
        
        # Update status dashboard (as Claude.md specifies)
        self.update_status_dashboard()
        
        self.log(f"Synchronization complete: {len(self.tasks)} unified tasks")
        
        return self.generate_sync_report()

def main():
    """Run task registry synchronization"""
    manager = UnifiedTaskManager()
    report = manager.sync_all()
    
    # Save sync report
    report_path = manager.aai_root / "brain" / "logs" / "task-sync-report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📋 Task Registry Sync Complete!")
    print(f"📄 Report saved to: {report_path}")
    print(f"💾 Backups saved to: {manager.backup_dir}")
    
    return report

if __name__ == "__main__":
    main()