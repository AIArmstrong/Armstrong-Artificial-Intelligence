#!/usr/bin/env python3
"""Test Supabase PostgreSQL connection and analyze usage"""

import os
import psycopg2
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

def test_connection():
    """Test PostgreSQL connection to Supabase"""
    try:
        # Get connection details from environment
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        
        print("✅ Successfully connected to Supabase PostgreSQL!")
        
        # Get cursor
        cur = conn.cursor()
        
        # Test query - get database size
        cur.execute("""
            SELECT 
                pg_database_size(current_database()) as db_size,
                pg_size_pretty(pg_database_size(current_database())) as db_size_pretty
        """)
        
        db_info = cur.fetchone()
        print(f"📊 Database size: {db_info[1]}")
        
        # List all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        print(f"\n📋 Found {len(tables)} tables:")
        for table in tables:
            # Get table size
            cur.execute(f"""
                SELECT 
                    pg_size_pretty(pg_total_relation_size('{table[0]}')) as size,
                    (SELECT COUNT(*) FROM {table[0]}) as row_count
            """)
            table_info = cur.fetchone()
            print(f"  - {table[0]}: {table_info[0]}, {table_info[1]} rows")
        
        # Close connection
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def analyze_supabase_usage():
    """Analyze which parts of codebase use Supabase"""
    print("\n🔍 Analyzing Supabase usage in codebase...")
    
    supabase_files = []
    base_path = Path("/mnt/c/Users/Brandon/AAI")
    
    # Search patterns
    patterns = [
        "supabase", "SUPABASE", "DB_", "DATABASE_URL", 
        "psycopg", "postgresql", "brain_cache", "cache_entries"
    ]
    
    # Scan Python files
    for py_file in base_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            for pattern in patterns:
                if pattern in content:
                    supabase_files.append(str(py_file.relative_to(base_path)))
                    break
        except:
            pass
    
    print(f"\n📁 Files using Supabase ({len(supabase_files)} found):")
    for file in sorted(supabase_files):
        print(f"  - {file}")
    
    return supabase_files

def memory_report():
    """Generate memory and capacity report"""
    print("\n💾 Memory & Capacity Report:")
    
    # Count files and calculate sizes
    base_path = Path("/mnt/c/Users/Brandon/AAI")
    
    folder_stats = {}
    total_size = 0
    total_files = 0
    
    for folder in ['brain', 'research', 'docs', 'examples', 'projects', 'ideas', 'PRPs']:
        folder_path = base_path / folder
        if folder_path.exists():
            files = list(folder_path.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            folder_size = sum(f.stat().st_size for f in files if f.is_file())
            folder_stats[folder] = {
                'files': file_count,
                'size': folder_size,
                'size_mb': round(folder_size / 1024 / 1024, 2)
            }
            total_size += folder_size
            total_files += file_count
    
    print(f"\n📊 Local Storage Usage:")
    print(f"Total files: {total_files}")
    print(f"Total size: {round(total_size / 1024 / 1024, 2)} MB")
    
    print(f"\n📁 Folder breakdown:")
    for folder, stats in folder_stats.items():
        print(f"  {folder}/: {stats['files']} files, {stats['size_mb']} MB")
    
    # Estimate what could be offloaded
    print(f"\n🚀 Offload Recommendations:")
    if folder_stats.get('research', {}).get('size_mb', 0) > 10:
        print(f"  - research/: {folder_stats['research']['size_mb']} MB of scraped docs → Supabase")
    if folder_stats.get('brain', {}).get('files', 0) > 100:
        print(f"  - brain/cache/: Ephemeral data → Supabase cache tables")
    print(f"  - brain/states/: Conversation history → Supabase for persistence")
    print(f"  - examples/: Code snippets → Supabase with embeddings for search")

if __name__ == "__main__":
    print("🔌 Testing Supabase Connection...\n")
    
    # Test connection
    connected = test_connection()
    
    # Analyze usage
    if connected:
        analyze_supabase_usage()
    
    # Memory report
    memory_report()