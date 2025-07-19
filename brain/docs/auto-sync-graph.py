#!/usr/bin/env python3
"""
Neural Decision Graph Auto-Sync System
Automatically updates decision-trace.mmd based on explain.md entries
"""

import re
import json
from datetime import datetime
from pathlib import Path

class NeuralGraphSync:
    def __init__(self, docs_path="/mnt/c/Users/Brandon/AAI/brain/docs"):
        self.docs_path = Path(docs_path)
        self.explain_file = self.docs_path / "explain.md"
        self.trace_file = self.docs_path / "decision-trace.mmd"
        self.sync_log = self.docs_path / "sync-log.json"
        
    def extract_decisions_from_explain(self):
        """Extract decision data from explain.md"""
        with open(self.explain_file, 'r') as f:
            content = f.read()
        
        decisions = []
        
        # Extract decision sections
        decision_pattern = r'### (.+?)\n\*\*Date\*\*: (.+?)\n\*\*Impact\*\*: (.+?)\n\*\*Status\*\*: (.+?)\n'
        matches = re.findall(decision_pattern, content, re.DOTALL)
        
        for match in matches:
            title, date, impact, status = match
            
            # Extract reasoning section
            reasoning_pattern = rf'### {re.escape(title)}.*?\*\*Reasoning\*\*:\s*\n(.+?)\n\*\*Alternatives'
            reasoning_match = re.search(reasoning_pattern, content, re.DOTALL)
            reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
            
            # Extract main WHY from reasoning
            why_lines = [line.strip() for line in reasoning.split('\n') if line.strip().startswith('- ')]
            primary_why = why_lines[0][2:] if why_lines else "Core system requirement"
            
            # Map impact to confidence score
            confidence_map = {
                '🔴 Critical': 95,
                '🟡 Major': 85,
                '🟢 Minor': 75
            }
            
            decisions.append({
                'id': title.lower().replace(' ', '-'),
                'title': title,
                'date': date,
                'impact': impact.strip(),
                'status': status.strip(),
                'confidence': confidence_map.get(impact.strip(), 80),
                'primary_why': primary_why,
                'reasoning': reasoning
            })
        
        return decisions
    
    def generate_mermaid_graph(self, decisions):
        """Generate updated Mermaid graph with all decisions"""
        
        # Create node definitions
        nodes = []
        edges = []
        why_edges = []
        
        # Add initial system node
        nodes.append("A[Initial AAI System]")
        
        # Process each decision
        prev_node = "A"
        for i, decision in enumerate(decisions):
            node_id = chr(66 + i)  # B, C, D, etc.
            nodes.append(f"{node_id}[{decision['title']}]")
            
            # Add decision flow edge
            edges.append(f"{prev_node} --> {node_id}")
            
            # Add WHY rationale edge
            why_edges.append(f'{prev_node} -.->|"WHY: {decision["primary_why"]}"| {node_id}')
            
            prev_node = node_id
        
        # Generate confidence-based styling
        critical_nodes = [chr(66 + i) for i, d in enumerate(decisions) if d['impact'] == '🔴 Critical']
        major_nodes = [chr(66 + i) for i, d in enumerate(decisions) if d['impact'] == '🟡 Major']
        minor_nodes = [chr(66 + i) for i, d in enumerate(decisions) if d['impact'] == '🟢 Minor']
        
        # Build complete graph
        graph = f"""graph LR
    %% AAI System Neural Decision Flow - Auto-Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}
    {chr(10).join(nodes)}
    
    %% Decision Flow
    {chr(10).join(edges)}
    
    %% Neural Rationale Connections (WHY paths)
    {chr(10).join(why_edges)}
    
    %% Confidence Scoring (stroke-width = confidence level)
    classDef critical fill:#ff6b6b,stroke:#c92a2a,stroke-width:4px,color:#fff
    classDef major fill:#ffd43b,stroke:#fab005,stroke-width:3px
    classDef minor fill:#51cf66,stroke:#37b24d,stroke-width:2px
    classDef validated fill:#40c057,stroke:#2f9e44,stroke-width:4px,color:#fff
    classDef unvalidated fill:#868e96,stroke:#495057,stroke-width:1px
    
    %% Apply confidence-based styles
    class {','.join(critical_nodes)} critical
    class {','.join(major_nodes)} major
    class {','.join(minor_nodes)} minor
    
    %% Feedback Loop Indicators
    {prev_node} --> K[Decision Outcome Tracker]
    K -.->|"Feedback Loop"| B
    K -.->|"Learning Signal"| C
    
    %% Decision Links with Confidence Scores
    {chr(10).join([f'click {chr(66 + i)} "#{d["id"]}|confidence:{d["confidence"]}%"' for i, d in enumerate(decisions)])}
    
    %% Neural Network Metadata
    subgraph Legend["🧠 Neural Rationale Legend"]
        L1[Solid Lines = Decision Flow]
        L2[Dotted Lines = WHY Rationale]
        L3[Thickness = Confidence Level]
        L4[Color = Validation Status]
    end"""
        
        return graph
    
    def sync_graph(self):
        """Main sync function"""
        print("🧠 Neural Decision Graph Auto-Sync Starting...")
        
        # Extract decisions from explain.md
        decisions = self.extract_decisions_from_explain()
        print(f"📊 Extracted {len(decisions)} decisions from explain.md")
        
        # Generate new graph
        new_graph = self.generate_mermaid_graph(decisions)
        
        # Write updated graph
        with open(self.trace_file, 'w') as f:
            f.write(new_graph)
        
        # Log sync operation
        sync_record = {
            'timestamp': datetime.now().isoformat(),
            'decisions_synced': len(decisions),
            'graph_updated': True
        }
        
        # Update sync log
        sync_history = []
        if self.sync_log.exists():
            with open(self.sync_log, 'r') as f:
                sync_history = json.load(f)
        
        sync_history.append(sync_record)
        
        with open(self.sync_log, 'w') as f:
            json.dump(sync_history, f, indent=2)
        
        print(f"✅ Neural graph updated with {len(decisions)} decisions")
        print(f"📈 Confidence scores and WHY rationales integrated")
        print(f"🔄 Feedback loop system activated")
        
        return sync_record

if __name__ == "__main__":
    syncer = NeuralGraphSync()
    result = syncer.sync_graph()
    print(f"🎯 Sync completed: {result}")