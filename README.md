# Sean Wang — Ph.D. Candidate Portfolio

A multi-page Streamlit portfolio for **Chun-Hsiang (Sean) Wang**, Ph.D. Candidate in
Plant Pathology at the University of Florida.

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sean-wang-portfolio.git
cd sean-wang-portfolio

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
sean-wang-portfolio/
├── app.py                    ← Main entry point; routing + page rendering
├── content_config.toml       ← ✏️  All personal info, bio, metrics, skills
├── requirements.txt
├── README.md
│
├── data/                     ← CSV data tables (edit to add real content)
│   ├── publications.csv
│   ├── grants.csv
│   ├── presentations.csv
│   └── research_projects.csv
│
├── assets/                   ← Static files (not committed if large)
│   ├── Sean_Wang_CV.pdf      ← Drop your PDF here to activate download button
│   └── profile.jpg           ← Optional profile photo
│
├── modules/                  ← Reusable Python modules
│   ├── data_loader.py        ← Cached CSV + TOML readers
│   ├── ui_components.py      ← card(), pub_item(), skill_badge(), etc.
│   └── pages/
│       └── __init__.py
│
└── .streamlit/
    └── config.toml           ← Theme (green accent, white background)
```

---

## Personalising Content

All content is driven by **two sources** — no Python editing required for most changes:

| What you want to change | Where to edit |
|---|---|
| Name, email, links, bio, metrics | `content_config.toml` |
| Publications | `data/publications.csv` |
| Grants & awards | `data/grants.csv` |
| Conference presentations | `data/presentations.csv` |
| Research projects | `data/research_projects.csv` |
| CV PDF | Drop file into `assets/` — filename must match `cv_filename` in config |
| App theme colours | `.streamlit/config.toml` |

---

## Deployment Checklist — Streamlit Community Cloud

> Complete these steps in order before clicking **Deploy**.

### 1 — Repo preparation
- [ ] Push all files to a **public** GitHub repository (or private with Streamlit Cloud access granted)
- [ ] Confirm `app.py` is at the **root** of the repo (not inside a subfolder)
- [ ] Confirm `requirements.txt` is at the root and lists all packages

### 2 — Content & assets
- [ ] Replace all `[placeholder]` values in `content_config.toml` with real data
- [ ] Fill in `data/*.csv` files with real publications, grants, and presentations
- [ ] Place `Sean_Wang_CV.pdf` in `assets/` (or update `cv_filename` in config)
- [ ] (Optional) Add `assets/profile.jpg` for a profile photo
- [ ] **Do not commit sensitive data** — use Streamlit Secrets for API keys if added later

### 3 — Python version
- [ ] Set Python **3.11+** in the Streamlit Cloud deploy settings so that `tomllib` is available without `tomli`
- [ ] If using Python < 3.11, confirm `tomli` is in `requirements.txt` and update the import in `data_loader.py`:
  ```python
  try:
      import tomllib
  except ImportError:
      import tomli as tomllib
  ```

### 4 — Deploy on Streamlit Community Cloud
- [ ] Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
- [ ] Click **New app** → select your repo, branch (`main`), and main file (`app.py`)
- [ ] Set Python version to 3.11 under **Advanced settings**
- [ ] Click **Deploy** — build takes 1–3 minutes

### 5 — Post-deployment checks
- [ ] Verify all five navigation pages load without errors
- [ ] Test the CV download button (or confirm the info banner shows if PDF not yet added)
- [ ] Check the app renders correctly on mobile (responsive layout)
- [ ] Copy the public URL (e.g. `https://seanwang.streamlit.app`) and add it to your GitHub repo description and LinkedIn profile

### 6 — Keeping it updated
- [ ] Whenever you add a publication, update `data/publications.csv` and push to GitHub — the live app redeploys automatically
- [ ] Streamlit Community Cloud free tier: 1 private app or unlimited public apps

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
