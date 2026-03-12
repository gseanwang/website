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


# ── Section divider ───────────────────────────────────────────────────────────

def section_divider(label: str = "") -> None:
    if label:
        st.markdown(f"### {label}")
    st.markdown(
        "<hr style='border:none;border-top:1px solid #e0e0e0;margin:0.5rem 0 1.2rem'>",
        unsafe_allow_html=True,
    )


# ── Impact metric row ─────────────────────────────────────────────────────────

def metric_row(items: list) -> None:
    """
    Render a responsive row of st.metric widgets.
    items: list of (label, value, delta) tuples.
    """
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)


# ── Photo gallery ─────────────────────────────────────────────────────────────

def photo_gallery(photos: list, *, cols: int = 3, caption_style: str = "below") -> None:
    """
    Render a responsive photo grid.

    Parameters
    ----------
    photos : list of dicts with keys {src, caption, alt_text}
             src can be a pathlib.Path (local) or a URL string.
    cols   : number of columns in the grid (default 3).
    caption_style : "below"  → caption appears under each image
                    "hover"  → shown as italicised note below (Streamlit limitation)
    """
    if not photos:
        return

    grid = st.columns(cols)
    for idx, photo in enumerate(photos):
        col = grid[idx % cols]
        with col:
            try:
                st.image(
                    photo["src"],
                    use_container_width=True,
                )
                if photo.get("caption"):
                    st.caption(photo["caption"])
            except Exception:
                # Image file listed but can't be loaded — show placeholder text
                st.markdown(
                    f"<div style='background:#f0f0f0;padding:1.5rem;text-align:center;"
                    f"border-radius:6px;color:#999;font-size:0.8rem'>"
                    f"📷 {photo.get('alt_text','Image not available')}</div>",
                    unsafe_allow_html=True,
                )


def profile_photo(src, *, width: int = 220, caption: str = "") -> None:
    """
    Render a circular-style profile photo with optional caption.
    Uses CSS border-radius trick via an HTML wrapper.
    Streamlit's st.image doesn't support CSS classes directly,
    so we use a base64 or URL approach depending on src type.

    Parameters
    ----------
    src   : pathlib.Path (local file) or URL string
    width : display width in pixels
    """
    import pathlib, base64

    if isinstance(src, pathlib.Path):
        # Local file → encode to base64 so HTML img tag works
        try:
            raw = src.read_bytes()
            suffix = src.suffix.lower().lstrip(".")
            mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
            b64  = base64.b64encode(raw).decode()
            img_src = f"data:image/{mime};base64,{b64}"
        except Exception:
            st.markdown("*Profile photo not available.*")
            return
    else:
        img_src = src  # URL string

    caption_html = (
        f'<p style="text-align:center;font-size:0.82rem;color:#666;margin-top:6px">'
        f'{caption}</p>'
        if caption else ""
    )

    st.markdown(
        f"""
        <div style="display:flex;flex-direction:column;align-items:center;margin-bottom:1rem">
          <img src="{img_src}"
               width="{width}"
               style="border-radius:50%;object-fit:cover;
                      border:3px solid #2e7d32;
                      box-shadow:0 2px 8px rgba(0,0,0,0.15);"
               alt="Profile photo" />
          {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
def profile_photo(src, *, width: int = 220, caption: str = "") -> None:
    import pathlib, base64
    if isinstance(src, pathlib.Path):
        try:
            raw  = src.read_bytes()
            mime = "jpeg" if src.suffix.lower() in (".jpg", ".jpeg") else src.suffix.lstrip(".")
            b64  = base64.b64encode(raw).decode()
            img_src = f"data:image/{mime};base64,{b64}"
        except Exception:
            st.markdown("*Profile photo not available.*")
            return
    else:
        img_src = src
    caption_html = (
        f'<p style="text-align:center;font-size:0.82rem;color:#666;margin-top:6px">{caption}</p>'
        if caption else ""
    )
    st.markdown(
        f'<div style="display:flex;flex-direction:column;align-items:center;margin-bottom:1rem">'
        f'<img src="{img_src}" width="{width}" '
        f'style="border-radius:50%;object-fit:cover;border:3px solid #2e7d32;'
        f'box-shadow:0 2px 8px rgba(0,0,0,0.15);" alt="Profile photo"/>'
        f'{caption_html}</div>',
        unsafe_allow_html=True,
    )


def photo_gallery(photos: list, *, cols: int = 3) -> None:
    if not photos:
        return
    grid = st.columns(cols)
    for idx, photo in enumerate(photos):
        with grid[idx % cols]:
            try:
                st.image(photo["src"], use_container_width=True)
                if photo.get("caption"):
                    st.caption(photo["caption"])
            except Exception:
                st.markdown(
                    f"<div style='background:#f0f0f0;padding:1.5rem;text-align:center;"
                    f"border-radius:6px;color:#999;font-size:0.8rem'>"
                    f"📷 {photo.get('alt_text','Image not available')}</div>",
                    unsafe_allow_html=True,
                )
