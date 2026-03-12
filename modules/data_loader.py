# modules/data_loader.py
# Centralised data-loading helpers. All read operations live here so
# app.py stays free of I/O boilerplate.

import pathlib
import tomllib          # stdlib in Python 3.11+; install tomli for 3.9/3.10
import pandas as pd
import streamlit as st

ROOT = pathlib.Path(__file__).parent.parent   # repo root
ASSETS = ROOT / "assets"


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
    df = pd.read_csv(ROOT / "data" / "publications.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_grants() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "grants.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_presentations() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "presentations.csv")
    return df.sort_values("year", ascending=False)


@st.cache_data
def load_research_projects() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "research_projects.csv")


@st.cache_data
def load_photos() -> pd.DataFrame:
    """
    Return photos.csv as a DataFrame.
    Columns: photo_id, page, section, filename, url, caption, alt_text, display_order

    Resolution priority per row:
      1. filename set  →  load from assets/<filename>  (local, committed to repo)
      2. url set       →  use URL directly              (Google Drive / Imgur / etc.)
      3. neither       →  skip
    """
    path = ROOT / "data" / "photos.csv"
    if not path.exists():
        return pd.DataFrame(columns=[
            "photo_id","page","section","filename","url",
            "caption","alt_text","display_order",
        ])
    df = pd.read_csv(path)
    df["display_order"] = pd.to_numeric(df["display_order"], errors="coerce").fillna(99)
    return df.sort_values("display_order")


# ── Photo resolution helpers ──────────────────────────────────────────────────

def resolve_photo(row: "pd.Series") -> "str | pathlib.Path | None":
    """Return local Path, URL string, or None for a photos.csv row."""
    filename = str(row.get("filename", "")).strip()
    url      = str(row.get("url", "")).strip()

    if filename and filename.lower() != "nan":
        local = ASSETS / filename
        if local.exists():
            return local
        return None          # listed but not yet uploaded — skip gracefully

    if url and url.lower() != "nan":
        return url

    return None


def get_photos(page: str, section: str) -> list:
    """
    Return [{src, caption, alt_text}, ...] for a given page + section.
    Only rows with a resolvable source are included.
    """
    df = load_photos()
    subset = df[(df["page"] == page) & (df["section"] == section)]
    result = []
    for _, row in subset.iterrows():
        src = resolve_photo(row)
        if src is not None:
            result.append({
                "src":      src,
                "caption":  str(row.get("caption", "")).strip(),
                "alt_text": str(row.get("alt_text", "")).strip(),
            })
    return result


# ── CV download ───────────────────────────────────────────────────────────────

def cv_bytes(filename: str) -> bytes | None:
    """Read CV PDF from /assets/. Returns None if not present."""
    cv_path = ASSETS / filename
    if cv_path.exists():
        return cv_path.read_bytes()
    return None
