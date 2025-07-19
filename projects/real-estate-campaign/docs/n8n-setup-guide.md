# n8n Server Setup Guide

## Current Status
Your n8n server at https://n8n.olympus-council.xyz is returning a 502 Bad Gateway error. This means nginx is running but n8n service is down.

## To Get n8n Back Online

### 1. SSH into your Digital Ocean droplet:
```bash
ssh root@your-droplet-ip
```

### 2. Check n8n service status:
```bash
systemctl status n8n
# or if using Docker:
docker ps -a | grep n8n
```

### 3. Restart n8n service:

#### If using systemd:
```bash
systemctl restart n8n
systemctl enable n8n  # ensures it starts on boot
```

#### If using Docker:
```bash
docker restart n8n
# or if not running:
docker start n8n
```

#### If using PM2:
```bash
pm2 restart n8n
pm2 save
pm2 startup  # ensures it starts on boot
```

### 4. Check logs for errors:
```bash
# Systemd logs:
journalctl -u n8n -f

# Docker logs:
docker logs n8n -f

# PM2 logs:
pm2 logs n8n
```

### 5. Common fixes:

#### Port conflict:
```bash
# Check if port 5678 is in use
netstat -tulpn | grep 5678
```

#### Environment variables:
Make sure your .env file has:
```
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_HOST_URL=https://n8n.olympus-council.xyz
WEBHOOK_URL=https://n8n.olympus-council.xyz
```

#### Nginx configuration:
Check `/etc/nginx/sites-available/n8n`:
```nginx
server {
    server_name n8n.olympus-council.xyz;
    
    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## n8n API Configuration

Once n8n is running, we'll need:

1. **API Key**: 
   - Go to Settings > API
   - Generate an API key
   - Save it securely

2. **Enable API**:
   - Settings > API
   - Enable "Public API"
   - Save settings

3. **Test API**:
   ```bash
   curl -X GET https://n8n.olympus-council.xyz/api/v1/workflows \
     -H "X-N8N-API-KEY: your-api-key"
   ```