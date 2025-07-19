#!/usr/bin/env python3
"""
Test Supabase connection with multiple fallback methods
"""

import os
import sys
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

def test_with_psycopg2():
    """Test with psycopg2 (direct PostgreSQL)"""
    try:
        import psycopg2
        
        print("🔌 Testing psycopg2 connection...")
        
        # Method 1: DATABASE_URL
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            print("✅ Connected via DATABASE_URL")
            
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"📊 PostgreSQL version: {version[:50]}...")
            
            # Test table existence
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'aai_%';")
            tables = cur.fetchall()
            print(f"📋 Found {len(tables)} AAI tables")
            
            cur.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ DATABASE_URL failed: {e}")
            
        # Method 2: Individual parameters
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                port=int(os.getenv('DB_PORT', 5432))
            )
            print("✅ Connected via individual parameters")
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Individual parameters failed: {e}")
            
        return False
        
    except ImportError:
        print("❌ psycopg2 not available")
        return False

def test_with_supabase_client():
    """Test with Supabase Python client"""
    try:
        from supabase import create_client, Client
        
        print("🔌 Testing Supabase client connection...")
        
        url = f"https://{os.getenv('DB_HOST').replace('db.', '')}"
        # This would need the anon key, which we don't have set up
        print(f"📍 Would connect to: {url}")
        print("⚠️  Supabase client needs anon key setup")
        return False
        
    except ImportError:
        print("❌ Supabase client not available")
        return False

def test_with_requests():
    """Test with HTTP requests to Supabase REST API"""
    try:
        import requests
        
        print("🔌 Testing HTTP API connection...")
        
        base_url = f"https://{os.getenv('DB_HOST').replace('db.', '')}"
        response = requests.get(f"{base_url}/rest/v1/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Supabase REST API reachable")
            return True
        else:
            print(f"❌ HTTP API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ HTTP API failed: {e}")
        return False

def main():
    """Test all connection methods"""
    print("🚀 AAI Supabase Connection Testing\n")
    
    print("🔧 Environment variables:")
    print(f"  DB_HOST: {os.getenv('DB_HOST')}")
    print(f"  DB_USER: {os.getenv('DB_USER')}")
    print(f"  DB_NAME: {os.getenv('DB_NAME')}")
    print(f"  DB_PORT: {os.getenv('DB_PORT')}")
    print(f"  DATABASE_URL: {os.getenv('DATABASE_URL')[:50]}...")
    print()
    
    success_count = 0
    
    # Test psycopg2
    if test_with_psycopg2():
        success_count += 1
    print()
    
    # Test Supabase client
    if test_with_supabase_client():
        success_count += 1
    print()
    
    # Test HTTP API
    if test_with_requests():
        success_count += 1
    print()
    
    print(f"📊 Connection test results: {success_count}/3 methods successful")
    
    if success_count == 0:
        print("\n🔧 Troubleshooting suggestions:")
        print("1. Check if you're connected to the internet")
        print("2. Verify Supabase project is running")
        print("3. Check if PostgreSQL port 5432 is accessible")
        print("4. Try using the manual SQL upload instead")
        print("5. Check Windows firewall/antivirus settings")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)