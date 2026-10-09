#!/usr/bin/env python3
"""Web dashboard entry point for JARVIS Agent System."""

from jarvis.dashboard import run_dashboard

if __name__ == "__main__":
    run_dashboard(host="0.0.0.0", port=5000, debug=True)
