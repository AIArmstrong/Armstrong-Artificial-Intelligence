# n8n Troubleshooting and Restart SOP

## Purpose
Standard Operating Procedure for diagnosing and resolving n8n service issues, including complete restart process and troubleshooting steps.

## Context
- **n8n Server**: https://n8n.olympus-council.xyz (production)
- **Direct Access**: http://142.93.74.22:5678 (development/debugging)
- **Deployment**: Docker container managed by docker-compose
- **Location**: /root/n8n-project/ on DigitalOcean droplet
- **SSH Access**: SSH key authentication required

## Prerequisites
- SSH key configured for root@142.93.74.22
- SSH key located at ~/.ssh/droplet_key
- Access to DigitalOcean console (backup access method)

## Troubleshooting Workflow

### Step 1: Verify n8n Service Status
```bash
# Check if n8n is accessible
curl -I https://n8n.olympus-council.xyz

# Expected: HTTP 200 response
# If 502 Bad Gateway: n8n service is down
# If timeout/connection refused: Network/server issue
```

### Step 2: SSH Server Access
```bash
# Connect to droplet
ssh -i ~/.ssh/droplet_key root@142.93.74.22

# If connection fails, check:
# 1. SSH key permissions: chmod 600 ~/.ssh/droplet_key
# 2. authorized_keys format on server (single line entries)
# 3. Use DigitalOcean console as backup access
```

### Step 3: Check Docker Container Status
```bash
# List all containers
docker ps -a

# Look for n8n container status:
# - Should see: n8n-project_n8n_1 with status "Up X minutes"
# - If "Exited": Container crashed and needs restart

# Check container logs for errors
docker logs n8n-project_n8n_1 --tail 50
```

### Step 4: Check n8n Project Directory
```bash
# Navigate to project directory
cd /root/n8n-project

# Verify docker-compose configuration
cat docker-compose.yml

# Check for correct n8n service configuration:
# - Image: n8nio/n8n
# - Ports: "5678:5678"
# - Environment variables set
# - Volume mounts configured
```

## Restart Procedures

### Method 1: Docker Compose Restart (Preferred)
```bash
# Navigate to project directory
cd /root/n8n-project

# Restart n8n service only
docker-compose restart n8n

# Verify restart successful
docker ps | grep n8n
```

### Method 2: Full Stack Restart
```bash
# Navigate to project directory
cd /root/n8n-project

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# Verify all containers running
docker ps
```

### Method 3: Emergency Recovery
```bash
# If docker-compose is corrupted or missing
cd /root/n8n-project

# Backup current configuration
cp docker-compose.yml docker-compose.yml.backup

# Pull latest n8n image
docker pull n8nio/n8n

# Force recreate containers
docker-compose up -d --force-recreate
```

## Common Issues and Solutions

### Issue: Container Keeps Crashing
**Symptoms**: Container starts then immediately exits
```bash
# Check container logs for specific error
docker logs n8n-project_n8n_1

# Common causes:
# 1. Port already in use
# 2. Volume mount permission issues
# 3. Environment variable problems
# 4. Corrupted data volume

# Solution: Check port conflicts
netstat -tlnp | grep 5678

# Solution: Fix volume permissions
sudo chown -R node:node /root/n8n-data
```

### Issue: SSH Key Authentication Failure
**Symptoms**: "Permission denied (publickey)"
```bash
# Verify SSH key exists locally
ls -la ~/.ssh/droplet_key*

# Check key permissions
chmod 600 ~/.ssh/droplet_key

# Test key authentication
ssh -i ~/.ssh/droplet_key -v root@142.93.74.22

# If still failing, use DigitalOcean console to fix authorized_keys:
# 1. Access droplet via console
# 2. Check: cat ~/.ssh/authorized_keys
# 3. Ensure SSH keys are single line entries (no line breaks)
# 4. Fix formatting: each key must be one continuous line
```

### Issue: n8n Web Interface Not Loading
**Symptoms**: 502 Bad Gateway or timeout
```bash
# Check nginx proxy status
systemctl status nginx

# Check if n8n container is running and port is open
docker ps | grep n8n
netstat -tlnp | grep 5678

# Verify n8n configuration
curl -I http://localhost:5678

# If nginx issues:
systemctl restart nginx
```

### Issue: High Memory Usage
**Symptoms**: Server becomes unresponsive
```bash
# Check system resources
free -h
df -h

# Check Docker container resource usage
docker stats

# If memory issues, restart with cleanup:
docker system prune -f
docker-compose restart
```

## Automated Restart Script

### Script Location
`/mnt/c/Users/Brandon/AAI/restart-n8n.sh`

### Script Usage
```bash
# Make script executable (if not already)
chmod +x restart-n8n.sh

# Run restart script
./restart-n8n.sh

# Expected output:
# "Connecting to droplet and restarting n8n..."
# "Connected to droplet. Restarting n8n..."
# "n8n restarted successfully!"
# "Done!"
```

### Script Troubleshooting
```bash
# If script fails, run manually:
ssh -i ~/.ssh/droplet_key root@142.93.74.22 "cd /root/n8n-project && docker-compose restart n8n"

# Check script permissions
ls -la restart-n8n.sh

# Verify script contents
cat restart-n8n.sh
```

## Verification Steps

### Post-Restart Verification
```bash
# 1. Check container status
docker ps | grep n8n

# 2. Test local access
curl -I http://localhost:5678

# 3. Test domain access
curl -I https://n8n.olympus-council.xyz

# 4. Check logs for errors
docker logs n8n-project_n8n_1 --tail 20

# 5. Verify web interface loads
# Open browser: https://n8n.olympus-council.xyz
# Should see n8n login/dashboard
```

### Health Check Commands
```bash
# Complete health check sequence
echo "=== n8n Health Check ==="
echo "Container Status:"
docker ps | grep n8n

echo "Port Status:"
netstat -tlnp | grep 5678

echo "Domain Response:"
curl -s -o /dev/null -w "%{http_code}" https://n8n.olympus-council.xyz

echo "Local Response:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5678

echo "Recent Logs:"
docker logs n8n-project_n8n_1 --tail 5
```

## Escalation Procedures

### Level 1: Self-Service (This SOP)
- Container restart via docker-compose
- Basic troubleshooting and log review
- SSH key authentication fixes

### Level 2: Advanced Troubleshooting
- DigitalOcean console access required
- System-level debugging (memory, disk, network)
- Docker system cleanup and rebuild

### Level 3: Infrastructure Changes
- Droplet resizing or migration
- DNS/domain configuration changes
- SSL certificate renewal

## Prevention and Monitoring

### Regular Maintenance
```bash
# Weekly health check (add to crontab)
0 2 * * 1 /root/scripts/n8n-health-check.sh

# Monthly cleanup
0 3 1 * * docker system prune -f && docker-compose restart
```

### Monitoring Setup
- Monitor https://n8n.olympus-council.xyz availability
- Set up alerts for container crashes
- Track disk space in /root/n8n-data volume
- Monitor SSL certificate expiration

### Backup Procedures
```bash
# Backup n8n data weekly
tar -czf /backup/n8n-data-$(date +%Y%m%d).tar.gz /root/n8n-data

# Backup docker-compose configuration
cp /root/n8n-project/docker-compose.yml /backup/
```

## Contact Information
- **Primary**: SSH access via droplet_key
- **Backup**: DigitalOcean console access
- **Emergency**: DigitalOcean support ticket

---
*Last Updated: 2025-07-16*  
*Next Review: 2025-08-16*

## Learning Events
- **2025-07-16**: SSH key formatting must be single-line entries in authorized_keys
- **2025-07-16**: n8n runs in Docker container, not as system service
- **2025-07-16**: Always check container logs first for specific error messages