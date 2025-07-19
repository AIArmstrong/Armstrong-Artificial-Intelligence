# SuperClaude v3 Command Mapping Guide

## 🔄 v2 to v3 Command Migration

### Critical Command Changes

#### `/build` Command - **BREAKING CHANGE**
```yaml
v2_behavior:
  command: "/build"
  purpose: "Feature implementation and development"
  usage: "/build user-authentication-system"
  
v3_behavior:
  command: "/build"  
  purpose: "Compilation and packaging ONLY"
  usage: "/build --react --production"
  
v3_replacement:
  command: "/sc:implement"
  purpose: "Feature implementation and development"
  usage: "/sc:implement user-authentication-system"
```

**Migration Required**: All `/build` commands used for feature development must change to `/sc:implement`

#### Command Prefix System
```yaml
v2_commands:
  format: "/command"
  examples: ["/analyze", "/improve", "/troubleshoot"]
  
v3_commands:
  format: "/sc:command"
  examples: ["/sc:analyze", "/sc:improve", "/sc:troubleshoot"]
```

### Complete Command Mapping

#### Development Commands
| v2 Command | v3 Command | Purpose | Changes |
|------------|------------|---------|---------|
| `/build [feature]` | `/sc:implement [feature]` | Feature implementation | ⚠️ **BREAKING** - Different command |
| `/build --compile` | `/sc:build` | Compilation/packaging | ✅ Consistent behavior |
| `/dev-setup` | `/sc:dev-setup` | Environment setup | ✅ Enhanced with profiles |
| `/test` | `/sc:test` | Testing workflows | ✅ Enhanced with Playwright |

#### Analysis Commands
| v2 Command | v3 Command | Purpose | Changes |
|------------|------------|---------|---------|
| `/analyze` | `/sc:analyze` | Code analysis | ✅ Enhanced with wave orchestration |
| `/troubleshoot` | `/sc:troubleshoot` | Debugging | ✅ Enhanced with MCP integration |
| `/explain` | `/sc:explain` | Documentation | ✅ Enhanced with Context7 |

#### Quality Commands
| v2 Command | v3 Command | Purpose | Changes |
|------------|------------|---------|---------|
| `/improve` | `/sc:improve` | Code enhancement | ✅ Enhanced with iterative loops |
| `/cleanup` | `/sc:cleanup` | Maintenance | ✅ Enhanced with validation |
| `/review` | `/sc:review` | Code review | ✅ Enhanced with evidence-based recommendations |

#### Operations Commands
| v2 Command | v3 Command | Purpose | Changes |
|------------|------------|---------|---------|
| `/deploy` | `/sc:deploy` | Deployment | ✅ Enhanced with safety checks |
| `/git` | `/sc:git` | Git operations | ✅ Enhanced with workflow management |
| `/scan` | `/sc:scan` | Security scanning | ✅ Enhanced with OWASP compliance |

#### Design & Workflow Commands
| v2 Command | v3 Command | Purpose | Changes |
|------------|------------|---------|---------|
| `/design` | `/sc:design` | System design | ✅ Enhanced with Magic integration |
| `/task` | `/sc:task` | Task management | ✅ Enhanced with wave orchestration |
| `/document` | `/sc:document` | Documentation | ✅ Enhanced with professional writing |

### New v3 Commands

#### Additional Commands in v3
| Command | Purpose | New Features |
|---------|---------|--------------|
| `/sc:estimate` | Project estimation | Evidence-based estimation with risk assessment |
| `/sc:migrate` | Data/code migration | Safe migrations with rollback capabilities |
| `/sc:index` | Command catalog | Interactive command discovery |
| `/sc:load` | Project context | Enhanced project understanding |
| `/sc:spawn` | Task orchestration | Parallel task execution |

### Enhanced Features in v3

#### Wave Orchestration
```yaml
activation:
  automatic: "complexity ≥0.7 + files >20 + operation_types >2"
  manual: "--wave-mode force"
  
strategies:
  progressive: "Incremental enhancement"
  systematic: "Methodical analysis"
  adaptive: "Dynamic configuration"
  enterprise: "Large-scale orchestration"
```

#### Enhanced Personas
```yaml
v2_personas: 9
v3_personas: 11
new_additions:
  - devops: "Infrastructure specialist"
  - scribe: "Professional documentation specialist"
  
improvements:
  - auto_activation: "Multi-factor scoring with context awareness"
  - specialization: "Domain-specific optimization"
  - collaboration: "Cross-persona coordination"
```

#### Advanced MCP Integration
```yaml
servers:
  context7: "Enhanced documentation and research"
  sequential: "Improved multi-step reasoning"
  magic: "Advanced UI component generation"
  playwright: "Comprehensive browser automation"
  
coordination:
  - intelligent_routing: "Task-server affinity matching"
  - fallback_strategies: "Graceful degradation"
  - caching: "Performance optimization"
```

### Migration Checklist

#### For AAI System Migration
- [x] Update bridge system to v3 paths
- [x] Update brain/Claude.md to reference v3 bridge
- [ ] Update any `/build` commands to `/sc:implement`
- [ ] Test v3 command functionality
- [ ] Verify MCP integration works
- [ ] Monitor persona auto-activation

#### For Users/Workflows
- [ ] Replace `/build [feature]` with `/sc:implement [feature]`
- [ ] Add `/sc:` prefix to all commands
- [ ] Update documentation and scripts
- [ ] Test wave orchestration features
- [ ] Verify enhanced persona behavior

### Backward Compatibility

#### What's Preserved
- **Command Behavior**: Core functionality remains the same
- **Persona System**: All v2 personas included with enhancements
- **MCP Integration**: Same servers with improved coordination
- **Token Efficiency**: UltraCompressed mode enhanced

#### What's Changed
- **Command Prefix**: `/command` → `/sc:command`
- **Build Command**: `/build [feature]` → `/sc:implement [feature]`
- **File Structure**: Different paths for framework files
- **Installation**: Python installer instead of bash scripts

### Error Handling

#### Common Migration Issues
```yaml
issue_1:
  problem: "Command not found"
  cause: "Missing /sc: prefix"
  solution: "Add /sc: prefix to all commands"
  
issue_2:
  problem: "Build command doesn't implement features"
  cause: "Using /sc:build instead of /sc:implement"
  solution: "Use /sc:implement for feature development"
  
issue_3:
  problem: "Bridge includes fail"
  cause: "Old v2 paths in bridge"
  solution: "Update to v3 bridge system"
```

### Testing Commands

#### Validation Tests
```bash
# Test basic command functionality
/sc:analyze --code --think

# Test feature implementation
/sc:implement "test feature" --tdd

# Test persona activation
/sc:design --api --persona-architect

# Test MCP integration
/sc:explain --depth expert --c7

# Test wave orchestration
/sc:improve --comprehensive --wave-mode auto
```

### Rollback Procedures

#### Emergency Rollback
```bash
# 1. Restore v2 bridge
cp brain/logs/archives/superclaude-v2-backup-20250715/superclaude-bridge-v2.md brain/modules/superclaude-bridge.md

# 2. Update brain/Claude.md to reference v2 bridge
# Change line 205 back to: @include brain/modules/superclaude-bridge.md

# 3. Restore v2 installation
cp -r brain/logs/archives/superclaude-v2-backup-20250715/superclaude-base ./
```

---

*SuperClaude v3 Command Mapping | Migration Guide | AAI Integration*