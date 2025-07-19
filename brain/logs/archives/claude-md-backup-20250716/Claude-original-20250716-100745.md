# AAI MASTER BRAIN v3.0 - MODULAR INTELLIGENCE SYSTEM
<!-- PROTECTED FILE - Use /init restrictions and version control -->

## 📊 Intelligence Feature Matrix

| Feature                     | Status | Module                    | Phase | Auto-Load |
|-----------------------------|--------|---------------------------|-------|-----------|
| Intent Clustering           | ✅     | intent-engine.md         | 1-3   | Always    |
| Prompt Recipes              | ✅     | prompt-recipes.md        | 1-3   | Always    |
| Tag Taxonomy Evolution      | ✅     | tag-taxonomy.md          | 2-3   | >3 tags   |
| Success Scoring             | ✅     | score-tracker.md         | 3     | Weekly    |
| Decision Correlation        | ✅     | trace-mapping.md         | 2-3   | >3 decisions |
| OpenRouter LLM Integration  | ✅     | openrouter-integration.md| 2-3   | Semantic tasks |
| Neural Decision Mapping     | ✅     | decision-neural.md       | 2-3   | Architectural decisions |
| Example Intelligence        | ✅     | example-engine.md        | 1-3   | Always    |
| SOP Auto-Generation         | ✅     | sop-generator.md         | 3     | Task completion |
| Idea Evaluation             | ✅     | idea-evaluator.md        | 2-3   | Innovation sessions |
| Seamless Pipeline Orchestration | ✅ | seamless-orchestrator.py | 1-3   | Idea input |
| PRP Scaffolding Automation     | ✅ | prp-scaffold.py          | 2-3   | PRP approval |
| Integration-Aware Enhancement  | ✅ | integration-aware-prp-enhancer.py | 2-3 | PRP creation |
| Research-PRP Integration       | ✅ | research-prp-integration.py | 2-3 | Research needed |
| Cross-Folder Analytics         | ✅ | unified-analytics.py     | 3     | Success tracking |
| Supabase Auto-Offload          | ✅ | supabase-integration.md  | 1-3   | Memory >80% |

## 🧠 Phase-Based Module Loading

### Phase 1 (Foundation)
```
@include brain/modules/intent-engine.md
@include brain/modules/prompt-recipes.md
@include brain/modules/example-engine.md
```

### Phase 2 (Intelligence)
```
@include brain/modules/tag-taxonomy.md  
@include brain/modules/trace-mapping.md
@include brain/modules/openrouter-integration.md
@include brain/modules/decision-neural.md
@include brain/modules/idea-evaluator.md
```

### Phase 3 (Optimization)
```
@include brain/modules/score-tracker.md
@include brain/modules/sop-generator.md
```

## 🔧 Core Rules & Triggers

### Essential Principles
- **Documentation is source of truth** - Your knowledge is out of date, freshly scraped documentation is absolute truth, NOT your own knowledge
- **Docker & Self-testing** - Must use Docker CLI, unit tests, everything confirmed working perfectly before delivery
- **Check all Jina scrapes** - Retry failed scrapes until you get actual content, scrape 30-100 pages total
- **Refer to research** - Before implementing features using third-party APIs, use research documentation for accuracy, never assume knowledge
- **Examples are memory bank** - Use `examples/` recommendations before implementing
- **Neural reasoning required** - Include WHY rationale + confidence score (70-95%) for decisions
- **Auto-learning active** - Systems capture patterns from successful implementations
- **Context Engineering** - Follow established PRP workflow (.claude/commands/)
- **Modular Architecture** - Keep files <500 lines, extract complexity to modules
- **CRITICAL: Module Creation Protocol** - Before creating ANY new module:
  1. **Search existing modules** - Check if functionality already exists in `/brain/modules/` and `/brain/workflows/`
  2. **Enhancement over creation** - If similar functionality exists, enhance the existing module instead of creating new
  3. **Collaboration requirement** - If new module needed, design it to collaborate with supporting/related existing modules
  4. **Integration validation** - Ensure new module integrates with existing scoring, tagging, and intelligence systems
  5. **Auto-trigger setup** - Add appropriate triggers to Smart Module Loading for automatic activation
- **Always reference recent learning events** - Before executing any new task, you must:
  - Check `/brain/workflows/feedback-learning.md` for relevant corrections in the past 3 days
  - If a similar error occurred previously, adjust your plan and include a "Lesson Considered" note in your rationale
  - If no relevant entries exist, proceed—but tag the task for possible later review (#learn)
- **Seamless Flow Priority** - Use orchestrated pipeline for idea-to-implementation
- **Research-Driven Implementation** - Auto-integrate research findings into PRPs and projects
- **Integration Intelligence** - Auto-recommend integrations based on PRP analysis
- **Pipeline Contradiction Check** - Run /log status at every stage transition
- **Quality Thresholds** - General ≥0.90, Project ≥0.75, validate before implementation
- **Pattern Promotion** - Auto-upgrade project patterns to general when quality threshold met
- **Dashboard Real-Time Updates** - dashboards/status.md serves as single source of truth for task status
- **Task Verification Protocol** - Always verify file system state before presenting task lists
- **API Token Management** - Break large requests into smaller pieces to avoid token limits
- **Growth Metrics Monitoring** - Track system expansion (files, capabilities, intelligence)
- **Auto-Offload Protocols** - When brain cache >80%, automatically offload older conversations, research docs, and examples to Supabase for searchable persistence
- **Database-First Storage** - Store completed PRPs, research findings, and successful examples in Supabase for cross-session intelligence and pattern detection

### Smart Module Loading
```
if (confidence < 0.85) → load intent-engine.md
if (>3 tags detected) → load tag-taxonomy.md  
if (>3 decisions in session) → load trace-mapping.md
if (semantic analysis needed) → load openrouter-integration.md
if (performance review mode) → load score-tracker.md
if (task completion + score ≥4.0) → run sop-generator.py
if (task starting) → run example-recommendation-engine.py
if (decision required) → apply WHY reasoning + confidence scoring
if (ideation needed) → use cognitive mode switching
if (architectural decisions) → load decision-neural.md
if (user_provides_idea) → load seamless-orchestrator.py + idea-evaluator.md
if (idea_added_to_registry) → load idea-evaluator.md + auto-grade + auto-route
if (prp_creation_mode) → load integration-aware-prp-enhancer.py + research-prp-integration.py
if (prp_approved) → load prp-scaffold.py
if (success_tracking) → load unified-analytics.py
if (pipeline_stage_change) → run /log status (contradiction check)

# v3 PRP Auto-Triggers
if (prp_v3_detected) → parse YAML frontmatter + extract metadata
if (research_topics_found) → trigger research-prp-integration.py
if (example_references_found) → validate examples + update scoring
if (auto_scaffold=true) → trigger prp-scaffold.py automatically
if (prp_completion) → update_examples_scoring + generate_sop_candidate + log_learning_event
if (dependency_conflicts) → run contradiction check + suggest mitigation
if (success_metrics_defined) → track metrics + auto-promote to SOP if threshold met
```

### File Placement Logic
- **Logs** → `/brain/logs/` (interactions, improvements, agent-history)
- **States** → `/brain/states/` (conversation-state.json, project contexts)
- **Workflows** → `/brain/workflows/` (intent-registry.md, prompt-history.md)
- **Modules** → `/brain/modules/` (intelligence capabilities)
- **Cache** → `/brain/cache/` (Supabase-backed volatile memory)
- **Research** → `/research/` (documentation findings - will be structured when implemented)

## 🔬 Research & Documentation Protocols

### Research Requirements
- **Always scrape 30-100 pages total** when doing research
- **Put successful Jina scrapes** in research with tech-named directories and .md/.txt files
- **Stick to OFFICIAL DOCUMENTATION PAGES ONLY** - No outdated tutorials
- **For maximum efficiency** - Invoke multiple tools simultaneously for independent operations
- **Take user's tech specifications as sacred truth** - Research exact model names, API versions specified

### Research Engine Integration
- **Hybrid Architecture**: Single source of truth with organized symlink access
- **Dual Quality System**: General research ≥0.90, Project research ≥0.75
- **Multi-Agent Intelligence**: GeneralResearcher + ProjectResearcher with auto-promotion
- **Semantic Search**: OpenRouter embeddings with keyword fallback
- **Docker + MCP Integration**: Containerized research delegation

### Agent Design Philosophy
- **Agents as intelligent human beings** - Give them decision making, detailed Jina research capabilities
- **Never use programmatic solutions** - Use reasoning and AI decision making for all problems
- **Every agent needs 5+ prompts** in agentic workflow to create unique content
- **Context continuity** - Each agent should have context of previous iterations
- **Dynamic prompts** - Never hardcode examples, make everything dynamic/contextual

## 🏗️ Code Structure & Quality

### Modularity Rules
- **Never create files longer than 500 lines** - Refactor into modules/helpers
- **Organize by feature/responsibility** with clear separation:
  - `agent.py` - Main agent definition and execution logic
  - `tools.py` - Tool functions used by the agent
  - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages)
- **Use python_dotenv and load_env()** for environment variables

### Testing & Reliability
- **Always create Pytest unit tests** for new features (functions, classes, routes)
- **After updating logic** - Check and update existing unit tests
- **Tests live in `/tests` folder** mirroring main app structure
- **Include at least**: 1 expected use test, 1 edge case, 1 failure case
- **Use Docker commands** for all Python execution including unit tests

### Style & Conventions
- **Use Python** as primary language
- **Follow PEP8**, use type hints, format with `black`
- **Use `pydantic` for data validation**
- **Ultrathink capabilities** - Use before PRP generation and code generation stages

## 🎯 Intelligence Triggers

- **Intent Analysis**: Every command → intent-engine classification
- **Pattern Matching**: Recipe selection → prompt-recipes consultation
- **Tag Evolution**: Auto-taxonomy → tag-taxonomy management
- **Correlation Mapping**: Decision networks → trace-mapping analysis
- **Performance Tracking**: Success metrics → score-tracker updates
- **Documentation Intelligence**: Task completion (score ≥4.0) → auto-generate SOP
- **Examples Intelligence**: Before tasks → check recommendations, after tasks → update scoring
- **Neural Reasoning**: Decision required → apply WHY analysis + confidence scoring
- **Creative Optimization**: Ideation sessions → cognitive mode switching (#Innovator/#Critic/#Enhancer/#Logic)
- **Architectural Decisions**: Before making architectural or strategic decisions:
  - Review `/brain/docs/explain.md` for prior rationale
  - Use `/brain/docs/decision-trace.mmd` to visualize existing decision flows
  - If unclear, trigger auto-generation of updated trace (via trace-mapping module)
- **SOP Generation**: After task completion:
  - If task score ≥4.0, generate or update SOP in `/docs/sops/`
  - Use patterns from `examples/` and `PRPs/` to auto-fill SOP steps
  - Cross-reference official guidance from `/docs/official/` before finalizing
- **Ideation Intelligence**: During ideation or strategic planning:
  - Use `/ideas/idea_registry.md` to:
    - Generate prompts via innovation modes: #Innovator, #Critic, #Enhancer, #Logic
    - Score feasibility using success-scoring.md
    - Auto-trigger research if idea meets confidence threshold
- **Examples Intelligence**: Before any new task:
  → Claude must check `/examples/` for matching implementation patterns
  → Prioritize high-scoring examples from `score-tracker.md`
  After task completion:
  → If successful outcome, log implementation snippet to `/examples/` with tags and task type
  → If it involved testing, update or create test in `/examples/tests/`
  Claude must distinguish:
  - `/examples/core/` → Reusable patterns and validated code
  - `/examples/tests/` → Test suites for functional accuracy (linked to PRPs)

## 🧠 Active Learning Behavior
Claude must learn from user corrections, misclassifications, or failed expectations.

Log these events in:
- `/brain/workflows/feedback-learning.md` → tracks user feedback and corrections
- `/brain/modules/success-scoring.md` → stores pattern accuracy over time
- `/brain/workflows/tagging-evolution.md` → tracks tag accuracy and learning

Claude must not modify this file (Claude.md) directly to log learning.

Claude must reference prior corrections during similar future tasks to improve response accuracy.

Reinforce new behavior only after confirmation or successful validation (e.g., via `/log status`)

### Pre-Task Learning Check
Before each newly initiated task:
- Search `/brain/workflows/feedback-learning.md` for similar past mistakes (#learn tag)
- If found, adjust approach and annotate rationale: "Lesson Considered: <summary>"
- If none, tag this task with `#learn` for future analysis

### Examples Auto-Scoring
- Claude should auto-score examples based on usage frequency and success validation
- High-performing examples get tagged as "preferred patterns" and suggested automatically
- If a test fails → trigger log entry and prompt Claude to refine example or flag mismatch

## 🛡️ Protection & Safety
- **Archive-First Protocol**: Backup before any major changes
- **Compatibility-First**: Preserve existing functionality while enhancing
- **Phase-Aware Loading**: Only load needed modules per phase
- **Version Control**: Auto-backup brain/Claude.md before modifications

### Critical Decision Protocols
- **#architecture, #security, #data-safety** → Red alert, mandatory backup
- **#performance, #compatibility, #workflow** → Extended review, impact assessment  
- **#research, #decision, #insight** → Standard processing, batch optimization

## 🎯 Current System Status
- **Phase**: 3 (Optimization Complete) + Seamless Pipeline Intelligence Active
- **Intelligence Maturity**: 96% (Enhanced with pipeline orchestration + growth tracking + idea grading)
- **System Growth**: 397.8% file expansion (46→229 files, 0→34 Python modules)
- **Active Modules**: All 15 modules (10 original + 5 pipeline orchestration)
- **Task Management**: Unified tracking with real-time dashboard accuracy
- **Pipeline Capabilities**: Idea→evaluate→grade→actionize→implement automation
- **Pattern Recognition**: 95% accuracy (Architecture decisions with WHY reasoning)
- **Learning Velocity**: 75% improvement rate + Auto-learning from successes
- **Decision Accuracy**: 88% predicted vs actual outcomes
- **Example Effectiveness**: Auto-scored based on usage feedback

---

### 🧠 SuperClaude Bridge Integration
```
@include brain/modules/superclaude-bridge-v3.md
```
**Auto-Loading Triggers**: Agent architecture, complex workflows (3+ files), error recovery

### 🎪 Seamless Pipeline System
```
@include brain/modules/seamless-orchestrator.py
@include brain/modules/prp-scaffold.py
@include brain/modules/integration-aware-prp-enhancer.py
@include brain/modules/research-prp-integration.py
@include brain/modules/unified-analytics.py
```
**Auto-Loading Triggers**: Idea input, PRP creation, project scaffolding, success tracking

### 🔬 Research Engine System
```
@include research/README.md
@include research/_map/inheritance.md
@include research/validation/scores.json
```
**Auto-Loading Triggers**: Research needed, PRP creation, pattern detection, quality validation

### 📊 Dashboard & Growth Systems
```
@include dashboards/status.md
@include brain/logs/dashboards/growth-metrics.md
@include brain/logs/dashboards/folder-interconnectedness-analysis.md
```
**Auto-Loading Triggers**: Task updates, system growth, completion verification

---

*AAI Master Brain v3.0 | Modular Intelligence | Jarvis-Level Cognition | Context Engineering Enabled*