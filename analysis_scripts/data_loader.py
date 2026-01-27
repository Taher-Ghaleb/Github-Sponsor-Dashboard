"""
Shared utilities for loading the sample GitHub Sponsors dataset.

All example analysis scripts in this package assume the repository layout:

- Project root
  - data/
    - sample_data.csv

The loader normalizes column names and types to make downstream analyses
easier and more robust.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "sample_data.csv"


def load_sample_data(path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the sample GitHub Sponsors dataset.

    Parameters
    ----------
    path:
        Optional explicit path to the CSV file. If omitted, defaults to
        `<project_root>/data/sample_data.csv`.

    Returns
    -------
    pd.DataFrame
        DataFrame with appropriate dtypes and cleaned columns.
    """
    csv_path = Path(path) if path is not None else DATA_PATH
    if not csv_path.exists():
        raise FileNotFoundError(f"Sample data not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Normalize column names to snake_case for convenience.
    df.columns = [c.strip().lower() for c in df.columns]

    # Coerce numeric columns.
    numeric_cols = [
        "total_sponsors",
        "total_sponsoring",
        "estimated_earnings",
        "public_repos",
        "followers",
        "following",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize a few categorical fields.
    if "type" in df.columns:
        df["type"] = df["type"].str.strip().str.title()

    if "gender" in df.columns:
        df["gender"] = df["gender"].fillna("Unknown").str.strip().str.title()

    if "location" in df.columns:
        df["location"] = df["location"].fillna("Unknown").str.strip()

    return df


__all__ = ["load_sample_data", "DATA_PATH"]
