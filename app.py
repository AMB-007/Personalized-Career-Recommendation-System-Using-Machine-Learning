"""
==============================================================================
AI Career Recommendation System — Root Launcher
==============================================================================
Run this file from the project root to start the entire application:

    python app.py

This script bootstraps the backend Flask server (backend/app.py) which also
serves the frontend (frontend/dist/) as static files — no separate frontend
server is needed.

Access the application at:  http://127.0.0.1:5000
API health check at:        http://127.0.0.1:5000/api/health
==============================================================================
"""

import os
import sys

# ── Resolve project root (directory of this file) ────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR  = os.path.join(PROJECT_ROOT, 'backend')

# Put the backend directory at the front of the path so that all relative
# imports inside backend/app.py (e.g. core/, models/) resolve correctly.
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Change the working directory to backend so that relative file references
# (e.g. .env, models/, venv/) inside app.py resolve correctly.
os.chdir(BACKEND_DIR)

# ── Import and run the Flask application ─────────────────────────────────────
# We import `app` from backend/app.py (now on sys.path as "app").
# __name__ guard is intentionally skipped here — we call app.run() directly
# so that this root launcher acts as the entry point regardless of how it
# is invoked.
from app import app, init_db  # noqa: E402

if __name__ == '__main__':
    print("=" * 60)
    print("  AI Career Recommendation System")
    print("  Starting server...")
    print("=" * 60)

    # Auto-create all database tables on first run
    try:
        init_db()
        print("[OK] Database initialised.")
    except Exception as db_err:
        print(f"[WARN] DB init skipped: {db_err}")

    print("\n  [OK] Frontend + Backend running at: http://127.0.0.1:5000")
    print("  [OK] API health check:              http://127.0.0.1:5000/api/health")
    print("  Press CTRL+C to stop.\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
