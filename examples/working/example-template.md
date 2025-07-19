# Example Template

## Overview
Template for creating new working examples in the AAI system.

## Required Files for Each Example

### 1. Example Code File
```python
# working/by-category/[category]/[example-name].py
"""
Example: [Example Title]

Description: [What this example demonstrates]
Category: [category]
Complexity: [beginner|intermediate|advanced]
Tags: [#tag1, #tag2, #tag3]
"""

def main():
    """Main example function"""
    pass

if __name__ == "__main__":
    main()
```

### 2. Test File
```python
# tests/unit/test_[example-name].py
"""
Tests for [example-name] example
"""
import pytest
from examples.working.by_category.[category].[example_name] import main

def test_example_works():
    """Test that example runs without error"""
    result = main()
    assert result is not None

def test_example_output():
    """Test example produces expected output"""
    # Add specific tests here
    pass
```

### 3. Metadata Entry
Add to `working/by-category/[category]/metadata.json`:
```json
{
  "example-name": {
    "id": "example-name",
    "title": "Example Title",
    "description": "What this example demonstrates",
    "category": "category-name",
    "tags": ["#tag1", "#tag2"],
    "complexity": "intermediate",
    "created": "2025-07-14T08:00:00Z",
    "last_used": null,
    "usage_count": 0,
    "success_rate": 0.0,
    "feedback_score": 0.0,
    "claude_version": "claude-3-sonnet",
    "technologies": ["python"],
    "test_file": "tests/unit/test_example.py",
    "dependencies": []
  }
}
```

## Categories
- **api-integration**: API calls, authentication, data fetching
- **data-processing**: Data manipulation, transformation, analysis
- **file-operations**: File I/O, parsing, generation
- **testing**: Testing patterns, mock setups, validation
- **automation**: Scripts, task automation, workflow tools
- **visualization**: Charts, graphs, dashboard components

## Quality Standards
- ✅ Must include comprehensive docstrings
- ✅ Must have corresponding unit tests
- ✅ Must include error handling
- ✅ Must be production-ready code
- ✅ Must include usage examples
- ✅ Must specify dependencies clearly

---
*Use this template to maintain consistency across all examples*