#!/usr/bin/env python3
"""
Setup OpenRouter embeddings for semantic search
Generates embeddings for existing content in Supabase
"""

import os
import json
import requests
from pathlib import Path
import time

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

class OpenRouterEmbeddings:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "text-embedding-ada-002"  # 1536 dimensions
        
    def generate_embedding(self, text):
        """Generate embedding for text using OpenRouter"""
        try:
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "input": text
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['data'][0]['embedding']
            else:
                print(f"❌ Embedding API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Embedding generation failed: {e}")
            return None
    
    def generate_embeddings_for_migration_data(self):
        """Generate embeddings for all migration data"""
        # Load migration data
        migration_file = Path(__file__).parent.parent / "migrations" / "supabase_migration_data.json"
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_data = json.load(f)
        
        embeddings_data = {
            "timestamp": time.time(),
            "model": self.model,
            "research_docs": [],
            "code_examples": [],
            "ideas": []
        }
        
        print("🔗 Generating embeddings for research documents...")
        for doc in migration_data.get('research_docs', []):
            text = f"{doc.get('title', '')} {doc.get('content', '')}"
            embedding = self.generate_embedding(text)
            if embedding:
                embeddings_data['research_docs'].append({
                    "title": doc.get('title'),
                    "content_hash": doc.get('content_hash'),
                    "embedding": embedding
                })
                print(f"  ✅ {doc.get('title')[:50]}...")
                time.sleep(0.1)  # Rate limiting
        
        print("💻 Generating embeddings for code examples...")
        for example in migration_data.get('code_examples', []):
            text = f"{example.get('title', '')} {example.get('description', '')} {example.get('code', '')}"
            embedding = self.generate_embedding(text)
            if embedding:
                embeddings_data['code_examples'].append({
                    "title": example.get('title'),
                    "embedding": embedding
                })
                print(f"  ✅ {example.get('title')[:50]}...")
                time.sleep(0.1)
        
        print("💡 Generating embeddings for ideas...")
        for idea in migration_data.get('ideas', []):
            text = f"{idea.get('title', '')} {idea.get('next_action', '')}"
            embedding = self.generate_embedding(text)
            if embedding:
                embeddings_data['ideas'].append({
                    "title": idea.get('title'),
                    "embedding": embedding
                })
                print(f"  ✅ {idea.get('title')[:50]}...")
                time.sleep(0.1)
        
        # Save embeddings
        output_file = Path(__file__).parent.parent / "migrations" / "embeddings_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings_data, f, indent=2)
        
        print(f"\n✅ Embeddings saved to: {output_file}")
        return embeddings_data
    
    def generate_embedding_update_sql(self, embeddings_data):
        """Generate SQL to update embeddings in Supabase"""
        sql_content = """-- Update embeddings in Supabase
-- Generated from embeddings_data.json

"""
        
        # Research documents
        sql_content += "-- Update research document embeddings\n"
        for doc in embeddings_data.get('research_docs', []):
            embedding_str = '[' + ','.join(map(str, doc['embedding'])) + ']'
            sql_content += f"""UPDATE aai_research_docs 
SET embedding = '{embedding_str}'::vector 
WHERE content_hash = '{doc['content_hash']}';

"""
        
        # Code examples
        sql_content += "-- Update code example embeddings\n"
        for example in embeddings_data.get('code_examples', []):
            embedding_str = '[' + ','.join(map(str, example['embedding'])) + ']'
            sql_content += f"""UPDATE aai_code_examples 
SET embedding = '{embedding_str}'::vector 
WHERE title = '{example['title'].replace("'", "''")}';

"""
        
        # Save SQL file
        output_file = Path(__file__).parent / "update_embeddings.sql"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print(f"📝 SQL file generated: {output_file}")
        return output_file

def main():
    """Main embeddings setup function"""
    print("🔗 AAI OpenRouter Embeddings Setup\n")
    
    embeddings = OpenRouterEmbeddings()
    
    if not embeddings.api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print(f"🔑 Using OpenRouter API key: {embeddings.api_key[:20]}...")
    print(f"📊 Model: {embeddings.model}")
    
    # Generate embeddings
    embeddings_data = embeddings.generate_embeddings_for_migration_data()
    
    # Generate SQL for updating embeddings
    sql_file = embeddings.generate_embedding_update_sql(embeddings_data)
    
    print(f"\n📋 Summary:")
    print(f"- Research docs: {len(embeddings_data['research_docs'])} embeddings")
    print(f"- Code examples: {len(embeddings_data['code_examples'])} embeddings")
    print(f"- Ideas: {len(embeddings_data['ideas'])} embeddings")
    
    print(f"\n🎯 Next steps:")
    print(f"1. Upload your data using manual_upload.sql")
    print(f"2. Run update_embeddings.sql to add semantic search")
    print(f"3. Test semantic search with supabase_search.py")

if __name__ == "__main__":
    main()