# SuperClaude Bridge Module
<!-- This file selectively imports key SuperClaude capabilities for use in AAI agents -->

## 🧠 Core SuperClaude Features {#SuperClaude_Features}

### 🧭 Thinking Modes
@include ../../superclaude-base/commands/shared/flag-inheritance.yml#Universal Flags (All Commands)

### 🔍 Introspection Capabilities
@include ../../superclaude-base/commands/shared/introspection-patterns.yml#Introspection_Mode

### 🧮 Advanced Token Economy
@include ../../superclaude-base/shared/superclaude-core.yml#Advanced_Token_Economy

### 🔁 Error Recovery
@include ../../superclaude-base/shared/superclaude-mcp.yml#Error_Recovery

### 🧬 Cognitive Personas (Optional)
<!-- Uncomment to enable persona-based problem solving -->
<!-- @include ../../superclaude-base/shared/superclaude-personas.yml#All_Personas -->

---

## 📘 Usage Notes

- Import this bridge module into project-specific `Claude.md` files to inherit select SuperClaude capabilities.
- This enables fine-tuned feature control without bloating your main brain context.
- Use only the features your project needs — don't over-include.
- Maintain strict separation between **AAI declarative logic** and **SuperClaude modular features**.

### 🔗 Example Usage

```md
@include brain/modules/superclaude-bridge.md#SuperClaude_Features
```

Use section-specific includes (#Introspection_Mode, etc.) when you only need certain blocks.

### 📌 Update Reminders
- If the SuperClaude repo structure changes, update the relative paths here.
- If you're using agents across machines or containers, verify brain/modules is properly mirrored.