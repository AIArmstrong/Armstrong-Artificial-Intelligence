# Example_Multi_Agent_Prp Structure Template
# Generated from successful PRP implementation

"""
PRP Structure Template based on EXAMPLE_multi_agent_prp
This template follows the proven structure from successful implementation.
"""

# Standard PRP sections identified:
sections = ['Purpose', 'Core Principles', 'Goal', 'Why', 'What', 'All Needed Context', 'Implementation Blueprint', 'Validation Loop', 'Final Validation Checklist', 'Anti-Patterns to Avoid', 'Confidence Score: 9/10']

def create_prp_structure():
    """Create PRP structure based on successful pattern"""
    structure = {}
    
    for section in sections:
        structure[section] = {
            'required': True,
            'description': f'Content for {section} section',
            'template': get_section_template(section)
        }
    
    return structure

def get_section_template(section_name):
    """Get template content for specific section"""
    templates = {
        'Goal': 'Clear statement of what needs to be achieved',
        'Why': 'Business value and user impact',
        'What': 'Technical requirements and user-visible behavior',
        'Success Criteria': 'Measurable outcomes and validation steps',
        'All Needed Context': 'Documentation, examples, and references'
    }
    
    return templates.get(section_name, f'Template for {section_name}')

def generate_prp_from_template(project_name, requirements):
    """Generate new PRP using this template"""
    structure = create_prp_structure()
    
    prp_content = f"# PRP: {project_name}\n\n"
    
    for section, details in structure.items():
        prp_content += f"## {section}\n"
        prp_content += f"{details['template']}\n\n"
    
    return prp_content

def main():
    """Main template generation function"""
    print("PRP Structure Template")
    print("Sections identified from successful PRP:")
    
    for i, section in enumerate(sections, 1):
        print(f"  {i}. {section}")
    
    structure = create_prp_structure()
    print(f"\nGenerated structure with {len(structure)} sections")
    
    return structure

if __name__ == "__main__":
    main()
