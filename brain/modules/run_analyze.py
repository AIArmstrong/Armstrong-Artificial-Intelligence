#!/usr/bin/env python3
"""
Simple wrapper to test the analyze command implementation
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_command_handler import handle_analyze_command

async def main():
    # Default command if none provided
    command = "/sc:analyze . --focus quality --depth quick"
    
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
    
    print(f"Running: {command}")
    await handle_analyze_command(command)

if __name__ == "__main__":
    asyncio.run(main())