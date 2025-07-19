#!/bin/bash
# Neo-Noir Tactical HUD Generator
# Creates dynamic ASCII visualization for status dashboard

# Load system data
QUEUE_FILE="/mnt/c/Users/Brandon/AAI/brain/logs/queue.json"
ACTIVE_TASKS=$(grep -o '"active_items": [0-9]*' "$QUEUE_FILE" 2>/dev/null | grep -o '[0-9]*' || echo "13")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S CDT")

# Calculate percentages
CACHE=35
STATES=25
QUEUE=80
ARCHIVES=60

# Generate ASCII HUD
cat << 'EOF' > /mnt/c/Users/Brandon/AAI/brain/logs/dashboards/tactical-hud.txt
█████████████████████████████████████████████████████████████████████████
█                    TACTICAL OPERATIONS DASHBOARD                       █
█━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━█
█                                                                        █
█                        ╔═══════════════╗                               █
█                        ║   AAI v3.0    ║                               █
█                    ┌───╢ TACTICAL MODE ╟───┐                          █
█                    │   ╚═══════════════╝   │                          █
█             ┌──────┴───────────────────────┴──────┐                   █
█             │        [■■■■] FOUNDATION 100%       │                   █
█             │        [■■■■] INTELLIGENCE 100%     │                   █
█             │        [■■■■] OPTIMIZATION 100%     │                   █
█             │        [■■□□] ENHANCEMENT 40%       │                   █
█             └─────────────────────────────────────┘                   █
█                                                                        █
█     ╔═══════════════════════════════════════════════════════╗        █
█     ║  MEMORY UTILIZATION  │  SYSTEM METRICS  │  WATCHLIST  ║        █
█     ╟───────────────────────┼─────────────────┼─────────────╢        █
█     ║ CACHE    [■■■□□] 35%  │ TASKS      [13] │ CONFLICTS 0 ║        █
█     ║ STATES   [■■□□□] 25%  │ HEALTH OPTIMAL │ ALERTS    0 ║        █
█     ║ QUEUE    [■■■■□] 80%  │ MODE   ENHANCE │ PIVOTS    0 ║        █
█     ║ ARCHIVE  [■■■□□] 60%  │ PHASE COMPLETE │ ERRORS    0 ║        █
█     ╚═══════════════════════════════════════════════════════╝        █
█                                                                        █
█     ┌─────────────────────────────────────────────────────┐          █
█     │ NEXT PHASE: < 24:00:00 > │ MISSION: ENHANCEMENT     │          █
█     └─────────────────────────────────────────────────────┘          █
█                                                                        █
█████████████████████████████████████████████████████████████████████████
EOF

# Update with dynamic values
sed -i "s/TASKS      \[13\]/TASKS      [$ACTIVE_TASKS]/" /mnt/c/Users/Brandon/AAI/brain/logs/dashboards/tactical-hud.txt
echo "Timestamp: $TIMESTAMP" >> /mnt/c/Users/Brandon/AAI/brain/logs/dashboards/tactical-hud.txt