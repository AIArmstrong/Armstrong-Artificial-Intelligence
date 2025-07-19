#!/usr/bin/env python3
"""
Upload AAI migration data to Supabase
Requires: pip install psycopg2-binary
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
import sys

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def connect_to_supabase():
    """Connect to Supabase PostgreSQL database"""
    try:
        # Get connection details from environment
        connection_string = os.getenv('DATABASE_URL')
        if not connection_string:
            # Fallback to individual variables
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                port=os.getenv('DB_PORT', 5432)
            )
        else:
            conn = psycopg2.connect(connection_string)
        
        print("✅ Connected to Supabase successfully!")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def upload_research_docs(conn, docs):
    """Upload research documents to aai_research_docs table"""
    cur = conn.cursor()
    
    uploaded = 0
    for doc in docs:
        try:
            cur.execute("""
                INSERT INTO aai_research_docs 
                (source_file, title, content, content_hash, category, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (content_hash) DO UPDATE SET
                    title = EXCLUDED.title,
                    content = EXCLUDED.content,
                    metadata = EXCLUDED.metadata,
                    updated_at = NOW()
            """, (
                doc.get('source_file'),
                doc.get('title'),
                doc.get('content'),
                doc.get('content_hash'),
                doc.get('category'),
                json.dumps(doc.get('metadata', {}))
            ))
            uploaded += 1
        except Exception as e:
            print(f"Error uploading research doc {doc.get('title')}: {e}")
    
    conn.commit()
    cur.close()
    print(f"📄 Uploaded {uploaded} research documents")
    return uploaded

def upload_code_examples(conn, examples):
    """Upload code examples to aai_code_examples table"""
    cur = conn.cursor()
    
    uploaded = 0
    for example in examples:
        try:
            cur.execute("""
                INSERT INTO aai_code_examples 
                (title, description, code, language, tags, category, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                example.get('title'),
                example.get('description'),
                example.get('code'),
                example.get('language'),
                example.get('tags', []),
                example.get('category'),
                json.dumps(example.get('metadata', {}))
            ))
            uploaded += 1
        except Exception as e:
            print(f"Error uploading code example {example.get('title')}: {e}")
    
    conn.commit()
    cur.close()
    print(f"💻 Uploaded {uploaded} code examples")
    return uploaded

def upload_cache_entries(conn, cache_data):
    """Upload cache entries and conversation states"""
    cur = conn.cursor()
    
    # Upload cache entries
    cache_uploaded = 0
    for entry in cache_data.get('cache_entries', []):
        try:
            cur.execute("""
                INSERT INTO aai_cache_entries (key, value, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (key) DO UPDATE SET
                    value = EXCLUDED.value,
                    metadata = EXCLUDED.metadata,
                    updated_at = NOW(),
                    accessed_at = NOW(),
                    access_count = aai_cache_entries.access_count + 1
            """, (
                entry.get('key'),
                json.dumps(entry.get('value')),
                json.dumps(entry.get('metadata', {}))
            ))
            cache_uploaded += 1
        except Exception as e:
            print(f"Error uploading cache entry {entry.get('key')}: {e}")
    
    # Upload conversation states
    states_uploaded = 0
    for state in cache_data.get('conversation_states', []):
        try:
            cur.execute("""
                INSERT INTO aai_conversation_states (session_id, state, context)
                VALUES (%s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE SET
                    state = EXCLUDED.state,
                    context = EXCLUDED.context,
                    updated_at = NOW(),
                    last_interaction = NOW()
            """, (
                state.get('session_id'),
                json.dumps(state.get('state')),
                json.dumps(state.get('context', {}))
            ))
            states_uploaded += 1
        except Exception as e:
            print(f"Error uploading conversation state {state.get('session_id')}: {e}")
    
    conn.commit()
    cur.close()
    print(f"🧠 Uploaded {cache_uploaded} cache entries and {states_uploaded} conversation states")
    return cache_uploaded + states_uploaded

def upload_ideas(conn, ideas):
    """Upload ideas to aai_ideas table"""
    cur = conn.cursor()
    
    uploaded = 0
    for idea in ideas:
        try:
            cur.execute("""
                INSERT INTO aai_ideas 
                (title, stage, next_action, research_ready, metadata)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                idea.get('title'),
                idea.get('stage'),
                idea.get('next_action'),
                idea.get('research_ready', False),
                json.dumps(idea.get('metadata', {}))
            ))
            uploaded += 1
        except Exception as e:
            print(f"Error uploading idea {idea.get('title')}: {e}")
    
    conn.commit()
    cur.close()
    print(f"💡 Uploaded {uploaded} ideas")
    return uploaded

def main():
    """Main upload function"""
    print("🚀 AAI Supabase Data Upload\n")
    
    # Load migration data
    migration_file = Path(__file__).parent.parent / "migrations" / "supabase_migration_data.json"
    
    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_data = json.load(f)
    
    print(f"📋 Loading migration data from {migration_file}")
    
    # Connect to database
    conn = connect_to_supabase()
    if not conn:
        print("❌ Cannot proceed without database connection")
        return
    
    try:
        # Upload each data type
        total_uploaded = 0
        
        if migration_data.get('research_docs'):
            total_uploaded += upload_research_docs(conn, migration_data['research_docs'])
        
        if migration_data.get('code_examples'):
            total_uploaded += upload_code_examples(conn, migration_data['code_examples'])
        
        if migration_data.get('brain_cache'):
            total_uploaded += upload_cache_entries(conn, migration_data['brain_cache'])
        
        if migration_data.get('ideas'):
            total_uploaded += upload_ideas(conn, migration_data['ideas'])
        
        print(f"\n✅ Upload complete! Total records uploaded: {total_uploaded}")
        
        # Verify upload by counting records
        cur = conn.cursor()
        tables = [
            'aai_research_docs',
            'aai_code_examples', 
            'aai_cache_entries',
            'aai_conversation_states',
            'aai_ideas'
        ]
        
        print("\n📊 Database counts after upload:")
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  {table}: {count} records")
        
        cur.close()
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()