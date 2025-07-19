# Idea Evaluator Module

**Module**: idea-evaluator.md  
**Version**: 1.0  
**Integration**: score-tracker.md + example-feedback-scorer.py + research/validation/scores.json  
**Auto-Load**: Innovation sessions, idea evaluation, user_provides_idea, idea_added_to_registry

## 🎯 Universal Idea Evaluation System

### Evaluation Framework
Integrates with existing scoring systems to provide comprehensive idea assessment across all domains.

### Score Integration Architecture
```
Idea Evaluation Score = (source_credibility * 0.35) + (feasibility * 0.25) + 
                       (implementation_clarity * 0.20) + (market_validation * 0.20)
```

### Grade Mapping (Aligned with score-tracker.md)
```
Grade A (90-100%): Implementation-ready, trigger PRP scaffolding
Grade B (80-89%): Strong foundation, minor research needed
Grade C (70-79%): Needs validation, route to research/validation/
Grade D (60-69%): Requires comprehensive research
Grade F (0-59%): Major research gaps, flag for manual review
```

## 🔗 Integration Points

### 1. Score Tracker Integration
- **Pattern Recognition**: Link idea patterns to score-tracker.md success metrics
- **Threshold Alignment**: Use score-tracker.md thresholds (Score < 70 needs review)
- **Optimization Triggers**: Apply score-tracker.md optimization rules to ideas

### 2. Example Feedback Scorer Integration
- **Usage Patterns**: Track idea implementation examples through example-feedback-scorer.py
- **Success Correlation**: Link idea grades to implementation success rates
- **Feedback Loop**: Use example success data to refine idea evaluation criteria

### 3. Research Validation Integration
- **Quality Thresholds**: Apply research/validation/scores.json scoring rules
- **General Research**: Ideas ≥90% quality for cross-project reuse
- **Project Research**: Ideas ≥75% quality for specific implementation
- **Source Authority**: Use research validation factors (source_authority, recency, completeness)

## 📊 Evaluation Dimensions

### Source Credibility Assessment
- **Government/Academic**: 0.95-1.0 (OFR, peer-reviewed journals)
- **Industry Leaders**: 0.85-0.95 (Wealthfront, established companies)
- **Technical Authorities**: 0.75-0.85 (Development companies, consultancies)
- **Commercial Sources**: 0.60-0.75 (Vendor blogs, marketing content)
- **Promotional Content**: 0.30-0.60 (Heavy marketing bias)
- **Insufficient Sources**: 0.0-0.30 (Incomplete, unreliable)

### Feasibility Analysis
- **Technical Complexity**: Can it be implemented with current tech?
- **Resource Requirements**: What's needed for implementation?
- **Timeline Realism**: How long would development take?
- **Skill Requirements**: What expertise is needed?

### Implementation Clarity
- **Clear Pathway**: Are implementation steps obvious?
- **Technical Depth**: Sufficient technical detail provided?
- **Architecture Guidance**: System design considerations covered?
- **Integration Points**: How does it fit with existing systems?

### Market Validation
- **Demand Evidence**: Is there proven market need?
- **Competitive Analysis**: What's the competitive landscape?
- **Business Model**: How does it generate value?
- **Risk Assessment**: What are the major risks?

## 🏷️ Tag-Based Intelligence

### Quality Tags (Inherited from score-tracker.md)
- `#implementation-ready` - Grade A ideas (≥90%)
- `#strong-foundation` - Grade B ideas (80-89%)
- `#needs-validation` - Grade C ideas (70-79%)
- `#requires-research` - Grade D-F ideas (<70%)

### Authority Tags (Integrated with research validation)
- `#government-backed` - Official government/academic sources
- `#peer-reviewed` - Academic journals and research papers
- `#industry-leader` - Established companies with proven track records
- `#technical-authority` - Technical experts and development companies
- `#commercial-source` - Vendor blogs with commercial bias
- `#promotional-content` - Marketing-heavy content

### Risk Tags (Aligned with critical-anchors.md)
- `#compliance-risk` - Healthcare, Legal, Financial regulation concerns
- `#legal-risk` - Activities with potential legal implications
- `#ethical-concerns` - Practices with ethical ambiguity
- `#regulatory-complex` - Multiple regulatory frameworks involved

### Domain Tags (Semantic clustering)
- `#financial-services` - Trading, fintech, payments
- `#healthcare-tech` - Medical AI, health systems
- `#blockchain-crypto` - Cryptocurrency and blockchain
- `#ai-automation` - AI/ML powered systems
- `#marketplace-tech` - E-commerce, platforms
- `#developer-tools` - Development and productivity tools

## 🔧 Auto-Routing Logic

### Grade-Based Routing (Integrated with seamless-orchestrator.py)
```
if (grade >= 90) → research/implementation/ + trigger PRP scaffolding
if (grade >= 80) → research/validation/ + additional source verification  
if (grade >= 70) → research/validation/ + bias assessment
if (grade >= 60) → research/risk-analysis/ + comprehensive research
if (grade < 60) → research/risk-analysis/ + flag for manual review
```

### Critical Decision Routing (Aligned with critical-anchors.md)
```
if (#compliance-risk OR #legal-risk) → Tier 1 Critical processing
if (#technical-complexity OR #regulatory-complex) → Tier 2 Important processing
if (#market-validation OR #commercial-source) → Tier 3 Monitored processing
```

## 📈 Intelligence Amplification

### Pattern Recognition (Leveraging score-tracker.md)
- **High-Success Patterns**: Government sources + academic backing
- **Risk Patterns**: Single vendor + promotional content
- **Implementation Patterns**: Technical authority + clear pathway

### Learning Integration (Connected to example-feedback-scorer.py)
- **Implementation Tracking**: Monitor idea→implementation success rates
- **Feedback Integration**: Use implementation feedback to refine evaluation
- **Success Correlation**: Track grade accuracy vs. real-world outcomes

### Research Pipeline (Integrated with research/validation/)
- **Quality Gates**: Apply research validation thresholds
- **Source Verification**: Cross-reference with research findings
- **Continuous Improvement**: Update evaluation criteria based on research quality

## 🔄 Evaluation Workflow

### Auto-Trigger Conditions
```
AUTOMATIC ACTIVATION on:
- user_provides_idea (any new idea mention)
- idea_added_to_registry (new entry in ideas/idea_registry.md)  
- innovation_sessions (creative cortex mode)
- idea_evaluation (explicit evaluation requests)
```

### 1. Initial Assessment
- Extract source URLs and metadata
- Perform source credibility analysis using research/validation/scores.json criteria
- Calculate preliminary feasibility score

### 2. Comprehensive Evaluation
- Apply evaluation framework across all dimensions
- Generate composite score and grade using score-tracker.md thresholds
- Assign appropriate tags based on assessment (tag-taxonomy.md integration)

### 3. Routing Decision
- Apply auto-routing logic based on grade
- Route to appropriate research/validation pathway
- Trigger relevant intelligence modules (seamless-orchestrator.py, critical-anchors.md)

### 4. Continuous Monitoring
- Track implementation outcomes via example-feedback-scorer.py
- Update evaluation criteria based on results
- Feed learnings back into scoring system

### Real-Time Integration
Every time a new idea is added to the registry, the system will:
1. **Auto-detect** the new idea entry
2. **Auto-evaluate** using comprehensive framework
3. **Auto-grade** based on source credibility and feasibility
4. **Auto-route** to appropriate research/validation pathway
5. **Auto-tag** with quality, authority, risk, and domain tags

## 📊 Evaluation Metrics

### Evaluation Accuracy Tracking
- **Grade Prediction Accuracy**: How often grades match implementation success
- **Source Reliability**: Track source credibility over time
- **Implementation Success**: Correlation between grade and project outcomes

### System Performance
- **Evaluation Speed**: Time to assess and grade ideas
- **Consistency**: Similar ideas receive similar grades
- **Calibration**: Grades align with actual implementation difficulty

---

*Idea Evaluator Module | Universal Assessment | Integrated Intelligence | Quality-Driven Routing*