# scripts/clean_knowledge_base.py
"""Clean the career knowledge requirements CSV.

This script reads the original ``career_knowledge_requirements.csv`` file,
applies domain‑specific minimum thresholds defined in ``backend/ml/config.yaml``
(and falls back to hard‑coded defaults if a domain is missing), and writes a
cleaned version ``career_knowledge_requirements_clean.csv``.

The cleaning is idempotent – running the script multiple times will produce the
same cleaned file.
"""
import pathlib
import sys
import pandas as pd
import yaml

# -----------------------------------------------------------------------------
# Paths
ROOT = pathlib.Path(__file__).resolve().parents[1]  # project root
DATA_DIR = ROOT / "backend" / "ml" / "data"
ORIG_CSV = DATA_DIR / "career_knowledge_requirements.csv"
CLEAN_CSV = DATA_DIR / "career_knowledge_requirements_clean.csv"
CONFIG_PATH = ROOT / "backend" / "ml" / "config.yaml"

# -----------------------------------------------------------------------------
# Load config (if it exists)
config = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
# Default thresholds (used when a domain is not listed in config)
DEFAULT_THRESHOLDS = {
    "healthcare": {"scientific_reasoning": 60, "mathematical_ability": 60},
    "engineering": {"engineering_interest": 55},
    "arts": {"arts_interest": 50},
}

def _get_domain_thresholds(domain: str) -> dict:
    """Return a dict of column -> minimum value for ``domain``.

    Order of precedence:
    1. Config file ``domain_requirements`` section.
    2. Hard‑coded ``DEFAULT_THRESHOLDS``.
    3. Empty dict (no filter) if the domain is unknown.
    """
    domain = domain.lower()
    cfg = config.get("domain_requirements", {})
    if domain in cfg:
        return cfg[domain]
    return DEFAULT_THRESHOLDS.get(domain, {})

def main():
    if not ORIG_CSV.exists():
        sys.stderr.write(f"[ERROR] Original CSV not found at {ORIG_CSV}\n")
        sys.exit(1)

    df = pd.read_csv(ORIG_CSV)
    # Ensure column names are stripped of whitespace
    df.columns = [c.strip() for c in df.columns]

    # Apply filtering per row
    def _keep(row):
        domain = str(row.get("career_domain", "")).lower()
        thresholds = _get_domain_thresholds(domain)
        for col, min_val in thresholds.items():
            try:
                cell_val = float(row.get(col, 0))
            except (ValueError, TypeError):
                return False
            if cell_val < float(min_val):
                return False
        return True

    filtered = df[df.apply(_keep, axis=1)]
    if filtered.empty:
        filtered = df
        print("[INFO] No rows satisfied thresholds – keeping original dataset.")
    else:
        print(f"[INFO] Filtered {len(df) - len(filtered)} rows; kept {len(filtered)}.")

    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(CLEAN_CSV, index=False)
    print(f"[DONE] Cleaned CSV written to {CLEAN_CSV}")

if __name__ == "__main__":
    main()
