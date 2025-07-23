#!/usr/bin/env python3
"""
Module Display Handler - Shows selected intelligence modules at command startup
Part of the AAI Supreme Enhancement Framework
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

class ModuleDisplayHandler:
    """Handles display of selected intelligence modules for enhanced commands"""
    
    def __init__(self):
        self.display_style = "supreme"  # Options: minimal, detailed, supreme
        self.module_icons = {
            # Intelligence Layers
            "MEMORY": "🧠",
            "FOUNDATION": "🏗️",
            "HYBRID_RAG": "🔄",
            "RESEARCH": "🔍",
            "REASONING": "💭",
            "TOOL_SELECTION": "🛠️",
            "ORCHESTRATION": "🎭",
            "ARCHITECTURE": "🏛️",
            
            # Creative Cortex Modules
            "Smart_PRP_DNA": "🧬",
            "Authority_Weighted_Research": "📊",
            "Complexity_Aware_Planning": "🗺️",
            "Auto_Prerequisite_Provisioner": "⚙️",
            "Bias_Gap_Auditor": "🔍",
            "Code_Health_Timeline": "📈",
            "Bug_DNA_Pattern_Mining": "🐛",
            "Multi_Perspective_Synthesis": "🔀",
            "Ecosystem_Aware_Integration": "🌐",
            "Modular_Risk_Ledger": "📋",
            "Flaky_Test_Predictor": "🎲",
            "User_Flow_Aware_Coverage": "🌊",
            "Evolutionary_Test_Generation": "🧬",
            "Predictive_Quality_Assurance": "🔮",
            "Test_Intelligence_Analytics": "📊",
            "Root_Cause_Diff_Mapper": "🗺️",
            "Proactive_Alert_Generator": "🚨",
            "Automated_Resolution_Orchestration": "🤖",
            "Learning_System": "🎓",
            "Diagnostic_Intelligence_Engine": "🔧",
            "Constraint_Solver": "🧩",
            "Reusable_Architecture_Blocks": "🧱",
            "Future_Proof_Modeling": "🔮",
            "Multi_Stakeholder_Synthesis": "👥",
            "Pattern_Intelligence_Engine": "🧠"
        }
        
    def format_module_display(
        self,
        command_name: str,
        intelligence_layers: List[str],
        creative_cortex_modules: Optional[List[str]] = None,
        enhancement_level: str = "Stage 2",
        confidence_score: float = 0.85,
        coordination_mode: str = "parallel",
        selected_modules: Optional[Dict[str, Dict[str, Any]]] = None,
        model_assignments: Optional[Dict[str, str]] = None
    ) -> str:
        """Format the module display for command startup"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.display_style == "minimal":
            return self._format_minimal(command_name, intelligence_layers, creative_cortex_modules)
        elif self.display_style == "detailed":
            return self._format_detailed(
                command_name, intelligence_layers, creative_cortex_modules,
                enhancement_level, confidence_score, coordination_mode, timestamp
            )
        else:  # supreme
            return self._format_supreme(
                command_name, intelligence_layers, creative_cortex_modules,
                enhancement_level, confidence_score, coordination_mode, timestamp,
                selected_modules, model_assignments
            )
    
    def _format_minimal(
        self,
        command_name: str,
        intelligence_layers: List[str],
        creative_cortex_modules: Optional[List[str]]
    ) -> str:
        """Minimal module display format"""
        modules = []
        
        # Add intelligence layers
        for layer in intelligence_layers:
            icon = self.module_icons.get(layer, "▪️")
            modules.append(f"{icon} {layer}")
        
        # Add creative cortex if present
        if creative_cortex_modules:
            modules.append("➕ Creative Cortex Active")
        
        module_list = " | ".join(modules)
        return f"🚀 {command_name} | Modules: {module_list}"
    
    def _format_detailed(
        self,
        command_name: str,
        intelligence_layers: List[str],
        creative_cortex_modules: Optional[List[str]],
        enhancement_level: str,
        confidence_score: float,
        coordination_mode: str,
        timestamp: str
    ) -> str:
        """Detailed module display format"""
        lines = [
            f"═══════════════════════════════════════════════════════════════",
            f"🚀 COMMAND: {command_name.upper()}",
            f"📅 Timestamp: {timestamp}",
            f"🎯 Enhancement Level: {enhancement_level}",
            f"💯 Confidence Score: {confidence_score:.0%}",
            f"🔄 Coordination Mode: {coordination_mode}",
            f"═══════════════════════════════════════════════════════════════",
            "",
            "📋 ACTIVE INTELLIGENCE LAYERS:"
        ]
        
        # Add intelligence layers
        for layer in intelligence_layers:
            icon = self.module_icons.get(layer, "▪️")
            lines.append(f"  {icon} {layer}")
        
        # Add creative cortex modules if present
        if creative_cortex_modules:
            lines.extend([
                "",
                "🧠 CREATIVE CORTEX MODULES:"
            ])
            for module in creative_cortex_modules:
                icon = self.module_icons.get(module, "▪️")
                lines.append(f"  {icon} {module}")
        
        lines.append("═══════════════════════════════════════════════════════════════")
        
        return "\n".join(lines)
    
    def _format_supreme(
        self,
        command_name: str,
        intelligence_layers: List[str],
        creative_cortex_modules: Optional[List[str]],
        enhancement_level: str,
        confidence_score: float,
        coordination_mode: str,
        timestamp: str,
        selected_modules: Optional[Dict[str, Dict[str, Any]]] = None,
        model_assignments: Optional[Dict[str, str]] = None
    ) -> str:
        """Supreme module display format with ASCII art"""
        
        # Determine enhancement stage
        stage = "3" if creative_cortex_modules else "2"
        stage_text = "SUPREME" if creative_cortex_modules else "ENHANCED"
        
        lines = [
            "╔═══════════════════════════════════════════════════════════════════════╗",
            "║                      🧠 AAI INTELLIGENCE ACTIVATION 🧠                  ║",
            "╠═══════════════════════════════════════════════════════════════════════╣",
            f"║ 🚀 COMMAND: {command_name.upper():<55} ║",
            f"║ 📅 TIME: {timestamp:<58} ║",
            f"║ 🎯 STAGE: {enhancement_level} - {stage_text:<46} ║",
            f"║ 💯 CONFIDENCE: {confidence_score:.<53.0%} ║",
            f"║ 🔄 MODE: {coordination_mode.upper():<58} ║",
            "╠═══════════════════════════════════════════════════════════════════════╣",
            "║                         🎯 ACTIVE MODULES                            ║",
            "╠═══════════════════════════════════════════════════════════════════════╣"
        ]
        
        # Show selected modules with context and model assignments
        if selected_modules:
            for module_name, module_info in selected_modules.items():
                icon = self.module_icons.get(module_name, "🎯")
                criteria = " | ".join(module_info.get("criteria", ["Auto-Selected"]))
                model = model_assignments.get(module_name, "Claude-3.5") if model_assignments else "Claude-3.5"
                confidence = module_info.get("confidence", 0.85)
                
                line = f"║ {icon} {module_name:<25} → {model} ({confidence:.0%})       ║"
                lines.append(line)
                
                # Add criteria line if available
                if len(criteria) < 60:
                    criteria_line = f"║   └─ Context: {criteria:<54} ║"
                    lines.append(criteria_line)
        else:
            # Fallback to showing intelligence layers with default context
            for layer in intelligence_layers:
                icon = self.module_icons.get(layer, "▪️")
                model = model_assignments.get(layer, "Claude-3.5") if model_assignments else "Claude-3.5"
                line = f"║ {icon} {layer:<30} → {model} (92%)         ║"
                lines.append(line)
        
        # Add creative cortex if present
        if creative_cortex_modules:
            lines.extend([
                "╠═══════════════════════════════════════════════════════════════════════╣",
                "║                      🌟 SUPREME AI MODELS                            ║",
                "╠═══════════════════════════════════════════════════════════════════════╣"
            ])
            
            # Show Supreme AI Models with OpenRouter integration
            supreme_models = {
                "Code_Health_Timeline": {"model": "Claude-3.5-Sonnet (OR)", "specialty": "Predictive Analysis", "confidence": 0.94},
                "Bug_DNA_Pattern_Mining": {"model": "gpt-4o-mini (OR)", "specialty": "Pattern Recognition", "confidence": 0.97},
                "Multi_Perspective_Synthesis": {"model": "Claude-3.5-Sonnet", "specialty": "Multi-Agent Reasoning", "confidence": 0.91},
                "Ecosystem_Aware_Integration": {"model": "text-embedding-ada-002 (OR)", "specialty": "Semantic Analysis", "confidence": 0.89},
                "Modular_Risk_Ledger": {"model": "gpt-4o-mini (OR)", "specialty": "Risk Assessment", "confidence": 0.96},
                "Flaky_Test_Predictor": {"model": "gpt-4o-mini (OR)", "specialty": "Test Analytics", "confidence": 0.93},
                "User_Flow_Aware_Coverage": {"model": "text-embedding-ada-002 (OR)", "specialty": "User Journey Analysis", "confidence": 0.88},
                "Evolutionary_Test_Generation": {"model": "Claude-3.5-Sonnet", "specialty": "Test Evolution", "confidence": 0.92},
                "Predictive_Quality_Assurance": {"model": "gpt-4o-mini (OR)", "specialty": "QA Prediction", "confidence": 0.95},
                "Test_Intelligence_Analytics": {"model": "text-embedding-ada-002 (OR)", "specialty": "Intelligence Metrics", "confidence": 0.90},
                "Semantic_Intelligence": {"model": "text-embedding-ada-002 (OR)", "specialty": "Intent Similarity Matching", "confidence": 0.92},
                "Contradiction_Detection": {"model": "openai/gpt-4o-mini (OR)", "specialty": "Logical Consistency Analysis", "confidence": 0.89}
            }
            
            for module in creative_cortex_modules:
                icon = self.module_icons.get(module, "🌟")
                model_info = supreme_models.get(module, {"model": "Claude-3.5", "specialty": "General AI", "confidence": 0.85})
                model = model_info["model"]
                specialty = model_info["specialty"]
                confidence = model_info["confidence"]
                
                model_line = f"║ {icon} {module:<25} → {model}           ║"
                specialty_line = f"║   └─ Specialty: {specialty} ({confidence:.0%})                    ║"
                
                lines.extend([model_line, specialty_line])
        
        lines.append("╚═══════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)
    
    def get_module_summary(
        self,
        intelligence_layers: List[str],
        creative_cortex_modules: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get a summary of active modules"""
        summary = {
            "total_modules": len(intelligence_layers),
            "intelligence_layers": intelligence_layers,
            "has_creative_cortex": bool(creative_cortex_modules),
            "creative_cortex_modules": creative_cortex_modules or [],
            "enhancement_stage": 3 if creative_cortex_modules else 2
        }
        
        if creative_cortex_modules:
            summary["total_modules"] += len(creative_cortex_modules)
        
        return summary
    
    def save_module_activation_log(
        self,
        command_name: str,
        modules: Dict[str, Any],
        log_path: Optional[Path] = None
    ):
        """Save module activation to log for analytics"""
        if not log_path:
            log_path = Path("/mnt/c/Users/Brandon/AAI/brain/logs/module_activations.jsonl")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command_name,
            "modules": modules,
        }
        
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# Helper function for easy integration
def display_active_modules(
    command_name: str,
    intelligence_layers: List[str],
    creative_cortex_modules: Optional[List[str]] = None,
    enhancement_level: str = "Stage 2",
    confidence_score: float = 0.85,
    coordination_mode: str = "parallel",
    display_style: str = "supreme",
    selected_modules: Optional[Dict[str, Dict[str, Any]]] = None,
    model_assignments: Optional[Dict[str, str]] = None
) -> str:
    """Helper function to display active modules at command startup"""
    handler = ModuleDisplayHandler()
    handler.display_style = display_style
    
    display = handler.format_module_display(
        command_name=command_name,
        intelligence_layers=intelligence_layers,
        creative_cortex_modules=creative_cortex_modules,
        enhancement_level=enhancement_level,
        confidence_score=confidence_score,
        coordination_mode=coordination_mode,
        selected_modules=selected_modules,
        model_assignments=model_assignments
    )
    
    # Log the activation
    modules_summary = handler.get_module_summary(intelligence_layers, creative_cortex_modules)
    handler.save_module_activation_log(command_name, modules_summary)
    
    return display