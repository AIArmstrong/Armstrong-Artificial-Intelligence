#!/usr/bin/env python3
"""
YouTube Command Executor - Main entry point for /youtube command
Integrates YouTube analysis with Claude Code command system
"""

import asyncio
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add brain modules to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    # Try direct import first (when run from brain/modules directory)
    from youtube_command_handler import YouTubeCommandHandler
    from youtube_analyzer import analyze_youtube_video
except ImportError:
    try:
        # Try absolute import from AAI root
        import os
        aai_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, aai_root)
        from brain.modules.youtube_command_handler import YouTubeCommandHandler
        from brain.modules.youtube_analyzer import analyze_youtube_video
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running from the AAI directory or brain/modules/ directory")
        print("Current working directory:", os.getcwd())
        print("Script location:", __file__)
        sys.exit(1)

class YouTubeCommandExecutor:
    """Main executor for /youtube command with argument parsing and error handling"""
    
    def __init__(self):
        self.handler = YouTubeCommandHandler()
        
    def parse_command_args(self, command: str) -> Dict[str, Any]:
        """Parse /youtube command arguments"""
        args = {
            "video_url": None,
            "focus": "all",
            "format": "detailed", 
            "save": False
        }
        
        parts = command.strip().split()
        
        # Skip the command itself
        if parts[0] in ["/youtube", "/sc:youtube"]:
            parts = parts[1:]
            
        # Parse video URL/ID (required first argument)
        if parts and not parts[0].startswith("--"):
            args["video_url"] = parts[0]
            parts = parts[1:]
        else:
            raise ValueError("Video URL or ID is required")
            
        # Parse flags
        i = 0
        while i < len(parts):
            if parts[i] == "--focus" and i + 1 < len(parts):
                focus_options = ["all", "technical", "summary", "transcript", "metadata"]
                if parts[i + 1] in focus_options:
                    args["focus"] = parts[i + 1]
                i += 2
            elif parts[i] == "--format" and i + 1 < len(parts):
                format_options = ["detailed", "summary", "json"]
                if parts[i + 1] in format_options:
                    args["format"] = parts[i + 1]
                i += 2
            elif parts[i] == "--save":
                args["save"] = True
                i += 1
            else:
                i += 1
                
        return args
    
    async def execute(self, command: str) -> str:
        """Execute the YouTube analysis command"""
        try:
            # Parse command arguments
            args = self.parse_command_args(command)
            
            # Display activation status
            print("🚀 **YouTube Analysis Engine Activated**")
            print(f"📺 Video URL: {args['video_url']}")
            print(f"🎯 Focus: {args['focus']}")
            print(f"📝 Format: {args['format']}")
            if args['save']:
                print("💾 Results will be saved")
            print()
            
            # Execute analysis
            result = await self.handler.handle_youtube_command(
                video_url=args['video_url'],
                focus=args['focus'],
                format=args['format'],
                save=args['save']
            )
            
            return result
            
        except Exception as e:
            error_msg = f"❌ **YouTube Command Error**\n\nError: {str(e)}\n\n"
            error_msg += "**Usage**: `/youtube VIDEO_URL [--focus all|technical|summary|transcript|metadata] [--format detailed|summary|json] [--save]`\n\n"
            error_msg += "**Examples**:\n"
            error_msg += "• `/youtube https://youtu.be/dQw4w9WgXcQ`\n"
            error_msg += "• `/youtube dQw4w9WgXcQ --focus technical --format summary`\n"
            error_msg += "• `/youtube https://www.youtube.com/watch?v=VIDEO_ID --save`"
            return error_msg

async def main():
    """Main entry point for command line execution"""
    if len(sys.argv) < 2:
        print("Usage: python youtube_command_executor.py 'VIDEO_URL [options]'")
        sys.exit(1)
        
    # Reconstruct command from arguments
    command_args = " ".join(sys.argv[1:])
    full_command = f"/youtube {command_args}"
    
    executor = YouTubeCommandExecutor()
    result = await executor.execute(full_command)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())