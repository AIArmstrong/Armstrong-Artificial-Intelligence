"""
Filesystem Specialized Agent

Handles file system operations, directory management, and file I/O
with focused capabilities and secure file handling.
"""
import logging
import asyncio
import os
import shutil
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False
    # Fallback synchronous file operations
    import io
import mimetypes

logger = logging.getLogger(__name__)


class FilesystemAgent:
    """
    Specialized agent for filesystem operations.
    
    Features:
    - File reading, writing, and manipulation
    - Directory creation and management
    - File search and listing operations
    - Secure path validation and sandboxing
    - Batch file operations
    - File metadata and permissions handling
    """
    
    def __init__(self, 
                 base_path: Optional[str] = None,
                 enable_write: bool = True,
                 enable_delete: bool = False):
        """Initialize filesystem agent"""
        
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.enable_write = enable_write
        self.enable_delete = enable_delete
        self.initialized = True
        
        # Agent metadata
        self.name = "Filesystem Operations Agent"
        self.version = "1.0.0"
        self.capabilities = [
            "read_file",
            "write_file",
            "create_directory",
            "list_directory", 
            "copy_file",
            "move_file",
            "delete_file",
            "get_file_info",
            "search_files",
            "create_backup",
            "batch_operations"
        ]
        
        # Security restrictions
        self.allowed_extensions = {
            '.txt', '.md', '.json', '.yaml', '.yml', '.csv', '.log',
            '.py', '.js', '.ts', '.html', '.css', '.xml', '.toml',
            '.cfg', '.conf', '.ini', '.env'
        }
        
        self.restricted_paths = {
            '/etc', '/usr/bin', '/bin', '/sbin', '/boot',
            'C:\\Windows', 'C:\\Program Files', 'C:\\System32'
        }
        
        # Performance tracking
        self.total_operations = 0
        self.successful_operations = 0
        self.last_operation_time = None
        self.bytes_processed = 0
        
        # Create base directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Filesystem agent initialized with base path: {self.base_path}")
    
    async def execute_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute filesystem-related task.
        
        Args:
            task: Task description to execute
            context: Additional context and parameters
            
        Returns:
            Task execution result
        """
        start_time = datetime.now()
        self.total_operations += 1
        
        try:
            logger.info(f"Executing filesystem task: {task[:100]}...")
            
            # Parse task and determine operation
            operation = await self._parse_task(task, context)
            
            # Validate security constraints
            security_check = await self._validate_security(operation)
            if not security_check["allowed"]:
                return {
                    "success": False,
                    "error": f"Security restriction: {security_check['reason']}",
                    "operation": operation["type"],
                    "agent": "filesystem"
                }
            
            # Execute operation
            result = await self._execute_operation(operation)
            
            # Track success
            self.successful_operations += 1
            self.last_operation_time = datetime.now()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "result": result,
                "operation": operation["type"],
                "execution_time_seconds": execution_time,
                "agent": "filesystem",
                "bytes_processed": result.get("bytes_processed", 0)
            }
            
        except Exception as e:
            logger.error(f"Filesystem task execution failed: {e}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": False,
                "error": str(e),
                "operation": "unknown",
                "execution_time_seconds": execution_time,
                "agent": "filesystem"
            }
    
    async def _parse_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse task description to determine specific operation"""
        
        task_lower = task.lower()
        
        # File reading operations
        if any(keyword in task_lower for keyword in ["read file", "open file", "get file", "load file"]):
            return {
                "type": "read_file",
                "path": context.get("path", self._extract_file_path(task)),
                "encoding": context.get("encoding", "utf-8"),
                "max_size": context.get("max_size", 10 * 1024 * 1024)  # 10MB default
            }
        
        # File writing operations
        elif any(keyword in task_lower for keyword in ["write file", "save file", "create file"]):
            return {
                "type": "write_file",
                "path": context.get("path", self._extract_file_path(task)),
                "content": context.get("content", self._extract_file_content(task)),
                "encoding": context.get("encoding", "utf-8"),
                "append": context.get("append", False),
                "create_dirs": context.get("create_dirs", True)
            }
        
        # Directory operations
        elif any(keyword in task_lower for keyword in ["create directory", "make directory", "mkdir"]):
            return {
                "type": "create_directory",
                "path": context.get("path", self._extract_directory_path(task)),
                "parents": context.get("parents", True),
                "exist_ok": context.get("exist_ok", True)
            }
        
        elif any(keyword in task_lower for keyword in ["list directory", "list files", "ls", "dir"]):
            return {
                "type": "list_directory",
                "path": context.get("path", self._extract_directory_path(task)),
                "recursive": context.get("recursive", False),
                "include_hidden": context.get("include_hidden", False),
                "filter_pattern": context.get("filter_pattern")
            }
        
        # File manipulation operations
        elif any(keyword in task_lower for keyword in ["copy file", "cp"]):
            return {
                "type": "copy_file",
                "source": context.get("source", self._extract_source_path(task)),
                "destination": context.get("destination", self._extract_destination_path(task)),
                "overwrite": context.get("overwrite", False)
            }
        
        elif any(keyword in task_lower for keyword in ["move file", "mv", "rename"]):
            return {
                "type": "move_file",
                "source": context.get("source", self._extract_source_path(task)),
                "destination": context.get("destination", self._extract_destination_path(task)),
                "overwrite": context.get("overwrite", False)
            }
        
        elif any(keyword in task_lower for keyword in ["delete file", "remove file", "rm"]):
            return {
                "type": "delete_file",
                "path": context.get("path", self._extract_file_path(task)),
                "force": context.get("force", False)
            }
        
        # Information operations
        elif any(keyword in task_lower for keyword in ["file info", "stat", "file details"]):
            return {
                "type": "get_file_info",
                "path": context.get("path", self._extract_file_path(task))
            }
        
        # Search operations
        elif any(keyword in task_lower for keyword in ["search files", "find files", "find"]):
            return {
                "type": "search_files",
                "path": context.get("path", str(self.base_path)),
                "pattern": context.get("pattern", self._extract_search_pattern(task)),
                "recursive": context.get("recursive", True),
                "content_search": context.get("content_search", False)
            }
        
        # Backup operations
        elif any(keyword in task_lower for keyword in ["backup", "create backup"]):
            return {
                "type": "create_backup",
                "path": context.get("path", self._extract_file_path(task)),
                "backup_dir": context.get("backup_dir", str(self.base_path / "backups"))
            }
        
        # Default to file reading
        else:
            return {
                "type": "read_file",
                "path": context.get("path", task),
                "fallback": True
            }
    
    def _extract_file_path(self, task: str) -> str:
        """Extract file path from task description"""
        
        # Look for quoted paths
        import re
        quoted_path = re.search(r'"([^"]*)"', task)
        if quoted_path:
            return quoted_path.group(1)
        
        # Look for file extensions
        file_extensions = ['.txt', '.md', '.json', '.py', '.js', '.html', '.css']
        for ext in file_extensions:
            if ext in task:
                # Extract around the extension
                words = task.split()
                for word in words:
                    if ext in word:
                        return word.strip('.,;:"')
        
        # Look for common path patterns
        path_pattern = r'\b([a-zA-Z0-9_./\\-]+(?:/[a-zA-Z0-9_.-]+)*)\b'
        match = re.search(path_pattern, task)
        if match:
            return match.group(1)
        
        return "example.txt"  # Default filename
    
    def _extract_directory_path(self, task: str) -> str:
        """Extract directory path from task description"""
        
        path = self._extract_file_path(task)
        
        # If it looks like a file, get its directory
        if '.' in os.path.basename(path):
            return os.path.dirname(path) or "."
        
        return path
    
    def _extract_file_content(self, task: str) -> str:
        """Extract file content from task description"""
        
        # Look for quoted content
        import re
        quoted_content = re.search(r'"([^"]*)"', task)
        if quoted_content:
            return quoted_content.group(1)
        
        # Look for content after keywords
        keywords = ["content", "text", "data", "write", "save"]
        task_lower = task.lower()
        
        for keyword in keywords:
            if keyword in task_lower:
                start_index = task_lower.find(keyword) + len(keyword)
                content = task[start_index:].strip()
                
                if content.startswith(':'):
                    content = content[1:].strip()
                
                if content:
                    return content
        
        return "File created via AAI filesystem agent"
    
    def _extract_source_path(self, task: str) -> str:
        """Extract source path for copy/move operations"""
        
        words = task.split()
        
        # Look for "from" keyword
        if "from" in task.lower():
            from_index = task.lower().find("from") + 4
            remaining = task[from_index:].strip()
            
            # Extract first path-like word
            for word in remaining.split():
                if '/' in word or '\\' in word or '.' in word:
                    return word.strip('.,;:"')
        
        # Fallback to first path-like word
        for word in words:
            if '/' in word or '\\' in word:
                return word.strip('.,;:"')
        
        return "source.txt"
    
    def _extract_destination_path(self, task: str) -> str:
        """Extract destination path for copy/move operations"""
        
        words = task.split()
        
        # Look for "to" keyword
        if "to" in task.lower():
            to_index = task.lower().find("to") + 2
            remaining = task[to_index:].strip()
            
            # Extract first path-like word
            for word in remaining.split():
                if '/' in word or '\\' in word or '.' in word:
                    return word.strip('.,;:"')
        
        # Look for second path in task
        paths = []
        for word in words:
            if '/' in word or '\\' in word:
                paths.append(word.strip('.,;:"'))
        
        if len(paths) >= 2:
            return paths[1]
        
        return "destination.txt"
    
    def _extract_search_pattern(self, task: str) -> str:
        """Extract search pattern from task description"""
        
        # Look for quoted pattern
        import re
        quoted_pattern = re.search(r'"([^"]*)"', task)
        if quoted_pattern:
            return quoted_pattern.group(1)
        
        # Look for pattern after keywords
        keywords = ["pattern", "name", "matching", "called", "find"]
        task_lower = task.lower()
        
        for keyword in keywords:
            if keyword in task_lower:
                start_index = task_lower.find(keyword) + len(keyword)
                remaining = task[start_index:].strip()
                
                if remaining:
                    pattern = remaining.split()[0]
                    return pattern.strip('.,;:"')
        
        return "*.*"  # Default pattern
    
    async def _validate_security(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Validate operation against security constraints"""
        
        op_type = operation["type"]
        
        # Check if operation is allowed
        if op_type == "write_file" and not self.enable_write:
            return {"allowed": False, "reason": "Write operations disabled"}
        
        if op_type == "delete_file" and not self.enable_delete:
            return {"allowed": False, "reason": "Delete operations disabled"}
        
        # Check paths
        paths_to_check = []
        
        if "path" in operation:
            paths_to_check.append(operation["path"])
        
        if "source" in operation:
            paths_to_check.append(operation["source"])
        
        if "destination" in operation:
            paths_to_check.append(operation["destination"])
        
        for path_str in paths_to_check:
            if not await self._is_path_safe(path_str):
                return {"allowed": False, "reason": f"Unsafe path: {path_str}"}
        
        # Check file extensions for write operations
        if op_type in ["write_file", "copy_file", "move_file"]:
            target_path = operation.get("path") or operation.get("destination", "")
            if target_path:
                ext = Path(target_path).suffix.lower()
                if ext and ext not in self.allowed_extensions:
                    return {"allowed": False, "reason": f"File extension not allowed: {ext}"}
        
        return {"allowed": True, "reason": "Operation allowed"}
    
    async def _is_path_safe(self, path_str: str) -> bool:
        """Check if path is safe for operations"""
        
        try:
            # Resolve path relative to base path
            path = Path(path_str)
            
            if path.is_absolute():
                # Check against restricted paths
                for restricted in self.restricted_paths:
                    if str(path).startswith(restricted):
                        return False
                
                resolved_path = path.resolve()
            else:
                resolved_path = (self.base_path / path).resolve()
            
            # Ensure path is within base path (prevent directory traversal)
            try:
                resolved_path.relative_to(self.base_path.resolve())
            except ValueError:
                return False
            
            # Check for dangerous patterns
            dangerous_patterns = ['..', '~', '$']
            for pattern in dangerous_patterns:
                if pattern in str(path):
                    return False
            
            return True
            
        except Exception:
            return False
    
    async def _execute_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the filesystem operation"""
        
        op_type = operation["type"]
        
        if op_type == "read_file":
            return await self._read_file(operation)
        
        elif op_type == "write_file":
            return await self._write_file(operation)
        
        elif op_type == "create_directory":
            return await self._create_directory(operation)
        
        elif op_type == "list_directory":
            return await self._list_directory(operation)
        
        elif op_type == "copy_file":
            return await self._copy_file(operation)
        
        elif op_type == "move_file":
            return await self._move_file(operation)
        
        elif op_type == "delete_file":
            return await self._delete_file(operation)
        
        elif op_type == "get_file_info":
            return await self._get_file_info(operation)
        
        elif op_type == "search_files":
            return await self._search_files(operation)
        
        elif op_type == "create_backup":
            return await self._create_backup(operation)
        
        else:
            raise ValueError(f"Unknown operation type: {op_type}")
    
    async def _read_file(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Read file content"""
        
        path = self._resolve_path(operation["path"])
        encoding = operation.get("encoding", "utf-8")
        max_size = operation.get("max_size", 10 * 1024 * 1024)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if path.stat().st_size > max_size:
            raise ValueError(f"File too large: {path.stat().st_size} bytes (max: {max_size})")
        
        async with aiofiles.open(path, 'r', encoding=encoding) as f:
            content = await f.read()
        
        self.bytes_processed += len(content.encode(encoding))
        
        return {
            "content": content,
            "file_path": str(path),
            "file_size": path.stat().st_size,
            "encoding": encoding,
            "bytes_processed": len(content.encode(encoding))
        }
    
    async def _write_file(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Write file content"""
        
        path = self._resolve_path(operation["path"])
        content = operation["content"]
        encoding = operation.get("encoding", "utf-8")
        append = operation.get("append", False)
        create_dirs = operation.get("create_dirs", True)
        
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        mode = 'a' if append else 'w'
        
        async with aiofiles.open(path, mode, encoding=encoding) as f:
            await f.write(content)
        
        bytes_written = len(content.encode(encoding))
        self.bytes_processed += bytes_written
        
        return {
            "file_written": True,
            "file_path": str(path),
            "bytes_written": bytes_written,
            "append_mode": append,
            "encoding": encoding
        }
    
    async def _create_directory(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Create directory"""
        
        path = self._resolve_path(operation["path"])
        parents = operation.get("parents", True)
        exist_ok = operation.get("exist_ok", True)
        
        path.mkdir(parents=parents, exist_ok=exist_ok)
        
        return {
            "directory_created": True,
            "directory_path": str(path),
            "parents_created": parents
        }
    
    async def _list_directory(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents"""
        
        path = self._resolve_path(operation["path"])
        recursive = operation.get("recursive", False)
        include_hidden = operation.get("include_hidden", False)
        filter_pattern = operation.get("filter_pattern")
        
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        
        files = []
        directories = []
        
        if recursive:
            for item in path.rglob("*"):
                if not include_hidden and item.name.startswith('.'):
                    continue
                
                if filter_pattern and not item.match(filter_pattern):
                    continue
                
                item_info = await self._get_item_info(item)
                
                if item.is_file():
                    files.append(item_info)
                elif item.is_dir():
                    directories.append(item_info)
        else:
            for item in path.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                
                if filter_pattern and not item.match(filter_pattern):
                    continue
                
                item_info = await self._get_item_info(item)
                
                if item.is_file():
                    files.append(item_info)
                elif item.is_dir():
                    directories.append(item_info)
        
        return {
            "directory_path": str(path),
            "files": files,
            "directories": directories,
            "file_count": len(files),
            "directory_count": len(directories),
            "recursive": recursive
        }
    
    async def _get_item_info(self, path: Path) -> Dict[str, Any]:
        """Get information about a file or directory"""
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "path": str(path),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "extension": path.suffix.lower() if path.is_file() else None
        }
    
    def _resolve_path(self, path_str: str) -> Path:
        """Resolve path relative to base path"""
        
        path = Path(path_str)
        
        if path.is_absolute():
            return path
        else:
            return self.base_path / path
    
    async def _copy_file(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Copy file operation"""
        
        source = self._resolve_path(operation["source"])
        destination = self._resolve_path(operation["destination"])
        overwrite = operation.get("overwrite", False)
        
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source}")
        
        if destination.exists() and not overwrite:
            raise FileExistsError(f"Destination exists and overwrite=False: {destination}")
        
        # Create destination directory if needed
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source, destination)
        
        return {
            "file_copied": True,
            "source": str(source),
            "destination": str(destination),
            "size": destination.stat().st_size
        }
    
    async def _move_file(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Move/rename file operation"""
        
        source = self._resolve_path(operation["source"])
        destination = self._resolve_path(operation["destination"])
        overwrite = operation.get("overwrite", False)
        
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source}")
        
        if destination.exists() and not overwrite:
            raise FileExistsError(f"Destination exists and overwrite=False: {destination}")
        
        # Create destination directory if needed
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(source), str(destination))
        
        return {
            "file_moved": True,
            "source": str(source),
            "destination": str(destination)
        }
    
    async def _delete_file(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Delete file operation"""
        
        path = self._resolve_path(operation["path"])
        force = operation.get("force", False)
        
        if not path.exists():
            if not force:
                raise FileNotFoundError(f"File not found: {path}")
            else:
                return {"file_deleted": False, "reason": "File did not exist"}
        
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        
        return {
            "file_deleted": True,
            "file_path": str(path)
        }
    
    async def _get_file_info(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed file information"""
        
        path = self._resolve_path(operation["path"])
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        stat = path.stat()
        
        info = {
            "name": path.name,
            "path": str(path),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "permissions": oct(stat.st_mode)[-3:]
        }
        
        if path.is_file():
            info["extension"] = path.suffix.lower()
            info["mime_type"] = mimetypes.guess_type(str(path))[0]
        
        return info
    
    async def _search_files(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Search for files matching pattern"""
        
        search_path = self._resolve_path(operation["path"])
        pattern = operation["pattern"]
        recursive = operation.get("recursive", True)
        content_search = operation.get("content_search", False)
        
        if not search_path.exists():
            raise FileNotFoundError(f"Search path not found: {search_path}")
        
        matches = []
        
        if recursive:
            search_iter = search_path.rglob(pattern)
        else:
            search_iter = search_path.glob(pattern)
        
        for match in search_iter:
            match_info = await self._get_item_info(match)
            
            # Content search if requested
            if content_search and match.is_file() and match.suffix.lower() in self.allowed_extensions:
                try:
                    async with aiofiles.open(match, 'r', encoding='utf-8') as f:
                        content = await f.read()
                        if pattern.lower() in content.lower():
                            match_info["content_match"] = True
                        else:
                            continue  # Skip if content doesn't match
                except Exception:
                    pass  # Skip files that can't be read
            
            matches.append(match_info)
        
        return {
            "search_path": str(search_path),
            "pattern": pattern,
            "matches": matches,
            "match_count": len(matches),
            "recursive": recursive,
            "content_search": content_search
        }
    
    async def _create_backup(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Create backup of file or directory"""
        
        source_path = self._resolve_path(operation["path"])
        backup_dir = Path(operation["backup_dir"])
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")
        
        # Create backup directory
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source_path.name}_{timestamp}"
        backup_path = backup_dir / backup_name
        
        # Copy to backup location
        if source_path.is_file():
            shutil.copy2(source_path, backup_path)
        else:
            shutil.copytree(source_path, backup_path)
        
        return {
            "backup_created": True,
            "source": str(source_path),
            "backup_path": str(backup_path),
            "backup_size": backup_path.stat().st_size if backup_path.is_file() else sum(
                f.stat().st_size for f in backup_path.rglob('*') if f.is_file()
            )
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and performance metrics"""
        
        success_rate = (
            self.successful_operations / max(1, self.total_operations)
        )
        
        return {
            "name": self.name,
            "version": self.version,
            "initialized": self.initialized,
            "base_path": str(self.base_path),
            "write_enabled": self.enable_write,
            "delete_enabled": self.enable_delete,
            "capabilities": self.capabilities,
            "allowed_extensions": list(self.allowed_extensions),
            "performance": {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "success_rate": success_rate,
                "bytes_processed": self.bytes_processed,
                "last_operation": self.last_operation_time.isoformat() if self.last_operation_time else None
            },
            "ready": self.initialized
        }


async def test_filesystem_agent():
    """Test filesystem agent functionality"""
    
    # Create temporary test directory
    test_dir = Path("./test_filesystem_agent")
    test_dir.mkdir(exist_ok=True)
    
    agent = FilesystemAgent(base_path=str(test_dir), enable_write=True, enable_delete=True)
    
    print("🧪 Testing Filesystem Agent")
    print("=" * 27)
    
    # Check agent status
    status = agent.get_agent_status()
    print(f"Agent initialized: {status['initialized']}")
    print(f"Base path: {status['base_path']}")
    print(f"Write enabled: {status['write_enabled']}")
    print(f"Delete enabled: {status['delete_enabled']}")
    print(f"Capabilities: {len(status['capabilities'])}")
    
    # Test operations
    print(f"\n🎯 Testing filesystem operations...")
    
    test_tasks = [
        {
            "task": "Write file test.txt with content 'Hello, World!'",
            "context": {"path": "test.txt", "content": "Hello, World!"}
        },
        {
            "task": "Read file test.txt",
            "context": {"path": "test.txt"}
        },
        {
            "task": "Create directory subdir",
            "context": {"path": "subdir"}
        },
        {
            "task": "List directory contents",
            "context": {"path": "."}
        },
        {
            "task": "Copy test.txt to subdir/test_copy.txt",
            "context": {"source": "test.txt", "destination": "subdir/test_copy.txt"}
        },
        {
            "task": "Get file info for test.txt",
            "context": {"path": "test.txt"}
        },
        {
            "task": "Search for files matching *.txt",
            "context": {"path": ".", "pattern": "*.txt", "recursive": True}
        }
    ]
    
    for i, test in enumerate(test_tasks, 1):
        print(f"\nTest {i}: {test['task']}")
        result = await agent.execute_task(test["task"], test["context"])
        
        print(f"  Success: {result['success']}")
        print(f"  Operation: {result.get('operation', 'unknown')}")
        
        if result['success']:
            operation_result = result['result']
            if 'content' in operation_result:
                print(f"  Content: {operation_result['content'][:50]}...")
            elif 'file_count' in operation_result:
                print(f"  Files found: {operation_result['file_count']}")
            elif 'size' in operation_result:
                print(f"  File size: {operation_result['size']} bytes")
            
        print(f"  Time: {result.get('execution_time_seconds', 0):.3f}s")
    
    # Check final status
    final_status = agent.get_agent_status()
    performance = final_status["performance"]
    print(f"\n📊 Final Performance:")
    print(f"Total operations: {performance['total_operations']}")
    print(f"Success rate: {performance['success_rate']:.1%}")
    print(f"Bytes processed: {performance['bytes_processed']}")
    
    # Cleanup test directory
    shutil.rmtree(test_dir, ignore_errors=True)
    
    print(f"\n✅ Filesystem Agent Testing Complete")
    print(f"Ready for file operations and data management")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_filesystem_agent())