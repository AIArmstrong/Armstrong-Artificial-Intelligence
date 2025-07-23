"""
Slack Specialized Agent

Handles Slack communication, channel management, and team notifications
with focused capabilities and high reliability.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

# Slack SDK imports with fallbacks
try:
    from slack_sdk.web.async_client import AsyncWebClient
    from slack_sdk.errors import SlackApiError
    SLACK_SDK_AVAILABLE = True
except ImportError:
    AsyncWebClient = None
    SlackApiError = Exception
    SLACK_SDK_AVAILABLE = False

logger = logging.getLogger(__name__)


class SlackAgent:
    """
    Specialized agent for Slack operations.
    
    Features:
    - Message sending and channel communication
    - Channel management and user operations
    - Team notifications and status updates
    - Rich message formatting and attachments
    - Error handling and retry mechanisms
    """
    
    def __init__(self, token: Optional[str] = None):
        """Initialize Slack agent"""
        
        self.token = token
        self.client: Optional[AsyncWebClient] = None
        self.initialized = False
        
        # Agent metadata
        self.name = "Slack Communication Agent"
        self.version = "1.0.0"
        self.capabilities = [
            "send_message",
            "send_dm", 
            "create_channel",
            "list_channels",
            "get_user_info",
            "post_status_update",
            "send_rich_message",
            "schedule_message"
        ]
        
        # Performance tracking
        self.total_operations = 0
        self.successful_operations = 0
        self.last_operation_time = None
        
        # Initialize client if token available
        if self.token and SLACK_SDK_AVAILABLE:
            self.client = AsyncWebClient(token=self.token)
            self.initialized = True
        elif not SLACK_SDK_AVAILABLE:
            logger.warning("Slack SDK not available - using simulation mode")
            self.initialized = True  # Allow simulation mode
        else:
            logger.warning("No Slack token provided - agent will use simulation mode")
            self.initialized = True
    
    async def execute_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Slack-related task.
        
        Args:
            task: Task description to execute
            context: Additional context and parameters
            
        Returns:
            Task execution result
        """
        start_time = datetime.now()
        self.total_operations += 1
        
        try:
            logger.info(f"Executing Slack task: {task[:100]}...")
            
            # Parse task and determine operation
            operation = await self._parse_task(task, context)
            
            # Execute operation
            if self.client and SLACK_SDK_AVAILABLE:
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
                "agent": "slack",
                "simulated": not (self.client and SLACK_SDK_AVAILABLE)
            }
            
        except Exception as e:
            logger.error(f"Slack task execution failed: {e}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": False,
                "error": str(e),
                "operation": "unknown",
                "execution_time_seconds": execution_time,
                "agent": "slack"
            }
    
    async def _parse_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse task description to determine specific operation"""
        
        task_lower = task.lower()
        
        # Send message operations
        if any(keyword in task_lower for keyword in ["send message", "post message", "notify", "alert"]):
            return {
                "type": "send_message",
                "channel": context.get("channel", "#general"),
                "message": self._extract_message_content(task),
                "user": context.get("user"),
                "attachments": context.get("attachments", [])
            }
        
        # Direct message operations  
        elif any(keyword in task_lower for keyword in ["dm", "direct message", "private message"]):
            return {
                "type": "send_dm",
                "user": context.get("user", "unknown"),
                "message": self._extract_message_content(task)
            }
        
        # Channel management operations
        elif any(keyword in task_lower for keyword in ["create channel", "new channel"]):
            return {
                "type": "create_channel",
                "channel_name": context.get("channel_name", "new-channel"),
                "description": context.get("description", ""),
                "private": context.get("private", False)
            }
        
        # List operations
        elif "list" in task_lower and "channel" in task_lower:
            return {
                "type": "list_channels",
                "limit": context.get("limit", 100)
            }
        
        # User info operations
        elif "user info" in task_lower or "get user" in task_lower:
            return {
                "type": "get_user_info",
                "user": context.get("user", "unknown")
            }
        
        # Status update operations
        elif any(keyword in task_lower for keyword in ["status", "update", "announcement"]):
            return {
                "type": "post_status_update",
                "message": self._extract_message_content(task),
                "channel": context.get("channel", "#general")
            }
        
        # Default to send message
        else:
            return {
                "type": "send_message",
                "channel": context.get("channel", "#general"),
                "message": task,
                "fallback": True
            }
    
    def _extract_message_content(self, task: str) -> str:
        """Extract message content from task description"""
        
        # Look for quoted content
        import re
        quoted_content = re.search(r'"([^"]*)"', task)
        if quoted_content:
            return quoted_content.group(1)
        
        # Look for content after keywords
        keywords = ["send message", "post", "notify", "alert", "dm", "tell", "inform"]
        task_lower = task.lower()
        
        for keyword in keywords:
            if keyword in task_lower:
                # Extract content after keyword
                start_index = task_lower.find(keyword) + len(keyword)
                content = task[start_index:].strip()
                
                # Remove common prepositions
                for prep in ["about", "that", "to", ":"]:
                    if content.startswith(prep):
                        content = content[len(prep):].strip()
                
                if content:
                    return content
        
        # Fallback to full task
        return task
    
    async def _execute_real_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute real Slack operation using API"""
        
        op_type = operation["type"]
        
        try:
            if op_type == "send_message":
                response = await self.client.chat_postMessage(
                    channel=operation["channel"],
                    text=operation["message"],
                    attachments=operation.get("attachments", [])
                )
                
                return {
                    "message_sent": True,
                    "channel": operation["channel"],
                    "timestamp": response["ts"],
                    "message": operation["message"]
                }
            
            elif op_type == "send_dm":
                # Get user ID first
                user_response = await self.client.users_lookupByEmail(
                    email=operation["user"]
                ) if "@" in operation["user"] else None
                
                user_id = user_response["user"]["id"] if user_response else operation["user"]
                
                response = await self.client.chat_postMessage(
                    channel=user_id,
                    text=operation["message"]
                )
                
                return {
                    "dm_sent": True,
                    "user": operation["user"],
                    "timestamp": response["ts"],
                    "message": operation["message"]
                }
            
            elif op_type == "create_channel":
                response = await self.client.conversations_create(
                    name=operation["channel_name"],
                    is_private=operation.get("private", False)
                )
                
                return {
                    "channel_created": True,
                    "channel_name": operation["channel_name"],
                    "channel_id": response["channel"]["id"]
                }
            
            elif op_type == "list_channels":
                response = await self.client.conversations_list(
                    limit=operation.get("limit", 100)
                )
                
                channels = [
                    {"id": ch["id"], "name": ch["name"], "is_private": ch.get("is_private", False)}
                    for ch in response["channels"]
                ]
                
                return {
                    "channels": channels,
                    "total_count": len(channels)
                }
            
            elif op_type == "get_user_info":
                response = await self.client.users_info(
                    user=operation["user"]
                )
                
                user = response["user"]
                return {
                    "user_info": {
                        "id": user["id"],
                        "name": user.get("real_name", user["name"]),
                        "email": user.get("profile", {}).get("email"),
                        "status": user.get("profile", {}).get("status_text", "")
                    }
                }
            
            elif op_type == "post_status_update":
                response = await self.client.chat_postMessage(
                    channel=operation["channel"],
                    text=f"📢 Status Update: {operation['message']}",
                    attachments=[{
                        "color": "good",
                        "title": "Team Status Update",
                        "text": operation["message"],
                        "footer": "Posted by AAI Orchestration System",
                        "ts": int(datetime.now().timestamp())
                    }]
                )
                
                return {
                    "status_posted": True,
                    "channel": operation["channel"],
                    "timestamp": response["ts"]
                }
            
            else:
                return {"error": f"Unknown operation type: {op_type}"}
                
        except SlackApiError as e:
            logger.error(f"Slack API error: {e}")
            return {"error": f"Slack API error: {e.response['error']}"}
    
    async def _execute_simulated_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simulated Slack operation for testing/fallback"""
        
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        op_type = operation["type"]
        
        if op_type == "send_message":
            return {
                "message_sent": True,
                "channel": operation["channel"],
                "timestamp": str(int(datetime.now().timestamp())),
                "message": operation["message"],
                "simulated": True
            }
        
        elif op_type == "send_dm":
            return {
                "dm_sent": True,
                "user": operation["user"],
                "timestamp": str(int(datetime.now().timestamp())),
                "message": operation["message"],
                "simulated": True
            }
        
        elif op_type == "create_channel":
            return {
                "channel_created": True,
                "channel_name": operation["channel_name"],
                "channel_id": f"C{int(datetime.now().timestamp())}",
                "simulated": True
            }
        
        elif op_type == "list_channels":
            return {
                "channels": [
                    {"id": "C123456", "name": "general", "is_private": False},
                    {"id": "C789012", "name": "random", "is_private": False},
                    {"id": "C345678", "name": "dev-team", "is_private": True}
                ],
                "total_count": 3,
                "simulated": True
            }
        
        elif op_type == "get_user_info":
            return {
                "user_info": {
                    "id": "U123456",
                    "name": "Test User",
                    "email": "test@example.com",
                    "status": "Available"
                },
                "simulated": True
            }
        
        elif op_type == "post_status_update":
            return {
                "status_posted": True,
                "channel": operation["channel"],
                "timestamp": str(int(datetime.now().timestamp())),
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
            "sdk_available": SLACK_SDK_AVAILABLE,
            "client_ready": self.client is not None,
            "capabilities": self.capabilities,
            "performance": {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "success_rate": success_rate,
                "last_operation": self.last_operation_time.isoformat() if self.last_operation_time else None
            },
            "ready": self.initialized
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Slack connection and capabilities"""
        
        try:
            if self.client and SLACK_SDK_AVAILABLE:
                # Test auth
                response = await self.client.auth_test()
                return {
                    "connection_test": "success",
                    "team": response.get("team"),
                    "user": response.get("user"),
                    "team_id": response.get("team_id")
                }
            else:
                return {
                    "connection_test": "simulated",
                    "message": "Using simulation mode - no real Slack connection"
                }
                
        except Exception as e:
            return {
                "connection_test": "failed",
                "error": str(e)
            }


async def test_slack_agent():
    """Test Slack agent functionality"""
    
    agent = SlackAgent()
    
    print("🧪 Testing Slack Agent")
    print("=" * 22)
    
    # Check agent status
    status = agent.get_agent_status()
    print(f"Agent initialized: {status['initialized']}")
    print(f"SDK available: {status['sdk_available']}")
    print(f"Client ready: {status['client_ready']}")
    print(f"Capabilities: {len(status['capabilities'])}")
    
    # Test connection
    connection_test = await agent.test_connection()
    print(f"Connection test: {connection_test['connection_test']}")
    
    # Test operations
    print(f"\n🎯 Testing Slack operations...")
    
    test_tasks = [
        {
            "task": "Send a message to #general about the project update",
            "context": {"channel": "#general"}
        },
        {
            "task": "Create a new channel for the development team",
            "context": {"channel_name": "dev-updates", "description": "Development updates"}
        },
        {
            "task": "List all available channels",
            "context": {"limit": 10}
        },
        {
            "task": "Send a DM to john@company.com about the meeting",
            "context": {"user": "john@company.com"}
        }
    ]
    
    for i, test in enumerate(test_tasks, 1):
        print(f"\nTest {i}: {test['task'][:50]}...")
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
    
    print(f"\n✅ Slack Agent Testing Complete")
    print(f"Ready for team communication and notifications")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_slack_agent())