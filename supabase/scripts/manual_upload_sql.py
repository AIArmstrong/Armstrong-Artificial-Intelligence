#!/usr/bin/env python3
"""
Generate SQL INSERT statements for manual upload to Supabase
Use this when direct connection isn't available
"""

import json
import hashlib
from pathlib import Path

def escape_sql_string(s):
    """Escape string for SQL"""
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''").replace("\\", "\\\\") + "'"

def generate_research_docs_sql(docs):
    """Generate SQL for research documents"""
    sql = "-- Research Documents\n"
    
    for doc in docs:
        sql += f"""INSERT INTO aai_research_docs 
(source_file, title, content, content_hash, category, metadata) 
VALUES (
    {escape_sql_string(doc.get('source_file'))},
    {escape_sql_string(doc.get('title'))},
    {escape_sql_string(doc.get('content'))},
    {escape_sql_string(doc.get('content_hash'))},
    {escape_sql_string(doc.get('category'))},
    {escape_sql_string(json.dumps(doc.get('metadata', {})))}
);

"""
    return sql

def generate_code_examples_sql(examples):
    """Generate SQL for code examples"""
    sql = "-- Code Examples\n"
    
    for example in examples:
        tags_str = '{' + ','.join(f'"{tag}"' for tag in example.get('tags', [])) + '}'
        
        sql += f"""INSERT INTO aai_code_examples 
(title, description, code, language, tags, category, metadata) 
VALUES (
    {escape_sql_string(example.get('title'))},
    {escape_sql_string(example.get('description'))},
    {escape_sql_string(example.get('code'))},
    {escape_sql_string(example.get('language'))},
    '{tags_str}',
    {escape_sql_string(example.get('category'))},
    {escape_sql_string(json.dumps(example.get('metadata', {})))}
);

"""
    return sql

def generate_ideas_sql(ideas):
    """Generate SQL for ideas"""
    sql = "-- Ideas\n"
    
    for idea in ideas:
        sql += f"""INSERT INTO aai_ideas 
(title, stage, next_action, research_ready, metadata) 
VALUES (
    {escape_sql_string(idea.get('title'))},
    {escape_sql_string(idea.get('stage'))},
    {escape_sql_string(idea.get('next_action'))},
    {str(idea.get('research_ready', False)).lower()},
    {escape_sql_string(json.dumps(idea.get('metadata', {})))}
);

"""
    return sql

def generate_cache_sql(cache_data):
    """Generate SQL for cache entries and conversation states"""
    sql = "-- Cache Entries\n"
    
    for entry in cache_data.get('cache_entries', []):
        sql += f"""INSERT INTO aai_cache_entries (key, value, metadata) 
VALUES (
    {escape_sql_string(entry.get('key'))},
    {escape_sql_string(json.dumps(entry.get('value')))},
    {escape_sql_string(json.dumps(entry.get('metadata', {})))}
);

"""
    
    sql += "-- Conversation States\n"
    for state in cache_data.get('conversation_states', []):
        sql += f"""INSERT INTO aai_conversation_states (session_id, state, context) 
VALUES (
    {escape_sql_string(state.get('session_id'))},
    {escape_sql_string(json.dumps(state.get('state')))},
    {escape_sql_string(json.dumps(state.get('context', {})))}
);

"""
    return sql

def main():
    """Generate SQL file for manual upload"""
    print("📝 Generating manual upload SQL file...")
    
    # Load migration data
    migration_file = Path(__file__).parent.parent / "migrations" / "supabase_migration_data.json"
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_data = json.load(f)
    
    # Generate SQL
    sql_content = """-- AAI Supabase Manual Upload
-- Generated from migration data
-- Copy and paste this into Supabase SQL Editor

"""
    
    if migration_data.get('research_docs'):
        sql_content += generate_research_docs_sql(migration_data['research_docs'])
    
    if migration_data.get('code_examples'):
        sql_content += generate_code_examples_sql(migration_data['code_examples'])
    
    if migration_data.get('ideas'):
        sql_content += generate_ideas_sql(migration_data['ideas'])
    
    if migration_data.get('brain_cache'):
        sql_content += generate_cache_sql(migration_data['brain_cache'])
    
    # Save SQL file
    output_file = Path(__file__).parent / "manual_upload.sql"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"✅ SQL file generated: {output_file}")
    print("\nTo upload data:")
    print("1. Open Supabase SQL Editor")
    print("2. Copy and paste the contents of manual_upload.sql")
    print("3. Run the SQL commands")
    
    # Generate summary
    print(f"\n📊 Data Summary:")
    print(f"- Research documents: {len(migration_data.get('research_docs', []))}")
    print(f"- Code examples: {len(migration_data.get('code_examples', []))}")
    print(f"- Ideas: {len(migration_data.get('ideas', []))}")
    print(f"- Cache entries: {len(migration_data.get('brain_cache', {}).get('cache_entries', []))}")
    print(f"- Conversation states: {len(migration_data.get('brain_cache', {}).get('conversation_states', []))}")

if __name__ == "__main__":
    main()