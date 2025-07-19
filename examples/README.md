# AAI Examples System - Memory Bank of Success

## Overview
Intelligent example repository that Claude can trust and reuse. Features self-recommendation, automatic scoring, and gap analysis.

## Structure
```
examples/
├── working/              # Tested, working code examples
│   ├── by-category/     # Organized by functionality
│   └── metadata.json    # Example tracking and scoring
├── tests/               # Test files that prove examples work
│   ├── unit/           # Unit tests for examples
│   └── integration/    # Integration test scenarios
├── templates/           # Boilerplate patterns
│   ├── prp-starters/   # Common PRP implementation patterns
│   └── api-patterns/   # API integration templates
├── mocks/              # Reusable testing components
│   ├── api-responses/  # Mock API data
│   └── fixtures/       # Test data fixtures
└── generated/          # Auto-generated from successful PRPs
    ├── from-tasks/     # Examples extracted from task completions
    └── patterns/       # Common patterns identified
```

## Key Features

### 🎯 Self-Recommendation Engine
- **Semantic Matching**: Uses OpenRouter embeddings to find relevant examples
- **Gap Analysis**: Identifies missing examples based on PRP patterns
- **Context Awareness**: Matches examples to current task context

### 📊 Feedback-Integrated Scoring
- **Success Tracking**: Monitors example usage outcomes
- **Automatic Scoring**: Updates effectiveness based on feedback
- **Lifecycle Management**: Promotes successful examples, retires ineffective ones

### 🔄 Auto-Generation
- **Pattern Extraction**: Identifies common patterns from successful implementations
- **Template Creation**: Generates boilerplate from repeated successful patterns
- **Continuous Learning**: Evolves example repository based on usage

## Example Metadata Format
Each example includes:
```json
{
  "id": "example-id",
  "title": "Example Title",
  "description": "What this example demonstrates",
  "category": "api-integration",
  "tags": ["#api", "#python", "#async"],
  "complexity": "intermediate",
  "created": "2025-07-14T08:00:00Z",
  "last_used": "2025-07-14T08:00:00Z",
  "usage_count": 5,
  "success_rate": 0.85,
  "feedback_score": 4.2,
  "claude_version": "claude-3-sonnet",
  "technologies": ["python", "fastapi", "asyncio"],
  "test_file": "tests/unit/test_example.py",
  "dependencies": ["requests", "pytest"]
}
```

## Usage

### Finding Examples
1. **Semantic Search**: System auto-recommends based on PRP context
2. **Category Browse**: Explore `working/by-category/`
3. **Tag Filtering**: Search by technology or pattern tags

### Contributing Examples
1. Add working code to `working/by-category/`
2. Create corresponding test in `tests/`
3. Update metadata with example details
4. System will auto-score based on usage

### Testing Examples
- All examples must have corresponding tests
- Run `pytest tests/` to validate example repository
- Integration tests ensure examples work in real scenarios

## Recommendation Engine
The system automatically:
- Analyzes current PRP requirements
- Searches for semantically similar examples
- Identifies gaps in example coverage
- Suggests relevant examples with confidence scores

## Scoring System
Examples are scored on:
- **Usage Frequency**: How often they're used
- **Success Rate**: Percentage of successful implementations
- **Recency**: How recently they've been used
- **Complexity Match**: How well they match task complexity
- **Feedback Score**: User/system feedback ratings

## Auto-Generation
The system automatically generates:
- **Templates**: From repeated successful patterns
- **Examples**: From successful PRP implementations
- **Mocks**: From common API interaction patterns
- **Tests**: Basic test structures for new examples

---
*Intelligent Example Repository | Self-Improving | Context-Aware*