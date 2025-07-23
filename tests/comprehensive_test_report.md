# AAI Comprehensive Module Test Report
Generated: 2025-07-20 11:32:37

## Executive Summary
- Total Modules Tested: 33
- Passed: 0 (0.0%)
- Warnings: 19 (57.6%)
- Failed: 14 (42.4%)

### Critical Issues Found: 14
- **unified_intelligence_coordinator**: Import Failure - NameError: name 'defaultdict' is not defined
Traceback (most recent call last):
  File "/mnt/c/Users...
- **dashboard-visualizer**: Import Failure - ModuleNotFoundError: No module named 'matplotlib'
Traceback (most recent call last):
  File "/mnt/c/...
- **enhanced-repository-analyzer**: Import Failure - ModuleNotFoundError: No module named 'core.pattern_registry'
Traceback (most recent call last):
  Fi...
- **github-analyzer**: Import Failure - ModuleNotFoundError: No module named 'docker'
Traceback (most recent call last):
  File "/mnt/c/User...
- **primary_agent**: Import Failure - ModuleNotFoundError: No module named 'agents.orchestration.models.models'; 'agents.orchestration.mod...

### Module Naming Verification
- ✓ mcp-orchestrator.py found (PRP7)
- ✓ tech-stack-expert.py found (PRP8)

## Detailed Results by Module Category

### BRAIN (11 modules)

#### mcp-orchestrator
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/mcp-orchestrator.py
- **Import Time**: 0.519s
- **Issues** (9):
  - High: 9
    - missing_error_handling: {'line': 13, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 23, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 101, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (9):
  - Line 12: Unknown
  - Line 22: Exception handling: except ImportError:
- **Async Issues**: Async function without await, Await in non-async function

#### tech-stack-expert
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/tech-stack-expert.py
- **Import Time**: 0.141s
- **Issues** (14):
  - High: 14
    - missing_error_handling: {'line': 14, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 24, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 130, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (10):
  - Line 13: Unknown
  - Line 23: Exception handling: except ImportError:
- **Async Issues**: Async function without await, Await in non-async function

#### unified_enhancement_loader
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/unified_enhancement_loader.py
- **Import Time**: 0.083s
- **Issues** (11):
  - High: 11
    - missing_error_handling: {'line': 17, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 27, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 109, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (11):
  - Line 26: Unknown
  - Line 111: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### unified_intelligence_coordinator
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py
- **Import Error**: NameError: name 'defaultdict' is not defined
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py", line 1131, in <module>
    unified_intelligence_coordinator = UnifiedIntelligenceCoordinator()
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py", line 123, in __init__
    "mode_usage": defaultdict(int),
                  ^^^^^^^^^^^
NameError: name 'defaultdict' is not defined

- **Issues** (26):
  - Critical: 1
    - Import Failure: NameError: name 'defaultdict' is not defined
Traceback (most recent call last):
...
  - High: 25
    - missing_error_handling: {'line': 17, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 27, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 146, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (7):
  - Line 16: Unknown
  - Line 148: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### analyze_command_handler
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/analyze_command_handler.py
- **Import Time**: 0.030s
- **Issues** (8):
  - High: 7
    - missing_error_handling: {'line': 12, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 51, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 57, 'type': 'Try without except', 'content': 'try:'}...
  - Medium: 1
    - fallback_patterns: {'line': 14, 'type': 'Exception triggering fallback', 'content': 'except ImportE...
- **Fallback Triggers** (1):
  - Line 15: Exception handling: except ImportError:
- **Async Issues**: Async function without await, Await in non-async function

#### analyze_orchestrator
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/analyze_orchestrator.py
- **Import Time**: 0.014s
- **Issues** (21):
  - High: 21
    - missing_error_handling: {'line': 170, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 209, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 237, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (3):
  - Line 474: Unknown
  - Line 579: Unknown
- **Resource Leaks**: Unclosed file handle
- **Async Issues**: Async function without await, Await in non-async function

#### anthropic-docs-integration
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/anthropic-docs-integration.py
- **Import Time**: 0.015s
- **Issues** (2):
  - High: 2
    - missing_error_handling: {'line': 44, 'type': 'Try without except', 'content': 'try:'}...
    - Resource Leak: Unclosed file handle...
- **Resource Leaks**: Unclosed file handle

#### dashboard-visualizer
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/dashboard-visualizer.py
- **Import Error**: ModuleNotFoundError: No module named 'matplotlib'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/brain/modules/dashboard-visualizer.py", line 8, in <module>
    import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'

- **Issues** (3):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'matplotlib'
Traceback (most recent call la...
  - High: 1
    - missing_error_handling: {'line': 59, 'type': 'Bare except clause', 'content': 'except:'}...
  - Medium: 1
    - Integration Issue: Missing comprehensive error handling for AAI integration...

#### enhanced-repository-analyzer
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/enhanced-repository-analyzer.py
- **Import Error**: ModuleNotFoundError: No module named 'core.pattern_registry'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/brain/modules/enhanced-repository-analyzer.py", line 23, in <module>
    from core.pattern_registry import PatternRegistry
ModuleNotFoundError: No module named 'core.pattern_registry'

- **Issues** (21):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'core.pattern_registry'
Traceback (most rec...
  - High: 15
    - missing_error_handling: {'line': 161, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 170, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 231, 'type': 'Try without except', 'content': 'try:'}...
  - Medium: 5
    - resource_management: {'line': 91, 'type': 'Connection without context manager', 'content': 'connect(s...
    - resource_management: {'line': 460, 'type': 'Connection without context manager', 'content': 'connect(...
    - resource_management: {'line': 485, 'type': 'Connection without context manager', 'content': 'connect(...
- **Async Issues**: Async function without await, Await outside async function, Await in non-async function

#### github-analyzer
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/github-analyzer.py
- **Import Error**: ModuleNotFoundError: No module named 'docker'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/brain/modules/github-analyzer.py", line 25, in <module>
    import docker
ModuleNotFoundError: No module named 'docker'

- **Issues** (19):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'docker'
Traceback (most recent call last):...
  - High: 18
    - hardcoded_values: {'line': 908, 'type': 'Hardcoded URL', 'content': '"https://github.com/octocat/H...
    - missing_error_handling: {'line': 134, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 172, 'type': 'Try without except', 'content': 'try:'}...
- **Resource Leaks**: Unclosed file handle, Unclosed connection
- **Async Issues**: Async function without await, Await in non-async function

#### smart-tool-selector
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/brain/modules/smart-tool-selector.py
- **Import Time**: 0.037s
- **Issues** (12):
  - High: 12
    - missing_error_handling: {'line': 13, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 23, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 85, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (12):
  - Line 12: Unknown
  - Line 22: Exception handling: except ImportError:
- **Async Issues**: Async function without await, Await in non-async function

### CORE (5 modules)

#### enhanced_command_processor
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/core/enhanced_command_processor.py
- **Import Time**: 0.016s
- **Issues** (27):
  - High: 19
    - missing_error_handling: {'line': 17, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 29, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 207, 'type': 'Try without except', 'content': 'try:'}...
  - Medium: 8
    - fallback_patterns: {'line': 577, 'type': 'Exception triggering fallback', 'content': 'except Except...
    - fallback_patterns: {'line': 595, 'type': 'Exception triggering fallback', 'content': 'except Except...
    - fallback_patterns: {'line': 613, 'type': 'Exception triggering fallback', 'content': 'except Except...
- **Fallback Triggers** (21):
  - Line 16: Unknown
  - Line 28: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### unified_enhancement_coordinator
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/core/unified_enhancement_coordinator.py
- **Import Time**: 0.015s
- **Issues** (17):
  - High: 17
    - missing_error_handling: {'line': 19, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 30, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 193, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (31):
  - Line 195: Unknown
  - Line 235: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### resource_optimization_manager
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/core/resource_optimization_manager.py
- **Import Time**: 0.014s
- **Issues** (19):
  - High: 19
    - missing_error_handling: {'line': 65, 'type': 'Try without except', 'content': 'class CacheEntry:'}...
    - missing_error_handling: {'line': 154, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 220, 'type': 'Try without except', 'content': 'try:'}...
- **Async Issues**: Async function without await, Await in non-async function

#### agent_interoperability_framework
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/core/agent_interoperability_framework.py
- **Import Time**: 0.018s
- **Issues** (26):
  - High: 26
    - missing_error_handling: {'line': 181, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 212, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 252, 'type': 'Try without except', 'content': 'try:'}...
- **Async Issues**: Async function without await, Await in non-async function

#### realtime_orchestration_monitor
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/core/realtime_orchestration_monitor.py
- **Import Time**: 0.020s
- **Issues** (31):
  - High: 31
    - missing_error_handling: {'line': 22, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 191, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 335, 'type': 'Try without except', 'content': 'try:'}...
- **Async Issues**: Async function without await, Await in non-async function

### MCP (2 modules)

#### server_manager
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/mcp/server_manager.py
- **Import Time**: 0.014s
- **Issues** (14):
  - High: 14
    - hardcoded_values: {'line': 423, 'type': 'Hardcoded URL', 'content': '"http://example.com"'}...
    - missing_error_handling: {'line': 15, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 26, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (24):
  - Line 14: Unknown
  - Line 153: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### health_monitor
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/mcp/health_monitor.py
- **Import Time**: 0.014s
- **Issues** (8):
  - High: 8
    - missing_error_handling: {'line': 97, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 127, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 134, 'type': 'Try without except', 'content': 'try:'}...
- **Async Issues**: Async function without await, Await in non-async function

### AGENTS_ORCH (2 modules)

#### delegation_engine
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/agents/orchestration/delegation_engine.py
- **Import Time**: 0.016s
- **Issues** (5):
  - High: 5
    - missing_error_handling: {'line': 14, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 95, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 525, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (5):
  - Line 581: Exception handling: except Exception as e:
  - Line 582: Exception handling: except Exception as e:
- **Async Issues**: Async function without await, Await in non-async function

#### primary_agent
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/orchestration/primary_agent.py
- **Import Error**: ModuleNotFoundError: No module named 'agents.orchestration.models.models'; 'agents.orchestration.models' is not a package
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/orchestration/primary_agent.py", line 35, in <module>
    from agents.orchestration.models.models import (
ModuleNotFoundError: No module named 'agents.orchestration.models.models'; 'agents.orchestration.models' is not a package

- **Issues** (15):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'agents.orchestration.models.models'; 'agen...
  - High: 13
    - missing_error_handling: {'line': 14, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 29, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 39, 'type': 'Try without except', 'content': 'try:'}...
  - Medium: 1
    - fallback_patterns: {'line': 380, 'type': 'Exception triggering fallback', 'content': 'except Except...
- **Fallback Triggers** (24):
  - Line 13: Unknown
  - Line 71: Unknown
- **Async Issues**: Async function without await, Await in non-async function

### AGENTS_SPEC (4 modules)

#### slack_agent
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/agents/specialized/slack_agent.py
- **Import Time**: 0.025s
- **Issues** (6):
  - High: 6
    - missing_error_handling: {'line': 13, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 88, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 226, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (4):
  - Line 12: Unknown
  - Line 188: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### github_agent
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/agents/specialized/github_agent.py
- **Import Time**: 0.293s
- **Issues** (11):
  - High: 11
    - hardcoded_values: {'line': 37, 'type': 'Hardcoded URL', 'content': '"https://api.github.com"'}...
    - hardcoded_values: {'line': 506, 'type': 'Hardcoded URL', 'content': '"https://github.com/{operatio...
    - hardcoded_values: {'line': 519, 'type': 'Hardcoded URL', 'content': '"https://github.com/{operatio...
- **Fallback Triggers** (5):
  - Line 13: Unknown
  - Line 261: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### filesystem_agent
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/specialized/filesystem_agent.py
- **Import Error**: ModuleNotFoundError: No module named 'aiofiles'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/specialized/filesystem_agent.py", line 15, in <module>
    import aiofiles
ModuleNotFoundError: No module named 'aiofiles'

- **Issues** (14):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'aiofiles'
Traceback (most recent call last...
  - High: 13
    - missing_error_handling: {'line': 99, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 423, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 438, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (2):
  - Line 243: Unknown
  - Line 325: Unknown
- **Resource Leaks**: Unclosed file handle
- **Async Issues**: Async function without await, Await in non-async function

#### jina_search_agent
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/agents/specialized/jina_search_agent.py
- **Import Time**: 0.014s
- **Issues** (15):
  - High: 15
    - hardcoded_values: {'line': 41, 'type': 'Hardcoded URL', 'content': '"https://s.jina.ai"'}...
    - hardcoded_values: {'line': 383, 'type': 'Hardcoded URL', 'content': '"https://r.jina.ai/{target_ur...
    - hardcoded_values: {'line': 427, 'type': 'Hardcoded URL', 'content': '"https://example-{i+1}.com/se...
- **Fallback Triggers** (4):
  - Line 13: Unknown
  - Line 271: Unknown
- **Async Issues**: Async function without await, Await in non-async function

### AGENTS_TECH (2 modules)

#### conversation_engine
- **Status**: WARN
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tech_expert/conversation_engine.py
- **Import Time**: 0.016s
- **Issues** (4):
  - High: 4
    - missing_error_handling: {'line': 14, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 594, 'type': 'Try without except', 'content': 'try:'}...
    - Async Pattern Issue: Async function without await...
- **Fallback Triggers** (3):
  - Line 377: Unknown
  - Line 395: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### recommender
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tech_expert/recommender.py
- **Import Error**: ModuleNotFoundError: No module named 'agents.tech_expert.models.models'; 'agents.tech_expert.models' is not a package
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tech_expert/recommender.py", line 19, in <module>
    from agents.tech_expert.models.models import (
ModuleNotFoundError: No module named 'agents.tech_expert.models.models'; 'agents.tech_expert.models' is not a package

- **Issues** (6):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'agents.tech_expert.models.models'; 'agents...
  - High: 4
    - missing_error_handling: {'line': 13, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 901, 'type': 'Try without except', 'content': 'try:'}...
    - Async Pattern Issue: Async function without await...
  - Medium: 1
    - Integration Issue: Missing comprehensive error handling for AAI integration...
- **Async Issues**: Async function without await, Await in non-async function

### AGENTS_R1 (2 modules)

#### dual_model_agent
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py
- **Import Error**: IndentationError: expected an indented block after 'try' statement on line 36 (dual_model_agent.py, line 37)
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 991, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1129, in get_code
  File "<frozen importlib._bootstrap_external>", line 1059, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py", line 37
    from .reasoning_engine import ReasoningEngine as R1ReasoningEngine
    ^^^^
IndentationError: expected an indented block after 'try' statement on line 36

- **Issues** (22):
  - Critical: 1
    - Import Failure: IndentationError: expected an indented block after 'try' statement on line 36 (d...
  - High: 21
    - missing_error_handling: {'line': 15, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 23, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 35, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (9):
  - Line 14: Unknown
  - Line 34: Unknown
- **Async Issues**: Async function without await, Await in non-async function

#### reasoning_engine
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py
- **Import Error**: IndentationError: expected an indented block after 'try' statement on line 36 (dual_model_agent.py, line 37)
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py", line 16, in <module>
    from .models import (
ImportError: attempted relative import with no known parent package

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py", line 22, in <module>
    from agents.r1_reasoning.models.models import (
  File "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/__init__.py", line 32, in <module>
    from .dual_model_agent import DualModelAgent, AgentTask, AgentResult
  File "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py", line 37
    from .reasoning_engine import ReasoningEngine as R1ReasoningEngine
    ^^^^
IndentationError: expected an indented block after 'try' statement on line 36

- **Issues** (11):
  - Critical: 1
    - Import Failure: IndentationError: expected an indented block after 'try' statement on line 36 (d...
  - High: 10
    - missing_error_handling: {'line': 15, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 27, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 85, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (1):
  - Line 497: Exception handling: except Exception as e:
- **Async Issues**: Async function without await, Await in non-async function

### AGENTS_TOOL (5 modules)

#### confidence_scorer
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tool-selection/confidence_scorer.py
- **Import Error**: IndentationError: expected an indented block after 'try' statement on line 439 (confidence_scorer.py, line 440)
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 991, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1129, in get_code
  File "<frozen importlib._bootstrap_external>", line 1059, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/confidence_scorer.py", line 440
    from .models import ContextAnalysis, FabricPattern, ToolMetadata, PromptContext, ToolCategory
    ^^^^
IndentationError: expected an indented block after 'try' statement on line 439

- **Issues** (6):
  - Critical: 1
    - Import Failure: IndentationError: expected an indented block after 'try' statement on line 439 (...
  - High: 5
    - missing_error_handling: {'line': 12, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 81, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 439, 'type': 'Try without except', 'content': 'try:'}...
- **Async Issues**: Async function without await, Await in non-async function

#### tool_selector
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tool-selection/tool_selector.py
- **Import Error**: IndentationError: expected an indented block after 'try' statement on line 294 (tool_selector.py, line 295)
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 991, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1129, in get_code
  File "<frozen importlib._bootstrap_external>", line 1059, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/tool_selector.py", line 295
    from .models import SelectionResult
IndentationError: expected an indented block after 'try' statement on line 294

- **Issues** (10):
  - Critical: 1
    - Import Failure: IndentationError: expected an indented block after 'try' statement on line 294 (...
  - High: 9
    - missing_error_handling: {'line': 12, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 22, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 26, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (7):
  - Line 332: Exception handling: except Exception as e:
  - Line 333: Exception handling: except Exception as e:
- **Async Issues**: Async function without await, Await in non-async function

#### learning_engine
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tool-selection/learning_engine.py
- **Import Error**: IndentationError: expected an indented block after 'try' statement on line 687 (learning_engine.py, line 688)
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 991, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1129, in get_code
  File "<frozen importlib._bootstrap_external>", line 1059, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/learning_engine.py", line 688
    from .models import ContextAnalysis, ToolSelection, SelectionResult, PromptContext
    ^^^^
IndentationError: expected an indented block after 'try' statement on line 687

- **Issues** (13):
  - Critical: 1
    - Import Failure: IndentationError: expected an indented block after 'try' statement on line 687 (...
  - High: 12
    - missing_error_handling: {'line': 14, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 95, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 204, 'type': 'Try without except', 'content': 'try:'}...
- **Resource Leaks**: Unclosed file handle
- **Async Issues**: Async function without await, Await in non-async function

#### fabric_integrator
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tool-selection/fabric_integrator.py
- **Import Error**: ModuleNotFoundError: No module named 'aiofiles'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/fabric_integrator.py", line 10, in <module>
    import aiofiles
ModuleNotFoundError: No module named 'aiofiles'

- **Issues** (24):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'aiofiles'
Traceback (most recent call last...
  - High: 23
    - hardcoded_values: {'line': 48, 'type': 'Hardcoded URL', 'content': '"https://github.com/danielmies...
    - hardcoded_values: {'line': 353, 'type': 'Hardcoded URL', 'content': '"https://api.github.com/repos...
    - missing_error_handling: {'line': 16, 'type': 'Try without except', 'content': 'try:'}...
- **Fallback Triggers** (6):
  - Line 102: Unknown
  - Line 255: Unknown
- **Resource Leaks**: Unclosed file handle
- **Async Issues**: Async function without await, Await in non-async function

#### prompt_analyzer
- **Status**: FAIL
- **Path**: /mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py
- **Import Error**: ModuleNotFoundError: No module named 'agents.tool_selection'
Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py", line 13, in <module>
    from .models import PromptContext, ContextAnalysis
ImportError: attempted relative import with no known parent package

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/mnt/c/Users/Brandon/AAI/tests/comprehensive_module_test.py", line 290, in test_module_import
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py", line 15, in <module>
    from agents.tool_selection.models import PromptContext, ContextAnalysis
ModuleNotFoundError: No module named 'agents.tool_selection'

- **Issues** (5):
  - Critical: 1
    - Import Failure: ModuleNotFoundError: No module named 'agents.tool_selection'
Traceback (most rec...
  - High: 4
    - missing_error_handling: {'line': 12, 'type': 'Try without except', 'content': 'try:'}...
    - missing_error_handling: {'line': 177, 'type': 'Try without except', 'content': 'try:'}...
    - Async Pattern Issue: Async function without await...
- **Fallback Triggers** (2):
  - Line 222: Exception handling: except Exception as e:
  - Line 277: Unknown
- **Async Issues**: Async function without await, Await in non-async function

## Fallback Analysis
Total fallback occurrences: 201

Fallback triggers by type:
- Unknown: 154 occurrences
  Modules: tech-stack-expert, mcp-orchestrator...
- Exception handling: 43 occurrences
  Modules: tech-stack-expert, mcp-orchestrator...
- Error condition: 4 occurrences
  Modules: unified_enhancement_loader, smart-tool-selector, enhanced_command_processor, mcp-orchestrator...

## Performance Bottlenecks

### Slow Imports (>0.5s): 0

### Large Files (>100KB): 0

## Resource Management Issues
Modules with potential resource leaks: 6
- analyze_orchestrator: Unclosed file handle
- anthropic-docs-integration: Unclosed file handle
- github-analyzer: Unclosed file handle, Unclosed connection
- filesystem_agent: Unclosed file handle
- learning_engine: Unclosed file handle
- fabric_integrator: Unclosed file handle

## AAI Integration Issues
Modules with integration issues: 2
- dashboard-visualizer:
  - Missing comprehensive error handling for AAI integration
- recommender:
  - Missing comprehensive error handling for AAI integration

## Critical Recommendations

### Immediate Actions Required:
1. **Fix Module Naming**:
   - All modules properly named

2. **Fix Critical Import Failures**:
   - unified_intelligence_coordinator: NameError
   - dashboard-visualizer: ModuleNotFoundError
   - enhanced-repository-analyzer: ModuleNotFoundError
   - github-analyzer: ModuleNotFoundError
   - primary_agent: ModuleNotFoundError

3. **Address Resource Leaks**:
   - 6 modules need resource management fixes

4. **Optimize Slow Imports**:
   - 0 modules have slow import times

5. **Fix Async Pattern Issues**:
   - 31 modules have async implementation issues