# modules/data_loader.py
import pathlib
import tomllib
import pandas as pd
import streamlit as st

ROOT   = pathlib.Path(__file__).parent.parent
ASSETS = ROOT / "assets"

@st.cache_data
def load_config() -> dict:
    with open(ROOT / "content_config.toml", "rb") as f:
        return tomllib.load(f)

@st.cache_data
def load_publications() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "publications.csv").sort_values("year", ascending=False)

@st.cache_data
def load_grants() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "grants.csv").sort_values("year", ascending=False)

@st.cache_data
def load_presentations() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "presentations.csv").sort_values("year", ascending=False)

@st.cache_data
def load_research_projects() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "research_projects.csv")

@st.cache_data
def load_photos() -> pd.DataFrame:
    path = ROOT / "data" / "photos.csv"
    if not path.exists():
        return pd.DataFrame(columns=["photo_id","page","section","filename","url","caption","alt_text","display_order"])
    df = pd.read_csv(path)
    df["display_order"] = pd.to_numeric(df["display_order"], errors="coerce").fillna(99)
    return df.sort_values("display_order")

def resolve_photo(row):
    filename = str(row.get("filename", "")).strip()
    url      = str(row.get("url", "")).strip()
    if filename and filename.lower() != "nan":
        local = ASSETS / filename
        if local.exists():
            return local
        return None
    if url and url.lower() != "nan":
        return url
    return None

def get_photos(page: str, section: str) -> list:
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

def cv_bytes(filename: str):
    cv_path = ASSETS / filename
    return cv_path.read_bytes() if cv_path.exists() else None
