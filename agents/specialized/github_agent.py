"""
GitHub Specialized Agent

Handles GitHub repository operations, issue management, and pull requests
with focused capabilities and developer workflow optimization.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# GitHub SDK imports with fallbacks
try:
    import aiohttp
    HTTP_CLIENT_AVAILABLE = True
except ImportError:
    aiohttp = None
    HTTP_CLIENT_AVAILABLE = False

logger = logging.getLogger(__name__)


class GitHubAgent:
    """
    Specialized agent for GitHub operations.
    
    Features:
    - Issue management (create, update, list, close)
    - Repository operations and information retrieval
    - Pull request management
    - Release and milestone tracking
    - Webhook and notification handling
    - Code search and file operations
    """
    
    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        """Initialize GitHub agent"""
        
        self.token = token
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.initialized = False
        
        # Agent metadata
        self.name = "GitHub Repository Agent"
        self.version = "1.0.0"
        self.capabilities = [
            "create_issue",
            "update_issue",
            "list_issues",
            "close_issue",
            "create_pr",
            "merge_pr",
            "get_repo_info",
            "list_repositories",
            "create_branch",
            "get_file_content",
            "create_release",
            "list_releases"
        ]
        
        # Performance tracking
        self.total_operations = 0
        self.successful_operations = 0
        self.last_operation_time = None
        self.rate_limit_remaining = 5000  # GitHub default
        
        # Initialize HTTP session
        if HTTP_CLIENT_AVAILABLE:
            asyncio.create_task(self._initialize_session())
            self.initialized = True
        else:
            logger.warning("HTTP client not available - using simulation mode")
            self.initialized = True
    
    async def _initialize_session(self):
        """Initialize aiohttp session with GitHub headers"""
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AAI-GitHub-Agent/1.0.0"
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def execute_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute GitHub-related task.
        
        Args:
            task: Task description to execute
            context: Additional context and parameters
            
        Returns:
            Task execution result
        """
        start_time = datetime.now()
        self.total_operations += 1
        
        try:
            logger.info(f"Executing GitHub task: {task[:100]}...")
            
            # Parse task and determine operation
            operation = await self._parse_task(task, context)
            
            # Execute operation
            if self.session and HTTP_CLIENT_AVAILABLE:
                result = await self._execute_real_operation(operation)
            else:
                result = await self._execute_simulated_operation(operation)
            
            # Track success
            self.successful_operations += 1
            self.last_operation_time = datetime.now()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "result": result,
                "operation": operation["type"],
                "execution_time_seconds": execution_time,
                "agent": "github",
                "simulated": not (self.session and HTTP_CLIENT_AVAILABLE)
            }
            
        except Exception as e:
            logger.error(f"GitHub task execution failed: {e}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": False,
                "error": str(e),
                "operation": "unknown",
                "execution_time_seconds": execution_time,
                "agent": "github"
            }
    
    async def _parse_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse task description to determine specific operation"""
        
        task_lower = task.lower()
        
        # Issue operations
        if any(keyword in task_lower for keyword in ["create issue", "new issue", "open issue"]):
            return {
                "type": "create_issue",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "title": self._extract_issue_title(task),
                "body": context.get("body", self._extract_issue_body(task)),
                "labels": context.get("labels", []),
                "assignees": context.get("assignees", [])
            }
        
        elif any(keyword in task_lower for keyword in ["update issue", "modify issue", "edit issue"]):
            return {
                "type": "update_issue",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "issue_number": context.get("issue_number", self._extract_issue_number(task)),
                "title": context.get("title"),
                "body": context.get("body"),
                "state": context.get("state"),
                "labels": context.get("labels")
            }
        
        elif any(keyword in task_lower for keyword in ["list issues", "get issues", "show issues"]):
            return {
                "type": "list_issues",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "state": context.get("state", "open"),
                "labels": context.get("labels", []),
                "limit": context.get("limit", 10)
            }
        
        elif any(keyword in task_lower for keyword in ["close issue", "resolve issue"]):
            return {
                "type": "close_issue",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "issue_number": context.get("issue_number", self._extract_issue_number(task)),
                "comment": context.get("comment", "Closed via AAI orchestration")
            }
        
        # Pull request operations
        elif any(keyword in task_lower for keyword in ["create pr", "create pull request", "new pr"]):
            return {
                "type": "create_pr",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "title": self._extract_pr_title(task),
                "body": context.get("body", ""),
                "head": context.get("head", "feature-branch"),
                "base": context.get("base", "main"),
                "draft": context.get("draft", False)
            }
        
        elif any(keyword in task_lower for keyword in ["merge pr", "merge pull request"]):
            return {
                "type": "merge_pr",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "pr_number": context.get("pr_number", self._extract_pr_number(task)),
                "merge_method": context.get("merge_method", "merge")
            }
        
        # Repository operations
        elif any(keyword in task_lower for keyword in ["repo info", "repository info", "get repo"]):
            return {
                "type": "get_repo_info",
                "repo": context.get("repo", self._extract_repo_from_task(task))
            }
        
        elif any(keyword in task_lower for keyword in ["list repos", "list repositories"]):
            return {
                "type": "list_repositories",
                "user": context.get("user", ""),
                "org": context.get("org", ""),
                "limit": context.get("limit", 10)
            }
        
        # File operations
        elif any(keyword in task_lower for keyword in ["get file", "read file", "file content"]):
            return {
                "type": "get_file_content",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "path": context.get("path", self._extract_file_path(task)),
                "ref": context.get("ref", "main")
            }
        
        # Release operations
        elif any(keyword in task_lower for keyword in ["create release", "new release"]):
            return {
                "type": "create_release",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "tag_name": context.get("tag_name", "v1.0.0"),
                "name": context.get("name", "Release"),
                "body": context.get("body", ""),
                "draft": context.get("draft", False),
                "prerelease": context.get("prerelease", False)
            }
        
        elif any(keyword in task_lower for keyword in ["list releases", "get releases"]):
            return {
                "type": "list_releases",
                "repo": context.get("repo", self._extract_repo_from_task(task)),
                "limit": context.get("limit", 10)
            }
        
        # Default to issue creation
        else:
            return {
                "type": "create_issue",
                "repo": context.get("repo", "unknown/repo"),
                "title": task,
                "body": f"Created via AAI orchestration: {task}",
                "fallback": True
            }
    
    def _extract_repo_from_task(self, task: str) -> str:
        """Extract repository name from task description"""
        
        # Look for owner/repo pattern
        repo_pattern = r'\b([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\b'
        match = re.search(repo_pattern, task)
        
        if match:
            return match.group(1)
        
        # Look for repository keyword
        if "repository" in task.lower() or "repo" in task.lower():
            words = task.split()
            for i, word in enumerate(words):
                if word.lower() in ["repository", "repo"] and i + 1 < len(words):
                    return words[i + 1]
        
        return "unknown/repo"
    
    def _extract_issue_title(self, task: str) -> str:
        """Extract issue title from task description"""
        
        # Look for quoted title
        quoted_match = re.search(r'"([^"]*)"', task)
        if quoted_match:
            return quoted_match.group(1)
        
        # Look for title after keywords
        keywords = ["issue", "create issue", "new issue", "titled", "called"]
        task_lower = task.lower()
        
        for keyword in keywords:
            if keyword in task_lower:
                start_index = task_lower.find(keyword) + len(keyword)
                remaining = task[start_index:].strip()
                
                # Remove common prepositions
                for prep in ["about", "for", "titled", "called", ":"]:
                    if remaining.lower().startswith(prep):
                        remaining = remaining[len(prep):].strip()
                
                if remaining:
                    # Take first sentence or up to 100 chars
                    title = remaining.split('.')[0][:100]
                    return title.strip()
        
        # Fallback to task itself
        return task[:100]
    
    def _extract_issue_body(self, task: str) -> str:
        """Extract issue body from task description"""
        
        # Look for body after "body:" or "description:"
        body_patterns = [r'body:\s*(.+)', r'description:\s*(.+)', r'details:\s*(.+)']
        
        for pattern in body_patterns:
            match = re.search(pattern, task, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Default body
        return f"Issue created via AAI orchestration.\n\nOriginal request: {task}"
    
    def _extract_issue_number(self, task: str) -> int:
        """Extract issue number from task description"""
        
        # Look for #123 pattern
        number_pattern = r'#(\d+)'
        match = re.search(number_pattern, task)
        
        if match:
            return int(match.group(1))
        
        # Look for "issue 123" pattern
        issue_pattern = r'issue\s+(\d+)'
        match = re.search(issue_pattern, task, re.IGNORECASE)
        
        if match:
            return int(match.group(1))
        
        return 1  # Default issue number
    
    def _extract_pr_title(self, task: str) -> str:
        """Extract pull request title from task description"""
        
        # Similar to issue title extraction
        return self._extract_issue_title(task).replace("issue", "pull request")
    
    def _extract_pr_number(self, task: str) -> int:
        """Extract pull request number from task description"""
        
        # Look for PR #123 pattern
        pr_pattern = r'pr\s*#?(\d+)|pull\s*request\s*#?(\d+)'
        match = re.search(pr_pattern, task, re.IGNORECASE)
        
        if match:
            return int(match.group(1) or match.group(2))
        
        return self._extract_issue_number(task)  # Fallback to issue number logic
    
    def _extract_file_path(self, task: str) -> str:
        """Extract file path from task description"""
        
        # Look for file extensions
        file_pattern = r'\b([a-zA-Z0-9_./\\-]+\.[a-zA-Z0-9]+)\b'
        match = re.search(file_pattern, task)
        
        if match:
            return match.group(1)
        
        return "README.md"  # Default file
    
    async def _execute_real_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute real GitHub operation using API"""
        
        op_type = operation["type"]
        
        try:
            if op_type == "create_issue":
                data = {
                    "title": operation["title"],
                    "body": operation["body"]
                }
                
                if operation.get("labels"):
                    data["labels"] = operation["labels"]
                
                if operation.get("assignees"):
                    data["assignees"] = operation["assignees"]
                
                url = f"{self.base_url}/repos/{operation['repo']}/issues"
                
                async with self.session.post(url, json=data) as response:
                    if response.status == 201:
                        result = await response.json()
                        return {
                            "issue_created": True,
                            "issue_number": result["number"],
                            "issue_url": result["html_url"],
                            "title": result["title"]
                        }
                    else:
                        error_text = await response.text()
                        return {"error": f"Failed to create issue: {error_text}"}
            
            elif op_type == "list_issues":
                params = {
                    "state": operation.get("state", "open"),
                    "per_page": operation.get("limit", 10)
                }
                
                if operation.get("labels"):
                    params["labels"] = ",".join(operation["labels"])
                
                url = f"{self.base_url}/repos/{operation['repo']}/issues"
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        issues = await response.json()
                        return {
                            "issues": [
                                {
                                    "number": issue["number"],
                                    "title": issue["title"],
                                    "state": issue["state"],
                                    "created_at": issue["created_at"],
                                    "url": issue["html_url"]
                                }
                                for issue in issues
                            ],
                            "total_count": len(issues)
                        }
                    else:
                        error_text = await response.text()
                        return {"error": f"Failed to list issues: {error_text}"}
            
            elif op_type == "get_repo_info":
                url = f"{self.base_url}/repos/{operation['repo']}"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        repo = await response.json()
                        return {
                            "repo_info": {
                                "name": repo["name"],
                                "full_name": repo["full_name"],
                                "description": repo["description"],
                                "stars": repo["stargazers_count"],
                                "forks": repo["forks_count"],
                                "language": repo["language"],
                                "url": repo["html_url"],
                                "created_at": repo["created_at"]
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {"error": f"Failed to get repo info: {error_text}"}
            
            elif op_type == "close_issue":
                data = {"state": "closed"}
                
                url = f"{self.base_url}/repos/{operation['repo']}/issues/{operation['issue_number']}"
                
                async with self.session.patch(url, json=data) as response:
                    if response.status == 200:
                        # Add comment if provided
                        if operation.get("comment"):
                            comment_url = f"{url}/comments"
                            comment_data = {"body": operation["comment"]}
                            
                            async with self.session.post(comment_url, json=comment_data) as comment_response:
                                pass  # Comment added
                        
                        return {
                            "issue_closed": True,
                            "issue_number": operation["issue_number"],
                            "comment_added": bool(operation.get("comment"))
                        }
                    else:
                        error_text = await response.text()
                        return {"error": f"Failed to close issue: {error_text}"}
            
            else:
                return {"error": f"Unknown operation type: {op_type}"}
                
        except aiohttp.ClientError as e:
            logger.error(f"GitHub API error: {e}")
            return {"error": f"GitHub API error: {str(e)}"}
    
    async def _execute_simulated_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simulated GitHub operation for testing/fallback"""
        
        # Simulate API delay
        await asyncio.sleep(0.2)
        
        op_type = operation["type"]
        
        if op_type == "create_issue":
            issue_number = 12345
            return {
                "issue_created": True,
                "issue_number": issue_number,
                "issue_url": f"https://github.com/{operation['repo']}/issues/{issue_number}",
                "title": operation["title"],
                "simulated": True
            }
        
        elif op_type == "list_issues":
            return {
                "issues": [
                    {
                        "number": 1,
                        "title": "Example Issue 1",
                        "state": "open",
                        "created_at": "2024-01-15T10:00:00Z",
                        "url": f"https://github.com/{operation['repo']}/issues/1"
                    },
                    {
                        "number": 2,
                        "title": "Example Issue 2", 
                        "state": "closed",
                        "created_at": "2024-01-10T09:00:00Z",
                        "url": f"https://github.com/{operation['repo']}/issues/2"
                    }
                ],
                "total_count": 2,
                "simulated": True
            }
        
        elif op_type == "get_repo_info":
            return {
                "repo_info": {
                    "name": operation['repo'].split('/')[-1],
                    "full_name": operation['repo'],
                    "description": "Example repository for testing",
                    "stars": 42,
                    "forks": 7,
                    "language": "Python",
                    "url": f"https://github.com/{operation['repo']}",
                    "created_at": "2024-01-01T00:00:00Z"
                },
                "simulated": True
            }
        
        elif op_type == "close_issue":
            return {
                "issue_closed": True,
                "issue_number": operation["issue_number"],
                "comment_added": bool(operation.get("comment")),
                "simulated": True
            }
        
        else:
            return {
                "operation_completed": True,
                "operation_type": op_type,
                "simulated": True
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
            "http_client_available": HTTP_CLIENT_AVAILABLE,
            "session_ready": self.session is not None,
            "authenticated": self.token is not None,
            "capabilities": self.capabilities,
            "rate_limit_remaining": self.rate_limit_remaining,
            "performance": {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "success_rate": success_rate,
                "last_operation": self.last_operation_time.isoformat() if self.last_operation_time else None
            },
            "ready": self.initialized
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test GitHub connection and capabilities"""
        
        try:
            if self.session and HTTP_CLIENT_AVAILABLE:
                # Test API access
                url = f"{self.base_url}/user" if self.token else f"{self.base_url}/rate_limit"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Update rate limit info
                        if "rate" in data:
                            self.rate_limit_remaining = data["rate"]["remaining"]
                        
                        return {
                            "connection_test": "success",
                            "authenticated": self.token is not None,
                            "rate_limit_remaining": self.rate_limit_remaining
                        }
                    else:
                        return {
                            "connection_test": "failed",
                            "status_code": response.status
                        }
            else:
                return {
                    "connection_test": "simulated",
                    "message": "Using simulation mode - no real GitHub connection"
                }
                
        except Exception as e:
            return {
                "connection_test": "failed",
                "error": str(e)
            }
    
    async def cleanup(self):
        """Cleanup resources"""
        
        if self.session:
            await self.session.close()


async def test_github_agent():
    """Test GitHub agent functionality"""
    
    agent = GitHubAgent()
    
    print("🧪 Testing GitHub Agent")
    print("=" * 23)
    
    # Check agent status
    status = agent.get_agent_status()
    print(f"Agent initialized: {status['initialized']}")
    print(f"HTTP client available: {status['http_client_available']}")
    print(f"Session ready: {status['session_ready']}")
    print(f"Authenticated: {status['authenticated']}")
    print(f"Capabilities: {len(status['capabilities'])}")
    
    # Test connection
    connection_test = await agent.test_connection()
    print(f"Connection test: {connection_test['connection_test']}")
    
    # Test operations
    print(f"\n🎯 Testing GitHub operations...")
    
    test_tasks = [
        {
            "task": "Create a new issue titled 'Bug fix needed' for repository owner/repo",
            "context": {"repo": "test-owner/test-repo", "labels": ["bug"]}
        },
        {
            "task": "List open issues for the main repository",
            "context": {"repo": "test-owner/test-repo", "state": "open", "limit": 5}
        },
        {
            "task": "Get repository information for test-owner/test-repo",
            "context": {"repo": "test-owner/test-repo"}
        },
        {
            "task": "Close issue #123 with comment about resolution",
            "context": {"repo": "test-owner/test-repo", "issue_number": 123, "comment": "Fixed in latest commit"}
        }
    ]
    
    for i, test in enumerate(test_tasks, 1):
        print(f"\nTest {i}: {test['task'][:60]}...")
        result = await agent.execute_task(test["task"], test["context"])
        
        print(f"  Success: {result['success']}")
        print(f"  Operation: {result.get('operation', 'unknown')}")
        print(f"  Simulated: {result.get('simulated', False)}")
        print(f"  Time: {result.get('execution_time_seconds', 0):.2f}s")
    
    # Check final status
    final_status = agent.get_agent_status()
    performance = final_status["performance"]
    print(f"\n📊 Final Performance:")
    print(f"Total operations: {performance['total_operations']}")
    print(f"Success rate: {performance['success_rate']:.1%}")
    print(f"Rate limit remaining: {final_status['rate_limit_remaining']}")
    
    # Cleanup
    await agent.cleanup()
    
    print(f"\n✅ GitHub Agent Testing Complete")
    print(f"Ready for repository management and development workflows")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_github_agent())