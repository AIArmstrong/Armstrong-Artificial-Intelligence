#!/usr/bin/expect -f

set timeout 30

spawn ssh root@142.93.74.22

expect {
    "password:" {
        send "\r"
        exp_continue
    }
    "Are you sure you want to continue connecting" {
        send "yes\r"
        exp_continue
    }
    "$ " {
        send "echo 'Connected to droplet. Attempting to restart n8n...'\r"
        
        # Try Docker first
        send "if docker ps | grep -q n8n; then echo 'Found n8n Docker container, restarting...'; docker restart n8n; exit 0; fi\r"
        
        # Try systemctl
        send "if systemctl is-active --quiet n8n; then echo 'Found n8n systemd service, restarting...'; systemctl restart n8n; exit 0; fi\r"
        
        # Try PM2
        send "if command -v pm2 >/dev/null 2>&1 && pm2 list | grep -q n8n; then echo 'Found n8n PM2 process, restarting...'; pm2 restart n8n; exit 0; fi\r"
        
        send "echo 'Could not find n8n service to restart'\r"
        send "exit\r"
    }
    timeout {
        puts "Connection timed out"
        exit 1
    }
    eof {
        puts "Connection closed"
        exit 1
    }
}

expect eof