---
# PRP Metadata - Required for auto-scaffolding and integration
id: research-task-automation-2025-07-15
project_name: research_task_automation
priority: high
auto_scaffold: true
integrations: [superclaude, openrouter, jina]
estimated_effort: "3-4 hours"
complexity: moderate
tags: ["#research", "#automation", "#prp", "#integration"]
created: 2025-07-15T19:30:00Z
author: AAI System
---

name: "Research Task Automation PRP - Seamless Idea to Implementation"
description: |
  Implement automatic PRP generation for research tasks using the seamless orchestrator's idea-to-implementation pipeline, ensuring all research follows structured PRP workflow.

## Purpose
Create an automated system that converts research ideas into structured PRPs, leverages the seamless orchestrator for implementation, and ensures consistent research-to-implementation workflows throughout the AAI system.

## Core Principles
1. **Seamless Integration**: All research tasks flow through PRP → implementation pipeline
2. **Structured Research**: Every research idea gets proper PRP treatment with context and validation
3. **Orchestrated Implementation**: Use seamless orchestrator for end-to-end execution
4. **Quality Assurance**: Apply 95% quality thresholds throughout research pipeline
5. **Documentation Integration**: Leverage Anthropic docs for research best practices

## Goal
Build a system that automatically:
- Converts research ideas into comprehensive PRPs
- Triggers seamless orchestrator for implementation
- Applies research validation and quality checks
- Generates research projects with full context and documentation

## Why
- **Consistency**: Ensures all research follows proven PRP methodology
- **Quality**: Applies structured validation to research tasks
- **Efficiency**: Automates research-to-implementation pipeline
- **Integration**: Seamlessly connects research with AAI brain systems
- **Scalability**: Enables systematic research scaling with quality controls

## What
An automated research task system that:
1. Detects research needs from idea inputs
2. Generates comprehensive PRPs for research tasks
3. Triggers seamless orchestrator implementation
4. Applies validation and quality checkpoints
5. Integrates with existing AAI brain modules

### Success Criteria
- [ ] Research ideas automatically generate structured PRPs
- [ ] Seamless orchestrator integration for research implementation
- [ ] Quality validation applied throughout research pipeline
- [ ] Research results integrate with AAI brain systems
- [ ] Comprehensive documentation and context capture

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- file: brain/modules/seamless-orchestrator.py
  why: Core orchestration patterns and idea-to-implementation pipeline
  
- file: PRPs/templates/prp_base.md
  why: PRP structure patterns and validation requirements
  
- file: brain/Claude.md
  why: AAI brain integration patterns and module loading triggers
  
- docfile: docs/official/anthropic/prompt-engineering/overview.md
  why: Research prompt optimization guidelines
  
- docfile: docs/official/anthropic/claude/tool-use.md
  why: Tool integration patterns for research automation
```

### Research & Context Linking
```yaml
research_topics:
  - topic: "PRP automation patterns"
    depth: 8
    target_folder: "research/prp-automation"
  - topic: "Seamless orchestrator integration"
    depth: 7
    target_folder: "research/orchestration"
  - topic: "Research validation methodologies"
    depth: 6
    target_folder: "research/validation"
```

### Example Pattern References
```yaml
example_references:
  - brain/modules/seamless-orchestrator.py
  - brain/modules/prp-scaffold.py
  - brain/modules/research-prp-integration.py
pattern_similarity_threshold: 0.8
fallback_action: "create_new_research_pattern"
```

### Current Codebase tree
```bash
AAI/
├── brain/modules/
│   ├── seamless-orchestrator.py        # Core orchestration
│   ├── research-prp-integration.py     # Research integration
│   └── prp-scaffold.py                 # PRP scaffolding
├── PRPs/
│   ├── templates/prp_base.md           # PRP template
│   └── research-task-automation.md     # This PRP
└── research/
    ├── _map/                           # Research organization
    └── validation/                     # Research validation
```

### Desired Codebase tree with files to be added
```bash
AAI/
├── brain/modules/
│   ├── research-task-detector.py       # Detects research needs
│   ├── research-prp-generator.py       # Auto-generates research PRPs
│   └── research-orchestrator.py        # Research-specific orchestration
├── research/
│   ├── automation/                     # Research automation tools
│   ├── templates/                      # Research PRP templates
│   └── validation/                     # Research validation frameworks
└── scripts/
    └── auto-research.py                # CLI for research automation
```

### Known Gotchas & Integration Points
```python
# CRITICAL: Seamless orchestrator requires proper idea evaluation
# Example: Research ideas need feasibility scoring before PRP generation
# Example: Integration with AAI brain modules requires proper trigger configuration

# Research validation requires structured criteria
# Example: Research quality thresholds must align with AAI 95% standard
# Example: Research context must be comprehensive for successful implementation

# PRP scaffolding needs research-specific templates
# Example: Research PRPs have different validation criteria than feature PRPs
# Example: Research projects require different folder structures and dependencies
```

## Dependencies & Integration

### Dependency Graph
```yaml
dependencies:
  internal:
    - module: "brain/modules/seamless-orchestrator.py"
      reason: "Core idea-to-implementation pipeline"
    - module: "brain/modules/prp-scaffold.py"
      reason: "PRP scaffolding and project creation"
    - module: "brain/modules/research-prp-integration.py"
      reason: "Research integration patterns"
  external:
    - package: "jina-ai >= 0.9.0"
      reason: "Research content scraping and analysis"
    - package: "openrouter-api"
      reason: "Research analysis and validation"
  aai_brain:
    - module: "intent-engine.md"
      reason: "Research intent classification"
    - module: "unified-analytics.py"
      reason: "Research success tracking"
  conflicts:
    - issue: "Research tasks bypass PRP workflow"
      mitigation: "Auto-detection and PRP generation for all research"
```

### Context Validation Checks
```yaml
context_validation:
  required_files_exist:
    - "brain/modules/seamless-orchestrator.py"
    - "PRPs/templates/prp_base.md"
    - "docs/official/anthropic/prompt-engineering/overview.md"
  integration_points_verified:
    - seamless_orchestrator_integration: "Idea evaluation and PRP generation"
    - aai_brain_integration: "Module loading and trigger configuration"
  research_infrastructure:
    - research_folder_structure: "Organized research storage and retrieval"
    - validation_framework: "Quality checkpoints and success criteria"
```

## Implementation Blueprint

### Data models and structure

Create research automation data models for consistency and validation.
```python
# Research task data models
@dataclass
class ResearchTask:
    id: str
    title: str
    description: str
    research_type: str  # "documentation", "analysis", "validation", "integration"
    priority: str       # "high", "medium", "low"
    estimated_effort: str
    context_requirements: List[str]
    validation_criteria: List[str]
    integration_points: List[str]

@dataclass 
class ResearchPRP:
    research_task: ResearchTask
    prp_content: str
    metadata: Dict
    validation_checklist: List[str]
    implementation_plan: Dict
    success_criteria: List[str]

@dataclass
class ResearchProject:
    prp: ResearchPRP
    project_path: str
    orchestration_result: Dict
    validation_results: Dict
    integration_status: str
```

### List of tasks to be completed in order

```yaml
Task 1:
CREATE brain/modules/research-task-detector.py:
  - IMPLEMENT ResearchTaskDetector class
  - ADD idea classification for research detection
  - INTEGRATE with intent-engine for research identification
  - PATTERN: Mirror existing intent classification patterns

Task 2:
CREATE brain/modules/research-prp-generator.py:
  - IMPLEMENT ResearchPRPGenerator class
  - ADD research-specific PRP templates
  - INTEGRATE with prp_base.md structure
  - PATTERN: Follow existing PRP generation patterns

Task 3:
MODIFY brain/modules/seamless-orchestrator.py:
  - ADD research-specific orchestration paths
  - INTEGRATE research validation checkpoints
  - PRESERVE existing orchestration functionality
  - PATTERN: Extend without breaking existing workflows

Task 4:
CREATE research/automation/research-orchestrator.py:
  - IMPLEMENT research-specific orchestration logic
  - ADD research validation frameworks
  - INTEGRATE with seamless orchestrator
  - PATTERN: Specialized orchestrator for research domain

Task 5:
CREATE scripts/auto-research.py:
  - IMPLEMENT CLI for research automation
  - ADD research task triggers and monitoring
  - INTEGRATE with AAI brain modules
  - PATTERN: Follow existing script patterns

Task 6:
UPDATE brain/Claude.md:
  - ADD research automation triggers
  - INTEGRATE research-prp pipeline loading
  - PRESERVE existing brain functionality
  - PATTERN: Extend brain capabilities without conflicts
```

### Per task pseudocode

```python
# Task 1: Research Task Detector
class ResearchTaskDetector:
    def detect_research_need(self, idea_text: str) -> Optional[ResearchTask]:
        # PATTERN: Use intent classification for research detection
        research_indicators = ["research", "analyze", "investigate", "study", "documentation"]
        
        if any(indicator in idea_text.lower() for indicator in research_indicators):
            # CRITICAL: Apply structured classification
            return self._classify_research_task(idea_text)
        
        return None
    
    def _classify_research_task(self, idea_text: str) -> ResearchTask:
        # PATTERN: Apply research taxonomy for classification
        # GOTCHA: Must align with AAI research categories
        research_type = self._determine_research_type(idea_text)
        priority = self._assess_research_priority(idea_text)
        
        return ResearchTask(
            id=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=self._extract_research_title(idea_text),
            description=idea_text,
            research_type=research_type,
            priority=priority,
            estimated_effort=self._estimate_research_effort(idea_text),
            context_requirements=self._extract_context_needs(idea_text),
            validation_criteria=self._generate_validation_criteria(research_type),
            integration_points=self._identify_integration_points(idea_text)
        )

# Task 2: Research PRP Generator
class ResearchPRPGenerator:
    def generate_research_prp(self, research_task: ResearchTask) -> ResearchPRP:
        # PATTERN: Use prp_base.md template with research extensions
        prp_content = self._build_research_prp_content(research_task)
        
        # CRITICAL: Apply research-specific validation requirements
        validation_checklist = self._create_research_validation_checklist(research_task)
        
        return ResearchPRP(
            research_task=research_task,
            prp_content=prp_content,
            metadata=self._generate_prp_metadata(research_task),
            validation_checklist=validation_checklist,
            implementation_plan=self._create_implementation_plan(research_task),
            success_criteria=self._define_success_criteria(research_task)
        )

# Task 3: Seamless Orchestrator Integration  
def process_research_idea(self, idea_text: str, context: Optional[Dict] = None) -> Dict:
    # PATTERN: Extend existing idea processing with research detection
    
    # Check if this is a research task
    research_task = self.research_detector.detect_research_need(idea_text)
    
    if research_task:
        # Use research-specific orchestration
        return self._process_research_task(research_task, context)
    else:
        # Use existing idea processing
        return self.process_idea(idea_text, context)
```

### Integration Points
```yaml
AAI_BRAIN:
  - trigger: "research_intent_detected"
    action: "load_research_automation_modules"
    modules: ["research-task-detector.py", "research-prp-generator.py"]
  
SEAMLESS_ORCHESTRATOR:
  - extension: "research_task_processing"
    integration: "research-specific orchestration paths"
    validation: "research quality checkpoints"
  
PRP_SYSTEM:
  - enhancement: "research_prp_templates"
    integration: "research-specific validation criteria"
    automation: "auto-generation from research tasks"

DOCUMENTATION:
  - integration: "anthropic_prompt_engineering_guidelines"
    application: "research prompt optimization"
    reference: "docs/official/anthropic/prompt-engineering/"
```

## Validation Loop

### Level 1: Research Detection & Classification
```bash
# Validate research task detection
python3 -c "
from brain.modules.research_task_detector import ResearchTaskDetector
detector = ResearchTaskDetector()
result = detector.detect_research_need('Research Anthropic documentation patterns')
assert result is not None and result.research_type == 'documentation'
print('✅ Research detection working')
"
```

### Level 2: PRP Generation & Validation
```python
# Test research PRP generation
def test_research_prp_generation():
    """Research PRP generation produces valid PRPs"""
    generator = ResearchPRPGenerator()
    research_task = ResearchTask(...)
    
    prp = generator.generate_research_prp(research_task)
    
    assert prp.prp_content is not None
    assert len(prp.validation_checklist) > 0
    assert prp.success_criteria is not None
    
def test_research_validation_criteria():
    """Research validation meets AAI quality standards"""
    # Apply 95% quality threshold to research validation
    validation_score = validate_research_quality(research_prp)
    assert validation_score >= 0.95
```

### Level 3: Orchestration Integration Test
```bash
# Test seamless orchestrator integration
python3 brain/modules/seamless-orchestrator.py "Research tmux orchestrator patterns for AAI integration"

# Expected: Research task detected, PRP generated, research project created
# Validation: Check research project structure and documentation
```

### Level 4: End-to-End Research Pipeline
```bash
# Test complete research automation pipeline
python3 scripts/auto-research.py --idea "Research SuperClaude personas for testing framework" --validate

# Expected: 
# 1. Research task detected and classified
# 2. Research PRP generated with proper structure
# 3. Research project scaffolded via orchestrator
# 4. Research validation checkpoints passed
# 5. Integration with AAI brain systems confirmed
```

## Success Metrics & Tracking

### Success Metrics Tracker
```yaml
success_metrics:
  automation:
    - metric: "Research Detection Accuracy"
      target: "≥ 95%"
      measurement: "correct_research_classifications / total_ideas"
      validation_gate: "research_detection_tests"
  quality:
    - metric: "Research PRP Quality Score"
      target: "≥ 95%"
      measurement: "comprehensive_prp_validation_score"
      validation_gate: "prp_generation_tests"
  integration:
    - metric: "Orchestration Success Rate"
      target: "≥ 90%"
      measurement: "successful_research_implementations / total_research_prps"
      validation_gate: "end_to_end_tests"
  productivity:
    - metric: "Research-to-Implementation Time"
      target: "≤ 2 hours"
      measurement: "time_from_idea_to_working_research_project"
      validation_gate: "performance_benchmarks"
```

### Learning & Feedback Integration
```yaml
learning_integration:
  feedback_file: "brain/workflows/feedback-learning.md"
  success_tracker: "brain/modules/score-tracker.md"
  auto_tag: ["#research", "#automation", "#prp", "#learn"]
  promotion_threshold: 4.5  # Auto-promote research patterns to general if score ≥ 4.5
```

### AAI Brain System Integration
```yaml
aai_integration:
  brain_modules:
    - "intent-engine.md"     # Research intent classification
    - "unified-analytics.py" # Research success tracking
    - "research-prp-integration.py" # Research-PRP coordination
  auto_triggers:
    - on_research_completion: "update_research_patterns"
    - on_research_success: "promote_research_methodology"
    - on_research_failure: "log_research_learning_event"
  anthropic_docs_integration:
    - on_research_start: "apply_prompt_engineering_guidelines"
    - on_validation: "reference_anthropic_best_practices"
    - on_analysis: "use_structured_reasoning_patterns"
```

## Final validation Checklist
- [ ] Research detection classifies ideas correctly: `python3 -m pytest tests/test_research_detection.py -v`
- [ ] Research PRP generation meets quality standards: `python3 -m pytest tests/test_research_prp_generation.py -v`
- [ ] Seamless orchestrator integration works: `python3 tests/test_research_orchestration.py`
- [ ] Research validation applies 95% quality threshold: `python3 tests/test_research_validation.py`
- [ ] AAI brain integration triggers properly: `python3 tests/test_brain_research_integration.py`
- [ ] Anthropic documentation patterns applied: Manual validation of research prompts and analysis
- [ ] End-to-end research pipeline functional: `python3 scripts/test_research_pipeline.py`
- [ ] Research success metrics tracked: Verify analytics integration
- [ ] Research learning events logged: Check feedback-learning.md updates

---

## Anti-Patterns to Avoid
- ❌ Don't bypass PRP workflow for "simple" research tasks
- ❌ Don't skip validation because research "should work"
- ❌ Don't ignore research quality thresholds
- ❌ Don't create research projects without proper context
- ❌ Don't forget to integrate with AAI brain systems
- ❌ Don't ignore Anthropic documentation best practices
- ❌ Don't skip orchestrator integration for research tasks
- ❌ Don't bypass research success tracking and learning

*This PRP ensures all research tasks flow through the proven idea-to-implementation pipeline with proper validation, integration, and quality controls.*