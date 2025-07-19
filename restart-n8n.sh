#!/bin/bash

echo "Connecting to droplet and restarting n8n..."

ssh -i ~/.ssh/droplet_key -o StrictHostKeyChecking=no root@142.93.74.22 << 'EOF'
echo "Connected to droplet. Restarting n8n..."

cd /root/n8n-project
docker-compose restart n8n

echo "n8n restarted successfully!"
EOF

echo "Done!"