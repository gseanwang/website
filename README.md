# Sean Wang — Ph.D. Candidate Portfolio

**🌐 Live site: https://seanwang.streamlit.app**

A multi-page Streamlit portfolio for **Chun-Hsiang (Sean) Wang**, Ph.D. Candidate in
Plant Pathology at the University of Florida.

---

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/gseanwang/website.git
cd website

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Project Structure

```
website/
├── app.py                    ← Main entry point; routing + page rendering
├── content_config.toml       ← ✏️  All personal info, bio, metrics, skills
├── config.toml               ← Streamlit theme (green accent, white background)
├── requirements.txt
├── README.md
│
├── data/                     ← CSV data tables
│   ├── publications.csv
│   ├── grants.csv
│   ├── presentations.csv
│   └── research_projects.csv
│
├── assets/                   ← Static files
│   ├── CV_Chun-Hsiang_Sean_Wang.pdf   ← CV download (filename matches cv_filename in config)
│   ├── profile.jpeg                    ← Profile photo
│   └── (workshop/lab/field photos used throughout the site)
│
└── modules/                  ← Reusable Python modules
    ├── data_loader.py        ← Cached CSV + TOML readers
    └── ui_components.py      ← card(), pub_item(), skill_badge(), etc.
```

---

## Updating Content

All content is data-driven — no Python editing required for most changes:

| What to change | Where to edit |
|---|---|
| Name, email, links, bio, metrics | `content_config.toml` |
| Publications | `data/publications.csv` |
| Grants & awards | `data/grants.csv` |
| Conference presentations | `data/presentations.csv` |
| Research projects | `data/research_projects.csv` |
| CV PDF | Replace file in `assets/` (filename must match `cv_filename` in config) |
| App theme colours | `config.toml` |

**Live site auto-redeploys on every push to `main`.** Edit → commit → push → wait 1–2 minutes → live.

---

## Python Version Note

`tomllib` is part of the Python 3.11 standard library.
For Python 3.9 / 3.10, install `tomli` (already in `requirements.txt`) and
update the import in `modules/data_loader.py`:

```python
try:
    import tomllib
except ImportError:
    import tomli as tomllib
```
