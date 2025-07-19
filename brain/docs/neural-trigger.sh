#!/bin/bash
# Neural Decision Graph Auto-Trigger
# Monitors explain.md for changes and auto-syncs the neural graph

DOCS_DIR="/mnt/c/Users/Brandon/AAI/brain/docs"
EXPLAIN_FILE="$DOCS_DIR/explain.md"
SYNC_SCRIPT="$DOCS_DIR/auto-sync-graph.py"

echo "🧠 Neural Decision Graph Auto-Trigger Activated"
echo "📊 Monitoring: $EXPLAIN_FILE"
echo "🔄 Sync Script: $SYNC_SCRIPT"

# Function to sync graph
sync_graph() {
    echo "🔄 Detected changes in explain.md - syncing neural graph..."
    cd "$DOCS_DIR"
    python3 auto-sync-graph.py
    echo "✅ Neural graph sync completed"
}

# Initial sync
sync_graph

# Watch for changes (using inotify if available)
if command -v inotifywait &> /dev/null; then
    echo "👁️ Watching for changes using inotifywait..."
    while inotifywait -e modify "$EXPLAIN_FILE"; do
        sleep 1  # Brief delay to allow file writing to complete
        sync_graph
    done
else
    echo "⚠️ inotifywait not available - manual sync required"
    echo "💡 Run: python3 $SYNC_SCRIPT"
fi