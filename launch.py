#!/usr/bin/env python3
"""
🦊 Kitsune AI V3 Launcher 🦊
SIMPLE LAUNCHER - NO COMPLEXITY
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def check_requirements():
    """Check if required modules are available"""
    try:
        import requests
        import pickle
        import json
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("📦 Install with: pip install requests")
        return False

def main():
    """Simple launcher"""
    print("🚀 Kitsune AI V3 Launcher")
    print("="*40)
    
    if not check_requirements():
        input("Press Enter to exit...")
        return
    
    try:
        from kitsune_tamagotchi import main as kitsune_main
        print("✅ All systems ready!")
        print("🦊 Starting Kitsune AI...")
        asyncio.run(kitsune_main())
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔍 Make sure all files are in the same directory")
    except Exception as e:
        print(f"❌ Startup error: {e}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()