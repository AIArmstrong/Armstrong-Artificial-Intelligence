#!/usr/bin/env python3
"""
Analyze Command Handler - Integrates with Claude's /analyze command
Provides proper tool_use/tool_result handling and chunked output
"""

import asyncio
import json
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from analyze_orchestrator import AnalysisOrchestrator, AnalysisFocus, AnalysisDepth

class AnalyzeCommandHandler:
    """Handles the /analyze command execution with proper Claude tool integration"""
    
    def __init__(self):
        self.orchestrator = AnalysisOrchestrator()
        self.max_output_size = 10000  # Max characters per response chunk
        
    def parse_command_args(self, command: str) -> Dict[str, Any]:
        """Parse /sc:analyze command arguments"""
        args = {
            "target": ".",
            "focus": AnalysisFocus.QUALITY,
            "depth": AnalysisDepth.QUICK,
            "enable_subagents": True,
            "format": "text",
            "resume": False
        }
        
        parts = command.strip().split()
        
        # Skip the command itself
        if parts[0] in ["/analyze", "/sc:analyze"]:
            parts = parts[1:]
            
        # Parse target if provided
        if parts and not parts[0].startswith("--"):
            args["target"] = parts[0]
            parts = parts[1:]
            
        # Parse flags
        i = 0
        while i < len(parts):
            if parts[i] == "--focus" and i + 1 < len(parts):
                try:
                    args["focus"] = AnalysisFocus(parts[i + 1])
                except ValueError:
                    print(f"Invalid focus: {parts[i + 1]}, using default 'quality'")
                i += 2
            elif parts[i] == "--depth" and i + 1 < len(parts):
                try:
                    args["depth"] = AnalysisDepth(parts[i + 1])
                except ValueError:
                    print(f"Invalid depth: {parts[i + 1]}, using default 'quick'")
                i += 2
            elif parts[i] == "--format" and i + 1 < len(parts):
                args["format"] = parts[i + 1]
                i += 2
            elif parts[i] == "--subagents":
                if i + 1 < len(parts) and parts[i + 1].lower() in ["false", "0", "no"]:
                    args["enable_subagents"] = False
                    i += 2
                else:
                    i += 1
            elif parts[i] == "--resume":
                args["resume"] = True
                i += 1
            else:
                i += 1
                
        return args
    
    def create_tool_use_block(self, tool_id: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a proper tool_use block for Claude"""
        return {
            "type": "tool_use",
            "id": tool_id,
            "name": tool_name,
            "input": parameters
        }
    
    def create_tool_result_block(self, tool_id: str, content: str, is_error: bool = False) -> Dict[str, Any]:
        """Create a proper tool_result block for Claude"""
        return {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": content,
            "is_error": is_error
        }
    
    def chunk_output(self, content: str, max_size: int = None) -> List[str]:
        """Break large output into smaller chunks"""
        max_size = max_size or self.max_output_size
        
        if len(content) <= max_size:
            return [content]
            
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            
            if current_size + line_size > max_size and current_chunk:
                # Save current chunk and start new one
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
                
        # Add remaining chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks
    
    def format_analysis_result(self, result: Dict[str, Any], format_type: str = "text") -> str:
        """Format analysis results for output"""
        if format_type == "json":
            return json.dumps(result, indent=2)
            
        # Text format
        output = []
        output.append(f"# Analysis Report: {result.get('target', 'Unknown')}")
        output.append(f"Focus: {result.get('focus', 'Unknown')}")
        output.append(f"Timestamp: {result.get('timestamp', 'Unknown')}")
        output.append("")
        
        # Summary
        summary = result.get('summary', {})
        output.append("## Summary")
        output.append(f"- Total Agents: {summary.get('total_agents', 0)}")
        output.append(f"- Successful: {summary.get('successful', 0)}")
        output.append(f"- Failed: {summary.get('failed', 0)}")
        output.append("")
        
        # Findings
        findings = result.get('findings', {})
        if findings:
            output.append("## Findings")
            for area, data in findings.items():
                output.append(f"\n### {area.replace('_', ' ').title()}")
                if isinstance(data, dict):
                    for key, value in data.items():
                        output.append(f"- {key}: {value}")
                else:
                    output.append(str(data))
            output.append("")
        
        # Recommendations
        recommendations = result.get('recommendations', [])
        if recommendations:
            output.append("## Recommendations")
            for i, rec in enumerate(recommendations, 1):
                output.append(f"{i}. {rec}")
            output.append("")
            
        # Errors
        errors = result.get('errors', [])
        if errors:
            output.append("## Errors Encountered")
            for error in errors:
                output.append(f"- {error.get('agent', 'Unknown')}: {error.get('error', 'Unknown error')}")
                if error.get('retry_count', 0) > 0:
                    output.append(f"  (Retried {error['retry_count']} times)")
            output.append("")
            
        return '\n'.join(output)
    
    async def execute_with_proper_tool_handling(self, command: str) -> List[Dict[str, Any]]:
        """Execute analysis with proper tool_use/tool_result pairing"""
        args = self.parse_command_args(command)
        
        # Create initial tool use block
        tool_id = f"analyze_{int(asyncio.get_event_loop().time() * 1000)}"
        
        messages = []
        
        # Add tool_use block
        messages.append(self.create_tool_use_block(
            tool_id=tool_id,
            tool_name="analyze_code",
            parameters={
                "target": args["target"],
                "focus": args["focus"].value,
                "depth": args["depth"].value,
                "enable_subagents": args["enable_subagents"]
            }
        ))
        
        try:
            # Execute analysis
            result = await self.orchestrator.analyze(
                target=args["target"],
                focus=args["focus"],
                depth=args["depth"],
                enable_subagents=args["enable_subagents"],
                resume=args["resume"]
            )
            
            # Format result
            formatted_result = self.format_analysis_result(result, args["format"])
            
            # Chunk if needed
            chunks = self.chunk_output(formatted_result)
            
            # Add tool_result block(s)
            for i, chunk in enumerate(chunks):
                if i == 0:
                    # First chunk uses the original tool_id
                    messages.append(self.create_tool_result_block(
                        tool_id=tool_id,
                        content=chunk,
                        is_error=False
                    ))
                else:
                    # Additional chunks as separate messages
                    messages.append({
                        "type": "text",
                        "content": f"[Analysis Report Continued - Part {i + 1}]\n\n{chunk}"
                    })
                    
        except Exception as e:
            # Always provide tool_result even on error
            messages.append(self.create_tool_result_block(
                tool_id=tool_id,
                content=f"Analysis failed: {str(e)}",
                is_error=True
            ))
            
        return messages
    
    async def run(self, command: str):
        """Main execution method"""
        print("Starting enhanced /analyze command with rate limiting and chunking...")
        
        try:
            messages = await self.execute_with_proper_tool_handling(command)
            
            # Output messages for Claude to process
            for message in messages:
                print(f"\n--- Message Type: {message.get('type', 'unknown')} ---")
                if message.get('type') == 'tool_use':
                    print(f"Tool: {message.get('name')}")
                    print(f"Parameters: {json.dumps(message.get('input', {}), indent=2)}")
                elif message.get('type') == 'tool_result':
                    print(f"Tool Result (Error: {message.get('is_error', False)})")
                    print(message.get('content', ''))
                else:
                    print(message.get('content', ''))
                    
        except Exception as e:
            print(f"Fatal error in analyze command: {e}")
            sys.exit(1)


# Integration point for Claude
async def handle_analyze_command(command: str):
    """Entry point for Claude to call the analyze command"""
    handler = AnalyzeCommandHandler()
    await handler.run(command)


if __name__ == "__main__":
    # Test execution
    command = "/sc:analyze src/ --focus quality --depth quick"
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        
    asyncio.run(handle_analyze_command(command))