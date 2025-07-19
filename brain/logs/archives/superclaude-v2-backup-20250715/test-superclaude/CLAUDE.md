# Test SuperClaude Integration Project

This test project verifies SuperClaude features work correctly with AAI.

## Base AAI Rules
<!-- Import core AAI brain rules -->
@include ../../brain/Claude.md

## SuperClaude Enhanced Features
<!-- Import SuperClaude capabilities via bridge -->
@include ../../brain/modules/superclaude-bridge.md#SuperClaude_Features

## Test-Specific Configuration

### Testing Priorities
1. Verify @include statements resolve correctly
2. Test introspection mode activation
3. Validate token economy features
4. Check error recovery mechanisms

### Expected Behaviors
- Should have access to AAI's core rules (Docker, testing, etc.)
- Should have SuperClaude's advanced features (thinking modes, introspection)
- Should maintain clear separation between declarative and modular logic

### Test Commands
```bash
# Test 1: Basic functionality
echo "Testing basic AAI rules..."

# Test 2: SuperClaude features
echo "Testing introspection mode..."
# [INTROSPECT] command should be available

# Test 3: Token economy
echo "Testing token optimization..."
# Should see compressed responses when appropriate
```

---
*Test project for AAI + SuperClaude integration*