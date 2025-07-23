"""
Specialized Agents for AAI Orchestration

Collection of specialized agents for different service domains,
each with focused toolsets and optimized performance.
"""

__version__ = "1.0.0"

# Import specialized agents with fallback handling
try:
    from .slack_agent import SlackAgent
except ImportError:
    SlackAgent = None

try:
    from .github_agent import GitHubAgent
except ImportError:
    GitHubAgent = None

try:
    from .filesystem_agent import FilesystemAgent
except ImportError:
    FilesystemAgent = None

try:
    from .jina_search_agent import JinaSearchAgent
except ImportError:
    JinaSearchAgent = None

try:
    from .airtable_agent import AirtableAgent
except ImportError:
    AirtableAgent = None

try:
    from .firecrawl_agent import FirecrawlAgent
except ImportError:
    FirecrawlAgent = None

__all__ = [
    "SlackAgent",
    "GitHubAgent", 
    "FilesystemAgent",
    "JinaSearchAgent",
    "AirtableAgent",
    "FirecrawlAgent"
]