#!/usr/bin/env python3
"""
Comprehensive Supabase connection diagnostics
"""

import os
import socket
import subprocess
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip()

load_env_file()

def test_dns_resolution():
    """Test if we can resolve the hostname"""
    host = os.getenv('DB_HOST')
    print(f"🔍 Testing DNS resolution for: {host}")
    
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolved to: {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def test_port_connectivity():
    """Test if we can connect to the port"""
    host = os.getenv('DB_HOST')
    
    # Test both standard PostgreSQL port and pooled port
    ports_to_test = [5432, 6543]
    
    for port in ports_to_test:
        print(f"🔌 Testing connection to {host}:{port}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ Port {port} is accessible")
                return port
            else:
                print(f"❌ Port {port} is not accessible")
        except Exception as e:
            print(f"❌ Port {port} test failed: {e}")
    
    return None

def test_network_tools():
    """Test with network tools"""
    host = os.getenv('DB_HOST')
    
    print(f"🌐 Testing network connectivity to {host}")
    
    # Test ping
    try:
        result = subprocess.run(['ping', '-c', '1', host], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ping successful")
        else:
            print(f"❌ Ping failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Ping test failed: {e}")
    
    # Test telnet (if available)
    for port in [5432, 6543]:
        try:
            result = subprocess.run(['timeout', '5', 'telnet', host, str(port)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Telnet to port {port} successful")
            else:
                print(f"❌ Telnet to port {port} failed")
        except Exception as e:
            print(f"❌ Telnet test failed: {e}")

def check_firewall_and_wsl():
    """Check potential WSL/Windows firewall issues"""
    print("🔥 Checking WSL/Windows networking...")
    
    # Check if we're in WSL
    try:
        with open('/proc/version', 'r') as f:
            version = f.read()
        if 'Microsoft' in version or 'WSL' in version:
            print("✅ Running in WSL")
            print("💡 WSL networking tips:")
            print("  - Windows firewall might block connections")
            print("  - Try: wsl --shutdown then restart")
            print("  - Check Windows Defender firewall settings")
    except:
        print("❌ Not in WSL or can't determine")
    
    # Check network interface
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        if result.returncode == 0:
            print("🌐 Network routes:")
            for line in result.stdout.split('\n')[:3]:
                if line.strip():
                    print(f"  {line}")
    except:
        print("❌ Can't check network routes")

def print_current_config():
    """Print current configuration"""
    print("📋 Current Supabase Configuration:")
    print(f"  DB_HOST: {os.getenv('DB_HOST')}")
    print(f"  DB_USER: {os.getenv('DB_USER')}")
    print(f"  DB_NAME: {os.getenv('DB_NAME')}")
    print(f"  DB_PORT: {os.getenv('DB_PORT')}")
    print(f"  DATABASE_URL: {os.getenv('DATABASE_URL')[:50]}...")

def main():
    """Run all diagnostics"""
    print("🔧 AAI Supabase Connection Diagnostics\n")
    
    print_current_config()
    print("\n" + "="*60 + "\n")
    
    # Test DNS
    dns_ok = test_dns_resolution()
    print()
    
    # Test port connectivity
    accessible_port = test_port_connectivity()
    print()
    
    # Test network tools
    test_network_tools()
    print()
    
    # Check WSL/firewall
    check_firewall_and_wsl()
    print()
    
    # Recommendations
    print("🎯 RECOMMENDATIONS:")
    
    if not dns_ok:
        print("1. ❌ DNS issue - check your internet connection")
    elif accessible_port:
        print(f"1. ✅ Use port {accessible_port} for connection")
        print(f"2. 🔄 Update DB_PORT={accessible_port} in .env file")
    else:
        print("1. ❌ No accessible ports found")
        print("2. 🔥 Check Windows firewall settings")
        print("3. 🌐 Try connecting from outside WSL")
        print("4. 📞 Contact your network administrator")
    
    print("\n📝 Next steps:")
    print("1. Copy the working connection details from Supabase dashboard")
    print("2. Update your .env file with correct values")
    print("3. Test again with the updated configuration")

if __name__ == "__main__":
    main()