
# AAI System Import Analysis Report

## Summary
- **Total Python files analyzed**: 409
- **Successfully importable**: 160 (39.1%)
- **Failed imports**: 249 (60.9%)

## Import Success Rate by Directory
- **.**: 2/2 (100.0%)
- **.claude/hooks**: 1/1 (100.0%)
- **.claude/implementations**: 3/3 (100.0%)
- **agents/orchestration**: 3/4 (75.0%)
- **agents/r1_reasoning**: 3/6 (50.0%)
- **agents/specialized**: 4/5 (80.0%)
- **agents/tech_expert**: 3/4 (75.0%)
- **agents/tool-selection**: 1/7 (14.3%)
- **api**: 2/2 (100.0%)
- **brain**: 1/1 (100.0%)
- **brain/docs**: 1/1 (100.0%)
- **brain/logs/archives/superclaude-v2-backup-20250715/test-superclaude**: 1/1 (100.0%)
- **brain/modules**: 20/28 (71.4%)
- **brain/modules/openrouter**: 0/4 (0.0%)
- **core**: 4/6 (66.7%)
- **enhancements/memory**: 2/5 (40.0%)
- **examples/generated/from-tasks**: 2/2 (100.0%)
- **fixes**: 2/2 (100.0%)
- **github-analyzer-legacy/tools**: 3/3 (100.0%)
- **ideas**: 1/1 (100.0%)
- **inference**: 4/4 (100.0%)
- **ingestion/r1_reasoning**: 4/4 (100.0%)
- **interfaces**: 2/2 (100.0%)
- **mcp**: 3/3 (100.0%)
- **n8n**: 1/1 (100.0%)
- **ottomator-agents/TinyDM-agent**: 0/2 (0.0%)
- **ottomator-agents/agentic-rag-knowledge-graph**: 1/1 (100.0%)
- **ottomator-agents/agentic-rag-knowledge-graph/agent**: 3/9 (33.3%)
- **ottomator-agents/agentic-rag-knowledge-graph/ingestion**: 1/4 (25.0%)
- **ottomator-agents/agentic-rag-knowledge-graph/tests**: 2/2 (100.0%)
- **ottomator-agents/agentic-rag-knowledge-graph/tests/agent**: 1/3 (33.3%)
- **ottomator-agents/agentic-rag-knowledge-graph/tests/ingestion**: 1/2 (50.0%)
- **ottomator-agents/ask-reddit-agent**: 0/2 (0.0%)
- **ottomator-agents/crawl4AI-agent**: 0/3 (0.0%)
- **ottomator-agents/crawl4AI-agent-v2**: 0/4 (0.0%)
- **ottomator-agents/crawl4AI-agent-v2/crawl4AI-examples**: 0/5 (0.0%)
- **ottomator-agents/crawl4AI-agent/crawl4AI-examples**: 0/3 (0.0%)
- **ottomator-agents/crawl4AI-agent/studio-integration-version**: 0/2 (0.0%)
- **ottomator-agents/file-agent**: 0/1 (0.0%)
- **ottomator-agents/foundational-rag-agent**: 0/2 (0.0%)
- **ottomator-agents/foundational-rag-agent/agent**: 1/5 (20.0%)
- **ottomator-agents/foundational-rag-agent/database**: 1/4 (25.0%)
- **ottomator-agents/foundational-rag-agent/document_processing**: 1/6 (16.7%)
- **ottomator-agents/foundational-rag-agent/tests**: 1/4 (25.0%)
- **ottomator-agents/foundational-rag-agent/ui**: 0/2 (0.0%)
- **ottomator-agents/genericsuite-app-maker-agent**: 1/3 (33.3%)
- **ottomator-agents/genericsuite-app-maker-agent/gsam_ottomator_agent**: 1/4 (25.0%)
- **ottomator-agents/genericsuite-app-maker-agent/lib**: 4/27 (14.8%)
- **ottomator-agents/genericsuite-app-maker-agent/src**: 1/3 (33.3%)
- **ottomator-agents/google-a2a-agent**: 1/2 (50.0%)
- **ottomator-agents/graphiti-agent**: 0/3 (0.0%)
- **ottomator-agents/lead-generator-agent**: 0/4 (0.0%)
- **ottomator-agents/light-rag-agent/BasicRAG**: 0/4 (0.0%)
- **ottomator-agents/light-rag-agent/LightRAG**: 0/4 (0.0%)
- **ottomator-agents/mcp-agent-army**: 0/1 (0.0%)
- **ottomator-agents/mcp-agent-army/basic-pydantic-mcp-agent**: 0/1 (0.0%)
- **ottomator-agents/mcp-agent-army/studio-integration-version**: 0/2 (0.0%)
- **ottomator-agents/mem0-agent/iterations**: 0/3 (0.0%)
- **ottomator-agents/mem0-agent/studio-integration-version**: 0/2 (0.0%)
- **ottomator-agents/n8n-expert**: 0/1 (0.0%)
- **ottomator-agents/nba-agent**: 0/1 (0.0%)
- **ottomator-agents/nba-agent/agent_trial**: 0/1 (0.0%)
- **ottomator-agents/openai-sdk-agent**: 0/6 (0.0%)
- **ottomator-agents/ottomarkdown-agent**: 0/2 (0.0%)
- **ottomator-agents/pydantic-ai-advanced-researcher**: 0/3 (0.0%)
- **ottomator-agents/pydantic-ai-advanced-researcher/studio-integration-version**: 0/2 (0.0%)
- **ottomator-agents/pydantic-ai-langfuse**: 0/2 (0.0%)
- **ottomator-agents/pydantic-ai-langfuse/iterations**: 0/2 (0.0%)
- **ottomator-agents/pydantic-ai-langgraph-parallelization**: 0/3 (0.0%)
- **ottomator-agents/pydantic-ai-langgraph-parallelization/agents**: 0/5 (0.0%)
- **ottomator-agents/pydantic-ai-langgraph-parallelization/extras**: 0/4 (0.0%)
- **ottomator-agents/pydantic-ai-mcp-agent**: 0/2 (0.0%)
- **ottomator-agents/pydantic-ai-mcp-agent/extras**: 0/4 (0.0%)
- **ottomator-agents/pydantic-ai-mcp-agent/studio-integration-version**: 0/3 (0.0%)
- **ottomator-agents/pydantic-github-agent**: 0/3 (0.0%)
- **ottomator-agents/pydantic-github-agent/studio-integration-version**: 0/2 (0.0%)
- **ottomator-agents/python-local-ai-agent**: 0/2 (0.0%)
- **ottomator-agents/simple-mcp-agent**: 0/2 (0.0%)
- **ottomator-agents/streambuzz-agent**: 1/2 (50.0%)
- **ottomator-agents/streambuzz-agent/agents**: 0/5 (0.0%)
- **ottomator-agents/streambuzz-agent/constants**: 2/3 (66.7%)
- **ottomator-agents/streambuzz-agent/exceptions**: 1/1 (100.0%)
- **ottomator-agents/streambuzz-agent/models**: 1/2 (50.0%)
- **ottomator-agents/streambuzz-agent/routers**: 1/2 (50.0%)
- **ottomator-agents/streambuzz-agent/utils**: 0/4 (0.0%)
- **ottomator-agents/streambuzz-agent/youtube_credentials**: 0/1 (0.0%)
- **ottomator-agents/thirdbrain-mcp-openai-agent**: 1/3 (33.3%)
- **ottomator-agents/thirdbrain-mcp-openai-agent/weather-server-python/src/weather**: 0/2 (0.0%)
- **ottomator-agents/thirdbrain-mcp-openai-agent/wip**: 0/2 (0.0%)
- **ottomator-agents/tweet-generator-agent**: 0/12 (0.0%)
- **ottomator-agents/youtube-summary-agent**: 0/1 (0.0%)
- **ottomator-agents/~sample-python-agent~**: 0/2 (0.0%)
- **ottomator-agents/~voiceflow-dialog-api-integration~**: 0/1 (0.0%)
- **projects/enhanced-repository-analyzer**: 1/1 (100.0%)
- **projects/enhanced-repository-analyzer/agents**: 1/3 (33.3%)
- **projects/enhanced-repository-analyzer/api**: 0/2 (0.0%)
- **projects/enhanced-repository-analyzer/collaborative**: 0/1 (0.0%)
- **projects/enhanced-repository-analyzer/core**: 5/5 (100.0%)
- **projects/enhanced-repository-analyzer/integrations**: 0/2 (0.0%)
- **projects/enhanced-repository-analyzer/ml**: 0/1 (0.0%)
- **projects/enhanced-repository-analyzer/tests**: 2/3 (66.7%)
- **projects/legacy-github-analyzer**: 3/5 (60.0%)
- **projects/test-superclaude**: 1/1 (100.0%)
- **projects/test-superclaude-v3-integration**: 1/1 (100.0%)
- **research/_map**: 2/2 (100.0%)
- **research/_semantic**: 1/1 (100.0%)
- **research/mcp**: 0/1 (0.0%)
- **research/scripts**: 6/6 (100.0%)
- **scripts**: 3/3 (100.0%)
- **supabase/modules**: 3/3 (100.0%)
- **supabase/scripts**: 6/7 (85.7%)
- **superclaude-v3**: 1/1 (100.0%)
- **superclaude-v3/SuperClaude/Hooks**: 1/1 (100.0%)
- **superclaude-v3/setup**: 1/1 (100.0%)
- **superclaude-v3/setup/base**: 2/3 (66.7%)
- **superclaude-v3/setup/components**: 0/5 (0.0%)
- **superclaude-v3/setup/core**: 4/6 (66.7%)
- **superclaude-v3/setup/operations**: 1/5 (20.0%)
- **superclaude-v3/setup/utils**: 3/4 (75.0%)
- **tests**: 6/6 (100.0%)
- **tests/enhancements/memory**: 1/1 (100.0%)
- **vector_store**: 4/4 (100.0%)

## Error Categories

### Missing Dependency (194 files)
- `agents/orchestration/primary_agent.py`: No module named 'agents.orchestration.models.models'; 'agents.orchestration.models' is not a package
- `agents/r1_reasoning/confidence_scorer.py`: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- `agents/r1_reasoning/dual_model_agent.py`: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- `agents/r1_reasoning/reasoning_engine.py`: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- `agents/specialized/filesystem_agent.py`: No module named 'aiofiles'
- `agents/tech_expert/recommender.py`: No module named 'agents.tech_expert.models.models'; 'agents.tech_expert.models' is not a package
- `agents/tool-selection/fabric_integrator.py`: No module named 'aiofiles'
- `agents/tool-selection/learning_engine.py`: No module named 'agents.tool_selection'
- `agents/tool-selection/prompt_analyzer.py`: No module named 'agents.tool_selection'
- `brain/modules/dashboard-visualizer.py`: No module named 'matplotlib'
- ... and 184 more files

### Unknown Error (9 files)
- `agents/tool-selection/__init__.py`: expected an indented block after 'try' statement on line 294 (tool_selector.py, line 295)
- `agents/tool-selection/confidence_scorer.py`: expected an indented block after 'try' statement on line 439 (<unknown>, line 440)
- `agents/tool-selection/tool_selector.py`: expected an indented block after 'try' statement on line 294 (<unknown>, line 295)
- `brain/modules/smart-tool-selector.py`: no running event loop
- `brain/modules/unified_enhancement_loader.py`: no running event loop
- `brain/modules/unified_intelligence_coordinator.py`: name 'AgentMessage' is not defined
- `core/agent_interoperability_framework.py`: no running event loop
- `core/realtime_orchestration_monitor.py`: no running event loop
- `projects/legacy-github-analyzer/comprehensive_analyzer_test.py`: [Errno 2] No such file or directory: '/mnt/c/Users/Brandon/AAI/projects/github-analyzer/test_analysis.log'

### Relative Import Issue (17 files)
- `brain/modules/openrouter/contradictions.py`: attempted relative import with no known parent package
- `enhancements/memory/command_enhancer.py`: attempted relative import with no known parent package
- `enhancements/memory/memory_layer.py`: attempted relative import with no known parent package
- `enhancements/memory/workflow_memory.py`: attempted relative import with no known parent package
- `superclaude-v3/setup/base/installer.py`: attempted relative import with no known parent package
- `superclaude-v3/setup/components/__init__.py`: attempted relative import beyond top-level package
- `superclaude-v3/setup/components/commands.py`: attempted relative import with no known parent package
- `superclaude-v3/setup/components/core.py`: attempted relative import with no known parent package
- `superclaude-v3/setup/components/hooks.py`: attempted relative import with no known parent package
- `superclaude-v3/setup/components/mcp.py`: attempted relative import with no known parent package
- ... and 7 more files

### Missing Attribute (29 files)
- `brain/modules/supabase-cache.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/TinyDM-agent/database.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/ask-reddit-agent/agent_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/crawl4AI-agent/studio-integration-version/pydantic_ai_expert_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/file-agent/file_agent.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/genericsuite-app-maker-agent/gsam_ottomator_agent/gsam_supabase_agent.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/lead-generator-agent/leadgen_agent_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/lead-generator-agent/studio_leadgen_agent_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/mcp-agent-army/studio-integration-version/mcp_agent_army_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- `ottomator-agents/mem0-agent/studio-integration-version/mem0_agent_endpoint.py`: cannot import name 'create_client' from 'supabase' (unknown location)
- ... and 19 more files

## Missing Dependencies (51 unique)
- PyPDF2
- agent
- agents
- aiofiles
- apscheduler
- asyncpg
- asyncpraw
- backoff
- brain
- bs4
- cachetools
- chromadb
- constants
- crawl4ai
- docker
- dotenv
- exceptions
- flask
- github_analyzer
- google
- google_auth_oauthlib
- googleapiclient
- graphiti_core
- groq
- huggingface_hub
- ingestion
- langchain_core
- langfuse
- langgraph
- lib
- lightrag
- llama_index
- logfire
- matplotlib
- mcp
- numpy
- ollama
- opentelemetry
- pptx
- psutil
- pydantic_ai
- pymongo
- speech_recognition
- streamlit
- supabase_utils
- test_module_2971404677243823967
- test_module_476234710954896751
- together
- tweepy
- utils
- uvicorn

## Detailed Failed Imports

### agents/orchestration/primary_agent.py
- **Error Type**: import_error
- **Error**: No module named 'agents.orchestration.models.models'; 'agents.orchestration.models' is not a package
- **Direct Imports**: logging, asyncio, uuid, asyncio
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Union

### agents/r1_reasoning/confidence_scorer.py
- **Error Type**: import_error
- **Error**: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- **Direct Imports**: re, math, logging, asyncio
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Tuple

### agents/r1_reasoning/dual_model_agent.py
- **Error Type**: import_error
- **Error**: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- **Direct Imports**: logging, asyncio, uuid, asyncio
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Union

### agents/r1_reasoning/reasoning_engine.py
- **Error Type**: import_error
- **Error**: No module named 'agents.r1_reasoning.models.models'; 'agents.r1_reasoning.models' is not a package
- **Direct Imports**: asyncio, time, uuid, re, logging
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Tuple

### agents/specialized/filesystem_agent.py
- **Error Type**: import_error
- **Error**: No module named 'aiofiles'
- **Direct Imports**: logging, asyncio, os, shutil, json
- **From Imports**: typing.Dict, typing.List, typing.Any, typing.Optional, datetime.datetime

### agents/tech_expert/recommender.py
- **Error Type**: import_error
- **Error**: No module named 'agents.tech_expert.models.models'; 'agents.tech_expert.models' is not a package
- **Direct Imports**: logging, asyncio, asyncio
- **From Imports**: typing.Dict, typing.List, typing.Any, typing.Optional, typing.Tuple

### agents/tool-selection/__init__.py
- **Error Type**: other_error
- **Error**: expected an indented block after 'try' statement on line 294 (tool_selector.py, line 295)
- **From Imports**: prompt_analyzer.PromptAnalyzer, prompt_analyzer.PromptContext, tool_selector.ToolSelector, tool_selector.ToolSelection, fabric_integrator.FabricIntegrator

### agents/tool-selection/confidence_scorer.py
- **Error Type**: syntax_error
- **Error**: expected an indented block after 'try' statement on line 439 (<unknown>, line 440)

### agents/tool-selection/fabric_integrator.py
- **Error Type**: import_error
- **Error**: No module named 'aiofiles'
- **Direct Imports**: os, logging, json, aiofiles, aiohttp
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Set

### agents/tool-selection/learning_engine.py
- **Error Type**: import_error
- **Error**: No module named 'agents.tool_selection'
- **Direct Imports**: logging, json, asyncio, asyncio
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Tuple

### agents/tool-selection/prompt_analyzer.py
- **Error Type**: import_error
- **Error**: No module named 'agents.tool_selection'
- **Direct Imports**: re, logging, asyncio
- **From Imports**: typing.List, typing.Dict, typing.Any, typing.Optional, typing.Tuple

### agents/tool-selection/tool_selector.py
- **Error Type**: syntax_error
- **Error**: expected an indented block after 'try' statement on line 294 (<unknown>, line 295)

### brain/modules/dashboard-visualizer.py
- **Error Type**: import_error
- **Error**: No module named 'matplotlib'
- **Direct Imports**: json, matplotlib.pyplot, matplotlib.patches, numpy, os
- **From Imports**: matplotlib.patches.Circle, matplotlib.patches.Wedge, matplotlib.patches.Rectangle, datetime.datetime

### brain/modules/enhanced-repository-analyzer.py
- **Error Type**: import_error
- **Error**: No module named 'agents.structure_agent'
- **Direct Imports**: asyncio, json, logging, sqlite3, time
- **From Imports**: datetime.datetime, pathlib.Path, typing.Any, typing.Dict, typing.List

### brain/modules/github-analyzer.py
- **Error Type**: import_error
- **Error**: No module named 'docker'
- **Direct Imports**: asyncio, ast, json, logging, os
- **From Imports**: dataclasses.dataclass, dataclasses.asdict, datetime.datetime, datetime.timezone, pathlib.Path

### brain/modules/openrouter/__init__.py
- **Error Type**: import_error
- **Error**: No module named 'dotenv'
- **From Imports**: router_client.OpenRouterClient, router_client.get_openrouter_client, embeddings.EmbeddingsEngine, embeddings.find_similar_patterns, embeddings.cache_current_intent

### brain/modules/openrouter/contradictions.py
- **Error Type**: import_error
- **Error**: attempted relative import with no known parent package
- **Direct Imports**: json, asyncio
- **From Imports**: datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

### brain/modules/openrouter/embeddings.py
- **Error Type**: import_error
- **Error**: No module named 'numpy'
- **Direct Imports**: json, asyncio, numpy
- **From Imports**: datetime.datetime, typing.List, typing.Dict, typing.Tuple, typing.Optional

### brain/modules/openrouter/router_client.py
- **Error Type**: import_error
- **Error**: No module named 'dotenv'
- **Direct Imports**: os, time, json, asyncio, aiohttp
- **From Imports**: datetime.datetime, typing.List, typing.Dict, typing.Any, typing.Optional

### brain/modules/seamless-orchestrator.py
- **Error Type**: import_error
- **Error**: No module named 'brain.modules.unified_analytics'
- **Direct Imports**: json, os, subprocess, sys, re
- **From Imports**: pathlib.Path, typing.Dict, typing.List, typing.Optional, typing.Any

*... and 229 more failed imports*

## Prioritized Fix Recommendations
1. **Install Missing Dependencies** (51 packages)
3. **Resolve Relative Import Issues** (17 files)
5. **Review Module Structure and Dependencies**
