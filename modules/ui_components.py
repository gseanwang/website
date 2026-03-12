# modules/ui_components.py
# Reusable HTML/Markdown component helpers so page modules stay DRY.

import streamlit as st


# ── Styled cards ──────────────────────────────────────────────────────────────

def card(title: str, body: str, *, accent: str = "#2e7d32") -> None:
    """Render a left-accented card using st.markdown."""
    st.markdown(
        f"""
        <div style="
            background:#f8f9fa;
            border-left: 4px solid {accent};
            padding: 0.9rem 1.1rem;
            border-radius: 4px;
            margin-bottom: 0.9rem;
            line-height: 1.6;
        ">
            <strong>{title}</strong><br>{body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def pub_item(citation: str, note: str = "") -> None:
    """Render a single publication entry with an optional contribution note."""
    note_html = (
        f'<br><em style="color:#666;font-size:0.84rem;">↳ {note}</em>'
        if note else ""
    )
    st.markdown(
        f"""
        <div style="
            padding: 0.55rem 0;
            border-bottom: 1px solid #f0f0f0;
            line-height: 1.65;
        ">{citation}{note_html}</div>
        """,
        unsafe_allow_html=True,
    )


# ── Skill badges ──────────────────────────────────────────────────────────────

def skill_badge(text: str) -> None:
    st.markdown(
        f"<span style='"
        f"display:inline-block;background:#e8f5e9;color:#1b5e20;"
        f"border-radius:12px;padding:2px 10px;font-size:0.82rem;"
        f"margin:3px 3px 3px 0;font-weight:500'>{text}</span>",
        unsafe_allow_html=True,
    )


# ── Section divider with optional label ──────────────────────────────────────

def section_divider(label: str = "") -> None:
    if label:
        st.markdown(f"### {label}")
    st.markdown("<hr style='border:none;border-top:1px solid #e0e0e0;margin:0.5rem 0 1.2rem'>",
                unsafe_allow_html=True)


# ── Impact metric row ─────────────────────────────────────────────────────────

def metric_row(items: list[tuple[str, str, str]]) -> None:
    """
    Render a responsive row of st.metric widgets.
    items: list of (label, value, delta) tuples.
    """
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)
