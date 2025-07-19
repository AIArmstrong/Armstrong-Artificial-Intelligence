#!/usr/bin/env python3
"""
Auto-generated SOP System
Monitors queue.json completions and converts successful tasks to reproducible SOPs
"""

import json
import os
from datetime import datetime
from pathlib import Path

class SOPGenerator:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.queue_file = self.aai_root / "brain/logs/queue.json"
        self.sop_dir = self.aai_root / "docs/sops"
        self.templates_dir = self.sop_dir / "templates"
        self.category_dir = self.sop_dir / "by-category"
        
    def load_queue_data(self):
        """Load queue.json data"""
        with open(self.queue_file, 'r') as f:
            return json.load(f)
    
    def extract_task_category(self, task_id, tags):
        """Extract category from task ID and tags"""
        # Use task ID prefix for primary categorization
        if '-' in task_id:
            category = task_id.split('-')[0]
        else:
            category = 'general'
            
        # Map categories to human-readable names
        category_mapping = {
            'docs': 'Documentation',
            'sop': 'Standard Operating Procedures',
            'prp': 'Project Request Prompts',
            'superclaude': 'SuperClaude Integration',
            'jina': 'Data Scraping',
            'testing': 'Testing Framework',
            'research': 'Research & Analysis',
            'examples': 'Code Examples',
            'ideas': 'Innovation Pipeline',
            'jarvis': 'AI Enhancement',
            'olympus': 'Project Migration',
            'manus': 'Documentation Import'
        }
        
        return category_mapping.get(category, category.title())
    
    def generate_sop_content(self, task):
        """Generate SOP content from completed task"""
        category = self.extract_task_category(task['id'], task.get('tags', []))
        
        sop_content = f"""# SOP: {task['title']}

## Overview
**Generated from**: Task `{task['id']}`
**Category**: {category}
**Completed**: {task.get('completed', 'Unknown')}
**Success Score**: {task.get('success_score', 'Not scored')}

## Description
{task['description']}

## Prerequisites
- AAI system operational
- Required tools: {', '.join(task.get('tags', []))}
- Estimated time: {task.get('estimated_duration', 'Variable')}

## Procedure

### Step 1: Preparation
1. Verify system status via `/log status`
2. Check dependencies are available
3. Review related documentation in `/docs/official/`

### Step 2: Execution
*This section would be populated with actual implementation steps*
*Currently auto-generated from task metadata*

Based on task ID `{task['id']}`, this involves:
- Primary action: {task['title'].split(' ')[0].lower()}
- Target system: {task['id'].split('-')[0] if '-' in task['id'] else 'general'}
- Expected outcome: {task['description']}

### Step 3: Validation
1. Verify completion criteria met
2. Run system health checks
3. Update documentation if needed
4. Log success metrics

## Success Criteria
- Task completed without errors
- System remains stable
- Documentation updated
- Knowledge captured for future use

## Troubleshooting
*Common issues and solutions would be populated from actual implementation experience*

## Related Resources
- Queue entry: `brain/logs/queue.json` (ID: {task['id']})
- Tags: {', '.join(task.get('tags', []))}
- Category docs: `docs/sops/by-category/{category.lower().replace(' ', '-')}/`

---
*Auto-generated SOP from successful task completion*
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}*
"""
        return sop_content
    
    def save_sop(self, task, content):
        """Save SOP to appropriate category folder"""
        category = self.extract_task_category(task['id'], task.get('tags', []))
        category_folder = self.category_dir / category.lower().replace(' ', '-')
        category_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate filename from task ID
        filename = f"{task['id']}.md"
        filepath = category_folder / filename
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    
    def create_sop_template(self):
        """Create SOP template for manual SOPs"""
        template_content = """# SOP: [Task Name]

## Overview
**Category**: [Category Name]
**Created**: [Date]
**Last Updated**: [Date]
**Success Score**: [Score/5]

## Description
[Brief description of what this SOP accomplishes]

## Prerequisites
- [List required tools/access]
- [List required knowledge/skills]
- [Estimated time requirement]

## Procedure

### Step 1: Preparation
1. [Preparation step 1]
2. [Preparation step 2]

### Step 2: Execution
1. [Main execution steps]
2. [With specific commands/actions]

### Step 3: Validation
1. [How to verify success]
2. [What to check for completion]

## Success Criteria
- [Specific measurable outcomes]
- [Quality checkpoints]

## Troubleshooting
### Common Issue 1
**Problem**: [Description]
**Solution**: [Fix]

### Common Issue 2
**Problem**: [Description]
**Solution**: [Fix]

## Related Resources
- [Links to relevant documentation]
- [Related SOPs]
- [External resources]

---
*Manual SOP - Template Version 1.0*
*Created: [Date]*
"""
        
        template_path = self.templates_dir / "sop-template.md"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        return template_path
    
    def process_completed_tasks(self, min_score=4.0):
        """Process completed tasks and generate SOPs"""
        queue_data = self.load_queue_data()
        completed_tasks = queue_data.get('completed', [])
        
        generated_sops = []
        
        for task in completed_tasks:
            # Skip if already has SOP
            task_id = task['id']
            category = self.extract_task_category(task_id, task.get('tags', []))
            category_folder = self.category_dir / category.lower().replace(' ', '-')
            potential_sop = category_folder / f"{task_id}.md"
            
            if potential_sop.exists():
                continue
            
            # Generate SOP for high-scoring tasks
            score = task.get('success_score', 5.0)  # Default to high score
            if score >= min_score:
                content = self.generate_sop_content(task)
                filepath = self.save_sop(task, content)
                generated_sops.append({
                    'task_id': task_id,
                    'category': category,
                    'filepath': str(filepath),
                    'score': score
                })
        
        return generated_sops
    
    def create_category_index(self):
        """Create index files for each category"""
        categories = {}
        
        # Scan existing SOPs
        for category_folder in self.category_dir.iterdir():
            if category_folder.is_dir():
                category_name = category_folder.name.replace('-', ' ').title()
                sop_files = list(category_folder.glob('*.md'))
                
                categories[category_name] = {
                    'folder': category_folder.name,
                    'count': len(sop_files),
                    'files': [f.name for f in sop_files]
                }
        
        # Generate index
        index_content = """# SOP Category Index

## Available Categories

"""
        for category, info in categories.items():
            index_content += f"### {category}\n"
            index_content += f"**Location**: `docs/sops/by-category/{info['folder']}/`\n"
            index_content += f"**SOPs**: {info['count']}\n\n"
            
            if info['files']:
                index_content += "**Available SOPs**:\n"
                for file in info['files']:
                    sop_name = file.replace('.md', '').replace('-', ' ').title()
                    index_content += f"- [{sop_name}]({info['folder']}/{file})\n"
                index_content += "\n"
        
        index_content += f"""
---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}*
*Total SOPs: {sum(info['count'] for info in categories.values())}*
"""
        
        index_path = self.sop_dir / "INDEX.md"
        with open(index_path, 'w') as f:
            f.write(index_content)
        
        return index_path

def main():
    generator = SOPGenerator()
    
    # Create SOP template
    template_path = generator.create_sop_template()
    print(f"Created SOP template: {template_path}")
    
    # Process completed tasks
    generated_sops = generator.process_completed_tasks()
    print(f"Generated {len(generated_sops)} SOPs")
    
    # Create category index
    index_path = generator.create_category_index()
    print(f"Created category index: {index_path}")
    
    return {
        'template': str(template_path),
        'generated_sops': generated_sops,
        'index': str(index_path)
    }

if __name__ == '__main__':
    result = main()
    print(f"SOP generation complete: {result}")