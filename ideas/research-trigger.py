#!/usr/bin/env python3
"""
Research Integration Trigger System
Automatically moves strong ideas to research/ directory based on criteria
"""

import re
import json
import os
from datetime import datetime
from pathlib import Path

class ResearchTrigger:
    def __init__(self, base_path="/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.ideas_path = self.base_path / "ideas"
        self.research_path = self.base_path / "research"
        self.trigger_log = self.ideas_path / "research-trigger-log.json"
        
        # Create research subdirectories if they don't exist
        self._ensure_research_dirs()
        
    def _ensure_research_dirs(self):
        """Create research directory structure"""
        dirs = [
            "validation",
            "implementation", 
            "risk-analysis",
            "ai-development",
            "archive"
        ]
        
        for dir_name in dirs:
            (self.research_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def extract_ideas_from_registry(self):
        """Extract ideas from idea_registry.md"""
        registry_file = self.ideas_path / "idea_registry.md"
        
        if not registry_file.exists():
            return []
            
        with open(registry_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        ideas = []
        
        # Extract lifecycle status table
        lifecycle_pattern = r'\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|'
        matches = re.findall(lifecycle_pattern, content)
        
        for match in matches:
            if match[0] == "Idea":  # Skip header
                continue
                
            idea, stage, last_updated, next_action, research_ready = match
            
            # Determine auto-trigger criteria
            auto_trigger = False
            trigger_reason = ""
            target_dir = "validation"
            
            # Check stage-based triggers
            if "🍎 Fruit" in stage:
                auto_trigger = True
                trigger_reason = "Implementation-ready (Fruit stage)"
                target_dir = "implementation"
            elif "🌳 Growth" in stage:
                auto_trigger = True
                trigger_reason = "Active development (Growth stage)"
                target_dir = "validation"
            elif "✅" in research_ready:
                auto_trigger = True
                trigger_reason = "Research ready flag"
                target_dir = "validation"
            
            # Check AI/ML domain triggers
            ai_keywords = ["neural", "ai", "intelligence", "learning", "cognitive"]
            if any(keyword in idea.lower() for keyword in ai_keywords):
                auto_trigger = True
                trigger_reason = "AI/ML domain"
                target_dir = "ai-development"
            
            # Check risk triggers
            risk_keywords = ["risk", "security", "privacy", "failure"]
            if any(keyword in next_action.lower() for keyword in risk_keywords):
                auto_trigger = True
                trigger_reason = "Risk assessment needed"
                target_dir = "risk-analysis"
            
            ideas.append({
                'title': idea.strip(),
                'stage': stage.strip(),
                'last_updated': last_updated.strip(),
                'next_action': next_action.strip(),
                'research_ready': research_ready.strip(),
                'auto_trigger': auto_trigger,
                'trigger_reason': trigger_reason,
                'target_dir': target_dir
            })
        
        return ideas
    
    def create_research_file(self, idea, target_dir):
        """Create research file for triggered idea"""
        
        # Generate filename
        safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', idea['title'])
        filename = safe_title.lower().replace(' ', '-') + '.md'
        
        research_file = self.research_path / target_dir / filename
        
        # Generate research template based on target directory
        if target_dir == "validation":
            template = self._validation_template(idea)
        elif target_dir == "implementation":
            template = self._implementation_template(idea)
        elif target_dir == "risk-analysis":
            template = self._risk_analysis_template(idea)
        elif target_dir == "ai-development":
            template = self._ai_development_template(idea)
        else:
            template = self._generic_template(idea)
        
        # Write research file
        with open(research_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        return research_file
    
    def _validation_template(self, idea):
        return f"""# 🔬 Research Validation: {idea['title']}
*Auto-triggered from ideas/lifecycle-tracker.md*

## 📊 Idea Overview
- **Stage**: {idea['stage']}
- **Last Updated**: {idea['last_updated']}
- **Next Action**: {idea['next_action']}
- **Trigger Reason**: {idea['trigger_reason']}

## 🎯 Validation Checklist
- [ ] **Problem Definition**: Clear articulation of what we're solving
- [ ] **Technical Feasibility**: Engineering requirements assessment
- [ ] **Market Validation**: User need confirmation
- [ ] **Resource Estimation**: Development effort estimation
- [ ] **Risk Assessment**: Potential issues identification
- [ ] **Success Metrics**: Measurable outcomes definition

## 📋 Research Plan
### Phase 1: Problem Validation
- [ ] User interviews
- [ ] Competitive analysis
- [ ] Technical spike

### Phase 2: Solution Design
- [ ] Architecture planning
- [ ] Prototype development
- [ ] Testing strategy

### Phase 3: Implementation Planning
- [ ] Resource allocation
- [ ] Timeline creation
- [ ] Risk mitigation

## 📈 Success Criteria
- **Technical**: [Define technical success metrics]
- **User**: [Define user success metrics]
- **Business**: [Define business success metrics]

## 🔄 Next Steps
1. Complete validation checklist
2. Conduct user research
3. Create implementation plan
4. Return to ideas/lifecycle-tracker.md with results

---
*Research Validation | Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    def _implementation_template(self, idea):
        return f"""# 🚀 Implementation Research: {idea['title']}
*Auto-triggered from ideas/lifecycle-tracker.md*

## 📊 Idea Overview
- **Stage**: {idea['stage']}
- **Last Updated**: {idea['last_updated']}
- **Next Action**: {idea['next_action']}
- **Trigger Reason**: {idea['trigger_reason']}

## 🛠️ Implementation Plan
### Technical Architecture
- [ ] **System Design**: High-level architecture
- [ ] **Technology Stack**: Tools and frameworks
- [ ] **Database Design**: Data structure planning
- [ ] **API Design**: Interface specifications

### Development Phases
- [ ] **Phase 1**: Core functionality
- [ ] **Phase 2**: User interface
- [ ] **Phase 3**: Integration testing
- [ ] **Phase 4**: Deployment preparation

## 📋 Resource Requirements
- **Development Time**: [Estimate hours/weeks]
- **Team Members**: [Required skills]
- **Infrastructure**: [Hardware/software needs]
- **Budget**: [Cost estimation]

## 🧪 Testing Strategy
- [ ] **Unit Testing**: Component-level testing
- [ ] **Integration Testing**: System integration
- [ ] **User Testing**: End-user validation
- [ ] **Performance Testing**: Load and stress testing

## 🎯 Success Metrics
- **Performance**: [Speed, efficiency metrics]
- **Quality**: [Bug rate, reliability metrics]
- **User Experience**: [Satisfaction, adoption metrics]

---
*Implementation Research | Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    def _risk_analysis_template(self, idea):
        return f"""# ⚠️ Risk Analysis: {idea['title']}
*Auto-triggered from ideas/lifecycle-tracker.md*

## 📊 Idea Overview
- **Stage**: {idea['stage']}
- **Last Updated**: {idea['last_updated']}
- **Next Action**: {idea['next_action']}
- **Trigger Reason**: {idea['trigger_reason']}

## 🔍 Risk Assessment Matrix
| Risk Category | Probability | Impact | Severity | Mitigation Strategy |
|---------------|-------------|--------|----------|-------------------|
| Technical | | | | |
| Market | | | | |
| Resource | | | | |
| Timeline | | | | |
| Security | | | | |

## 🚨 Critical Risk Factors
### Technical Risks
- [ ] **Complexity**: [Assess technical complexity]
- [ ] **Dependencies**: [External system dependencies]
- [ ] **Scalability**: [Performance under load]

### Market Risks
- [ ] **User Adoption**: [Will users actually use this?]
- [ ] **Competition**: [Market saturation risk]
- [ ] **Timing**: [Market readiness]

### Resource Risks
- [ ] **Budget**: [Cost overrun potential]
- [ ] **Timeline**: [Delivery delay risk]
- [ ] **Skills**: [Team capability gaps]

## 🛡️ Risk Mitigation Plan
- **High Priority**: [Address immediately]
- **Medium Priority**: [Monitor closely]
- **Low Priority**: [Periodic review]

---
*Risk Analysis | Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    def _ai_development_template(self, idea):
        return f"""# 🧠 AI Development Research: {idea['title']}
*Auto-triggered from ideas/lifecycle-tracker.md*

## 📊 Idea Overview
- **Stage**: {idea['stage']}
- **Last Updated**: {idea['last_updated']}
- **Next Action**: {idea['next_action']}
- **Trigger Reason**: {idea['trigger_reason']}

## 🤖 AI/ML Requirements
### Intelligence Capabilities
- [ ] **Natural Language Processing**: [NLP requirements]
- [ ] **Machine Learning**: [ML model needs]
- [ ] **Knowledge Representation**: [Data structure needs]
- [ ] **Reasoning**: [Logic and inference needs]

### Technical Infrastructure
- [ ] **Model Training**: [Training data and compute]
- [ ] **Inference Engine**: [Real-time processing]
- [ ] **Data Pipeline**: [Data ingestion and processing]
- [ ] **Model Deployment**: [Serving infrastructure]

## 🔬 Research & Development
### Literature Review
- [ ] **State of the Art**: [Current research landscape]
- [ ] **Best Practices**: [Industry standards]
- [ ] **Open Source**: [Available tools and libraries]

### Prototype Development
- [ ] **Proof of Concept**: [Minimal viable intelligence]
- [ ] **Performance Benchmarks**: [Accuracy and speed metrics]
- [ ] **Scalability Testing**: [Growth potential]

## 📈 Intelligence Metrics
- **Accuracy**: [Prediction/classification accuracy]
- **Speed**: [Response time requirements]
- **Learning**: [Adaptation and improvement]
- **Robustness**: [Error handling and edge cases]

---
*AI Development Research | Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    def _generic_template(self, idea):
        return f"""# 🔍 Research: {idea['title']}
*Auto-triggered from ideas/lifecycle-tracker.md*

## 📊 Idea Overview
- **Stage**: {idea['stage']}
- **Last Updated**: {idea['last_updated']}
- **Next Action**: {idea['next_action']}
- **Trigger Reason**: {idea['trigger_reason']}

## 📋 Research Checklist
- [ ] **Problem Definition**: [What problem are we solving?]
- [ ] **Solution Approach**: [How will we solve it?]
- [ ] **Technical Feasibility**: [Can we build this?]
- [ ] **User Validation**: [Do people want this?]
- [ ] **Resource Planning**: [What do we need?]

## 🎯 Research Outcomes
- **Go/No-Go Decision**: [Should we proceed?]
- **Implementation Plan**: [How will we build it?]
- **Success Criteria**: [How will we measure success?]

---
*Research | Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    def trigger_research_pipeline(self):
        """Main trigger function"""
        print("🔬 Research Integration Trigger System Starting...")
        
        ideas = self.extract_ideas_from_registry()
        triggered_ideas = [idea for idea in ideas if idea['auto_trigger']]
        
        print(f"📊 Analyzed {len(ideas)} ideas, {len(triggered_ideas)} triggered for research")
        
        created_files = []
        
        for idea in triggered_ideas:
            try:
                research_file = self.create_research_file(idea, idea['target_dir'])
                created_files.append({
                    'idea': idea['title'],
                    'file': str(research_file),
                    'reason': idea['trigger_reason'],
                    'directory': idea['target_dir']
                })
                print(f"✅ Created research file: {research_file}")
            except Exception as e:
                print(f"❌ Failed to create research file for {idea['title']}: {e}")
        
        # Log trigger operation
        trigger_record = {
            'timestamp': datetime.now().isoformat(),
            'ideas_analyzed': len(ideas),
            'ideas_triggered': len(triggered_ideas),
            'files_created': created_files
        }
        
        # Update trigger log
        trigger_history = []
        if self.trigger_log.exists():
            with open(self.trigger_log, 'r', encoding='utf-8') as f:
                trigger_history = json.load(f)
        
        trigger_history.append(trigger_record)
        
        with open(self.trigger_log, 'w', encoding='utf-8') as f:
            json.dump(trigger_history, f, indent=2)
        
        print(f"🎯 Research trigger completed: {len(created_files)} files created")
        return trigger_record

if __name__ == "__main__":
    trigger = ResearchTrigger()
    result = trigger.trigger_research_pipeline()
    print(f"📈 Trigger result: {result}")