# modules/data_loader.py
# Centralised data-loading helpers. All read operations live here so
# app.py stays free of I/O boilerplate.

import pathlib
import tomllib          # stdlib in Python 3.11+; install tomli for 3.9/3.10
import pandas as pd
import streamlit as st

ROOT = pathlib.Path(__file__).parent.parent   # repo root


# ── Config ────────────────────────────────────────────────────────────────────

@st.cache_data
def load_config() -> dict:
    """Load content_config.toml and return as a dict."""
    config_path = ROOT / "content_config.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)


# ── CSV helpers ───────────────────────────────────────────────────────────────

@st.cache_data
def load_publications() -> pd.DataFrame:
    """Return the publications dataframe, sorted newest-first."""
    df = pd.read_csv(ROOT / "data" / "publications.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_grants() -> pd.DataFrame:
    """Return the grants/awards dataframe."""
    df = pd.read_csv(ROOT / "data" / "grants.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_presentations() -> pd.DataFrame:
    """Return the presentations dataframe."""
    df = pd.read_csv(ROOT / "data" / "presentations.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_research_projects() -> pd.DataFrame:
    """Return the research projects dataframe."""
    return pd.read_csv(ROOT / "data" / "research_projects.csv")


# ── Asset helpers ─────────────────────────────────────────────────────────────

def cv_bytes(filename: str) -> bytes | None:
    """
    Read the CV PDF from /assets/ and return raw bytes.
    Returns None (silently) if the file is not yet present.
    """
    cv_path = ROOT / "assets" / filename
    if cv_path.exists():
        return cv_path.read_bytes()
    return None
