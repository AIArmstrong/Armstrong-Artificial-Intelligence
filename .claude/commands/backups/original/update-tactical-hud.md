# Update Tactical HUD

This command refreshes the Neo-Noir Tactical HUD dashboard with current system metrics.

## Command
```bash
# Generate updated ASCII HUD
/mnt/c/Users/Brandon/AAI/brain/modules/generate-tactical-hud.sh

# Update status.md with latest data
python3 -c "
import json
from datetime import datetime

# Load queue data
with open('/mnt/c/Users/Brandon/AAI/brain/logs/queue.json', 'r') as f:
    data = json.load(f)
    active_tasks = data['metadata']['active_items']

# Update status.md
with open('/mnt/c/Users/Brandon/AAI/brain/logs/dashboards/status.md', 'r') as f:
    content = f.read()

# Update task count in HUD
content = content.replace('TASKS      [13]', f'TASKS      [{active_tasks}]')

# Update timestamp
current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
content = content.replace('Dashboard generated: 2025-07-14T07:14:00Z', f'Dashboard generated: {current_time}')

with open('/mnt/c/Users/Brandon/AAI/brain/logs/dashboards/status.md', 'w') as f:
    f.write(content)

print(f'Tactical HUD updated: {active_tasks} active tasks')
"
```

## Usage
Run this whenever you need to refresh the dashboard with current system state.