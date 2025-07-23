"""
Safety Mechanisms for Code Improvements

Provides preview modes, rollback capabilities, and safe file modification.
"""

import os
import shutil
import tempfile
import hashlib
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
import logging

from .models import ImprovementRecommendation, QualityMetrics
from .config import SAFETY_CHECKS, get_config

logger = logging.getLogger(__name__)

class SafetyMechanisms:
    """
    Implements safety mechanisms for code improvements including:
    - Preview mode for changes
    - Atomic file modifications
    - Rollback capabilities
    - Backup and restore functionality
    """
    
    def __init__(self):
        self.safety_config = SAFETY_CHECKS
        self.backup_dir = Path("brain/logs/improvements/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.active_session = None
        self.changes_log = []
    
    @contextmanager
    def safe_modification_session(self, session_id: str):
        """
        Context manager for safe file modifications.
        Ensures all changes can be rolled back if needed.
        """
        self.active_session = {
            "id": session_id,
            "start_time": datetime.now(),
            "backups": {},
            "changes": [],
            "rolled_back": False
        }
        
        try:
            yield self
        except Exception as e:
            logger.error(f"Error during modification session: {str(e)}")
            self.rollback_session()
            raise
        finally:
            if not self.active_session["rolled_back"]:
                self.finalize_session()
    
    def preview_changes(self, 
                       file_path: str,
                       original_content: str,
                       modified_content: str,
                       recommendation: Optional[ImprovementRecommendation] = None) -> Dict[str, Any]:
        """
        Generate a preview of changes without applying them.
        
        Returns:
            Dictionary with preview information including diff, stats, and visualization
        """
        preview = {
            "file_path": file_path,
            "recommendation": recommendation.title if recommendation else "Manual change",
            "statistics": self._calculate_change_statistics(original_content, modified_content),
            "diff": self._generate_diff(original_content, modified_content),
            "affected_functions": self._find_affected_functions(original_content, modified_content),
            "preview_id": hashlib.md5(f"{file_path}{datetime.now()}".encode()).hexdigest()[:8]
        }
        
        # Add syntax validation
        preview["syntax_valid"] = self._validate_syntax(modified_content, file_path)
        
        # Add impact preview if recommendation provided
        if recommendation:
            preview["expected_impact"] = {
                "quality_improvement": recommendation.expected_improvement.overall_score,
                "risk_level": recommendation.risk_level,
                "effort_estimate": recommendation.effort_estimate
            }
        
        return preview
    
    def backup_file(self, file_path: str) -> str:
        """
        Create a backup of a file before modification.
        
        Returns:
            Backup file path
        """
        if not self.active_session:
            raise RuntimeError("No active modification session")
        
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        backup_name = f"{Path(file_path).stem}_{timestamp}_{file_hash}{Path(file_path).suffix}"
        backup_path = self.backup_dir / self.active_session["id"] / backup_name
        
        # Create backup directory
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Store backup info
        self.active_session["backups"][file_path] = {
            "backup_path": str(backup_path),
            "original_hash": file_hash,
            "timestamp": timestamp
        }
        
        logger.info(f"Backed up {file_path} to {backup_path}")
        return str(backup_path)
    
    def apply_change_safely(self,
                           file_path: str,
                           modified_content: str,
                           validate: bool = True) -> Dict[str, Any]:
        """
        Apply a change to a file with safety checks and validation.
        
        Args:
            file_path: Path to file to modify
            modified_content: New content for the file
            validate: Whether to validate the change before applying
            
        Returns:
            Result dictionary with success status and any issues
        """
        result = {
            "success": False,
            "file_path": file_path,
            "issues": [],
            "rollback_available": True
        }
        
        try:
            # Ensure we have a backup
            if file_path not in self.active_session["backups"]:
                self.backup_file(file_path)
            
            # Validate if requested
            if validate:
                validation_result = self._validate_change(file_path, modified_content)
                if not validation_result["valid"]:
                    result["issues"] = validation_result["issues"]
                    return result
            
            # Apply change atomically
            temp_file = None
            try:
                # Write to temporary file first
                with tempfile.NamedTemporaryFile(mode='w', 
                                               suffix=Path(file_path).suffix,
                                               delete=False) as temp_file:
                    temp_file.write(modified_content)
                    temp_path = temp_file.name
                
                # Atomic move
                shutil.move(temp_path, file_path)
                
                # Record change
                self.active_session["changes"].append({
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat(),
                    "content_hash": hashlib.md5(modified_content.encode()).hexdigest()[:8]
                })
                
                result["success"] = True
                logger.info(f"Successfully applied change to {file_path}")
                
            finally:
                # Clean up temp file if it exists
                if temp_file and os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            
        except Exception as e:
            result["issues"].append(f"Failed to apply change: {str(e)}")
            logger.error(f"Error applying change to {file_path}: {str(e)}")
        
        return result
    
    def rollback_file(self, file_path: str) -> bool:
        """
        Rollback a single file to its backed up state.
        
        Returns:
            True if rollback successful, False otherwise
        """
        if not self.active_session or file_path not in self.active_session["backups"]:
            logger.error(f"No backup found for {file_path}")
            return False
        
        try:
            backup_info = self.active_session["backups"][file_path]
            backup_path = backup_info["backup_path"]
            
            # Restore from backup
            shutil.copy2(backup_path, file_path)
            logger.info(f"Rolled back {file_path} from {backup_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback {file_path}: {str(e)}")
            return False
    
    def rollback_session(self) -> Dict[str, Any]:
        """
        Rollback all changes in the current session.
        
        Returns:
            Summary of rollback operation
        """
        if not self.active_session:
            return {"success": False, "reason": "No active session"}
        
        rollback_summary = {
            "success": True,
            "files_rolled_back": [],
            "failures": []
        }
        
        # Rollback each changed file
        for change in reversed(self.active_session["changes"]):
            file_path = change["file_path"]
            if self.rollback_file(file_path):
                rollback_summary["files_rolled_back"].append(file_path)
            else:
                rollback_summary["failures"].append(file_path)
                rollback_summary["success"] = False
        
        self.active_session["rolled_back"] = True
        logger.info(f"Session rollback complete: {rollback_summary}")
        
        return rollback_summary
    
    def finalize_session(self):
        """Finalize the modification session and clean up old backups"""
        if not self.active_session:
            return
        
        # Log session summary
        session_summary = {
            "session_id": self.active_session["id"],
            "duration": (datetime.now() - self.active_session["start_time"]).total_seconds(),
            "files_modified": len(self.active_session["changes"]),
            "rolled_back": self.active_session["rolled_back"]
        }
        
        # Save session log
        log_path = self.backup_dir / f"session_{self.active_session['id']}.json"
        with open(log_path, 'w') as f:
            json.dump(session_summary, f, indent=2)
        
        # Clean up old backups (keep last 7 days)
        self._cleanup_old_backups()
        
        self.active_session = None
    
    def _calculate_change_statistics(self, original: str, modified: str) -> Dict[str, int]:
        """Calculate statistics about the changes"""
        orig_lines = original.splitlines()
        mod_lines = modified.splitlines()
        
        stats = {
            "lines_added": max(0, len(mod_lines) - len(orig_lines)),
            "lines_removed": max(0, len(orig_lines) - len(mod_lines)),
            "total_changes": abs(len(mod_lines) - len(orig_lines)),
            "original_size": len(original),
            "modified_size": len(modified),
            "size_change": len(modified) - len(original)
        }
        
        return stats
    
    def _generate_diff(self, original: str, modified: str) -> str:
        """Generate a unified diff of changes"""
        import difflib
        
        orig_lines = original.splitlines(keepends=True)
        mod_lines = modified.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            orig_lines,
            mod_lines,
            fromfile="original",
            tofile="modified",
            n=3
        )
        
        return ''.join(diff)
    
    def _find_affected_functions(self, original: str, modified: str) -> List[str]:
        """Find functions that are affected by changes"""
        import ast
        
        affected = []
        
        try:
            # Parse both versions
            orig_tree = ast.parse(original)
            mod_tree = ast.parse(modified)
            
            # Extract function names
            orig_functions = {node.name for node in ast.walk(orig_tree) 
                            if isinstance(node, ast.FunctionDef)}
            mod_functions = {node.name for node in ast.walk(mod_tree) 
                           if isinstance(node, ast.FunctionDef)}
            
            # Find changes
            removed = orig_functions - mod_functions
            added = mod_functions - orig_functions
            
            if removed:
                affected.extend([f"Removed: {name}" for name in removed])
            if added:
                affected.extend([f"Added: {name}" for name in added])
            
            # TODO: Detect modified functions by comparing AST
            
        except:
            # If parsing fails, try regex approach
            import re
            func_pattern = re.compile(r"def\s+(\w+)\s*\(")
            orig_funcs = set(func_pattern.findall(original))
            mod_funcs = set(func_pattern.findall(modified))
            
            affected = list(orig_funcs.symmetric_difference(mod_funcs))
        
        return affected
    
    def _validate_syntax(self, content: str, file_path: str) -> bool:
        """Validate syntax of modified content"""
        if file_path.endswith('.py'):
            try:
                compile(content, file_path, 'exec')
                return True
            except SyntaxError:
                return False
        
        # Add other language validators as needed
        return True
    
    def _validate_change(self, file_path: str, content: str) -> Dict[str, Any]:
        """Validate a change before applying"""
        validation = {
            "valid": True,
            "issues": []
        }
        
        # Check syntax
        if not self._validate_syntax(content, file_path):
            validation["valid"] = False
            validation["issues"].append("Syntax error in modified content")
        
        # Check file size limits
        max_size = get_config("max_file_size", 10 * 1024 * 1024)  # 10MB default
        if len(content) > max_size:
            validation["valid"] = False
            validation["issues"].append(f"File size exceeds limit ({max_size} bytes)")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r"exec\s*\(",
            r"eval\s*\(",
            r"__import__",
            r"subprocess\.call",
            r"os\.system"
        ]
        
        import re
        for pattern in suspicious_patterns:
            if re.search(pattern, content):
                validation["issues"].append(f"Suspicious pattern detected: {pattern}")
        
        return validation
    
    def _cleanup_old_backups(self):
        """Clean up backups older than retention period"""
        retention_days = get_config("backup_retention_days", 7)
        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)
        
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir():
                # Check directory modification time
                if backup_dir.stat().st_mtime < cutoff_time:
                    shutil.rmtree(backup_dir)
                    logger.info(f"Cleaned up old backup directory: {backup_dir}")
    
    def get_session_summary(self) -> Optional[Dict[str, Any]]:
        """Get summary of current session"""
        if not self.active_session:
            return None
        
        return {
            "session_id": self.active_session["id"],
            "files_backed_up": len(self.active_session["backups"]),
            "changes_applied": len(self.active_session["changes"]),
            "duration": (datetime.now() - self.active_session["start_time"]).total_seconds(),
            "can_rollback": not self.active_session["rolled_back"]
        }