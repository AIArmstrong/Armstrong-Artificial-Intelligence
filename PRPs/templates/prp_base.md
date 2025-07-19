---
# PRP Metadata - Required for auto-scaffolding and integration
id: prp-<timestamp>
project_name: my_feature
priority: high | medium | low
auto_scaffold: true
integrations: [superclaude, openrouter]
estimated_effort: "2-3 hours"
complexity: simple | moderate | complex | enterprise
tags: ["#feature", "#api", "#enhancement"]
created: <timestamp>
author: <username>
---

name: "Base PRP Template v3 - AI-Optimized with Intelligence Integration"
description: |

## Purpose
Template optimized for AI agents to implement features with sufficient context, self-validation capabilities, and deep integration with AAI brain system to achieve working code through iterative refinement.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md
6. **Intelligence Integration**: Leverage AAI brain modules for enhancement and learning

---

## Goal
[What needs to be built - be specific about the end state and desires]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]
  
- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]
  
- doc: [Library documentation URL] 
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [PRPs/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "FastAPI async routes"
    depth: 10
    target_folder: "projects/my_feature/research/fastapi"
  - topic: "JWT authentication patterns"  
    depth: 5
    target_folder: "projects/my_feature/research/auth"
```

### Example Pattern References
```yaml
example_references:
  - examples/core/auth_patch.py
  - examples/tests/test_feature.py
  - PRPs/successful/similar_feature.md
pattern_similarity_threshold: 0.8
fallback_action: "create_new_example"
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash

```

### Desired Codebase tree with files to be added and responsibility of file
```bash

```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: [Library name] requires [specific setup]
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
# Example: We use pydantic v2 and  
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "src/auth"
      reason: "Uses existing auth patterns"
    - prp: "PRPs/user_management.md"  
      reason: "Builds on user system"
  external:
    - package: "fastapi ≥ 0.100.0"
    - package: "python-jose[cryptography]"
  conflicts:
    - issue: "Breaks existing OAuth flow"
      mitigation: "Add backward compatibility layer"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "src/core/auth.py"
    - "tests/conftest.py"
  api_documentation_current:
    - check: "API docs updated within 30 days"
  example_relevance:
    - similarity_threshold: 0.8
    - fallback: "Create new example if none match"
```

## 📦 Implementation Readiness Assessment

*Auto-generated validation framework to prevent development surprises and ensure all gates are open before implementation begins.*

### 🔧 Auto-Generated Readiness Validation Script
```bash
# Generated script: ./scripts/validate_prp_readiness.py
# Run before implementation to identify blockers
python scripts/validate_prp_readiness.py --prp <prp_id> --report json
```

### 🚪 Implementation Gates

#### Infrastructure Gates
```yaml
infrastructure_gates:
  network_connectivity:
    - service: "external_api_host"
      test: "ping -c 3 <host>"
      expected: "0% packet loss"
      owner: "devops"
      
  service_availability:
    - service: "n8n_server" 
      test: "curl -f http://HOST:PORT/health"
      expected: "200 OK"
      fallback: "Deploy local n8n instance"
      time_to_fix: "15 minutes"
      owner: "user"
      
  port_accessibility:
    - service: "database"
      test: "telnet <host> <port>"
      expected: "Connected"
      fallback: "Check firewall rules"
```

#### Credential Gates
```yaml
credential_gates:
  critical:
    - credential: "API_KEY_NAME"
      location: ".env"
      validation: "curl -H 'Authorization: Bearer $API_KEY' <test_endpoint>"
      expected: "200 or 401 (key format valid)"
      owner: "user"
      expires_in: "30d"
      warned_days_before: 7
      time_to_fix: "5 minutes"
      
    - credential: "OAUTH_REFRESH_TOKEN"
      location: "OAuth setup"
      validation: "test_oauth_refresh.py"
      expected: "Token refresh successful"
      owner: "user"
      setup_guide: "docs/oauth_setup.md"
      time_to_fix: "30 minutes"
      
  optional:
    - credential: "OPTIONAL_SERVICE_KEY"
      fallback: "Degraded functionality - features X,Y disabled"
      impact: "Non-critical features unavailable"
```

#### Dependency Gates
```yaml
system_dependencies:
  python_packages:
    - package: "fastapi>=0.100.0"
      install: "pip install fastapi"
      validation: "python -c 'import fastapi; print(fastapi.__version__)'"
      expected: ">=0.100.0"
      
  external_services:
    - service: "docker"
      validation: "docker --version"
      expected: "Docker version"
      fallback: "Install Docker or use local alternatives"
      
database_gates:
  schema_checks:
    - query: "SELECT to_regclass('public.users');"
      expected: "not null"
      fallback: "Run migration scripts first"
      fix_command: "python manage.py migrate"
      
rate_limit_tests:
  - api_endpoint: "openrouter.ai/api/v1"
    test_requests: 5
    time_window: "1 minute"
    threshold: "60 requests/minute"
    expected: "No 429 errors"
```

#### Environment Gates
```yaml
environment_validation:
  required_directories:
    - path: "logs/"
      create_if_missing: true
    - path: "data/cache/"
      create_if_missing: true
      
  required_files:
    - file: ".env"
      template: ".env.example"
      required_vars: ["API_KEY", "DATABASE_URL"]
      
  configuration_files:
    - file: "config/settings.json"
      validation: "python -c 'import json; json.load(open(\"config/settings.json\"))'"
      expected: "Valid JSON"
```

### 📊 Readiness Scoring & Thresholds

```yaml
readiness_scoring:
  gate_weights:
    infrastructure: 0.35    # Network, services, ports
    credentials: 0.30       # API keys, tokens, auth
    dependencies: 0.20      # Packages, external services  
    environment: 0.15       # Files, directories, config
    
  phase_thresholds:
    Phase_1_Development: 70%   # Can start core development
    Phase_2_Integration: 85%   # Can begin service integration
    Phase_3_Production: 95%    # Ready for production deployment
    
  fallback_strategies:
    90-100%: "Full implementation - all features enabled"
    75-89%: "Core implementation - document deferred features"
    60-74%: "Partial implementation - critical path only"
    <60%: "HALT - fix critical gates first"
```

### 🎯 Readiness Execution Results

```bash
# Example output from validation script:
=====================================
PRP Readiness Assessment: my_feature
=====================================

🏗️  Infrastructure Gates: ⚠️  80% (4/5 passed)
  ✅ Network connectivity to external APIs
  ✅ Database port accessible  
  ✅ Docker service running
  ❌ n8n server health check failed (502 Bad Gateway)
  ⚠️  Redis connection timeout (degraded performance)

🔐 Credential Gates: ❌ 60% (3/5 passed)
  ✅ OPENROUTER_API_KEY valid
  ✅ DATABASE_URL configured
  ❌ N8N_API_KEY missing from .env
  ❌ GMAIL_REFRESH_TOKEN not configured
  ⚠️  JWT_SECRET using default value (security risk)

🔧 Dependency Gates: ✅ 95% (19/20 passed)
  ✅ All Python packages installed
  ✅ Database schema up to date
  ⚠️  Optional package 'redis' not installed

🌍 Environment Gates: ✅ 100% (5/5 passed)
  ✅ All required directories exist
  ✅ Configuration files valid
  ✅ Log directory writable

=====================================
OVERALL READINESS: ⚠️ 78%
RECOMMENDATION: Partial Implementation
BLOCKERS: 2 critical credential issues
TIME TO FIX: ~45 minutes
=====================================

📋 Required Actions (Priority Order):
1. 🔴 Add N8N_API_KEY to .env (user, ~5 min)
   Command: echo "N8N_API_KEY=your_key_here" >> .env
   
2. 🔴 Configure Gmail OAuth refresh token (user, ~30 min)
   Guide: docs/gmail_oauth_setup.md
   
3. 🟡 Restart n8n service on server (user, ~10 min)
   Command: ssh user@server "sudo systemctl restart n8n"
   
4. 🟡 Change JWT_SECRET from default (user, ~2 min)
   Command: Generate secure key and update .env

🎯 Next Steps:
- Fix items 1-2 → Re-run validation
- At ≥85% readiness → Proceed with core implementation
- Document deferred features requiring n8n integration
```

### 🤖 Intelligence-Assisted Adaptation

```yaml
auto_adaptation:
  failed_gate_actions:
    missing_env_var:
      action: "Auto-generate .env stub with placeholder and documentation links"
      script: "scripts/generate_env_template.py"
      
    service_unreachable:
      action: "Check for local alternatives and suggest docker-compose setup"
      fallback: "Generate local development stack"
      
    dependency_missing:
      action: "Auto-generate requirements.txt and installation script"
      script: "scripts/install_dependencies.sh"
      
  historical_learning:
    track_file: "brain/logs/readiness_history.md"
    pattern_recognition: "Identify common failure patterns across PRPs"
    auto_improvement: "Suggest infrastructure improvements based on recurring issues"
```

### 📈 Readiness History & Tracking

```yaml
readiness_tracking:
  history_file: "brain/logs/readiness_history.md"
  
  tracking_metadata:
    - prp_id: "<prp_id>"
      timestamp: "<timestamp>"
      overall_score: "78%"
      critical_failures: ["N8N_API_KEY", "GMAIL_OAUTH"]
      time_to_resolution: "45 minutes"
      
  success_correlation:
    readiness_vs_success: "Track correlation between readiness scores and implementation success"
    common_blockers: "Identify most frequent gate failures"
    optimization_opportunities: "Suggest infrastructure improvements"
    
  notifications:
    slack_webhook: "${SLACK_READINESS_WEBHOOK}"
    github_issues: "Auto-create issues for critical gate failures"
    team_alerts: "Notify relevant team members based on gate ownership"
```

### 🔄 Continuous Readiness Integration

```yaml
ci_integration:
  pre_implementation_hook:
    command: "python scripts/validate_prp_readiness.py --prp ${PRP_ID} --fail-threshold 70"
    on_failure: "Block implementation until gates pass"
    
  post_fix_validation:
    auto_rerun: true
    success_threshold: 85
    notification: "Ready for implementation when threshold met"
    
  development_workflow:
    1: "Generate PRP → Auto-run readiness assessment"
    2: "Fix identified blockers → Re-validate"
    3: "Reach threshold → Proceed with implementation"
    4: "Log results → Update historical patterns"
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.
```python
Examples: 
 - orm models
 - pydantic models
 - pydantic schemas
 - pydantic validators
```

### list of tasks to be completed to fullfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.py:
  - FIND pattern: "class OldImplementation"
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures

CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...
```

### Per task pseudocode as needed added to each task
```python
# Task 1
# Pseudocode with CRITICAL details dont write entire code
async def new_feature(param: str) -> Result:
    # PATTERN: Always validate input first (see src/validators.py)
    validated = validate_input(param)  # raises ValidationError
    
    # GOTCHA: This library requires connection pooling
    async with get_connection() as conn:  # see src/db/pool.py
        # PATTERN: Use existing retry decorator
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # CRITICAL: API returns 429 if >10 req/sec
            await rate_limiter.acquire()
            return await external_api.call(validated)
        
        result = await _inner()
    
    # PATTERN: Standardized response format
    return format_response(result)  # see src/utils/responses.py
```

### Integration Points
```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"
  
CONFIG:
  - add to: config/settings.py
  - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
  
ROUTES:
  - add to: src/api/routes.py  
  - pattern: "router.include_router(feature_router, prefix='/feature')"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check src/new_feature.py --fix  # Auto-fix what's possible
mypy src/new_feature.py              # Type checking

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns
```python
# CREATE test_new_feature.py with these test cases:
def test_happy_path():
    """Basic functionality works"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """Handles timeouts gracefully"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# Run and iterate until passing:
uv run pytest test_new_feature.py -v
# If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
```

### Level 3: Integration Test
```bash
# Start the service
uv run python -m src.main --dev

# Test the endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs at logs/app.log for stack trace
```

### Level 4: Custom Validation Scripts
```yaml
custom_validations:
  security:
    - script: "scripts/security_scan.py"
    - requirements: ["no_hardcoded_secrets", "input_sanitization"]  
  domain:
    - script: "scripts/business_logic_check.py"
    - description: "Validates business rules consistency"
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  performance:
    - metric: "API Response Time"
      target: "≤ 200ms"  
      measurement: "curl -w '%{time_total}'"
      validation_gate: "integration_tests"
  quality:
    - metric: "Test Coverage"
      target: "≥ 85%"
      measurement: "coverage report --show-missing"
      validation_gate: "unit_tests"
  business:
    - metric: "User Satisfaction"
      target: "≥ 4.0/5.0"
      measurement: "post_deploy_survey"
      validation_gate: "production"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md" 
  success_tracker: "brain/modules/score-tracker.md"
  auto_tag: ["#learn", "#prp-success"]
  promotion_threshold: 4.5  # Auto-promote to SOP if score ≥ 4.5
```

### AAI Brain System Integration
```yaml
aai_integration:
  brain_modules:
    - "intent-engine.md"  # For classification
    - "unified-analytics.py"  # For success tracking  
    - "contradiction-check.py"  # For validation
  auto_triggers:
    - on_completion: "update_examples_scoring"
    - on_success: "generate_sop_candidate" 
    - on_failure: "log_learning_event"
```

## Final validation Checklist
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed
- [ ] Success metrics achieved
- [ ] Learning events logged
- [ ] Example patterns updated

---

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't ignore dependency conflicts
- ❌ Don't skip context validation checks
- ❌ Don't forget to update success metrics
- ❌ Don't bypass AAI brain integration hooks