"""
==============================================================================
AI Career Recommendation System - Root Launcher
==============================================================================
Recommended ways to run:

  Option A (easiest - double-click):
      start.bat

  Option B (terminal - activate backend venv first, then run):
      backend/venv/Scripts/activate
      python app.py

  Option C (direct, no activation needed):
      backend/venv/Scripts/python.exe app.py

Access the app at : http://127.0.0.1:5000
Health check      : http://127.0.0.1:5000/api/health
==============================================================================
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR  = os.path.join(PROJECT_ROOT, 'backend')

# Re-launch with backend venv Python if not already using it
BACKEND_PYTHON_WIN = os.path.join(BACKEND_DIR, 'venv', 'Scripts', 'python.exe')
BACKEND_PYTHON_NIX = os.path.join(BACKEND_DIR, 'venv', 'bin', 'python')
BACKEND_PYTHON = (
    BACKEND_PYTHON_WIN if os.path.exists(BACKEND_PYTHON_WIN)
    else BACKEND_PYTHON_NIX if os.path.exists(BACKEND_PYTHON_NIX)
    else None
)

def _is_backend_venv():
    """True when already running inside backend/venv."""
    exe = sys.executable.replace('\\', '/')
    return 'backend' in exe and 'venv' in exe

if BACKEND_PYTHON and not _is_backend_venv():
    import subprocess
    try:
        result = subprocess.run([BACKEND_PYTHON, __file__] + sys.argv[1:])
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(0)

# Running inside backend/venv - start the server
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

from app import app, init_db  # noqa: E402

if __name__ == '__main__':
    print("=" * 60)
    print("  AI Career Recommendation System")
    print("=" * 60)

    try:
        init_db()
        print("[OK] Database initialised.")
    except Exception as db_err:
        print(f"[WARN] DB init skipped: {db_err}")

    print("\n  [OK] Running at: http://127.0.0.1:5000")
    print("  [OK] Health:     http://127.0.0.1:5000/api/health")
    print("  Press CTRL+C to stop.\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
