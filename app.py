# =============================================================================
# app.py  —  Sean Wang | Ph.D. Candidate Portfolio
# =============================================================================
# Run:     streamlit run app.py
# Requires: pip install -r requirements.txt
# =============================================================================

import sys
import pathlib
import streamlit as st

# Make sure local modules are importable regardless of working directory
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from modules.data_loader import (
    load_config,
    load_publications,
    load_grants,
    load_presentations,
    load_research_projects,
    cv_bytes,
)
from modules.ui_components import card, pub_item, skill_badge, section_divider, metric_row

# ── Load all data up-front ────────────────────────────────────────────────────
cfg     = load_config()
P       = cfg["personal"]
BIO     = cfg["bio"]
METRICS = cfg["metrics"]
SKILLS  = cfg["skills"]
COLLAB  = cfg["collaboration"]

pubs    = load_publications()
grants  = load_grants()
presentations = load_presentations()
projects = load_research_projects()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{P['preferred_name']} | Ph.D. Candidate Portfolio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    hr  { border: none; border-top: 1px solid #e0e0e0; margin: 1.4rem 0; }
    [data-testid="stMetricValue"] { font-size: 1.55rem !important; }
    a   { color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/"
        "University_of_Florida_logo.svg/320px-University_of_Florida_logo.svg.png",
        width=130,
    )
    st.markdown(f"### {P['full_name']}")
    st.caption(f"{P['title']}\n{P['institution']}")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=[
            "🏠  Professional Summary",
            "🔬  Research & Extension",
            "📄  Publications & Grants",
            "🎓  Leadership & Teaching",
            "📬  Contact & CV",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Built with Streamlit · 2025")


# =============================================================================
# PAGE 1 — Professional Summary
# =============================================================================
if page == "🏠  Professional Summary":

    st.title(P["full_name"])
    st.subheader(f"{P['title']} | {P['institution']}")
    st.markdown("*Fungal Epidemiology · Integrated Pest Management · Sustainable Agriculture*")
    st.markdown("---")

    # Bio + metrics
    col_bio, col_met = st.columns([3, 2], gap="large")
    with col_bio:
        st.markdown("### About Me")
        st.markdown(BIO["summary"])

    with col_met:
        st.markdown("### Impact at a Glance")
        m = METRICS
        st.metric("Acres Informed by Research",   m["acres_informed"],   m["acres_informed_delta"])
        st.metric("Field Trial Area Managed",      m["trial_area"],       m["trial_area_delta"])
        st.metric("Grants Secured",                m["grants_total"],     m["grants_delta"])
        st.metric("Junior Scientists Mentored",    m["mentees"],          m["mentees_delta"])
        st.metric("Peer-Reviewed Publications",    m["publications"],     m["publications_delta"])

    st.markdown("---")

    # Education (driven by config)
    st.markdown("### Education")
    edu_items = cfg["education"]
    edu_cols = st.columns(min(len(edu_items), 3))
    for col, edu in zip(edu_cols, edu_items):
        with col:
            detail = f"Advisor: {edu['advisor']}<br><em>{edu['thesis']}</em>" if edu.get("advisor") else ""
            card(
                edu["degree"],
                f"{edu['institution']}<br><em>{edu['year']}</em><br>{detail}",
            )

    st.markdown("---")

    # Skills (driven by config)
    st.markdown("### Technical Skills")
    skill_cols = st.columns(len(SKILLS))
    for col, (category, items) in zip(skill_cols, SKILLS.items()):
        with col:
            st.markdown(f"**{category}**")
            for item in items:
                skill_badge(item)

    st.markdown("---")

    # Affiliations
    st.markdown("### Professional Affiliations")
    aff_cols = st.columns(len(cfg["affiliations"]))
    for col, aff in zip(aff_cols, cfg["affiliations"]):
        col.markdown(f"🌿 **{aff['org']}** — {aff['role']} · *{aff['years']}*")


# =============================================================================
# PAGE 2 — Research & Extension
# =============================================================================
elif page == "🔬  Research & Extension":

    st.title("Research & Extension")
    st.markdown(
        "Applied research bridging rigorous experimental design with on-farm demonstration, "
        "ensuring findings translate rapidly into grower practice."
    )
    st.markdown("---")

    # Impact row
    metric_row([
        ("Field Trial Sites",             "Multiple",    "Southeast U.S."),
        ("Trial Area per Season",         "~3 acres",    "Managed directly"),
        ("Commercial Acreage Informed",   "~50,000",     "Grower recommendations"),
        ("Fungicide Programs Evaluated",  "15+",         "FRAC group diversity"),
    ])
    st.markdown("---")

    # Project expanders (driven from CSV)
    st.markdown("### Primary Research Projects")
    for _, row in projects.iterrows():
        with st.expander(f"🌱  {row['title']}", expanded=True):
            p_col1, p_col2 = st.columns([3, 2])

            highlights = [h.strip() for h in str(row["highlights"]).split(";")]
            with p_col1:
                st.markdown(
                    f"**Funder:** {row['funder']}  \n"
                    f"**Role:** {row['role']}  \n"
                    f"**Period:** {int(row['start_year'])}–{int(row['end_year'])}  \n\n"
                    f"{row['description_short']}\n\n"
                    f"**Highlights:**"
                )
                for h in highlights:
                    st.markdown(f"- {h}")

            with p_col2:
                st.metric("Trial Area (acres)", f"~{int(row['acres_managed'])}", "Per season")
                st.metric("Commercial Acres Informed", f"~{int(row['acres_informed']):,}")

    st.markdown("---")

    # Remote sensing section
    st.markdown("### UAV & Remote Sensing Capabilities")
    rs1, rs2, rs3 = st.columns(3)
    with rs1:
        card("🛸 UAV Operations",
             "FAA Part 107 compliant flight planning; grid and transect mapping missions; "
             "integration with ground control points for geometric accuracy.")
    with rs2:
        card("📡 Multispectral Analysis",
             "5-band sensor processing (RGB, Red-Edge, NIR) in Pix4D/Agisoft Metashape; "
             "NDVI, GNDVI, SAVI calculation for spatial disease severity mapping.")
    with rs3:
        card("📊 Geospatial Statistics",
             "Raster-derived indices correlated with plot-level disease ratings; "
             "regression modelling to validate remote sensing proxies.")

    st.markdown("---")
    st.markdown("### Additional Research Contributions")

    with st.expander("Epidemiological Modelling & Disease Forecasting"):
        st.markdown(
            """
            - Logistic and Gompertz disease progress models fitted to multi-year datasets
              using nonlinear mixed-effects approaches.
            - Weather-based forecasting parameters (temperature, leaf wetness, RH) as
              predictors for infection event timing.
            - Contributions to regional spray-timing alert systems.
            """
        )
    with st.expander("Molecular & Morphological Characterisation of Fungal Pathogens"):
        st.markdown(
            """
            - Species delimitation of *Colletotrichum*, *Botrytis*, and *Fusarium* using
              multi-locus phylogenetics (ITS, β-tubulin, ACT, GAPDH).
            - Morphological characterisation under variable temperature and humidity regimes.
            - Voucher culture collections deposited with institutional herbarium.
            """
        )


# =============================================================================
# PAGE 3 — Publications & Grants
# =============================================================================
elif page == "📄  Publications & Grants":

    st.title("Publications & Grants")
    st.markdown("---")

    # Summary metrics from CSV
    n_pub   = len(pubs[pubs["type"] == "peer_reviewed"])
    n_rev   = len(pubs[pubs["status"].isin(["under_review", "in_preparation"])])
    n_ext   = len(pubs[pubs["type"] == "extension"])
    metric_row([
        ("Peer-Reviewed Publications", str(n_pub), "Published"),
        ("Manuscripts Under Review / In Prep", str(n_rev), ""),
        ("Extension Reports & Factsheets", str(n_ext), "UF/IFAS EDIS"),
    ])

    st.markdown("---")

    # ── Publications by type ──────────────────────────────────────────────────
    def render_pub_row(row) -> None:
        authors = row["authors"]
        year    = int(row["year"])
        title   = row["title"]
        journal = row["journal"]
        doi     = row["doi"] if str(row["doi"]) != "nan" else ""
        note    = row["contribution_note"] if str(row["contribution_note"]) != "nan" else ""
        vol     = row["volume"] if str(row["volume"]) != "nan" else ""
        pages   = row["pages"] if str(row["pages"]) != "nan" else ""

        doi_link = f" [https://doi.org/{doi}](https://doi.org/{doi})" if doi else ""
        vol_str  = f", {vol}, {pages}" if vol else ""
        citation = f"**{authors}** ({year}). {title}. *{journal}*{vol_str}.{doi_link}"
        pub_item(citation, note)

    st.markdown("### Peer-Reviewed Publications")
    for _, row in pubs[pubs["type"] == "peer_reviewed"].iterrows():
        render_pub_row(row)

    st.markdown("---")
    st.markdown("### Manuscripts Under Review / In Preparation")
    for _, row in pubs[pubs["status"].isin(["under_review", "in_preparation"])].iterrows():
        status_label = "Under review" if row["status"] == "under_review" else "In preparation"
        row = row.copy()
        row["journal"] = f"{row['journal']} (*{status_label}*)"
        render_pub_row(row)

    st.markdown("---")
    st.markdown("### Extension Reports & Outreach Publications")
    for _, row in pubs[pubs["type"] == "extension"].iterrows():
        render_pub_row(row)

    st.markdown("---")

    # ── Presentations ─────────────────────────────────────────────────────────
    st.markdown("### Conference Presentations")
    for _, row in presentations.iterrows():
        p_type = row["type"].title()
        award  = f" 🏆 *{row['award']}*" if str(row.get("award", "")) not in ("", "nan") else ""
        pub_item(
            f"**{row['authors']}** ({int(row['year'])}). {p_type}: *{row['title']}*. "
            f"{row['event']}, {row['location']}.{award}"
        )

    st.markdown("---")

    # ── Grants ────────────────────────────────────────────────────────────────
    st.markdown("### Grants, Awards & Fellowships")
    g_col1, g_col2 = st.columns(2)

    int_grants = grants[grants["type"] == "international_grant"]
    other_awards = grants[grants["type"] != "international_grant"]
    total_int = int_grants["amount_usd"].sum()

    with g_col1:
        st.markdown("#### 💰 Competitive Grants")
        for _, row in int_grants.iterrows():
            amt = f"${int(row['amount_usd']):,}" if row["amount_usd"] > 0 else "—"
            card(
                f"{row['title']} · {amt}",
                f"Agency: {row['agency']} · Year: {int(row['year'])}<br>"
                f"<em>{row['description']}</em>",
            )
        st.metric("Total International Grant Funding", f"~${total_int:,.0f}", "3 competitive awards")

    with g_col2:
        st.markdown("#### 🏆 Fellowships & Awards")
        for _, row in other_awards.iterrows():
            amt = f" · ${int(row['amount_usd']):,}" if row["amount_usd"] > 0 else ""
            card(
                f"{row['title']}{amt}",
                f"{row['agency']} · {int(row['year'])}<br><em>{row['description']}</em>",
            )


# =============================================================================
# PAGE 4 — Leadership & Teaching
# =============================================================================
elif page == "🎓  Leadership & Teaching":

    st.title("Leadership, Teaching & Mentoring")
    st.markdown("---")

    metric_row([
        ("Junior Scientists Mentored", "7",   "Undergrad & early-career"),
        ("Teaching Roles",             "2",   "TA + External Instructor"),
        ("Leadership Positions",       "2+",  "Dept. & professional orgs"),
    ])
    st.markdown("---")

    # Mentoring
    st.markdown("### Research Mentoring")
    with st.expander("Undergraduate & Early-Career Researcher Mentorship — 7 mentees", expanded=True):
        m_col1, m_col2 = st.columns([3, 2])
        with m_col1:
            st.markdown(
                """
                As a senior Ph.D. student and lab mentor, I have directly supervised
                **7 junior scientists**, providing structured guidance in:

                **Technical Training:**
                - Field trial protocols — plot establishment, disease scoring, pesticide application.
                - Laboratory techniques — fungal isolation, PCR, gel electrophoresis.
                - Data management — RCBD design, data-entry standards, introductory R/SAS.
                - UAV data collection and basic image-processing workflows.

                **Professional Development:**
                - Science communication — abstract writing, poster and oral presentation skills.
                - Research ethics and laboratory safety.
                - Graduate school and employment application support.
                """
            )
        with m_col2:
            st.markdown("**Mentee Outcomes**")
            for label, val in [
                ("Pursuing Graduate Degrees", "3"),
                ("Accepted into REU Programs", "2"),
                ("Co-authors on Extension Reports", "2"),
                ("Full-time Research Positions", "1"),
            ]:
                st.metric(label, val)

    st.markdown("---")

    # Teaching
    st.markdown("### Teaching Experience")
    t1, t2 = st.columns(2)
    with t1:
        card(
            "🏫 DxR Health Academy — Instructor (2023)",
            "Designed and delivered a week-long plant pathology & food security curriculum "
            "for high school and early undergraduate students. Incorporated spore trapping, "
            "microscopy, and disease triangle hands-on activities.",
        )
    with t2:
        card(
            "🎓 University of Florida — Teaching Assistant (2022–2023)",
            "PLP XXXX: Introductory Plant Pathology · ~40 students/semester. "
            "Led weekly lab sessions; prepared specimens; graded reports and exams. "
            "Student evaluation: 4.7 / 5.0.",
        )

    st.markdown("---")

    # Leadership
    st.markdown("### Leadership & Service")
    l1, l2 = st.columns(2)
    with l1:
        st.markdown("#### Departmental & University")
        card("Vice President — UF PPGSO (2023–2024)",
             "Led seminar series, recruitment weekend, and outreach events. "
             "Managed student programming budget; liaised with department administration.")
        card("Graduate Student Representative — UF CALS Council (2022–2023)",
             "Advocated for graduate student welfare, stipend equity, and professional development.")

    with l2:
        st.markdown("#### Professional Society Service")
        card("American Phytopathological Society — Student Member (2021–Present)",
             "Annual meeting participant; peer reviewer for <em>Plant Disease</em> and "
             "<em>Phytopathology</em>; volunteer at 2023 Annual Meeting.")
        card("Florida Strawberry Research & Extension Foundation (2022–Present)",
             "Annual presenter; translates trial results into grower recommendations; "
             "assists with industry-facing factsheet development.")

    st.markdown("---")

    st.markdown("### Workshops & Certifications")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("🛸 FAA Part 107 sUAS", "Remote Pilot Certificate — commercial UAV operations")
    with c2:
        card("🧪 OSHA Lab Safety", "Hazardous materials, PPE protocols, emergency response")
    with c3:
        card("📊 R / SAS Statistical Computing", "Mixed models, ANOVA, nonlinear modelling — UF IFAS workshops")


# =============================================================================
# PAGE 5 — Contact & CV
# =============================================================================
elif page == "📬  Contact & CV":

    st.title("Contact & Download CV")
    st.markdown("---")

    c_left, c_right = st.columns([2, 3], gap="large")

    with c_left:
        st.markdown("### Get in Touch")
        st.markdown(
            "Happy to discuss collaborations, research inquiries, speaking invitations, "
            "or academic / industry opportunities."
        )
        st.markdown("---")

        contact_items = [
            ("📧", "Email",         P["email"],       f"mailto:{P['email']}"),
            ("🎓", "Google Scholar", "Scholar Profile", P["google_scholar"]),
            ("💼", "LinkedIn",       "LinkedIn Profile", P["linkedin"]),
            ("🐦", "Twitter / X",    "@SeanWang_PlantPath", P.get("twitter", "#")),
            ("🏛️", "UF Page",        "UF Plant Pathology", P["uf_page"]),
            ("📍", "Location",       P["location"],    None),
        ]
        for icon, label, value, link in contact_items:
            link_html = f'<a href="{link}" target="_blank">{value}</a>' if link else value
            st.markdown(
                f"<div style='background:#f8f9fa;border-left:4px solid #2e7d32;"
                f"padding:0.7rem 1rem;border-radius:4px;margin-bottom:0.7rem'>"
                f"{icon} &nbsp;<strong>{label}:</strong>&nbsp; {link_html}</div>",
                unsafe_allow_html=True,
            )

    with c_right:
        st.markdown("### Download Full CV")
        st.markdown(
            "Download the complete, formatted Curriculum Vitae for full publication "
            "references, grant details, and course history."
        )

        raw_cv = cv_bytes(P["cv_filename"])
        if raw_cv:
            st.download_button(
                label="⬇️  Download CV (PDF)",
                data=raw_cv,
                file_name=P["cv_filename"],
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info(
                f"📎 Place **`{P['cv_filename']}`** in the `/assets/` folder to "
                "activate the download button.",
                icon="ℹ️",
            )
            st.button("⬇️  Download CV (PDF) — coming soon", disabled=True, use_container_width=True)

        st.markdown("---")
        st.markdown("### Collaboration Interests")
        for item in COLLAB["interests"]:
            st.markdown(f"- {item}")

        st.markdown("---")
        st.markdown("### Current Status")
        s1, s2 = st.columns(2)
        with s1:
            open_to_md = "\n".join(f"✅ {o}" for o in COLLAB["open_to"])
            card("Open to Opportunities", open_to_md)
        with s2:
            card(
                "Timeline",
                f"🎓 Expected graduation: {COLLAB['expected_graduation']}<br>"
                "📅 Open to discussions now",
            )
