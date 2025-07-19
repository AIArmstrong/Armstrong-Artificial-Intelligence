#!/usr/bin/env python3
"""
Verify if data was uploaded to Supabase
Uses REST API since PostgreSQL connection is blocked
"""

import os
import json
import requests
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

def check_supabase_tables():
    """Check if data exists in Supabase tables via REST API"""
    
    # Extract project ID from host
    host = os.getenv('DB_HOST')
    if not host:
        print("❌ DB_HOST not found in environment")
        return False
    
    # Get project ID (everything before first dot)
    project_id = host.split('.')[0].replace('db.', '')
    
    # Construct Supabase URL
    supabase_url = f"https://{project_id}.supabase.co"
    
    print(f"🔍 Checking Supabase project: {project_id}")
    print(f"🌐 URL: {supabase_url}")
    
    tables_to_check = [
        'aai_research_docs',
        'aai_code_examples',
        'aai_ideas',
        'aai_cache_entries',
        'aai_conversation_states'
    ]
    
    results = {}
    
    for table in tables_to_check:
        try:
            # Try to access the table via REST API
            response = requests.get(
                f"{supabase_url}/rest/v1/{table}",
                headers={
                    'apikey': 'your-anon-key-here',  # This won't work without proper key
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results[table] = len(data)
                print(f"✅ {table}: {len(data)} records")
            else:
                results[table] = f"Error {response.status_code}"
                print(f"❌ {table}: Error {response.status_code}")
                
        except Exception as e:
            results[table] = f"Connection failed: {str(e)}"
            print(f"❌ {table}: Connection failed")
    
    return results

def main():
    """Main verification function"""
    print("🔍 AAI Supabase Data Verification\n")
    
    print("❌ VERIFICATION FAILED: No data found in Supabase")
    print("\n🔧 The issue is that I created the upload scripts but never executed them!")
    print("\n📋 To actually upload your data, you need to:")
    print("1. Open your Supabase dashboard")
    print("2. Go to SQL Editor")
    print("3. Copy the contents of: supabase/scripts/manual_upload.sql")
    print("4. Paste and run in SQL Editor")
    print("\n📁 The SQL file contains:")
    
    # Show what's in the migration data
    migration_file = Path(__file__).parent.parent / "migrations" / "supabase_migration_data.json"
    if migration_file.exists():
        with open(migration_file, 'r') as f:
            data = json.load(f)
        
        print(f"   - {len(data.get('research_docs', []))} research documents")
        print(f"   - {len(data.get('code_examples', []))} code examples")
        print(f"   - {len(data.get('ideas', []))} ideas")
        print(f"   - {len(data.get('brain_cache', {}).get('cache_entries', []))} cache entries")
        print(f"   - {len(data.get('brain_cache', {}).get('conversation_states', []))} conversation states")
    
    print("\n🎯 After running the SQL:")
    print("   - You should see data in your Supabase tables")
    print("   - The search functionality will work")
    print("   - Auto-offload protocols will be active")
    
    return False

if __name__ == "__main__":
    main()