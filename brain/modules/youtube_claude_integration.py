#!/usr/bin/env python3
"""
YouTube Claude Integration - Bridge between Claude Code and YouTube analyzer
Enables Claude to execute /youtube commands with full integration
"""

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional

class YouTubeClaudeIntegration:
    """Integration layer for Claude Code to execute YouTube analysis commands"""
    
    @staticmethod
    async def execute_youtube_command(video_url: str, 
                                    focus: str = "all", 
                                    format: str = "detailed", 
                                    save: bool = False) -> str:
        """
        Execute YouTube analysis command for Claude Code
        
        Args:
            video_url: YouTube video URL or ID
            focus: Analysis focus (all, technical, summary, transcript, metadata)
            format: Output format (detailed, summary, json)
            save: Save results to file
            
        Returns:
            Formatted analysis results
        """
        
        try:
            # Build command arguments
            cmd_args = [video_url]
            cmd_args.extend(["--focus", focus])
            cmd_args.extend(["--format", format])
            if save:
                cmd_args.append("--save")
                
            # Get path to executor
            executor_path = Path(__file__).parent / "youtube_command_executor.py"
            
            # Execute command
            process = await asyncio.create_subprocess_exec(
                sys.executable, str(executor_path), " ".join(cmd_args),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode('utf-8')
            else:
                error_output = stderr.decode('utf-8') if stderr else "Unknown error"
                return f"❌ **YouTube Analysis Error**\n\n{error_output}"
                
        except Exception as e:
            return f"❌ **Integration Error**\n\nFailed to execute YouTube analysis: {str(e)}"
    
    @staticmethod
    def validate_video_url(url: str) -> bool:
        """Validate if a URL looks like a YouTube video URL or ID"""
        youtube_patterns = [
            "youtube.com/watch",
            "youtu.be/",
            "youtube.com/playlist"
        ]
        
        # Check if it's a direct video ID (11 characters)
        if len(url) == 11 and url.replace('-', '').replace('_', '').isalnum():
            return True
            
        # Check for YouTube URL patterns
        return any(pattern in url.lower() for pattern in youtube_patterns)

# Convenience function for direct usage
async def analyze_youtube_video_for_claude(video_url: str, 
                                         focus: str = "all",
                                         format: str = "detailed") -> str:
    """
    Convenience function for Claude to analyze YouTube videos
    
    Usage in Claude prompts:
        from brain.modules.youtube_claude_integration import analyze_youtube_video_for_claude
        
        result = await analyze_youtube_video_for_claude("https://youtu.be/VIDEO_ID", "technical")
        print(result)
    """
    integration = YouTubeClaudeIntegration()
    return await integration.execute_youtube_command(video_url, focus, format)

if __name__ == "__main__":
    # Example usage
    async def test():
        result = await analyze_youtube_video_for_claude("dQw4w9WgXcQ", "summary")
        print(result)
    
    asyncio.run(test())