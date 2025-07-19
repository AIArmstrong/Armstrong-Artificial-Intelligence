#!/usr/bin/env python3
"""
Automatic Data Offloading Protocol for AAI
Monitors folders and automatically offloads data to Supabase when thresholds are met
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    print("⚠️  Supabase client not available. Running in analysis mode only.")
    SUPABASE_AVAILABLE = False

class AutoOffloadProtocol:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/Brandon/AAI")
        self.config = {
            "research": {
                "threshold_mb": 5,  # Offload when research folder > 5MB
                "file_age_days": 7,  # Offload files older than 7 days
                "extensions": [".md", ".txt", ".json"]
            },
            "brain/cache": {
                "threshold_files": 50,  # Offload when > 50 cache files
                "file_age_hours": 24,  # Offload cache older than 24 hours
                "extensions": [".json"]
            },
            "brain/states": {
                "threshold_files": 20,  # Offload when > 20 state files
                "file_age_days": 3,  # Offload states older than 3 days
                "extensions": [".json"]
            },
            "examples": {
                "threshold_mb": 10,  # Offload when examples > 10MB
                "file_age_days": 30,  # Offload examples not used in 30 days
                "extensions": [".py", ".js", ".md"]
            },
            "brain/logs/rule-compliance.log": {
                "threshold_mb": 1,  # Offload when rule-compliance.log > 1MB
                "file_age_days": 7,  # Offload entries older than 7 days
                "preserve_recent_days": 3,  # Keep last 3 days locally
                "type": "jsonl"  # JSON Lines format
            }
        }
        
    def check_offload_conditions(self) -> Dict[str, Any]:
        """Check which folders meet offload conditions"""
        offload_needed = {}
        
        for folder, config in self.config.items():
            # Handle specific files like rule-compliance.log
            if folder.endswith('.log'):
                file_path = self.base_path / folder
                if not file_path.exists():
                    continue
                    
                file_size_mb = file_path.stat().st_size / 1024 / 1024
                size_threshold = config.get("threshold_mb", float('inf'))
                
                if file_size_mb > size_threshold:
                    offload_needed[folder] = {
                        "reason": f"Size: {file_size_mb:.2f}MB > {size_threshold}MB",
                        "size_mb": file_size_mb,
                        "file_count": 1,
                        "config": config,
                        "type": "file"
                    }
                continue
                
            # Handle folders
            folder_path = self.base_path / folder
            if not folder_path.exists():
                continue
                
            # Calculate folder size and file count
            files = list(folder_path.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            folder_size_mb = sum(f.stat().st_size for f in files if f.is_file()) / 1024 / 1024
            
            # Check thresholds
            size_threshold = config.get("threshold_mb", float('inf'))
            file_threshold = config.get("threshold_files", float('inf'))
            
            if folder_size_mb > size_threshold or file_count > file_threshold:
                offload_needed[folder] = {
                    "reason": f"Size: {folder_size_mb:.2f}MB > {size_threshold}MB" 
                             if folder_size_mb > size_threshold 
                             else f"Files: {file_count} > {file_threshold}",
                    "size_mb": folder_size_mb,
                    "file_count": file_count,
                    "config": config,
                    "type": "folder"
                }
                
        return offload_needed
    
    def generate_offload_manifest(self) -> Dict[str, Any]:
        """Generate manifest of files to offload"""
        conditions = self.check_offload_conditions()
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "offload_tasks": []
        }
        
        for folder, info in conditions.items():
            folder_path = self.base_path / folder
            files_to_offload = []
            
            # Get age threshold
            if "hours" in str(info['config'].get('file_age_hours', '')):
                age_seconds = info['config']['file_age_hours'] * 3600
            else:
                age_seconds = info['config'].get('file_age_days', 30) * 86400
            
            current_time = datetime.now().timestamp()
            
            # Find files matching criteria
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in info['config']['extensions']:
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > age_seconds:
                        files_to_offload.append({
                            "path": str(file_path.relative_to(self.base_path)),
                            "size_kb": file_path.stat().st_size / 1024,
                            "age_days": file_age / 86400,
                            "last_modified": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat()
                        })
            
            if files_to_offload:
                manifest["offload_tasks"].append({
                    "folder": folder,
                    "reason": info["reason"],
                    "files": files_to_offload,
                    "total_files": len(files_to_offload),
                    "total_size_mb": sum(f["size_kb"] for f in files_to_offload) / 1024
                })
                
        return manifest
    
    def upload_rule_compliance_to_supabase(self, log_file_path: Path) -> bool:
        """Upload rule-compliance.log entries to Supabase"""
        
        if not SUPABASE_AVAILABLE:
            print("❌ Supabase client not available. Cannot upload rule compliance data.")
            return False
        
        # Load environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Error: SUPABASE_URL or SUPABASE_ANON_KEY not found in environment")
            return False
        
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Load rule compliance entries
        entries = []
        cutoff_date = datetime.now() - timedelta(days=7)
        
        try:
            with open(log_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            # Parse timestamp and check if older than 7 days
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                            if entry_time < cutoff_date:
                                entries.append(entry)
                        except (json.JSONDecodeError, ValueError, KeyError) as e:
                            print(f"Warning: Could not parse line: {line} - {e}")
        except Exception as e:
            print(f"❌ Error reading rule compliance log: {e}")
            return False
        
        if not entries:
            print("✅ No rule compliance entries older than 7 days found")
            return True
        
        # Upload entries in batches
        batch_size = 100
        total_uploaded = 0
        
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            
            # Transform entries for Supabase
            supabase_entries = []
            for entry in batch:
                supabase_entry = {
                    'timestamp': entry.get('timestamp'),
                    'session_id': entry.get('session_id'),
                    'rule_id': entry.get('rule_id'),
                    'status': entry.get('status'),
                    'details': entry.get('details'),
                    'tool': entry.get('tool'),
                    'phase': entry.get('phase', 'unknown')
                }
                supabase_entries.append(supabase_entry)
            
            try:
                response = supabase.table('aai_rule_compliance').insert(supabase_entries).execute()
                total_uploaded += len(batch)
                print(f"✅ Uploaded rule compliance batch {i//batch_size + 1}: {len(batch)} entries")
            except Exception as e:
                print(f"❌ Error uploading rule compliance batch {i//batch_size + 1}: {e}")
                return False
        
        print(f"🎉 Rule compliance upload complete! Total entries uploaded: {total_uploaded}")
        return True
    
    def archive_old_rule_compliance_entries(self, log_file_path: Path) -> bool:
        """Archive old rule compliance entries locally after Supabase upload"""
        
        preserve_days = self.config['brain/logs/rule-compliance.log']['preserve_recent_days']
        cutoff_date = datetime.now() - timedelta(days=preserve_days)
        
        # Read current entries
        recent_entries = []
        old_entries = []
        
        try:
            with open(log_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                            
                            if entry_time >= cutoff_date:
                                recent_entries.append(line)
                            else:
                                old_entries.append(line)
                        except (json.JSONDecodeError, ValueError, KeyError):
                            # Keep malformed entries for manual review
                            recent_entries.append(line)
        except Exception as e:
            print(f"❌ Error reading rule compliance log: {e}")
            return False
        
        # Write back only recent entries
        try:
            with open(log_file_path, 'w') as f:
                for entry in recent_entries:
                    f.write(entry + '\n')
            
            print(f"✅ Archived {len(old_entries)} old rule compliance entries")
            print(f"📋 Kept {len(recent_entries)} recent entries (last {preserve_days} days)")
            return True
            
        except Exception as e:
            print(f"❌ Error writing rule compliance log: {e}")
            return False
    
    def create_offload_script(self):
        """Create SQL script for offloading data"""
        manifest = self.generate_offload_manifest()
        
        if not manifest["offload_tasks"]:
            print("✅ No data meets offload criteria at this time")
            return
            
        # Save manifest
        manifest_file = self.base_path / "supabase_offload_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        print(f"📋 Offload manifest created: {manifest_file}")
        
        # Create follow-up actions
        actions_file = self.base_path / "supabase_offload_actions.md"
        with open(actions_file, 'w') as f:
            f.write("# Supabase Data Offload Actions\n\n")
            f.write(f"Generated: {manifest['timestamp']}\n\n")
            
            for task in manifest["offload_tasks"]:
                f.write(f"## {task['folder']}\n")
                f.write(f"- **Reason**: {task['reason']}\n")
                f.write(f"- **Files**: {task['total_files']}\n")
                f.write(f"- **Size**: {task['total_size_mb']:.2f} MB\n\n")
                
                f.write("### Actions Required:\n")
                f.write("1. Run migration script to upload files to Supabase\n")
                f.write("2. Generate embeddings for searchability\n")
                f.write("3. Update local references to point to Supabase\n")
                f.write("4. Archive or remove local files after verification\n\n")
        
        print(f"📝 Action plan created: {actions_file}")
        
        return manifest

if __name__ == "__main__":
    print("🔄 AAI Auto-Offload Protocol\n")
    
    protocol = AutoOffloadProtocol()
    
    # Check current conditions
    conditions = protocol.check_offload_conditions()
    
    if conditions:
        print("📊 Folders/Files meeting offload criteria:")
        for folder, info in conditions.items():
            print(f"  - {folder}: {info['reason']}")
            
            # Handle rule-compliance.log specifically
            if folder == "brain/logs/rule-compliance.log":
                log_file_path = protocol.base_path / folder
                print(f"\n🛡️  Processing rule-compliance.log archival...")
                
                # Upload to Supabase first
                if protocol.upload_rule_compliance_to_supabase(log_file_path):
                    print("✅ Rule compliance data uploaded to Supabase successfully")
                    
                    # Archive old entries locally
                    if protocol.archive_old_rule_compliance_entries(log_file_path):
                        print("✅ Local rule compliance log archived successfully")
                        print("🔍 Recent entries preserved for quick access")
                    else:
                        print("❌ Failed to archive local rule compliance entries")
                else:
                    print("❌ Failed to upload rule compliance data to Supabase")
                    print("🚨 Local data NOT archived for safety")
                
                print()
    else:
        print("✅ No folders/files currently meet offload criteria")
    
    print("\n" + "="*50 + "\n")
    
    # Generate offload plan for other files
    manifest = protocol.create_offload_script()
    
    if manifest and manifest.get("offload_tasks"):
        print(f"\n📈 Additional Offload Summary:")
        total_files = sum(t["total_files"] for t in manifest["offload_tasks"])
        total_size = sum(t["total_size_mb"] for t in manifest["offload_tasks"])
        print(f"- Total files to offload: {total_files}")
        print(f"- Total size: {total_size:.2f} MB")
    
    print("\n🔧 Auto-offload protocol configured and ready!")