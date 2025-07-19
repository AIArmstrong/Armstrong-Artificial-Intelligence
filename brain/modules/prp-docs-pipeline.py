#!/usr/bin/env python3
"""
PRP to Docs Integration Pipeline
Auto-documents successful PRPs with context, validation results, and reusable patterns
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

class PRPDocsPipeline:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.prp_dir = self.aai_root / "PRPs"
        self.docs_dir = self.aai_root / "docs"
        self.generated_dir = self.docs_dir / "generated/from-prps"
        self.patterns_dir = self.docs_dir / "patterns"
        self.queue_file = self.aai_root / "brain/logs/queue.json"
        
    def scan_prp_files(self):
        """Scan PRP directory for project files"""
        prp_files = []
        
        for file_path in self.prp_dir.rglob("*.md"):
            if file_path.name != "prp_base.md":  # Skip template
                prp_files.append(file_path)
        
        return prp_files
    
    def extract_prp_metadata(self, prp_path):
        """Extract metadata from PRP file"""
        with open(prp_path, 'r') as f:
            content = f.read()
        
        metadata = {
            'filepath': str(prp_path),
            'name': prp_path.stem,
            'size': len(content),
            'created': datetime.fromtimestamp(prp_path.stat().st_mtime).isoformat(),
            'sections': []
        }
        
        # Extract sections
        sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
        metadata['sections'] = sections
        
        # Extract goals if present
        goal_match = re.search(r'## Goal\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if goal_match:
            metadata['goal'] = goal_match.group(1).strip()
        
        # Extract why section
        why_match = re.search(r'## Why\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if why_match:
            metadata['why'] = why_match.group(1).strip()
        
        # Extract success criteria
        success_match = re.search(r'### Success Criteria\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if success_match:
            criteria = re.findall(r'- \[ \] (.+)', success_match.group(1))
            metadata['success_criteria'] = criteria
        
        return metadata
    
    def generate_prp_documentation(self, prp_metadata):
        """Generate documentation from PRP metadata"""
        name = prp_metadata['name']
        
        doc_content = f"""# PRP Documentation: {name.replace('-', ' ').title()}

## Overview
**Source PRP**: `{prp_metadata['filepath']}`
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}
**Last Modified**: {prp_metadata['created']}

## Project Summary
"""
        
        if 'goal' in prp_metadata:
            doc_content += f"### Goal\n{prp_metadata['goal']}\n\n"
        
        if 'why' in prp_metadata:
            doc_content += f"### Business Value\n{prp_metadata['why']}\n\n"
        
        if 'success_criteria' in prp_metadata:
            doc_content += "### Success Criteria\n"
            for criterion in prp_metadata['success_criteria']:
                doc_content += f"- {criterion}\n"
            doc_content += "\n"
        
        doc_content += f"""## Implementation Status
**Status**: {self.get_prp_status(name)}
**Completion**: {self.get_completion_percentage(prp_metadata)}%

## PRP Structure Analysis
**Sections Detected**: {len(prp_metadata['sections'])}
**Content Size**: {prp_metadata['size']} characters

### Sections Overview
"""
        
        for section in prp_metadata['sections']:
            doc_content += f"- {section}\n"
        
        doc_content += f"""

## Reusable Patterns
*This section would be populated with patterns extracted from successful implementation*

### Context Patterns
- PRP structure follows template v2 with validation loops
- Includes comprehensive documentation references
- Success criteria are measurable and specific

### Implementation Patterns
*To be populated after successful implementation*

## Related Resources
- **Source PRP**: `{prp_metadata['filepath']}`
- **Template**: `PRPs/templates/prp_base.md`
- **Related SOPs**: `docs/sops/by-category/prp/`

## Lessons Learned
*To be populated after implementation completion*

---
*Auto-generated from PRP analysis*
*Pipeline: PRP → Docs Integration*
"""
        
        return doc_content
    
    def get_prp_status(self, prp_name):
        """Determine PRP implementation status"""
        # Check queue for related tasks
        try:
            with open(self.queue_file, 'r') as f:
                queue_data = json.load(f)
            
            # Look for tasks that might be related to this PRP
            for task in queue_data.get('queue', []) + queue_data.get('completed', []):
                if prp_name.lower() in task.get('description', '').lower():
                    return task.get('status', 'unknown')
        except:
            pass
        
        return 'not_started'
    
    def get_completion_percentage(self, prp_metadata):
        """Calculate completion percentage based on success criteria"""
        if 'success_criteria' not in prp_metadata:
            return 0
        
        total_criteria = len(prp_metadata['success_criteria'])
        if total_criteria == 0:
            return 0
        
        # For now, assume 0% completion for new PRPs
        # This would be updated based on actual implementation tracking
        return 0
    
    def extract_patterns(self, prp_metadata):
        """Extract reusable patterns from PRP"""
        patterns = {
            'context_patterns': [],
            'structure_patterns': [],
            'validation_patterns': []
        }
        
        # Analyze PRP structure
        sections = prp_metadata.get('sections', [])
        
        if 'All Needed Context' in sections:
            patterns['context_patterns'].append({
                'pattern': 'comprehensive_context',
                'description': 'PRP includes detailed context requirements',
                'value': 'Reduces implementation errors by providing complete context'
            })
        
        if 'Success Criteria' in sections:
            patterns['validation_patterns'].append({
                'pattern': 'measurable_success',
                'description': 'Clear, measurable success criteria defined',
                'value': 'Enables objective completion validation'
            })
        
        # Structure analysis
        if len(sections) >= 5:
            patterns['structure_patterns'].append({
                'pattern': 'comprehensive_structure',
                'description': 'Well-structured PRP with multiple sections',
                'value': 'Provides complete project context and requirements'
            })
        
        return patterns
    
    def save_prp_documentation(self, prp_metadata, doc_content):
        """Save PRP documentation to generated folder"""
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{prp_metadata['name']}.md"
        filepath = self.generated_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(doc_content)
        
        return filepath
    
    def save_patterns(self, prp_name, patterns):
        """Save extracted patterns to patterns directory"""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        
        patterns_file = self.patterns_dir / "prp-patterns.json"
        
        # Load existing patterns or create new
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                all_patterns = json.load(f)
        else:
            all_patterns = {}
        
        # Add new patterns
        all_patterns[prp_name] = {
            'extracted_on': datetime.now().isoformat(),
            'patterns': patterns
        }
        
        # Save updated patterns
        with open(patterns_file, 'w') as f:
            json.dump(all_patterns, f, indent=2)
        
        return patterns_file
    
    def generate_prp_index(self, documented_prps):
        """Generate index of all documented PRPs"""
        index_content = """# PRP Documentation Index

## Overview
Auto-generated documentation for all Project Request Prompts (PRPs) in the system.

## Available PRP Documentation

"""
        
        for prp in documented_prps:
            name = prp['name'].replace('-', ' ').title()
            index_content += f"### {name}\n"
            index_content += f"**Status**: {prp['status']}\n"
            index_content += f"**Completion**: {prp['completion']}%\n"
            index_content += f"**Documentation**: [View]({prp['doc_file']})\n"
            index_content += f"**Source PRP**: `{prp['source_path']}`\n\n"
        
        index_content += f"""
## Statistics
- **Total PRPs**: {len(documented_prps)}
- **Completed**: {sum(1 for p in documented_prps if p['status'] == 'completed')}
- **In Progress**: {sum(1 for p in documented_prps if p['status'] == 'in_progress')}
- **Not Started**: {sum(1 for p in documented_prps if p['status'] == 'not_started')}

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}*
*Pipeline: PRP → Docs Integration*
"""
        
        index_path = self.generated_dir / "INDEX.md"
        with open(index_path, 'w') as f:
            f.write(index_content)
        
        return index_path
    
    def process_all_prps(self):
        """Process all PRPs and generate documentation"""
        prp_files = self.scan_prp_files()
        documented_prps = []
        
        for prp_file in prp_files:
            print(f"Processing PRP: {prp_file.name}")
            
            # Extract metadata
            metadata = self.extract_prp_metadata(prp_file)
            
            # Generate documentation
            doc_content = self.generate_prp_documentation(metadata)
            doc_path = self.save_prp_documentation(metadata, doc_content)
            
            # Extract and save patterns
            patterns = self.extract_patterns(metadata)
            patterns_path = self.save_patterns(metadata['name'], patterns)
            
            documented_prps.append({
                'name': metadata['name'],
                'status': self.get_prp_status(metadata['name']),
                'completion': self.get_completion_percentage(metadata),
                'doc_file': doc_path.name,
                'source_path': prp_file.relative_to(self.aai_root)
            })
        
        # Generate index
        index_path = self.generate_prp_index(documented_prps)
        
        return {
            'documented_prps': documented_prps,
            'index_path': str(index_path),
            'patterns_file': str(self.patterns_dir / "prp-patterns.json")
        }

def main():
    pipeline = PRPDocsPipeline()
    result = pipeline.process_all_prps()
    
    print(f"Processed {len(result['documented_prps'])} PRPs")
    print(f"Generated index: {result['index_path']}")
    print(f"Patterns saved: {result['patterns_file']}")
    
    return result

if __name__ == '__main__':
    main()