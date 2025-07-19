# Third-Party Libraries Documentation

## Purpose
Source truth documentation for external libraries, frameworks, and integrations used in AAI system.

## Structure
```
libraries/
├── jina/            # Jina scraping framework
├── supabase/        # Database and caching
├── matplotlib/      # Visualization libraries
├── langchain/       # LLM orchestration (if used)
├── fastapi/         # API framework documentation
└── testing/         # Testing framework docs
```

## Current Integrations
- **Jina**: Document scraping and processing
- **Supabase**: Database and caching backend
- **Matplotlib**: Dashboard visualization
- **OpenRouter**: LLM API routing
- **Pytest**: Testing framework (if implemented)

## Usage Guidelines
1. **Version Tracking** - Always specify version used
2. **Integration Patterns** - Document how we use each library
3. **Gotchas** - Common issues and solutions
4. **Performance** - Optimization tips and benchmarks

## Critical Files to Add
- [ ] Jina documentation and scraping patterns
- [ ] Supabase API reference and schema
- [ ] Matplotlib visualization guides
- [ ] OpenRouter integration documentation
- [ ] Testing framework setup guides

---
*Maintained by AAI system - Last updated: 2025-07-14*