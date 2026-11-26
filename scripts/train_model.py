"""
CLI Entry Point to Execute the Authoritative ML Training Notebook End-to-End.
Executes model_training/model_training.ipynb in-place so the notebook,
EDA reports, publication figures, and serialized backend model artifacts
stay 100% synchronized from a single source of truth.
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    notebook_path = project_root / "model_training" / "model_training.ipynb"

    if not notebook_path.exists():
        print(f"ERROR: Training notebook not found at {notebook_path}", file=sys.stderr)
        return 1

    print("=" * 80)
    print("EXECUTING AUTHORITATIVE TRAINING NOTEBOOK")
    print(f"Notebook: {notebook_path}")
    print("=" * 80)

    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=600",
        str(notebook_path),
    ]
    result = subprocess.run(cmd, cwd=str(project_root))
    if result.returncode == 0:
        print("=" * 80)
        print("SUCCESS: Notebook executed and all model/EDA artifacts synchronized.")
        print("=" * 80)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
