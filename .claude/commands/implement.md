---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, TodoWrite, Task]
description: "Feature and code implementation with intelligent persona activation and MCP integration"
---

# /sc:implement - Feature Implementation

## Purpose
Implement features, components, and code functionality with intelligent expert activation and comprehensive development support.

## Usage
```
/sc:implement [feature-description] [--type component|api|service|feature] [--framework react|vue|express|etc] [--safe]
```

## Arguments
- `feature-description` - Description of what to implement
- `--type` - Implementation type (component, api, service, feature, module)
- `--framework` - Target framework or technology stack
- `--safe` - Use conservative implementation approach
- `--iterative` - Enable iterative development with validation steps
- `--with-tests` - Include test implementation
- `--documentation` - Generate documentation alongside implementation

## Execution
1. Analyze implementation requirements and detect technology context
2. Auto-activate relevant personas (frontend, backend, security, etc.)
3. Coordinate with MCP servers (Magic for UI, Context7 for patterns, Sequential for complex logic)
4. Generate implementation code with best practices
5. Apply security and quality validation
6. Provide testing recommendations and next steps

## 🔗 SUPREME CLAUDE CODE INTEGRATION

### Enhanced Tool Orchestration
```yaml
Core_Tools:
  Write_MultiEdit: "Intelligent code generation with pattern recognition"
  Read_Glob: "Advanced codebase analysis with semantic understanding"
  TodoWrite: "Smart progress tracking with dependency awareness"
  Task: "Complex multi-step orchestration with failure recovery"
  WebFetch_Search: "Real-time documentation and best practice research"
  
MCP_Integration:
  Magic: "Enhanced UI generation with component intelligence"
  Context7: "Advanced pattern recognition and code suggestions"
  Sequential: "Complex logic orchestration with reasoning chains"
  
AI_Coordination:
  parallel_execution: "Coordinate multiple AI agents simultaneously"
  context_sharing: "Share context and learning across tool interactions"
  failure_recovery: "Intelligent fallback and error recovery strategies"
```

### 🎭 SUPREME AUTO-ACTIVATION PATTERNS

#### Frontend Excellence
```yaml
Frontend_Supremacy:
  triggers: ["UI", "component", "React", "Vue", "Angular", "interface"]
  personas: ["UI/UX Expert", "Accessibility Specialist", "Performance Optimizer"]
  tools: ["Magic MCP", "Component Library", "Style Guide"]
  enhancements: ["Responsive Design", "Accessibility", "Performance"]
```

#### Backend Mastery
```yaml
Backend_Intelligence:
  triggers: ["API", "service", "database", "server", "microservice"]
  personas: ["Backend Architect", "Database Expert", "API Designer"]
  tools: ["Sequential MCP", "Database Tools", "API Testing"]
  enhancements: ["Scalability", "Security", "Performance"]
```

#### Security Fortress
```yaml
Security_Supremacy:
  triggers: ["auth", "security", "encryption", "privacy", "compliance"]
  personas: ["Security Expert", "Compliance Officer", "Crypto Specialist"]
  tools: ["Security Scanner", "Vulnerability Assessment", "Audit Tools"]
  enhancements: ["Zero Trust", "Defense in Depth", "Compliance"]
```

#### Architecture Wisdom
```yaml
Architecture_Excellence:
  triggers: ["system", "architecture", "design", "pattern", "structure"]
  personas: ["Solution Architect", "Design Pattern Expert", "System Designer"]
  tools: ["Context7 MCP", "Pattern Library", "Architecture Tools"]
  enhancements: ["Modularity", "Extensibility", "Maintainability"]
```

#### Performance Optimization
```yaml
Performance_Supremacy:
  triggers: ["performance", "optimization", "speed", "efficiency", "scale"]
  personas: ["Performance Engineer", "Optimization Expert", "Scalability Specialist"]
  tools: ["Profiling Tools", "Benchmark Suite", "Monitoring"]
  enhancements: ["Speed", "Memory Efficiency", "Scalability"]
```

## Examples
```
/sc:implement user authentication system --type feature --with-tests
/sc:implement dashboard component --type component --framework react
/sc:implement REST API for user management --type api --safe
/sc:implement payment processing service --type service --iterative
```