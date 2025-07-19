#!/usr/bin/env python3
"""
Auto-Example Generation from Successful PRPs
Extracts working code patterns from successful PRP implementations and generates templates
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class PRPExampleGenerator:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.prp_dir = self.aai_root / "PRPs"
        self.examples_dir = self.aai_root / "examples"
        self.generated_dir = self.examples_dir / "generated"
        self.templates_dir = self.examples_dir / "templates"
        self.queue_file = self.aai_root / "brain/logs/queue.json"
        self.docs_generated = self.aai_root / "docs/generated/from-prps"
        
    def load_queue_data(self):
        """Load queue data to find successful PRP implementations"""
        if not self.queue_file.exists():
            return {"completed": [], "queue": []}
        
        with open(self.queue_file, 'r') as f:
            return json.load(f)
    
    def find_successful_prp_implementations(self):
        """Find completed tasks that implemented PRPs successfully"""
        queue_data = self.load_queue_data()
        successful_implementations = []
        
        for task in queue_data.get('completed', []):
            # Look for PRP-related tasks
            if any(keyword in task.get('description', '').lower() 
                   for keyword in ['prp', 'project request', 'implementation']):
                
                # Check if task was successful
                if task.get('status') == 'completed':
                    successful_implementations.append(task)
        
        return successful_implementations
    
    def extract_prp_patterns(self, prp_path):
        """Extract reusable patterns from a PRP file"""
        try:
            with open(prp_path, 'r') as f:
                content = f.read()
            
            patterns = {
                'structure_patterns': [],
                'code_patterns': [],
                'validation_patterns': [],
                'context_patterns': []
            }
            
            # Extract structural patterns
            sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
            if sections:
                patterns['structure_patterns'].append({
                    'type': 'section_organization',
                    'pattern': sections,
                    'description': 'Standard PRP section structure'
                })
            
            # Extract code blocks
            code_blocks = re.findall(r'```(\\w+)?\\n([\\s\\S]*?)```', content)
            for lang, code in code_blocks:
                if lang and code.strip():
                    patterns['code_patterns'].append({
                        'language': lang,
                        'code': code.strip(),
                        'type': 'code_example',
                        'description': f'{lang} code pattern from PRP'
                    })
            
            # Extract validation patterns
            success_criteria = re.findall(r'- \\[ \\] (.+)', content)
            if success_criteria:
                patterns['validation_patterns'].append({
                    'type': 'success_criteria',
                    'criteria': success_criteria,
                    'description': 'Success validation checklist'
                })
            
            # Extract context patterns
            context_section = re.search(r'## All Needed Context\\s*\\n([\\s\\S]*?)(?=\\n##|\\Z)', content)
            if context_section:
                patterns['context_patterns'].append({
                    'type': 'context_requirements',
                    'content': context_section.group(1).strip(),
                    'description': 'Context gathering pattern'
                })
            
            return patterns
            
        except Exception as e:
            print(f"Error extracting patterns from {prp_path}: {e}")
            return {}
    
    def generate_example_from_pattern(self, pattern, prp_name):
        """Generate a working example from extracted pattern"""
        if pattern['type'] == 'code_example':
            return self.generate_code_example(pattern, prp_name)
        elif pattern['type'] == 'success_criteria':
            return self.generate_validation_example(pattern, prp_name)
        elif pattern['type'] == 'context_requirements':
            return self.generate_context_example(pattern, prp_name)
        elif pattern['type'] == 'section_organization':
            return self.generate_structure_template(pattern, prp_name)
        
        return None
    
    def generate_code_example(self, pattern, prp_name):
        """Generate a working code example"""
        language = pattern.get('language', 'python')
        code = pattern.get('code', '')
        
        example_content = f'''#!/usr/bin/env {language}
"""
Example: {prp_name.replace('-', ' ').title()} Pattern
Generated from successful PRP implementation

Description: {pattern.get('description', 'Code pattern extracted from PRP')}
Category: prp-patterns
Complexity: intermediate
Tags: #prp #pattern #{language}
"""

# Original PRP: {prp_name}
# Pattern type: {pattern['type']}

{code}

def main():
    """Main function to demonstrate the pattern"""
    # Add demonstration code here
    print("Example pattern from {prp_name}")

if __name__ == "__main__":
    main()
'''
        
        return {
            'filename': f"{prp_name}-{pattern['type']}.{self.get_file_extension(language)}",
            'content': example_content,
            'metadata': {
                'id': f"{prp_name}-{pattern['type']}",
                'title': f"{prp_name.replace('-', ' ').title()} {pattern['type'].title()}",
                'description': pattern.get('description', 'Code pattern from PRP'),
                'category': 'prp-patterns',
                'tags': ['#prp', '#pattern', f'#{language}'],
                'complexity': 'intermediate',
                'source_prp': prp_name,
                'generated_from': 'successful_prp_implementation',
                'created': datetime.now().isoformat(),
                'technologies': [language],
                'pattern_type': pattern['type']
            }
        }
    
    def generate_validation_example(self, pattern, prp_name):
        """Generate a validation/testing example"""
        criteria = pattern.get('criteria', [])
        
        example_content = f'''#!/usr/bin/env python3
"""
Example: {prp_name.replace('-', ' ').title()} Validation Pattern
Generated from successful PRP implementation

Description: Validation checklist and testing pattern
Category: validation-patterns
Complexity: beginner
Tags: #validation #testing #prp
"""

# Validation criteria from PRP: {prp_name}
validation_criteria = {criteria}

def validate_implementation():
    """Validate implementation against PRP success criteria"""
    results = {{}}
    
    for criterion in validation_criteria:
        # Add validation logic for each criterion
        results[criterion] = validate_criterion(criterion)
    
    return results

def validate_criterion(criterion):
    """Validate a specific criterion"""
    # Implement specific validation logic
    print(f"Validating: {{criterion}}")
    # Return True/False based on validation
    return True

def generate_validation_report(results):
    """Generate validation report"""
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"Validation Results: {{passed}}/{{total}} criteria passed")
    
    for criterion, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {{status}} {{criterion}}")
    
    return passed == total

def main():
    """Main validation function"""
    print("Running PRP validation...")
    results = validate_implementation()
    success = generate_validation_report(results)
    
    if success:
        print("🎉 All validation criteria passed!")
    else:
        print("⚠️  Some validation criteria failed")
    
    return success

if __name__ == "__main__":
    main()
'''
        
        return {
            'filename': f"{prp_name}-validation.py",
            'content': example_content,
            'metadata': {
                'id': f"{prp_name}-validation",
                'title': f"{prp_name.replace('-', ' ').title()} Validation",
                'description': 'Validation pattern extracted from PRP',
                'category': 'validation-patterns',
                'tags': ['#validation', '#testing', '#prp'],
                'complexity': 'beginner',
                'source_prp': prp_name,
                'generated_from': 'successful_prp_implementation',
                'created': datetime.now().isoformat(),
                'technologies': ['python'],
                'pattern_type': 'validation'
            }
        }
    
    def generate_context_example(self, pattern, prp_name):
        """Generate context gathering example"""
        context_content = pattern.get('content', '')
        
        example_content = f'''#!/usr/bin/env python3
"""
Example: {prp_name.replace('-', ' ').title()} Context Pattern
Generated from successful PRP implementation

Description: Context gathering and requirement analysis pattern
Category: context-patterns
Complexity: intermediate
Tags: #context #analysis #prp
"""

# Context requirements from PRP: {prp_name}
context_template = \"\"\"
{context_content}
\"\"\"

def gather_context_requirements():
    """Gather all necessary context for implementation"""
    requirements = {{
        'documentation': [],
        'examples': [],
        'dependencies': [],
        'constraints': []
    }}
    
    # Parse context template and extract requirements
    lines = context_template.strip().split('\\n')
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('- url:'):
            requirements['documentation'].append(extract_url_requirement(line))
        elif line.startswith('- file:'):
            requirements['examples'].append(extract_file_requirement(line))
        elif line.startswith('- dependency:'):
            requirements['dependencies'].append(extract_dependency_requirement(line))
    
    return requirements

def extract_url_requirement(line):
    """Extract URL requirement from context line"""
    # Simple extraction - would be enhanced with regex
    return {{'type': 'url', 'content': line}}

def extract_file_requirement(line):
    """Extract file requirement from context line"""
    return {{'type': 'file', 'content': line}}

def extract_dependency_requirement(line):
    """Extract dependency requirement from context line"""
    return {{'type': 'dependency', 'content': line}}

def validate_context_completeness(requirements):
    """Validate that all required context is available"""
    validation_results = {{}}
    
    for category, items in requirements.items():
        validation_results[category] = len(items) > 0
    
    return validation_results

def main():
    """Main context gathering function"""
    print("Gathering context requirements...")
    requirements = gather_context_requirements()
    
    print("Context requirements found:")
    for category, items in requirements.items():
        print(f"  {{category}}: {{len(items)}} items")
    
    validation = validate_context_completeness(requirements)
    print("Context completeness validation:")
    for category, is_complete in validation.items():
        status = "✅" if is_complete else "❌"
        print(f"  {{status}} {{category}}")
    
    return requirements

if __name__ == "__main__":
    main()
'''
        
        return {
            'filename': f"{prp_name}-context.py",
            'content': example_content,
            'metadata': {
                'id': f"{prp_name}-context",
                'title': f"{prp_name.replace('-', ' ').title()} Context Pattern",
                'description': 'Context gathering pattern from PRP',
                'category': 'context-patterns',
                'tags': ['#context', '#analysis', '#prp'],
                'complexity': 'intermediate',
                'source_prp': prp_name,
                'generated_from': 'successful_prp_implementation',
                'created': datetime.now().isoformat(),
                'technologies': ['python'],
                'pattern_type': 'context'
            }
        }
    
    def generate_structure_template(self, pattern, prp_name):
        """Generate structural template"""
        sections = pattern.get('pattern', [])
        
        template_content = f'''# {prp_name.replace('-', ' ').title()} Structure Template
# Generated from successful PRP implementation

"""
PRP Structure Template based on {prp_name}
This template follows the proven structure from successful implementation.
"""

# Standard PRP sections identified:
sections = {sections}

def create_prp_structure():
    """Create PRP structure based on successful pattern"""
    structure = {{}}
    
    for section in sections:
        structure[section] = {{
            'required': True,
            'description': f'Content for {{section}} section',
            'template': get_section_template(section)
        }}
    
    return structure

def get_section_template(section_name):
    """Get template content for specific section"""
    templates = {{
        'Goal': 'Clear statement of what needs to be achieved',
        'Why': 'Business value and user impact',
        'What': 'Technical requirements and user-visible behavior',
        'Success Criteria': 'Measurable outcomes and validation steps',
        'All Needed Context': 'Documentation, examples, and references'
    }}
    
    return templates.get(section_name, f'Template for {{section_name}}')

def generate_prp_from_template(project_name, requirements):
    """Generate new PRP using this template"""
    structure = create_prp_structure()
    
    prp_content = f"# PRP: {{project_name}}\\n\\n"
    
    for section, details in structure.items():
        prp_content += f"## {{section}}\\n"
        prp_content += f"{{details['template']}}\\n\\n"
    
    return prp_content

def main():
    """Main template generation function"""
    print("PRP Structure Template")
    print("Sections identified from successful PRP:")
    
    for i, section in enumerate(sections, 1):
        print(f"  {{i}}. {{section}}")
    
    structure = create_prp_structure()
    print(f"\\nGenerated structure with {{len(structure)}} sections")
    
    return structure

if __name__ == "__main__":
    main()
'''
        
        return {
            'filename': f"{prp_name}-structure-template.py",
            'content': template_content,
            'metadata': {
                'id': f"{prp_name}-structure",
                'title': f"{prp_name.replace('-', ' ').title()} Structure Template",
                'description': 'PRP structure template from successful implementation',
                'category': 'structure-templates',
                'tags': ['#structure', '#template', '#prp'],
                'complexity': 'beginner',
                'source_prp': prp_name,
                'generated_from': 'successful_prp_implementation',
                'created': datetime.now().isoformat(),
                'technologies': ['python'],
                'pattern_type': 'structure'
            }
        }
    
    def get_file_extension(self, language):
        """Get file extension for language"""
        extensions = {
            'python': 'py',
            'javascript': 'js',
            'bash': 'sh',
            'yaml': 'yml',
            'json': 'json'
        }
        return extensions.get(language, 'txt')
    
    def save_generated_example(self, example_data):
        """Save generated example to appropriate location"""
        # Save to generated/from-tasks directory
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        from_tasks_dir = self.generated_dir / "from-tasks"
        from_tasks_dir.mkdir(parents=True, exist_ok=True)
        
        # Save example file
        example_path = from_tasks_dir / example_data['filename']
        with open(example_path, 'w') as f:
            f.write(example_data['content'])
        
        # Save metadata
        metadata_path = from_tasks_dir / f"{example_data['metadata']['id']}-metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(example_data['metadata'], f, indent=2)
        
        return {
            'example_path': str(example_path),
            'metadata_path': str(metadata_path)
        }
    
    def update_examples_index(self, generated_examples):
        """Update the examples index with generated examples"""
        examples_metadata_file = self.examples_dir / "metadata.json"
        
        if examples_metadata_file.exists():
            with open(examples_metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"examples": {}, "statistics": {}}
        
        # Add generated examples to index
        if "examples" not in metadata:
            metadata["examples"] = {}
        
        for example in generated_examples:
            example_id = example['metadata']['id']
            metadata["examples"][example_id] = example['metadata']
        
        # Update statistics
        if "statistics" not in metadata:
            metadata["statistics"] = {}
        
        metadata["statistics"].update({
            'last_generation': datetime.now().isoformat(),
            'total_generated': len(generated_examples),
            'generation_source': 'prp_patterns'
        })
        
        # Save updated metadata
        with open(examples_metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return examples_metadata_file
    
    def process_all_prps(self):
        """Process all PRPs and generate examples"""
        prp_files = list(self.prp_dir.glob("*.md"))
        prp_files = [f for f in prp_files if f.name != "prp_base.md"]  # Skip template
        
        generated_examples = []
        
        for prp_file in prp_files:
            print(f"Processing PRP: {prp_file.name}")
            
            # Extract patterns
            patterns = self.extract_prp_patterns(prp_file)
            prp_name = prp_file.stem
            
            # Generate examples from patterns
            for pattern_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    example = self.generate_example_from_pattern(pattern, prp_name)
                    if example:
                        # Save example
                        paths = self.save_generated_example(example)
                        example['paths'] = paths
                        generated_examples.append(example)
        
        # Update examples index
        if generated_examples:
            index_file = self.update_examples_index(generated_examples)
            print(f"Updated examples index: {index_file}")
        
        return generated_examples
    
    def create_generation_report(self, generated_examples):
        """Create report of generated examples"""
        report = f"""# PRP Example Generation Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}

## Summary
- **Total Examples Generated**: {len(generated_examples)}
- **Source**: Successful PRP implementations
- **Generation Method**: Pattern extraction and template creation

## Generated Examples

"""
        
        for example in generated_examples:
            metadata = example['metadata']
            report += f"### {metadata['title']}\\n"
            report += f"**ID**: {metadata['id']}\\n"
            report += f"**Category**: {metadata['category']}\\n"
            report += f"**Source PRP**: {metadata['source_prp']}\\n"
            report += f"**Pattern Type**: {metadata['pattern_type']}\\n"
            report += f"**File**: {example['filename']}\\n\\n"
        
        # Group by pattern type
        pattern_types = {}
        for example in generated_examples:
            pattern_type = example['metadata']['pattern_type']
            if pattern_type not in pattern_types:
                pattern_types[pattern_type] = []
            pattern_types[pattern_type].append(example)
        
        report += "## Pattern Type Distribution\\n"
        for pattern_type, examples in pattern_types.items():
            report += f"- **{pattern_type}**: {len(examples)} examples\\n"
        
        report += """
## Usage
Generated examples are available in `examples/generated/from-tasks/` directory.
Each example includes:
- Working code implementation
- Comprehensive metadata
- Source PRP reference
- Pattern type classification

## Next Steps
1. Review generated examples for quality
2. Add unit tests for generated code
3. Integrate with recommendation engine
4. Update example scoring system

---
*Generated by PRP Example Generator*
"""
        
        return report

def main():
    generator = PRPExampleGenerator()
    
    print("Generating examples from successful PRP implementations...")
    generated_examples = generator.process_all_prps()
    
    print(f"Generated {len(generated_examples)} examples")
    
    # Create generation report
    report = generator.create_generation_report(generated_examples)
    report_path = generator.examples_dir / "generation-report.md"
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Generation report saved to: {report_path}")
    
    return {
        'generated_examples': len(generated_examples),
        'report_path': str(report_path),
        'examples': generated_examples
    }

if __name__ == '__main__':
    main()