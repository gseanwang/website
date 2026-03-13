# =============================================================================
# app.py  —  Chun-Hsiang (Sean) Wang | Ph.D. Portfolio
# =============================================================================
import sys, base64, pathlib
import streamlit as st

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))

from modules.data_loader import (
    load_config, load_publications, load_grants,
    load_presentations, load_research_projects, cv_bytes,
)
from modules.ui_components import card, pub_item, skill_badge, section_divider, metric_row

# ── Data ──────────────────────────────────────────────────────────────────────
cfg     = load_config()
P       = cfg["personal"]
BIO     = cfg["bio"]
METRICS = cfg["metrics"]
SKILLS  = cfg["skills"]
COLLAB  = cfg["collaboration"]

pubs          = load_publications()
grants        = load_grants()
presentations = load_presentations()
projects      = load_research_projects()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sean Wang | Ph.D. Candidate Portfolio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
<style>
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 1.2rem 0; }
    a  { color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)


# ── Photo helpers (direct scan — no CSV dependency) ───────────────────────────
def _find_image(stem_keyword: str) -> pathlib.Path | None:
    assets = ROOT / "assets"
    if not assets.exists():
        return None
    for f in sorted(assets.iterdir()):
        if stem_keyword.lower() in f.stem.lower() and \
           f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            return f
    return None

def _find_all_images(stem_keyword: str) -> list:
    assets = ROOT / "assets"
    if not assets.exists():
        return []
    return sorted([
        f for f in assets.iterdir()
        if stem_keyword.lower() in f.stem.lower()
        and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
    ])

def _img_b64(path: pathlib.Path) -> tuple:
    mime = "jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "png"
    b64  = base64.b64encode(path.read_bytes()).decode()
    return mime, b64

def _render_circle_photo(path: pathlib.Path, width: int = 180) -> None:
    mime, b64 = _img_b64(path)
    st.markdown(
        f'<div style="display:flex;justify-content:center;margin-bottom:1rem">'
        f'<img src="data:image/{mime};base64,{b64}" width="{width}" '
        f'style="border-radius:50%;object-fit:cover;'
        f'border:3px solid #2e7d32;box-shadow:0 2px 8px rgba(0,0,0,.15)"/></div>',
        unsafe_allow_html=True,
    )

def _render_image_grid(paths: list, cols: int = 3) -> None:
    if not paths:
        return
    grid = st.columns(cols)
    for i, p in enumerate(paths):
        with grid[i % cols]:
            mime, b64 = _img_b64(p)
            st.markdown(
                f'<img src="data:image/{mime};base64,{b64}" '
                f'style="width:100%;border-radius:8px;margin-bottom:4px"/>',
                unsafe_allow_html=True,
            )
            st.caption(p.stem.replace("_", " ").title())


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/"
        "University_of_Florida_logo.svg/320px-University_of_Florida_logo.svg.png",
        width=130,
    )
    _p = _find_image("profile")
    if _p:
        _render_circle_photo(_p, width=90)

    st.markdown(f"### {P['full_name']}")
    st.caption(f"{P['title']}\n{P['institution']}")
    st.markdown("---")

    page = st.radio("Navigate", [
        "🏠  Professional Summary",
        "🔬  Research & Experience",
        "📄  Publications & Grants",
        "🎓  Teaching & Leadership",
        "📰  In the News",
        "📬  Contact & CV",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.caption("Built with Streamlit · 2026")


# =============================================================================
# PAGE 1 — Professional Summary
# =============================================================================
if page == "🏠  Professional Summary":
    st.title(P["full_name"])
    st.subheader(f"{P['title']} | {P['institution']}")
    st.markdown("*Fungal Epidemiology · Seed Pathology · IPM · Sustainable Agriculture*")
    st.markdown("---")

    col_bio, col_met = st.columns([3, 2], gap="large")

    with col_bio:
        st.markdown("### About Me")
        _profile = _find_image("profile")
        if _profile:
            ph_col, bio_col = st.columns([1, 3])
            with ph_col:
                _render_circle_photo(_profile, width=180)
            with bio_col:
                st.markdown(BIO["summary"])
        else:
            st.info("📷 Drop **`profile.jpg`** into `/assets/` to display your photo.", icon="ℹ️")
            st.markdown(BIO["summary"])

    with col_met:
        st.markdown("### Impact at a Glance")
        m = METRICS
        st.metric("Acres Informed by Research",   m["acres_informed"],  m["acres_informed_delta"])
        st.metric("Field Trial Area Managed",      m["trial_area"],      m["trial_area_delta"])
        st.metric("International Grant Funding",   m["grants_total"],    m["grants_delta"])
        st.metric("Junior Scientists Mentored",    m["mentees"],         m["mentees_delta"])
        st.metric("Publications & Reports",        m["publications"],    m["publications_delta"])

    st.markdown("---")

    # Education
    st.markdown("### Education")
    edu_items = cfg["education"]
    edu_cols  = st.columns(len(edu_items))
    for col, edu in zip(edu_cols, edu_items):
        with col:
            detail = f"Advisor: {edu['advisor']}<br><em>{edu['thesis']}</em>" if edu.get("advisor") else ""
            card(edu["degree"], f"{edu['institution']}<br><em>{edu['year']}</em><br><br>{detail}")

    st.markdown("---")

    # Skills — from CV
    st.markdown("### Technical Skills & Certifications")
    skill_cols = st.columns(len(SKILLS))
    for col, (category, items) in zip(skill_cols, SKILLS.items()):
        with col:
            st.markdown(f"**{category}**")
            for item in items:
                skill_badge(item)

    st.markdown("")
    st.markdown("**Certifications:**")
    cert_cols = st.columns(3)
    certs = [
        ("🌱", "APS Seed Health Assays", "American Phytopathological Society, 2026"),
        ("🤖", "Deep Learning Fundamentals", "NVIDIA Deep Learning Institute, 2025"),
        ("🥬", "Produce Supply Chain Management", "International Fresh Produce Association, 2025"),
    ]
    for col, (icon, name, org) in zip(cert_cols, certs):
        col.markdown(f"{icon} **{name}**  \n*{org}*")

    st.markdown("---")

    # Affiliations
    st.markdown("### Professional Affiliations & Memberships")
    for aff in cfg["affiliations"]:
        st.markdown(f"🌿 **{aff['org']}** — {aff['role']} · *{aff['years']}*")


# =============================================================================
# PAGE 2 — Research & Professional Experience
# =============================================================================
elif page == "🔬  Research & Experience":
    st.title("Research & Professional Experience")
    st.markdown("---")

    metric_row([
        ("Field Trial Area",           "~3 acres",  "CRD per season"),
        ("Commercial Acres Informed",  "~50,000",   "Grimmway Farms, national"),
        ("U.S. Carrot Production",     "86%",        "Informed by fungicide trials"),
        ("Pesticide Reduction",        "80–90%",     "MOA IPM protocols, Taiwan"),
    ])
    st.markdown("---")

    # ── Funded Research Projects ──────────────────────────────────────────────
    st.markdown("### Funded Research Projects")
    for _, row in projects.iterrows():
        with st.expander(f"🌱  {row['title']}", expanded=True):
            p1, p2 = st.columns([3, 2])
            highlights = [h.strip() for h in str(row["highlights"]).split(";")]
            with p1:
                st.markdown(
                    f"**Funder:** {row['funder']}  \n"
                    f"**Role:** {row['role']}  \n"
                    f"**Period:** {int(row['start_year'])}–{int(row['end_year'])}  \n\n"
                    f"{row['description_short']}\n\n**Key contributions:**"
                )
                for h in highlights:
                    st.markdown(f"- {h}")
            with p2:
                st.metric("Trial Area (acres)", f"~{int(row['acres_managed'])}")
                st.metric("Commercial Acres Informed", f"~{int(row['acres_informed']):,}")

    st.markdown("---")

    # ── Professional Experience ───────────────────────────────────────────────
    st.markdown("### Professional Experience")

    with st.expander("🇺🇸  Graduate Research Assistant & Project Coordinator — University of Florida (2022–Present)", expanded=True):
        st.markdown("""
**Fungicide Efficacy & Application Technology**
- Executed large-scale (~3-acre) CRD field trials comparing chemigation (solid-set overhead sprinklers) vs. tractor-mounted sprayers for Alternaria leaf blight control
- Integrated UAV-based DJI platforms for NDVI/NDRE multispectral analysis to quantify disease severity
- Findings adopted by Grimmway Farms for ~50,000 acres of commercial carrot production nationally

**Cropping Systems Pathology (USDA-NIFA Organic Transitions)**
- Managed multi-year (2023–2026) field study across Conventional and Organic Carrot-Peanut-Corn rotations
- Demonstrated regenerative management suppressed *Alternaria* leaf blight (AUDPC) in conventional systems
- Identified *Gibberella* ear rot transitional risks in corn and evidence of soil suppressiveness against *Rhizoctonia solani*

**Seed Pathology & Inoculum Dynamics**
- Led four-year survey of commercial carrot seed lots; identified *A. alternata* as predominant pathogen via ITS, GAPDH, Alt a 1 phylogenetics
- Evaluated FQ-Cu hybrid nanoparticle, conventional fungicides, and biocontrols via ISTA-standard bioassays
- Used Python for 4PL regression modeling of EC50/EC90 fungicide sensitivity

**Diagnostic Pathology & AI Integration**
- Identified *Pythium* spp. as causal agent of post-harvest lesions via Koch's postulates
- Integrated ML frameworks for automated fungal spore image analysis

**Extension & Stakeholder Engagement**
- Collaborated directly with Grimmway Farms; authored UF/IFAS EDIS extension guide for Florida carrot producers
""")

    with st.expander("🇹🇼  Research Assistant & Extension Specialist — Ministry of Agriculture, Hualien Station (2021–2022)"):
        st.markdown("""
- Authored **4 technical extension bulletins** on IPM for Welsh Onion and Watermelon; protocols reduced pesticide usage by **80–90%**
- Conducted regional RT-PCR disease surveillance for viral outbreaks in Watermelon, Welsh Onion, and Chayote
- Established virus-free propagation systems highlighted by national media
- Optimized *Bacillus* spp. fermentation parameters; screened isolates against *Colletotrichum* spp. and *Stagonosporopsis* spp.
""")

    with st.expander("🇹🇼  Graduate Research Assistant — National Taiwan University (2018–2021)"):
        st.markdown("""
- Secured **~$48,333 USD** in competitive government grants (Ministry of Agriculture, Taiwan) as Co-Author & Lead Investigator
- Performed multi-locus phylogenetics (MEGA, RAxML) characterizing *Stemphylium* spp. diversity — first-author publication in *Plant Disease*
- Conducted field scouting, fungicide resistance profiling, and EC50 sensitivity assays across major Welsh onion production regions
- Used R and SAS for resistance profiling and epidemiological modeling
""")

    with st.expander("🏭  Research & Industry Internships (2016–2018)"):
        st.markdown("""
**Research Intern — China Agriculture University, Beijing (2018)**
- Screened *Bacillus* spp. bio-formulations against soilborne vegetable pathogens in greenhouse assays

**R&D Intern — SING-FLOW SEED CO., LTD., Taiwan (2017)**
- Assisted in Broccoli and Tomato germplasm screening for disease resistance; analyzed phenotypic trait data for breeder selection

**Undergraduate Research Intern — National Chung Hsing University, Taichung (2017)**
- Isolated and characterized endophytic communities from *Camellia sinensis* (Tea); investigated microbial diversity vs. secondary metabolite profiles

**Research Intern — Tea Research and Extension Station, MOA, Nantou (2016)**
- Characterized feeding behavior and spatial distribution of *Helopeltis fasciaticollis* on tea; contributed data for regional IPM strategies
""")

    st.markdown("---")

    # ── Field Photos ──────────────────────────────────────────────────────────
    st.markdown("### Field Work Gallery")
    _field_imgs = _find_all_images("field")
    if _field_imgs:
        _render_image_grid(_field_imgs, cols=3)
    else:
        st.info("📷 Drop images with 'field' in the filename into `/assets/` to display here.", icon="ℹ️")


# =============================================================================
# PAGE 3 — Publications & Grants
# =============================================================================
elif page == "📄  Publications & Grants":
    st.title("Publications, Presentations & Grants")
    st.markdown("---")

    n_peer  = len(pubs[pubs["type"] == "peer_reviewed"])
    n_inprep = len(pubs[pubs["status"].isin(["under_review", "in_preparation"])])
    n_ext   = len(pubs[pubs["type"] == "extension"])
    metric_row([
        ("Peer-Reviewed Publications",         str(n_peer),   "Published"),
        ("Manuscripts Under Review / In Prep", str(n_inprep), "2025–2026"),
        ("Extension Reports",                  str(n_ext),    "UF/IFAS EDIS & MOA bulletins"),
        ("Conference Presentations",           str(len(presentations)), "Oral & poster"),
    ])
    st.markdown("---")

    def _pub_row(row):
        authors = row["authors"]
        year    = int(row["year"])
        title   = row["title"]
        journal = row["journal"]
        doi     = str(row.get("doi","")).strip()
        note    = str(row.get("contribution_note","")).strip()
        vol     = str(row.get("volume","")).strip()
        pages   = str(row.get("pages","")).strip()
        doi_link = f" [[DOI]](https://doi.org/{doi})" if doi and doi != "nan" else ""
        vol_str  = f", {vol}" if vol and vol != "nan" else ""
        pgs_str  = f", {pages}" if pages and pages != "nan" else ""
        pub_item(f"**{authors}** ({year}). {title}. *{journal}*{vol_str}{pgs_str}.{doi_link}",
                 note if note != "nan" else "")

    st.markdown("### 📰 Peer-Reviewed Publications")
    for _, row in pubs[pubs["type"] == "peer_reviewed"].iterrows():
        _pub_row(row)

    st.markdown("---")
    st.markdown("### 📝 Manuscripts Under Review & In Preparation")
    for _, row in pubs[pubs["status"].isin(["under_review","in_preparation"])].iterrows():
        label = "Under Review" if row["status"] == "under_review" else "In Progress"
        r = row.copy()
        r["journal"] = f"{row['journal']} (*{label}*)"
        _pub_row(r)

    st.markdown("---")
    st.markdown("### 📋 Extension & Technical Reports")
    for _, row in pubs[pubs["type"] == "extension"].iterrows():
        _pub_row(row)

    st.markdown("---")
    st.markdown("### 🎤 Conference Presentations")
    oral = presentations[presentations["type"] == "Oral"]
    poster = presentations[presentations["type"] == "Poster"]

    st.markdown("**Oral Presentations**")
    for _, row in oral.iterrows():
        award = f" 🏆 *{row['award']}*" if str(row.get("award","")) not in ("","nan") else ""
        pub_item(f"**{row['authors']}** ({int(row['year'])}). *{row['title']}*. {row['event']}, {row['location']}.{award}")

    st.markdown("**Poster Presentations**")
    for _, row in poster.iterrows():
        pub_item(f"**{row['authors']}** ({int(row['year'])}). *{row['title']}*. {row['event']}, {row['location']}.")

    st.markdown("---")
    st.markdown("### 💰 Grants, Awards & Fellowships")

    g1, g2 = st.columns(2)
    competitive = grants[grants["type"].isin(["international_grant"])]
    awards      = grants[~grants["type"].isin(["international_grant"])]

    with g1:
        st.markdown("#### Competitive Grants")
        for _, row in competitive.iterrows():
            amt = f"${int(row['amount_usd']):,}"
            card(f"{row['title']}  ·  {amt}",
                 f"**Agency:** {row['agency']}  ·  **Year:** {int(row['year'])}<br>"
                 f"**Role:** {row['role']}<br><em>{row['description']}</em>")
        total = competitive["amount_usd"].sum()
        st.metric("Total Competitive Grant Funding", f"~${total:,.0f}")

    with g2:
        st.markdown("#### Scholarships, Fellowships & Awards")
        for _, row in awards.iterrows():
            amt = f" · ${int(row['amount_usd']):,}" if row["amount_usd"] > 0 else ""
            card(f"{row['title']}{amt}",
                 f"{row['agency']} · {int(row['year'])}<br><em>{row['description']}</em>")


# =============================================================================
# PAGE 4 — Teaching, Mentoring & Leadership
# =============================================================================
elif page == "🎓  Teaching & Leadership":
    st.title("Teaching, Mentoring & Leadership")
    st.markdown("---")

    metric_row([
        ("Junior Scientists Mentored", "7",  "Across UF, MOA, NTU"),
        ("Teaching Roles",             "3",  "TA & Lecturer positions"),
        ("Outreach Events",            "10+","Workshops, lectures, tours"),
        ("Leadership Positions",       "4",  "VP, Co-Chair, Representative"),
    ])
    st.markdown("---")

    # Teaching
    st.markdown("### 🎓 Teaching Experience")
    t1, t2, t3 = st.columns(3)
    with t1:
        card("Lecturer — STEM Scientific Writing",
             "DXR Healthy Academy, 2025<br>"
             "Designed and taught 10-course curriculum on research article structure and scientific grammar "
             "for high school students preparing competitive science fair manuscripts.")
    with t2:
        card("Teaching Assistant — Fungal Plant Pathogens",
             "University of Florida, 2024<br>"
             "Lecturer: Dr. Jeffrey A. Rollins. Assisted in course material development and laboratory "
             "preparation, specializing in Mucoromycota.")
    with t3:
        card("Teaching Assistant — Mycology",
             "National Taiwan University, 2018–2019<br>"
             "Lecturer: Dr. Hiran Ariyawansa. Independently managed student lab sessions and graded "
             "projects, focusing on Mucoromycota and Ascomycota.")

    st.markdown("---")

    # Mentoring
    st.markdown("### 🧑‍🔬 Research Mentoring (7 Junior Scientists)")
    m1, m2 = st.columns([3, 2])
    with m1:
        with st.expander("View all mentees", expanded=True):
            st.markdown("""
| Period | Institution | Mentee | Role | Key Training |
|--------|------------|--------|------|-------------|
| 2025–Present | University of Florida | Savannah Beaulieu | Undergrad RA | Fungal isolation, DNA extraction, PCR amplification |
| 2021–2022 | MOA Hualien Station | Tzu-Ching Yang | Research Assistant | Viral RNA extraction, RT-PCR disease diagnostics |
| 2021–2022 | MOA Hualien Station | Tzu-Ching Cheng | Intern | Single-spore isolation, culture maintenance |
| 2018–2020 | National Taiwan University | Chien-Yuan Wang | M.S. Student | Experimental design, greenhouse pathogenicity assays |
| 2018–2020 | National Taiwan University | Hsiang-Ching Weng | M.S. Student | EC50 fungicide sensitivity, field disease scouting |
| 2018–2020 | National Taiwan University | Chia-Yun Yen | Undergrad | DNA extraction, field scouting protocols |
| 2018–2020 | National Taiwan University | Yu-Tseng Lin | Undergrad | DNA extraction, field scouting protocols |
""")
    with m2:
        st.metric("Institutions", "3", "UF, MOA, NTU")
        st.metric("M.S. Students Mentored", "2")
        st.metric("Undergrad & RA Mentored", "5")

    st.markdown("---")

    # Leadership
    st.markdown("### 🏛️ Leadership Experience")
    l1, l2 = st.columns(2)
    with l1:
        card("Vice President (Event Coordinator) — UF Plant Pathology Graduate Student Organization (2025–2026)",
             "Led operations for 50+ member organization; managed schedules, events, meeting agendas, "
             "and internal communications. Served as primary bridge between student body and faculty administration.")
        card("Elected Student Representative — NCHU Student Council (2016–2017)",
             "Represented student body at National Chung Hsing University; advocated for student welfare and academic policies.")
    with l2:
        card("Co-Chair, Events Committee — UF Plant Science Council (2025–2026)",
             "Orchestrated the Plant Science Symposium (400+ attendees) and social events; "
             "oversaw logistics, vendor coordination, and budget allocation.")
        card("Counselor — NEO Education College Summer Camp (2024)",
             "Facilitated educational programming for college-bound students.")

    st.markdown("---")

    # Peer Review & Service
    st.markdown("### 🔍 Peer Review & Professional Service")
    pr1, pr2, pr3 = st.columns(3)
    with pr1:
        card("Journal Reviewer",
             "*Physiological and Molecular Plant Pathology* — reviewed original research and review articles (2025)")
    with pr2:
        card("Book Chapter Reviewer",
             "American Phytopathological Society — reviewed Chapter III for the *Compendium of Pepper Diseases* (2025)")
    with pr3:
        card("Regional Scientific Reviewer",
             "Junior Science & Humanities Symposium (U.S. Dept. of Defense, 2025) — "
             "evaluated experimental design for 10 independent STEM research investigations")

    st.markdown("---")

    # Extension & Outreach
    st.markdown("### 📣 Extension & Outreach")
    with st.expander("Workshop Speaker (4)", expanded=True):
        st.markdown("""
- **2026** — *Plant Disease Diagnostic Workshop* | 2026 Plant Science Symposium — Educated students (n=7) on biotic and abiotic disease identification
- **2025** — *4-H University Workshop* | Florida 4-H Foundation — Trained students (n=10) on identifying plant diseases and using photographic leaf data to train AI models
- **2025** — *Plants Get Sick Too Teacher Workshop* | K-12 Professional Development — Co-led PD for K-12 teachers (n=25) on Florida plant diseases
- **2024–2025** — *Annual UF Workshop on the Plant Immune System* | K-12 Professional Development — contributed content for K-12 teachers (n=8)
""")

    with st.expander("Guest Lecturer (2)"):
        st.markdown("""
- **2025** — SEFS Program | Miami-Dade high school — plant anatomy and evolution for K-12 students (n=60)
- **2025** — SEFS Program | Boca Raton high school — plant science careers for K-12 students (n=50)
""")

    with st.expander("Tour Host & Event Organizer"):
        st.markdown("""
**Tour Host (3):**
- 2025 — APS Joint Meeting Caribbean & Southern Division: UF laboratory tours for college students (n=50)
- 2025 — Florida Junior Academy's JSHS 2025: UF laboratory tours for high school students (n=30)
- 2024 — UF/IFAS Spring Festival: Plant fungal pathogen culture display for local community

**Event Organizer (5):**
- 2026 — 10th Annual Plant Science Symposium
- 2025 — 2025 Joint Meeting of the Caribbean and Southern Division APS
- 2021 — Welsh Onion Conservation Healthy Seedlings Workshop
- 2021 — Welsh Onion IPM and Reduce Costs through Rational Use of Chemicals Workshop
- 2019 — Annual Meeting of Mycological Society ROC Taiwan
""")


# =============================================================================
# PAGE 5 — In the News
# =============================================================================
elif page == "📰  In the News":
    st.title("In the News")
    st.markdown("Research and outreach work featured in media and institutional publications.")
    st.markdown("---")

    news_items = [
        {
            "emoji": "🇺🇸",
            "outlet": "UF/IFAS Horticultural Sciences Blog",
            "date": "March 14, 2025",
            "title": "Stakeholders, researchers, and regulators committed to advancing soil health through long-term adoption of cover cropping",
            "title_en": "",
            "description": (
                "Sean Wang (doctoral student, Plant Pathology) is featured in this UF/IFAS blog post "
                "covering the 2025 Annual Soil Health and Cover Crop Training Workshop at the North Florida "
                "Research and Education Center (NFREC), Live Oak, FL. The article describes the USDA-funded "
                "regenerative agriculture project Sean leads under Dr. Gabriel Maltais-Landry and "
                "Dr. Mathews Paret — including results from Corn-Peanut-Carrot rotation trials comparing "
                "traditional vs. regenerative management. Sean also contributed a photo credited in the "
                "article (Photo Credit: UF/IFAS S. Wang)."
            ),
            "url": "https://blogs.ifas.ufl.edu/hosdept/2025/03/14/stakeholders-researchers-and-regulators-committed-to-advancing-soil-health-through-long-term-adoption-of-cover-cropping/",
            "tags": ["USDA-NIFA", "Regenerative Agriculture", "Soil Health", "UF/IFAS"],
        },
        {
            "emoji": "🇹🇼",
            "outlet": "自由時報 (Liberty Times) — Taiwan National Media",
            "date": "May 5, 2021",
            "title": "花蓮成功「移地保種」三星蔥 16噸青蔥收成回娘家",
            "title_en": "Hualien successfully completes ex-situ conservation of Sanxing Welsh Onion — 16 tonnes harvested",
            "description": (
                "This national news report covers the landmark ex-situ germplasm conservation initiative "
                "at Hualien District Agricultural Research and Extension Station (MOA), where Sean served "
                "as Research Assistant & Extension Specialist. Following severe crop damage from prolonged "
                "rainfall in Yilan's Sanxing region, the team relocated and propagated Welsh Onion seed "
                "stock in Hualien over 119 days, producing 16 tonnes across 1 hectare. The initiative — "
                "involving virus screening, soil fertility management, and disease monitoring — was "
                "described as unprecedented by the station and highlighted by national media for "
                "restoring regional crop productivity."
            ),
            "url": "https://news.ltn.com.tw/news/life/breakingnews/3521624",
            "tags": ["Welsh Onion", "IPM", "Extension", "Taiwan MOA", "National Media"],
        },
    ]

    for item in news_items:
        tags_html = " ".join(
            f'<span style="background:#e8f5e9;color:#2e7d32;padding:2px 10px;'
            f'border-radius:20px;font-size:0.78rem;margin-right:4px">{t}</span>'
            for t in item["tags"]
        )
        title_display = item["title"]
        if item.get("title_en"):
            title_display += (
                f'<br><span style="font-size:0.9rem;color:#555;font-style:italic">'
                f'{item["title_en"]}</span>'
            )
        st.markdown(
            f'<div style="border:1px solid #e0e0e0;border-radius:10px;padding:1.4rem 1.6rem;'
            f'margin-bottom:1.4rem;background:#fafafa;">'
            f'<div style="font-size:0.82rem;color:#888;margin-bottom:0.3rem">'
            f'{item["emoji"]} &nbsp;<strong>{item["outlet"]}</strong>'
            f' &nbsp;·&nbsp; {item["date"]}</div>'
            f'<div style="font-size:1.1rem;font-weight:600;margin-bottom:0.7rem;color:#1a1a1a">'
            f'{title_display}</div>'
            f'<p style="color:#444;font-size:0.95rem;margin-bottom:0.8rem">'
            f'{item["description"]}</p>'
            f'{tags_html}<br><br>'
            f'<a href="{item["url"]}" target="_blank" style="color:#2e7d32;font-weight:500">'
            f'Read the full article →</a>'
            f'</div>',
            unsafe_allow_html=True,
        )


# =============================================================================
# PAGE 6 — Contact & CV
# =============================================================================
elif page == "📬  Contact & CV":
    st.title("Contact & Download CV")
    st.markdown("---")

    c_left, c_right = st.columns([2, 3], gap="large")

    with c_left:
        st.markdown("### Get in Touch")
        st.markdown(
            "Happy to discuss research collaborations, speaking invitations, "
            "or academic and industry opportunities."
        )
        st.markdown("---")
        contact_items = [
            ("📧", "Email",          P["email"],      f"mailto:{P['email']}"),
            ("📍", "Location",       P["location"],   None),
            ("🎓", "Google Scholar", "Scholar Profile", P["google_scholar"]),
            ("💼", "LinkedIn",       "LinkedIn Profile", P["linkedin"]),
            ("🏛️", "UF Page",       "UF Plant Pathology", P["uf_page"]),
        ]
        for icon, label, value, link in contact_items:
            link_html = f'<a href="{link}" target="_blank">{value}</a>' if link else value
            st.markdown(
                f"<div style='background:#f8f9fa;border-left:4px solid #2e7d32;"
                f"padding:.7rem 1rem;border-radius:4px;margin-bottom:.6rem'>"
                f"{icon} &nbsp;<strong>{label}:</strong>&nbsp; {link_html}</div>",
                unsafe_allow_html=True,
            )

    with c_right:
        st.markdown("### Download Full CV")
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
                f"📎 Place **`{P['cv_filename']}`** in the `/assets/` folder to enable download.",
                icon="ℹ️",
            )
            st.button("⬇️  Download CV (PDF) — coming soon", disabled=True, use_container_width=True)

        st.markdown("---")
        st.markdown("### Research Interests & Collaboration")
        for item in COLLAB["interests"]:
            st.markdown(f"- {item}")

        st.markdown("---")
        st.markdown("### Current Availability")
        s1, s2 = st.columns(2)
        with s1:
            open_to_md = "<br>".join(f"✅ {o}" for o in COLLAB["open_to"])
            card("Open To", open_to_md)
        with s2:
            card("Timeline",
                 f"🎓 Expected graduation: {COLLAB['expected_graduation']}<br>"
                 "📅 Available for discussions now")
