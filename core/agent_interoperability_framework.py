"""
AAI Agent Interoperability Framework
Enables standardized communication and data sharing between all enhancement layers.

Provides unified communication protocols, context sharing, cross-agent learning,
and coordination mechanisms for seamless interoperability across the 8 enhancement agents.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
import uuid
import weakref

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of inter-agent messages"""
    CONTEXT_SHARE = "context_share"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    LEARNING_EVENT = "learning_event"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_RESPONSE = "resource_response"
    STATUS_UPDATE = "status_update"
    ERROR_NOTIFICATION = "error_notification"
    WORKFLOW_EVENT = "workflow_event"


class MessagePriority(Enum):
    """Priority levels for messages"""
    CRITICAL = "critical"  # Must be delivered
    HIGH = "high"  # Important for performance
    MEDIUM = "medium"  # Normal priority
    LOW = "low"  # Best effort delivery


class AgentRole(Enum):
    """Roles of agents in the interoperability framework"""
    MEMORY_ENHANCER = "memory_enhancer"
    FOUNDATION_ENHANCER = "foundation_enhancer"
    RESEARCH_ENHANCER = "research_enhancer"
    HYBRID_RAG_ENHANCER = "hybrid_rag_enhancer"
    REASONING_ENHANCER = "reasoning_enhancer"
    TOOL_SELECTION_ENHANCER = "tool_selection_enhancer"
    ORCHESTRATION_ENHANCER = "orchestration_enhancer"
    ARCHITECTURE_ENHANCER = "architecture_enhancer"
    COORDINATOR = "coordinator"
    RESOURCE_MANAGER = "resource_manager"


@dataclass
class AgentMessage:
    """Standardized inter-agent message"""
    message_id: str
    message_type: MessageType
    sender_agent: AgentRole
    recipient_agent: Optional[AgentRole] = None  # None for broadcast
    priority: MessagePriority = MessagePriority.MEDIUM
    payload: Dict[str, Any] = field(default_factory=dict)
    context_id: Optional[str] = None
    workflow_id: Optional[str] = None
    confidence_score: float = 0.70
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: timedelta = field(default_factory=lambda: timedelta(minutes=15))
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class AgentRegistration:
    """Agent registration information"""
    agent_id: str
    agent_role: AgentRole
    capabilities: List[str]
    message_handlers: Dict[MessageType, str]  # message_type -> handler_method
    status: str = "active"
    last_heartbeat: datetime = field(default_factory=datetime.now)
    message_count: int = 0
    error_count: int = 0


@dataclass
class SharedContext:
    """Shared context between agents"""
    context_id: str
    workflow_id: str
    context_data: Dict[str, Any]
    contributors: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    confidence_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class LearningEvent:
    """Cross-agent learning event"""
    event_id: str
    event_type: str
    source_agent: AgentRole
    pattern_data: Dict[str, Any]
    success_metrics: Dict[str, float]
    applicability: Dict[AgentRole, float]  # Relevance score per agent
    timestamp: datetime = field(default_factory=datetime.now)
    validation_status: str = "pending"


class AgentInteroperabilityFramework:
    """
    Unified framework for agent interoperability and communication.
    
    Features:
    - Standardized message passing between all enhancement agents
    - Shared context management with automatic synchronization
    - Cross-agent learning and pattern sharing
    - Coordination protocols for complex workflows
    - Error handling and recovery mechanisms
    - Performance monitoring and optimization
    """
    
    def __init__(self):
        """Initialize agent interoperability framework"""
        
        # Agent registry
        self.registered_agents = {}
        self.agent_capabilities = defaultdict(list)
        
        # Message routing
        self.message_queue = asyncio.Queue()
        self.message_handlers = {}
        self.message_history = deque(maxlen=1000)
        
        # Shared context management
        self.shared_contexts = {}
        self.context_subscriptions = defaultdict(set)
        
        # Cross-agent learning
        self.learning_events = {}
        self.learning_patterns = defaultdict(list)
        self.pattern_effectiveness = defaultdict(float)
        
        # Coordination state
        self.active_workflows = {}
        self.coordination_chains = defaultdict(list)
        
        # Performance tracking
        self.performance_metrics = {
            "total_messages": 0,
            "successful_deliveries": 0,
            "failed_deliveries": 0,
            "average_delivery_time": 0.0,
            "context_shares": 0,
            "learning_events": 0,
            "agent_response_times": defaultdict(list)
        }
        
        # Configuration
        self.max_context_size = 10 * 1024 * 1024  # 10MB
        self.context_ttl = timedelta(hours=2)
        self.heartbeat_interval = timedelta(minutes=1)
        self.message_processing_timeout = 30.0
        
        # Framework state
        self.initialized = False
        self.message_processor_task = None
        self.heartbeat_task = None
        
        # Initialize framework
        asyncio.create_task(self._initialize_framework())
    
    async def _initialize_framework(self):
        """Initialize interoperability framework"""
        
        try:
            # Start message processing
            self.message_processor_task = asyncio.create_task(self._process_messages())
            
            # Start heartbeat monitoring
            self.heartbeat_task = asyncio.create_task(self._monitor_heartbeats())
            
            self.initialized = True
            logger.info("Agent Interoperability Framework initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Agent Interoperability Framework: {e}")
            self.initialized = False
    
    async def register_agent(self,
                           agent_id: str,
                           agent_role: AgentRole,
                           capabilities: List[str],
                           message_handlers: Dict[MessageType, Callable]) -> bool:
        """
        Register an agent with the interoperability framework.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_role: Role of the agent in the system
            capabilities: List of agent capabilities
            message_handlers: Message type to handler mappings
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if agent_id in self.registered_agents:
                logger.warning(f"Agent {agent_id} already registered")
                return False
            
            # Create registration
            registration = AgentRegistration(
                agent_id=agent_id,
                agent_role=agent_role,
                capabilities=capabilities,
                message_handlers={
                    msg_type: handler.__name__ if callable(handler) else str(handler)
                    for msg_type, handler in message_handlers.items()
                }
            )
            
            # Store registration
            self.registered_agents[agent_id] = registration
            self.agent_capabilities[agent_role].extend(capabilities)
            
            # Store actual handlers
            self.message_handlers[agent_id] = message_handlers
            
            logger.info(f"Registered agent {agent_id} with role {agent_role.value}")
            return True
            
        except Exception as e:
            logger.error(f"Agent registration failed: {e}")
            return False
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from the framework.
        
        Args:
            agent_id: Agent to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        try:
            if agent_id not in self.registered_agents:
                logger.warning(f"Agent {agent_id} not registered")
                return False
            
            registration = self.registered_agents[agent_id]
            
            # Remove from registry
            del self.registered_agents[agent_id]
            del self.message_handlers[agent_id]
            
            # Remove from capabilities
            if registration.agent_role in self.agent_capabilities:
                del self.agent_capabilities[registration.agent_role]
            
            # Clean up context subscriptions
            for context_id in list(self.context_subscriptions.keys()):
                self.context_subscriptions[context_id].discard(agent_id)
                if not self.context_subscriptions[context_id]:
                    del self.context_subscriptions[context_id]
            
            logger.info(f"Unregistered agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Agent unregistration failed: {e}")
            return False
    
    async def send_message(self, message: AgentMessage) -> bool:
        """
        Send a message through the interoperability framework.
        
        Args:
            message: Message to send
            
        Returns:
            True if message queued successfully, False otherwise
        """
        try:
            if not self.initialized:
                logger.warning("Framework not initialized")
                return False
            
            # Validate message
            if not await self._validate_message(message):
                return False
            
            # Add to queue
            await self.message_queue.put(message)
            
            # Update metrics
            self.performance_metrics["total_messages"] += 1
            
            logger.debug(f"Queued message {message.message_id} from {message.sender_agent.value}")
            return True
            
        except Exception as e:
            logger.error(f"Message sending failed: {e}")
            return False
    
    async def broadcast_message(self, 
                              message: AgentMessage,
                              exclude_agents: Optional[Set[str]] = None) -> int:
        """
        Broadcast a message to all registered agents.
        
        Args:
            message: Message to broadcast
            exclude_agents: Agents to exclude from broadcast
            
        Returns:
            Number of agents the message was sent to
        """
        try:
            exclude_agents = exclude_agents or set()
            sent_count = 0
            
            for agent_id in self.registered_agents:
                if agent_id not in exclude_agents:
                    # Create copy for each recipient
                    broadcast_msg = AgentMessage(
                        message_id=f"{message.message_id}_bc_{agent_id}",
                        message_type=message.message_type,
                        sender_agent=message.sender_agent,
                        recipient_agent=None,  # Broadcast indicator
                        priority=message.priority,
                        payload=message.payload.copy(),
                        context_id=message.context_id,
                        workflow_id=message.workflow_id,
                        confidence_score=message.confidence_score,
                        timestamp=message.timestamp,
                        ttl=message.ttl
                    )
                    
                    if await self.send_message(broadcast_msg):
                        sent_count += 1
            
            logger.info(f"Broadcasted message to {sent_count} agents")
            return sent_count
            
        except Exception as e:
            logger.error(f"Message broadcast failed: {e}")
            return 0
    
    async def share_context(self,
                          context_id: str,
                          workflow_id: str,
                          context_data: Dict[str, Any],
                          contributor_agent: str,
                          confidence: float = 0.80) -> bool:
        """
        Share context data with other agents.
        
        Args:
            context_id: Unique context identifier
            workflow_id: Associated workflow ID
            context_data: Context data to share
            contributor_agent: Agent contributing the context
            confidence: Confidence in the context data
            
        Returns:
            True if context shared successfully, False otherwise
        """
        try:
            # Check context size
            context_size = len(json.dumps(context_data))
            if context_size > self.max_context_size:
                logger.warning(f"Context too large: {context_size} bytes")
                return False
            
            # Create or update shared context
            if context_id in self.shared_contexts:
                shared_context = self.shared_contexts[context_id]
                shared_context.context_data.update(context_data)
                shared_context.contributors.add(contributor_agent)
                shared_context.updated_at = datetime.now()
                shared_context.confidence_scores[contributor_agent] = confidence
            else:
                shared_context = SharedContext(
                    context_id=context_id,
                    workflow_id=workflow_id,
                    context_data=context_data,
                    contributors={contributor_agent},
                    confidence_scores={contributor_agent: confidence}
                )
                self.shared_contexts[context_id] = shared_context
            
            # Notify subscribed agents
            await self._notify_context_subscribers(context_id, contributor_agent)
            
            # Update metrics
            self.performance_metrics["context_shares"] += 1
            
            logger.info(f"Shared context {context_id} from {contributor_agent}")
            return True
            
        except Exception as e:
            logger.error(f"Context sharing failed: {e}")
            return False
    
    async def subscribe_to_context(self, agent_id: str, context_id: str) -> bool:
        """
        Subscribe an agent to context updates.
        
        Args:
            agent_id: Agent to subscribe
            context_id: Context to subscribe to
            
        Returns:
            True if subscription successful, False otherwise
        """
        try:
            if agent_id not in self.registered_agents:
                logger.warning(f"Agent {agent_id} not registered")
                return False
            
            self.context_subscriptions[context_id].add(agent_id)
            
            # Send current context if available
            if context_id in self.shared_contexts:
                await self._send_context_update(agent_id, context_id)
            
            logger.debug(f"Agent {agent_id} subscribed to context {context_id}")
            return True
            
        except Exception as e:
            logger.error(f"Context subscription failed: {e}")
            return False
    
    async def unsubscribe_from_context(self, agent_id: str, context_id: str) -> bool:
        """
        Unsubscribe an agent from context updates.
        
        Args:
            agent_id: Agent to unsubscribe
            context_id: Context to unsubscribe from
            
        Returns:
            True if unsubscription successful, False otherwise
        """
        try:
            if context_id in self.context_subscriptions:
                self.context_subscriptions[context_id].discard(agent_id)
                
                if not self.context_subscriptions[context_id]:
                    del self.context_subscriptions[context_id]
            
            logger.debug(f"Agent {agent_id} unsubscribed from context {context_id}")
            return True
            
        except Exception as e:
            logger.error(f"Context unsubscription failed: {e}")
            return False
    
    async def get_shared_context(self, context_id: str, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get shared context data.
        
        Args:
            context_id: Context to retrieve
            agent_id: Requesting agent
            
        Returns:
            Context data if available, None otherwise
        """
        try:
            if context_id not in self.shared_contexts:
                return None
            
            shared_context = self.shared_contexts[context_id]
            shared_context.access_count += 1
            
            # Return context with metadata
            return {
                "context_id": context_id,
                "workflow_id": shared_context.workflow_id,
                "data": shared_context.context_data,
                "contributors": list(shared_context.contributors),
                "confidence_scores": shared_context.confidence_scores,
                "created_at": shared_context.created_at.isoformat(),
                "updated_at": shared_context.updated_at.isoformat(),
                "access_count": shared_context.access_count
            }
            
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return None
    
    async def share_learning_event(self, learning_event: LearningEvent) -> bool:
        """
        Share a learning event with relevant agents.
        
        Args:
            learning_event: Learning event to share
            
        Returns:
            True if learning event shared successfully, False otherwise
        """
        try:
            # Store learning event
            self.learning_events[learning_event.event_id] = learning_event
            
            # Update learning patterns
            pattern_key = f"{learning_event.source_agent.value}_{learning_event.event_type}"
            self.learning_patterns[pattern_key].append(learning_event)
            
            # Calculate relevance for each agent
            relevant_agents = [
                agent_role for agent_role, relevance in learning_event.applicability.items()
                if relevance >= 0.75  # Threshold for relevance
            ]
            
            # Send learning event to relevant agents
            sent_count = 0
            for agent_role in relevant_agents:
                # Find registered agents with this role
                for agent_id, registration in self.registered_agents.items():
                    if registration.agent_role == agent_role:
                        message = AgentMessage(
                            message_id=f"learning_{learning_event.event_id}_{agent_id}",
                            message_type=MessageType.LEARNING_EVENT,
                            sender_agent=learning_event.source_agent,
                            recipient_agent=agent_role,
                            priority=MessagePriority.MEDIUM,
                            payload={
                                "learning_event": {
                                    "event_id": learning_event.event_id,
                                    "event_type": learning_event.event_type,
                                    "pattern_data": learning_event.pattern_data,
                                    "success_metrics": learning_event.success_metrics,
                                    "relevance": learning_event.applicability.get(agent_role, 0.0)
                                }
                            },
                            confidence_score=max(learning_event.success_metrics.values()) if learning_event.success_metrics else 0.70
                        )
                        
                        if await self.send_message(message):
                            sent_count += 1
            
            # Update metrics
            self.performance_metrics["learning_events"] += 1
            
            logger.info(f"Shared learning event {learning_event.event_id} with {sent_count} agents")
            return True
            
        except Exception as e:
            logger.error(f"Learning event sharing failed: {e}")
            return False
    
    async def coordinate_workflow(self,
                                workflow_id: str,
                                coordination_plan: Dict[str, Any],
                                coordinator_agent: str) -> bool:
        """
        Coordinate a complex workflow across multiple agents.
        
        Args:
            workflow_id: Unique workflow identifier
            coordination_plan: Plan for workflow coordination
            coordinator_agent: Agent coordinating the workflow
            
        Returns:
            True if coordination initiated successfully, False otherwise
        """
        try:
            # Store workflow state
            self.active_workflows[workflow_id] = {
                "coordinator": coordinator_agent,
                "plan": coordination_plan,
                "status": "active",
                "started_at": datetime.now(),
                "participants": set(),
                "completion_status": {}
            }
            
            # Send coordination requests to participating agents
            participants = coordination_plan.get("participants", [])
            
            for participant in participants:
                # Find agent by role
                for agent_id, registration in self.registered_agents.items():
                    if registration.agent_role.value == participant or agent_id == participant:
                        message = AgentMessage(
                            message_id=f"coord_{workflow_id}_{agent_id}",
                            message_type=MessageType.COORDINATION_REQUEST,
                            sender_agent=AgentRole.COORDINATOR,  # Assuming coordinator role
                            recipient_agent=registration.agent_role,
                            priority=MessagePriority.HIGH,
                            payload={
                                "workflow_id": workflow_id,
                                "coordination_plan": coordination_plan,
                                "participant_role": participant,
                                "coordinator": coordinator_agent
                            },
                            workflow_id=workflow_id,
                            confidence_score=0.85
                        )
                        
                        if await self.send_message(message):
                            self.active_workflows[workflow_id]["participants"].add(agent_id)
            
            logger.info(f"Initiated workflow coordination {workflow_id} with {len(participants)} participants")
            return True
            
        except Exception as e:
            logger.error(f"Workflow coordination failed: {e}")
            return False
    
    async def _validate_message(self, message: AgentMessage) -> bool:
        """Validate a message before processing"""
        
        try:
            # Check TTL
            if datetime.now() > message.timestamp + message.ttl:
                logger.warning(f"Message {message.message_id} expired")
                return False
            
            # Check sender registration
            sender_found = False
            for agent_id, registration in self.registered_agents.items():
                if registration.agent_role == message.sender_agent:
                    sender_found = True
                    break
            
            if not sender_found:
                logger.warning(f"Sender {message.sender_agent.value} not registered")
                return False
            
            # Check recipient if specified
            if message.recipient_agent:
                recipient_found = False
                for registration in self.registered_agents.values():
                    if registration.agent_role == message.recipient_agent:
                        recipient_found = True
                        break
                
                if not recipient_found:
                    logger.warning(f"Recipient {message.recipient_agent.value} not registered")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Message validation failed: {e}")
            return False
    
    async def _process_messages(self):
        """Process messages from the queue"""
        
        while True:
            try:
                # Get message from queue
                message = await self.message_queue.get()
                
                start_time = datetime.now()
                
                # Process message
                success = await self._deliver_message(message)
                
                # Update metrics
                delivery_time = (datetime.now() - start_time).total_seconds()
                current_avg = self.performance_metrics["average_delivery_time"]
                total_messages = self.performance_metrics["total_messages"]
                
                new_avg = (current_avg * (total_messages - 1) + delivery_time) / total_messages
                self.performance_metrics["average_delivery_time"] = new_avg
                
                if success:
                    self.performance_metrics["successful_deliveries"] += 1
                else:
                    self.performance_metrics["failed_deliveries"] += 1
                
                # Add to history
                self.message_history.append({
                    "message_id": message.message_id,
                    "type": message.message_type.value,
                    "sender": message.sender_agent.value,
                    "recipient": message.recipient_agent.value if message.recipient_agent else "broadcast",
                    "success": success,
                    "delivery_time": delivery_time,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Message processing failed: {e}")
                await asyncio.sleep(0.1)  # Brief pause on error
    
    async def _deliver_message(self, message: AgentMessage) -> bool:
        """Deliver a message to its recipient(s)"""
        
        try:
            if message.recipient_agent:
                # Directed message
                return await self._deliver_to_agent(message, message.recipient_agent)
            else:
                # Broadcast message
                success_count = 0
                total_count = 0
                
                for agent_id, registration in self.registered_agents.items():
                    # Skip sender
                    if registration.agent_role == message.sender_agent:
                        continue
                    
                    total_count += 1
                    if await self._deliver_to_agent(message, registration.agent_role):
                        success_count += 1
                
                return success_count > 0  # At least one successful delivery
                
        except Exception as e:
            logger.error(f"Message delivery failed: {e}")
            return False
    
    async def _deliver_to_agent(self, message: AgentMessage, recipient_role: AgentRole) -> bool:
        """Deliver a message to a specific agent"""
        
        try:
            # Find registered agent with the role
            target_agents = [
                (agent_id, registration) for agent_id, registration in self.registered_agents.items()
                if registration.agent_role == recipient_role and registration.status == "active"
            ]
            
            if not target_agents:
                logger.warning(f"No active agents found for role {recipient_role.value}")
                return False
            
            # Use first available agent (could be enhanced with load balancing)
            agent_id, registration = target_agents[0]
            
            # Get message handler
            if agent_id not in self.message_handlers:
                logger.warning(f"No message handlers for agent {agent_id}")
                return False
            
            handlers = self.message_handlers[agent_id]
            if message.message_type not in handlers:
                logger.warning(f"No handler for message type {message.message_type.value} in agent {agent_id}")
                return False
            
            # Call handler
            handler = handlers[message.message_type]
            
            try:
                if callable(handler):
                    # Direct callable
                    result = await asyncio.wait_for(
                        handler(message),
                        timeout=self.message_processing_timeout
                    )
                else:
                    # Handler name - would need agent instance to call
                    logger.warning(f"Handler {handler} is not callable for agent {agent_id}")
                    return False
                
                # Update agent stats
                registration.message_count += 1
                registration.last_heartbeat = datetime.now()
                
                return result is not False  # Handler should return False for failure
                
            except asyncio.TimeoutError:
                logger.warning(f"Message handler timeout for agent {agent_id}")
                registration.error_count += 1
                return False
            except Exception as e:
                logger.error(f"Message handler error for agent {agent_id}: {e}")
                registration.error_count += 1
                return False
                
        except Exception as e:
            logger.error(f"Message delivery to agent failed: {e}")
            return False
    
    async def _notify_context_subscribers(self, context_id: str, contributor_agent: str):
        """Notify subscribers about context updates"""
        
        try:
            if context_id not in self.context_subscriptions:
                return
            
            subscribers = self.context_subscriptions[context_id]
            
            for subscriber_id in subscribers:
                if subscriber_id != contributor_agent:  # Don't notify contributor
                    await self._send_context_update(subscriber_id, context_id)
                    
        except Exception as e:
            logger.error(f"Context notification failed: {e}")
    
    async def _send_context_update(self, agent_id: str, context_id: str):
        """Send context update to a specific agent"""
        
        try:
            if agent_id not in self.registered_agents:
                return
            
            registration = self.registered_agents[agent_id]
            shared_context = self.shared_contexts.get(context_id)
            
            if not shared_context:
                return
            
            message = AgentMessage(
                message_id=f"ctx_update_{context_id}_{agent_id}_{int(datetime.now().timestamp())}",
                message_type=MessageType.CONTEXT_SHARE,
                sender_agent=AgentRole.COORDINATOR,  # Framework as sender
                recipient_agent=registration.agent_role,
                priority=MessagePriority.MEDIUM,
                payload={
                    "context_update": {
                        "context_id": context_id,
                        "workflow_id": shared_context.workflow_id,
                        "data": shared_context.context_data,
                        "contributors": list(shared_context.contributors),
                        "confidence_scores": shared_context.confidence_scores,
                        "updated_at": shared_context.updated_at.isoformat()
                    }
                },
                context_id=context_id,
                workflow_id=shared_context.workflow_id
            )
            
            await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Context update sending failed: {e}")
    
    async def _monitor_heartbeats(self):
        """Monitor agent heartbeats and update status"""
        
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval.total_seconds())
                
                current_time = datetime.now()
                stale_threshold = current_time - (self.heartbeat_interval * 3)  # 3x interval
                
                for agent_id, registration in self.registered_agents.items():
                    if registration.last_heartbeat < stale_threshold:
                        if registration.status == "active":
                            registration.status = "stale"
                            logger.warning(f"Agent {agent_id} marked as stale")
                    else:
                        if registration.status == "stale":
                            registration.status = "active"
                            logger.info(f"Agent {agent_id} recovered from stale status")
                
            except Exception as e:
                logger.error(f"Heartbeat monitoring failed: {e}")
    
    async def update_agent_heartbeat(self, agent_id: str) -> bool:
        """
        Update agent heartbeat timestamp.
        
        Args:
            agent_id: Agent to update
            
        Returns:
            True if heartbeat updated, False otherwise
        """
        try:
            if agent_id in self.registered_agents:
                self.registered_agents[agent_id].last_heartbeat = datetime.now()
                if self.registered_agents[agent_id].status == "stale":
                    self.registered_agents[agent_id].status = "active"
                return True
            return False
            
        except Exception as e:
            logger.error(f"Heartbeat update failed: {e}")
            return False
    
    async def get_framework_status(self) -> Dict[str, Any]:
        """Get comprehensive framework status"""
        
        agent_summary = {}
        for agent_id, registration in self.registered_agents.items():
            agent_summary[agent_id] = {
                "role": registration.agent_role.value,
                "status": registration.status,
                "capabilities": registration.capabilities,
                "message_count": registration.message_count,
                "error_count": registration.error_count,
                "last_heartbeat": registration.last_heartbeat.isoformat()
            }
        
        return {
            "framework_initialized": self.initialized,
            "registered_agents": len(self.registered_agents),
            "agent_details": agent_summary,
            "active_contexts": len(self.shared_contexts),
            "context_subscriptions": len(self.context_subscriptions),
            "active_workflows": len(self.active_workflows),
            "learning_events": len(self.learning_events),
            "message_queue_size": self.message_queue.qsize(),
            "performance_metrics": self.performance_metrics,
            "recent_messages": list(self.message_history)[-10:]  # Last 10 messages
        }
    
    async def cleanup_expired_data(self):
        """Clean up expired contexts and workflows"""
        
        try:
            current_time = datetime.now()
            
            # Clean up expired contexts
            expired_contexts = [
                context_id for context_id, context in self.shared_contexts.items()
                if current_time > context.updated_at + self.context_ttl
            ]
            
            for context_id in expired_contexts:
                del self.shared_contexts[context_id]
                if context_id in self.context_subscriptions:
                    del self.context_subscriptions[context_id]
            
            # Clean up old learning events (keep last 100 per pattern)
            for pattern_key in self.learning_patterns:
                events = self.learning_patterns[pattern_key]
                if len(events) > 100:
                    # Keep most recent 100
                    self.learning_patterns[pattern_key] = sorted(
                        events, key=lambda x: x.timestamp, reverse=True
                    )[:100]
            
            # Clean up completed workflows (older than 1 hour)
            workflow_cutoff = current_time - timedelta(hours=1)
            expired_workflows = [
                workflow_id for workflow_id, workflow in self.active_workflows.items()
                if (workflow.get("status") == "completed" and 
                    workflow.get("completed_at", current_time) < workflow_cutoff)
            ]
            
            for workflow_id in expired_workflows:
                del self.active_workflows[workflow_id]
            
            if expired_contexts or expired_workflows:
                logger.info(f"Cleaned up {len(expired_contexts)} contexts and {len(expired_workflows)} workflows")
                
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
    
    async def shutdown(self):
        """Shutdown interoperability framework"""
        
        try:
            # Cancel background tasks
            if self.message_processor_task:
                self.message_processor_task.cancel()
                try:
                    await self.message_processor_task
                except asyncio.CancelledError:
                    pass
            
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
                try:
                    await self.heartbeat_task
                except asyncio.CancelledError:
                    pass
            
            # Clear data
            self.registered_agents.clear()
            self.shared_contexts.clear()
            self.active_workflows.clear()
            
            logger.info("Agent Interoperability Framework shutdown completed")
            
        except Exception as e:
            logger.error(f"Framework shutdown failed: {e}")


# Initialize global framework instance
agent_interoperability_framework = AgentInteroperabilityFramework()


async def test_agent_interoperability_framework():
    """Test Agent Interoperability Framework functionality"""
    
    framework = AgentInteroperabilityFramework()
    
    print("🧪 Testing Agent Interoperability Framework")
    print("=" * 45)
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    # Test agent registration
    print(f"\n🤝 Testing agent registration...")
    
    async def dummy_handler(message: AgentMessage) -> bool:
        print(f"  Handler received: {message.message_type.value}")
        return True
    
    # Register test agents
    agents_registered = 0
    
    test_agents = [
        (AgentRole.MEMORY_ENHANCER, ["context_management", "learning"]),
        (AgentRole.RESEARCH_ENHANCER, ["web_search", "documentation"]),
        (AgentRole.REASONING_ENHANCER, ["analysis", "decision_making"]),
        (AgentRole.ORCHESTRATION_ENHANCER, ["service_coordination", "workflow"])
    ]
    
    for role, capabilities in test_agents:
        agent_id = f"test_{role.value}"
        handlers = {
            MessageType.CONTEXT_SHARE: dummy_handler,
            MessageType.COORDINATION_REQUEST: dummy_handler,
            MessageType.LEARNING_EVENT: dummy_handler
        }
        
        success = await framework.register_agent(agent_id, role, capabilities, handlers)
        if success:
            agents_registered += 1
            print(f"✅ Registered {role.value}")
    
    print(f"Registered {agents_registered}/{len(test_agents)} agents")
    
    # Test messaging
    print(f"\n📨 Testing message passing...")
    
    test_message = AgentMessage(
        message_id="test_msg_001",
        message_type=MessageType.CONTEXT_SHARE,
        sender_agent=AgentRole.MEMORY_ENHANCER,
        recipient_agent=AgentRole.RESEARCH_ENHANCER,
        payload={"test_data": "context sharing test"},
        confidence_score=0.85
    )
    
    message_sent = await framework.send_message(test_message)
    print(f"Message sent: {message_sent}")
    
    # Wait for processing
    await asyncio.sleep(1)
    
    # Test broadcasting
    print(f"\n📡 Testing message broadcasting...")
    
    broadcast_message = AgentMessage(
        message_id="broadcast_msg_001",
        message_type=MessageType.STATUS_UPDATE,
        sender_agent=AgentRole.COORDINATOR,
        payload={"status": "system_update", "version": "1.0.0"},
        priority=MessagePriority.HIGH
    )
    
    broadcast_count = await framework.broadcast_message(broadcast_message)
    print(f"Broadcast to {broadcast_count} agents")
    
    # Test context sharing
    print(f"\n🔄 Testing context sharing...")
    
    context_data = {
        "command_type": "generate-prp",
        "user_requirements": "authentication system",
        "confidence": 0.90,
        "enhancement_layers": ["memory", "research", "reasoning"]
    }
    
    context_shared = await framework.share_context(
        context_id="test_context_001",
        workflow_id="test_workflow_001",
        context_data=context_data,
        contributor_agent="test_memory_enhancer",
        confidence=0.90
    )
    
    print(f"Context shared: {context_shared}")
    
    # Test context subscription
    subscriber_success = await framework.subscribe_to_context(
        "test_research_enhancer", 
        "test_context_001"
    )
    print(f"Context subscription: {subscriber_success}")
    
    # Test context retrieval
    retrieved_context = await framework.get_shared_context(
        "test_context_001", 
        "test_research_enhancer"
    )
    print(f"Context retrieved: {retrieved_context is not None}")
    
    # Test learning event sharing
    print(f"\n🧠 Testing learning event sharing...")
    
    learning_event = LearningEvent(
        event_id="test_learning_001",
        event_type="pattern_recognition",
        source_agent=AgentRole.RESEARCH_ENHANCER,
        pattern_data={
            "pattern_type": "effective_search_strategy",
            "context": "documentation_lookup",
            "success_rate": 0.92
        },
        success_metrics={"accuracy": 0.92, "efficiency": 0.88},
        applicability={
            AgentRole.RESEARCH_ENHANCER: 0.95,
            AgentRole.HYBRID_RAG_ENHANCER: 0.85,
            AgentRole.MEMORY_ENHANCER: 0.75
        }
    )
    
    learning_shared = await framework.share_learning_event(learning_event)
    print(f"Learning event shared: {learning_shared}")
    
    # Test workflow coordination
    print(f"\n⚙️ Testing workflow coordination...")
    
    coordination_plan = {
        "workflow_type": "enhanced_command_processing",
        "participants": ["memory_enhancer", "research_enhancer", "reasoning_enhancer"],
        "coordination_mode": "sequential",
        "timeout": 30.0
    }
    
    workflow_started = await framework.coordinate_workflow(
        workflow_id="test_workflow_001",
        coordination_plan=coordination_plan,
        coordinator_agent="test_coordinator"
    )
    print(f"Workflow coordination started: {workflow_started}")
    
    # Wait for message processing
    await asyncio.sleep(2)
    
    # Get framework status
    status = await framework.get_framework_status()
    print(f"\n📊 Framework Status:")
    print(f"Registered agents: {status['registered_agents']}")
    print(f"Active contexts: {status['active_contexts']}")
    print(f"Active workflows: {status['active_workflows']}")
    print(f"Learning events: {status['learning_events']}")
    print(f"Total messages: {status['performance_metrics']['total_messages']}")
    print(f"Successful deliveries: {status['performance_metrics']['successful_deliveries']}")
    print(f"Average delivery time: {status['performance_metrics']['average_delivery_time']:.3f}s")
    
    # Cleanup
    await framework.cleanup_expired_data()
    await framework.shutdown()
    
    print(f"\n✅ Agent Interoperability Framework Testing Complete")
    print(f"Standardized communication ready for all enhancement agents")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_interoperability_framework())