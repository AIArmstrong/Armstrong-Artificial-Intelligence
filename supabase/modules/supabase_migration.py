#!/usr/bin/env python3
"""
Supabase Data Migration Tool
Migrates local AAI data to Supabase for searchability and persistence
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import asyncio
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

class SupabaseMigration:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/Brandon/AAI")
        self.connection_string = os.getenv('DATABASE_URL')
        
    def prepare_research_docs(self) -> List[Dict[str, Any]]:
        """Prepare research documents for migration"""
        docs = []
        research_path = self.base_path / "research"
        
        # Process markdown files in research folder
        for md_file in research_path.rglob("*.md"):
            if "README" not in str(md_file):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    content_hash = hashlib.md5(content.encode()).hexdigest()
                    
                    doc = {
                        "source_file": str(md_file.relative_to(self.base_path)),
                        "title": md_file.stem.replace("-", " ").title(),
                        "content": content,
                        "content_hash": content_hash,
                        "category": self._determine_category(md_file),
                        "metadata": {
                            "file_size": md_file.stat().st_size,
                            "last_modified": md_file.stat().st_mtime
                        }
                    }
                    docs.append(doc)
                except Exception as e:
                    print(f"Error processing {md_file}: {e}")
                    
        print(f"Prepared {len(docs)} research documents for migration")
        return docs
    
    def prepare_code_examples(self) -> List[Dict[str, Any]]:
        """Prepare code examples for migration"""
        examples = []
        examples_path = self.base_path / "examples"
        
        # Process Python files
        for py_file in examples_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Extract description from docstring if present
                description = ""
                if '"""' in content:
                    start = content.find('"""') + 3
                    end = content.find('"""', start)
                    if end > start:
                        description = content[start:end].strip()
                
                example = {
                    "title": py_file.stem.replace("_", " ").title(),
                    "description": description,
                    "code": content,
                    "language": "python",
                    "tags": self._extract_tags(py_file),
                    "category": self._determine_category(py_file),
                    "metadata": {
                        "file_path": str(py_file.relative_to(self.base_path)),
                        "file_size": py_file.stat().st_size
                    }
                }
                examples.append(example)
            except Exception as e:
                print(f"Error processing {py_file}: {e}")
                
        print(f"Prepared {len(examples)} code examples for migration")
        return examples
    
    def prepare_brain_cache(self) -> Dict[str, Any]:
        """Prepare brain cache data for migration"""
        cache_data = {
            "cache_entries": [],
            "conversation_states": []
        }
        
        # Check for existing cache files
        cache_path = self.base_path / "brain" / "cache"
        states_path = self.base_path / "brain" / "states"
        
        # Process cache entries
        if cache_path.exists():
            for json_file in cache_path.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    cache_data["cache_entries"].append({
                        "key": json_file.stem,
                        "value": data,
                        "metadata": {"source": "brain_cache"}
                    })
                except Exception as e:
                    print(f"Error processing cache {json_file}: {e}")
        
        # Process conversation states
        if states_path.exists():
            for json_file in states_path.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    cache_data["conversation_states"].append({
                        "session_id": json_file.stem,
                        "state": data,
                        "context": data.get("context", {})
                    })
                except Exception as e:
                    print(f"Error processing state {json_file}: {e}")
                    
        print(f"Prepared {len(cache_data['cache_entries'])} cache entries and "
              f"{len(cache_data['conversation_states'])} conversation states")
        return cache_data
    
    def prepare_ideas(self) -> List[Dict[str, Any]]:
        """Extract ideas from idea registry"""
        ideas = []
        idea_registry = self.base_path / "ideas" / "idea_registry.md"
        
        if idea_registry.exists():
            content = idea_registry.read_text(encoding='utf-8', errors='ignore')
            
            # Parse lifecycle status table
            if "Current Lifecycle Status" in content:
                # Extract table rows (simple parsing)
                lines = content.split('\n')
                in_table = False
                
                for line in lines:
                    if "| Idea | Stage |" in line:
                        in_table = True
                        continue
                    if in_table and line.startswith("|") and "---" not in line:
                        parts = [p.strip() for p in line.split("|")[1:-1]]
                        if len(parts) >= 5:
                            idea = {
                                "title": parts[0],
                                "stage": self._parse_stage(parts[1]),
                                "next_action": parts[3],
                                "research_ready": "✅" in parts[4],
                                "metadata": {
                                    "last_updated": parts[2],
                                    "source": "idea_registry"
                                }
                            }
                            ideas.append(idea)
                    elif in_table and not line.startswith("|"):
                        break
                        
        print(f"Prepared {len(ideas)} ideas for migration")
        return ideas
    
    def _determine_category(self, file_path: Path) -> str:
        """Determine category based on file path"""
        parts = file_path.parts
        if "research" in parts:
            if "ai-development" in parts:
                return "ai-development"
            elif "validation" in parts:
                return "validation"
            elif "implementation" in parts:
                return "implementation"
            return "research"
        elif "examples" in parts:
            if "tests" in parts:
                return "tests"
            elif "working" in parts:
                return "working"
            return "examples"
        return "general"
    
    def _extract_tags(self, file_path: Path) -> List[str]:
        """Extract tags from file path and content"""
        tags = []
        
        # Add path-based tags
        parts = file_path.parts
        for part in parts:
            if part not in ["AAI", "examples", "brain", "research"]:
                tags.append(part)
                
        # Add file type tag
        tags.append(file_path.suffix[1:])
        
        return list(set(tags))
    
    def _parse_stage(self, stage_text: str) -> str:
        """Parse stage from emoji representation"""
        stage_map = {
            "🌱": "seed",
            "🌿": "sprout", 
            "🌳": "growth",
            "🍎": "fruit",
            "🌰": "harvest",
            "🍂": "archive"
        }
        
        for emoji, stage in stage_map.items():
            if emoji in stage_text:
                return stage
        return "seed"
    
    def generate_migration_script(self):
        """Generate migration data as JSON for manual execution"""
        migration_data = {
            "timestamp": datetime.now().isoformat(),
            "research_docs": self.prepare_research_docs(),
            "code_examples": self.prepare_code_examples(),
            "brain_cache": self.prepare_brain_cache(),
            "ideas": self.prepare_ideas()
        }
        
        # Save to file
        output_file = self.base_path / "supabase_migration_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(migration_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ Migration data prepared: {output_file}")
        print("\nNext steps:")
        print("1. Run setup_supabase_schema.sql in Supabase SQL Editor")
        print("2. Use the migration data to populate tables")
        print("3. Set up embeddings using OpenRouter API")
        
        return migration_data

if __name__ == "__main__":
    print("🚀 AAI Supabase Migration Tool\n")
    
    migrator = SupabaseMigration()
    migration_data = migrator.generate_migration_script()
    
    print(f"\n📊 Migration Summary:")
    print(f"- Research documents: {len(migration_data['research_docs'])}")
    print(f"- Code examples: {len(migration_data['code_examples'])}")
    print(f"- Cache entries: {len(migration_data['brain_cache']['cache_entries'])}")
    print(f"- Conversation states: {len(migration_data['brain_cache']['conversation_states'])}")
    print(f"- Ideas: {len(migration_data['ideas'])}")