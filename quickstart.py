#!/usr/bin/env python3
"""Quick start script for JARVIS Agent System."""

import sys
import subprocess
import os
from pathlib import Path


def main():
    print("\n🤖 JARVIS Agent System - Quick Start")
    print("="*50)
    print()
    print("Select how you want to run JARVIS:")
    print()
    print("  [1] CLI Mode (interactive terminal)")
    print("  [2] Web Dashboard (http://localhost:5000)")
    print("  [3] Exit")
    print()
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        return
    
    if choice == "1":
        print("\n📡 Starting JARVIS CLI Mode...\n")
        subprocess.run([sys.executable, "main.py"])
    elif choice == "2":
        print("\n🌐 Starting JARVIS Web Dashboard...")
        print("\nDashboard will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server\n")
        subprocess.run([sys.executable, "dashboard.py"])
    elif choice == "3":
        print("\nGoodbye!")
    else:
        print("\n❌ Invalid choice. Please try again.")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown complete.")
        sys.exit(0)
