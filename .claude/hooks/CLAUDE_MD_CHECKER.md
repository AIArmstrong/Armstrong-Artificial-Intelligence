# Advanced Claude.md Compliance Checker Hook

**Version**: 1.0  
**Created**: July 16, 2025  
**Integration**: Pre-tool execution hook with intelligent compliance monitoring

## 🎯 Overview

The Claude.md Checker Hook implements a sophisticated compliance monitoring system that automatically checks Claude.md rules before every task execution. It features context-aware rule triggering, relevance scoring, and intelligent compliance monitoring.

## 🚀 Features Implemented

### 🧠 1. Context-Aware Rule Triggering
- **Session Context Extraction**: Automatically detects current tool, intent tags, phase, and task type
- **Relevance Scoring**: Prioritizes rules based on current context using semantic embeddings
- **Smart Rule Loading**: Only highlights relevant sections instead of reading entire file

### 📚 2. Rule Relevance Scoring Algorithm
```python
Relevance Score = base_relevance(0.3) + 
                 phase_match(0.3) + 
                 intent_tags(0.2 * matches) + 
                 usage_frequency(0.1) + 
                 recency_bonus(0.1) + 
                 compliance_score(0.1)
```

### ⏳ 3. Time-Sensitive Rule Management
- **Automatic Timestamps**: Every rule gets creation and last-updated timestamps
- **Stale Rule Detection**: Identifies rules not used in 30+ days
- **Version Hashing**: Tracks rule changes with MD5 hashes
- **Usage Analytics**: Monitors rule usage frequency and patterns

### ⚠️ 4. Three-Tier Alert System
- **❗ CRITICAL**: Violations block progression (Docker, Testing, Security, Backup)
- **⚠️ ADVISORY**: Warnings logged but can be overridden (Code quality, Documentation)
- **ℹ️ INFO**: Informational notices for awareness

### 🔄 5. Enforcement + Action Suggestions
- **Smart Suggestions**: When rules are violated, provides specific next steps
- **Auto-Detection**: Checks for Docker availability, test existence, backup needs
- **Contextual Actions**: Tailored recommendations based on current operation

### 🗓️ 6. Pre-Flight Compliance Checks
Before any multi-step operation:
- Summarizes relevant rules for current context
- Performs compliance validation
- Shows critical violations (blocking) and advisory warnings (non-blocking)
- Provides clear guidance on required actions

### 📊 7. Comprehensive Audit Trail
- **Compliance Logging**: Every rule check logged to `brain/logs/rule-compliance.log`
- **Usage Tracking**: Monitors which rules are followed, violated, or skipped
- **Performance Metrics**: Tracks compliance scores and rule effectiveness
- **Session Correlation**: Links compliance events to specific sessions

### 🛠️ 8. Auto-Refinement System
- **Compliance Score Tracking**: Rules get scored based on follow-through
- **Stale Rule Flagging**: Identifies potentially outdated rules
- **Usage Pattern Analysis**: Suggests rule priority adjustments
- **Maintenance Recommendations**: Proposes rule updates or retirement

### ⚙️ 9. Interactive Dashboard
```bash
# Show compliance dashboard
python3 .claude/hooks/claude-md-checker.py --dashboard

# Filter by specific phase
python3 .claude/hooks/claude-md-checker.py --dashboard --phase testing

# Show stale rules needing review
python3 .claude/hooks/claude-md-checker.py --dashboard --stale

# Show unused rules
python3 .claude/hooks/claude-md-checker.py --dashboard --unused

# Get update suggestions
python3 .claude/hooks/claude-md-checker.py --dashboard --suggest-updates
```

### 🎯 10. Variant-Driven Rule Loading
- **Phase-Specific**: Load rules relevant to current development phase
- **Tool-Specific**: Different rule sets for different tools (Bash, Edit, Write, etc.)
- **Context-Specific**: Rules filtered by intent tags and task type

## 📁 File Structure

```
.claude/hooks/
├── claude-md-checker.py           # Main hook script (570+ lines)
├── rule-metadata.json             # Auto-generated rule metadata
├── CLAUDE_MD_CHECKER.md           # This documentation
└── README.md                      # General hooks documentation

brain/logs/
├── rule-compliance.log            # Compliance audit trail
└── archives/
    └── claude-md-backup-YYYYMMDD/ # Automated backups

brain/cache/
└── session-context.json           # Session context storage
```

## 🔧 Hook Configuration

The hook is configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "python3 /path/to/claude-md-checker.py",
      "Edit": "python3 /path/to/claude-md-checker.py",
      "Write": "python3 /path/to/claude-md-checker.py",
      "MultiEdit": "python3 /path/to/claude-md-checker.py",
      "Task": "python3 /path/to/claude-md-checker.py"
    }
  }
}
```

## 🎮 Usage Examples

### Automatic Execution (Default)
```bash
# Hook runs automatically before any tool execution
claude edit myfile.py
# → Compliance check runs first
# → Shows relevant rules
# → Blocks if critical violations found
# → Proceeds if compliant
```

### Manual Dashboard Inspection
```bash
# General dashboard
python3 .claude/hooks/claude-md-checker.py --dashboard

# Phase-specific rules
python3 .claude/hooks/claude-md-checker.py --dashboard --phase intelligence

# Maintenance mode
python3 .claude/hooks/claude-md-checker.py --dashboard --stale --suggest-updates
```

## 📊 Rule Metadata Structure

Each rule is tracked with comprehensive metadata:

```json
{
  "RULE-001": {
    "rule_id": "RULE-001",
    "content": "Documentation is source of truth - Your knowledge...",
    "section": "Essential Principles",
    "alert_level": "CRITICAL",
    "last_used": "2025-07-16T10:15:30",
    "usage_count": 15,
    "compliance_score": 0.85,
    "version_hash": "a1b2c3d4",
    "created_date": "2025-07-16T08:00:00",
    "last_updated": "2025-07-16T10:00:00",
    "tags": ["#docs", "#research", "#jina"],
    "phase_relevance": ["foundation", "intelligence", "optimization"]
  }
}
```

## 🔍 Compliance Checking Logic

### Critical Rule Validation
- **Docker Rules**: Checks if Docker is available when required
- **Testing Rules**: Validates test existence for Python files
- **Backup Rules**: Warns about backup needs before file edits
- **Security Rules**: Enforces security protocols and protected file handling

### Advisory Rule Guidance
- **Code Quality**: Suggests formatting and style improvements
- **Documentation**: Recommends documentation for new code
- **Best Practices**: Guides toward optimal development patterns

## 📈 Analytics & Reporting

### Compliance Metrics
- **Rule Adherence Rate**: Percentage of rules followed vs. violated
- **Usage Frequency**: Which rules are most/least used
- **Compliance Trends**: Improvement/degradation over time
- **Context Effectiveness**: Which contexts have best compliance

### Dashboard Insights
- **Top Relevant Rules**: Rules most important for current context
- **Stale Rules**: Rules needing review or retirement
- **Violation Patterns**: Common compliance issues
- **Improvement Suggestions**: Actionable recommendations

## 🔄 Auto-Refinement Features

### Rule Evolution
- **Usage-Based Scoring**: Rules get scored based on actual usage
- **Compliance Feedback**: Rules adjust importance based on follow-through
- **Stale Detection**: Automatically flags outdated rules
- **Conflict Resolution**: Identifies contradictory rules

### Maintenance Automation
- **Backup Management**: Automatic Claude.md backups before changes
- **Version Tracking**: Hash-based change detection
- **Metadata Persistence**: Continuous rule metadata updates
- **Analytics Collection**: Performance data for optimization

## 🚀 Advanced Features

### Session Context Intelligence
- **Git Integration**: Extracts intent from recent commits
- **File Path Analysis**: Understands current operation context
- **Tool Awareness**: Different behaviors for different tools
- **Phase Detection**: Automatically determines development phase

### Rule Enhancement System
```python
# Example of automatic rule enhancement
def enhance_rule_metadata(rule_content, section):
    # Extract semantic tags
    tags = extract_semantic_tags(rule_content)
    
    # Determine alert level
    alert_level = classify_rule_importance(rule_content, section)
    
    # Assign phase relevance
    phases = determine_phase_relevance(rule_content, section)
    
    return enhanced_rule
```

## 🎯 Benefits

### For Development
- **Proactive Compliance**: Catches issues before they happen
- **Context Awareness**: Only shows relevant rules
- **Learning System**: Improves over time with usage
- **Time Savings**: Prevents compliance-related delays

### For Quality
- **Consistent Standards**: Enforces development standards
- **Best Practices**: Guides toward optimal patterns
- **Risk Reduction**: Prevents common mistakes
- **Audit Trail**: Complete compliance history

### For Maintenance
- **Rule Evolution**: Identifies outdated rules automatically
- **Usage Analytics**: Shows which rules are effective
- **Optimization**: Continuously improves rule relevance
- **Documentation**: Self-documenting compliance system

## 🔧 Customization Options

### Rule Priority Adjustment
```python
# Modify relevance calculation weights
RELEVANCE_WEIGHTS = {
    'base_relevance': 0.3,
    'phase_match': 0.3,
    'intent_tags': 0.2,
    'usage_frequency': 0.1,
    'recency_bonus': 0.1,
    'compliance_score': 0.1
}
```

### Alert Level Customization
```python
# Customize alert level determination
CRITICAL_KEYWORDS = ['must', 'never', 'always', 'critical', 'essential']
ADVISORY_KEYWORDS = ['should', 'recommend', 'prefer', 'consider']
```

### Context Detection Tuning
```python
# Enhance context extraction
def extract_enhanced_context():
    # Add custom context detection logic
    # Integrate with additional tools
    # Expand intent recognition
```

## 📋 Maintenance Schedule

### Daily
- Automatic compliance logging
- Rule usage tracking
- Context analysis

### Weekly
- Stale rule identification
- Compliance trend analysis
- Dashboard review

### Monthly
- Rule effectiveness evaluation
- Metadata cleanup
- System optimization

---

*Advanced Claude.md Compliance Checker | Context-Aware | Self-Improving | Audit-Ready*