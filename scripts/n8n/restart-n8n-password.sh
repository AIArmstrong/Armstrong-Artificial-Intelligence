#!/bin/bash

echo "Connecting to droplet with password and restarting n8n..."

sshpass -p 'Wazzup365' ssh -o StrictHostKeyChecking=no root@142.93.74.22 << 'EOF'
echo "Connected to droplet. Attempting to restart n8n..."

# Try Docker first
if docker ps | grep -q n8n; then
    echo "Found n8n Docker container, restarting..."
    docker restart n8n
    exit 0
fi

# Try systemctl
if systemctl is-active --quiet n8n; then
    echo "Found n8n systemd service, restarting..."
    systemctl restart n8n
    exit 0
fi

# Try PM2
if command -v pm2 >/dev/null 2>&1 && pm2 list | grep -q n8n; then
    echo "Found n8n PM2 process, restarting..."
    pm2 restart n8n
    exit 0
fi

echo "Could not find n8n service to restart"
exit 1
EOF

echo "Done!"