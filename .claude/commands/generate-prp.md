# Create PRP

YOU MUST DO IN-DEPTH RESEARCH, FOLLOW THE <RESEARCH PROCESS>

<RESEARCH PROCESS>

   - Don't only research one page, and don't use your own webscraping tool - instead scrape many relevant pages from all documentation links mentioned in the initial.md file
   - Take my tech as sacred truth, for example if I say a model name then research that model name for LLM usage - don't assume from your own knowledge at any point
   - When I say don't just research one page, I mean do incredibly in-depth research, like to the ponit where it's just absolutely ridiculous how much research you've actually done, then when you creat the PRD document you need to put absolutely everything into that including references to the .md files you put inside the /research/ directory so any AI can pick up your PRD and generate WORKING and COMPLETE production ready code.

</RESEARCH PROCESS>

## Feature file: $ARGUMENTS

Generate a complete PRP for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

The AI agent only gets the context you are appending to the PRP and training data. Assuma the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Research Process

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRP
   - Note existing conventions to follow
   - Check test patterns for validation approach

2. **External Research**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls
   - Don't only research one page, and don't use your own webscraping tool - instead scrape many relevant pages from all documentation links mentioned in the initial.md file
   - Take my tech as sacred truth, for example if I say a model name then research that model name for LLM usage - don't assume from your own knowledge at any point
   - When I say don't just research one page, I mean do incredibly in-depth research, like to the ponit where it's just absolutely ridiculous how much research you've actually done, then when you creat the PRD document you need to put absolutely everything into that including INCREDIBLY IN DEPTH CODE EXMAPLES so any AI can pick up your PRD and generate WORKING and COMPLETE production ready code.

3. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

## PRP Generation

Generate a PRP and save to the PRPs directory.   

Using PRPs/templates/prp_base.md as template:

### Critical Context to Include and pass to the AI agent as part of the PRP
- **Documentation**: URLs with specific sections
- **Code Examples**: Real references to .md documentation
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- list tasks to be completed to fullfill the PRP in the order they should be completed

### Validation Gates (Must be Executable) eg for python
```bash
# Syntax/Style
ruff check --fix && mypy .

# Unit Tests
uv run pytest tests/ -v

```

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***

*** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***

## Output

Save as: `PRPs/{project-name}.md`

## 📦 Implementation Readiness Assessment

*** CRITICAL AFTER SAVING THE PRP FILE ***

Automatically run the Implementation Readiness Assessment to identify blockers:

```bash
# Auto-generate and run readiness validation
python scripts/validate_prp_readiness.py --prp PRPs/{project-name}.md --report console

# This will:
# 1. Parse the PRP file for infrastructure/credential/dependency gates
# 2. Test each gate for readiness 
# 3. Generate readiness score and blockers list
# 4. Provide specific fix commands and time estimates
# 5. Log results to brain/logs/readiness_history.md
```

### Readiness Integration Workflow
1. **Generate PRP** → Save to PRPs directory
2. **Auto-run Readiness Assessment** → Identify blockers  
3. **Present Blockers to User** → Clear action items with time estimates
4. **User Fixes Blockers** → Re-run assessment until ≥85% ready
5. **Proceed with Implementation** → High confidence success

### Expected Readiness Output
```bash
=====================================
PRP Readiness Assessment: {project-name}
=====================================

🏗️  Infrastructure Gates: ⚠️  80% (4/5 passed)
🔐 Credential Gates: ❌ 60% (3/5 passed)  
🔧 Dependency Gates: ✅ 95% (19/20 passed)
🌍 Environment Gates: ✅ 100% (5/5 passed)

=====================================
OVERALL READINESS: ⚠️ 78%
RECOMMENDATION: Partial Implementation
BLOCKERS: 2 critical credential issues
TIME TO FIX: ~45 minutes
=====================================

📋 Required Actions (Priority Order):
1. 🔴 Add N8N_API_KEY to .env (user, ~5 min)
2. 🔴 Configure Gmail OAuth refresh token (user, ~30 min)
3. 🟡 Restart n8n service on server (user, ~10 min)
```

### Readiness-Based PRP Scoring
- **Readiness ≥95%**: PRP Score +2 (implementation almost guaranteed)
- **Readiness 85-94%**: PRP Score +1 (high confidence)
- **Readiness 70-84%**: PRP Score +0 (baseline confidence)
- **Readiness <70%**: PRP Score -2 (significant implementation risk)

## Quality Checklist
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented
- [ ] **Implementation gates defined for readiness assessment**
- [ ] **Readiness assessment completed with ≥85% score**

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

**Final Score Adjustment**: Add readiness bonus/penalty to base PRP score for realistic implementation confidence.

Remember: The goal is one-pass implementation success through comprehensive context AND verified readiness.