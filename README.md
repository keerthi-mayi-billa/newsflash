# NewsFlash - Multi-Model News Article Summarization
### Senior Design Project

A fully automated news website that scrapes Times of India daily, summarizes articles using BART AI, and publishes them — all without you running any code.

---

## Live Architecture

```
GitHub Actions (cron: 6 AM IST daily)
       |
       ├── python scraper.py        → scraped_news.json
       ├── python summarizer.py     → summarized_news.json
       └── git push → static/      → GitHub Pages (your public website)
```

---

## One-Time Setup (do this once, then it's fully automatic)

### Step 1 — Get a Free HuggingFace Token

1. Go to https://huggingface.co → Sign Up (free)
2. Go to https://huggingface.co/settings/tokens
3. Click **New token** → Name it `newsflash` → Role: **Read**
4. Copy the token (starts with `hf_...`)

---

### Step 2 — Upload to GitHub

1. Go to https://github.com → Sign Up (free)
2. Click **+** → **New repository**
3. Name: `newsflash` | Visibility: **Public** | Click **Create**
4. Upload ALL your project files:
   - `scraper.py`
   - `summarizer.py`
   - `requirements.txt`
   - `static/index.html`
   - `static/summarized_news.json`
   - `.github/workflows/daily_update.yml`

**Easiest way to upload:** On your new repo page, click **uploading an existing file**, then drag all files in.

> For the `.github/workflows/` folder: Create it manually on GitHub.
> Click **Create new file** → type `.github/workflows/daily_update.yml` → paste the workflow content.

---

### Step 3 — Add Your HuggingFace Token as a Secret

1. In your GitHub repo → click **Settings**
2. Left sidebar → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `HF_TOKEN`
5. Value: paste your `hf_...` token
6. Click **Add secret**

---

### Step 4 — Enable GitHub Pages

1. In your GitHub repo → **Settings**
2. Left sidebar → **Pages**
3. Source: **Deploy from a branch**
4. Branch: `main` | Folder: `/static`
5. Click **Save**

Wait 2 minutes → GitHub will show your public URL:
```
https://YOUR-USERNAME.github.io/newsflash/
```

---

### Step 5 — Run the First Update Manually

1. In your GitHub repo → click **Actions** tab
2. Click **Daily News Update** workflow on the left
3. Click **Run workflow** → **Run workflow**
4. Watch it run (takes about 3-5 minutes)
5. After it finishes, refresh your website — real news will appear!

---

## After Setup — Fully Automatic

Every day at **6:00 AM IST**, GitHub Actions will:
1. Scrape latest news from Times of India (9 categories, ~36 articles)
2. Summarize each article using BART AI via HuggingFace API
3. Commit the new JSON to your repo
4. GitHub Pages automatically serves the updated website

**You don't need to do anything.**

---

## Manual Trigger (anytime you want fresh news)

Go to GitHub repo → **Actions** → **Daily News Update** → **Run workflow**

---

## Files Explained

| File | Purpose |
|------|---------|
| `scraper.py` | Fetches news from TOI RSS feeds |
| `summarizer.py` | Calls HuggingFace API to summarize with BART |
| `requirements.txt` | Python dependencies |
| `.github/workflows/daily_update.yml` | GitHub Actions automation |
| `static/index.html` | The public website |
| `static/summarized_news.json` | Latest news data (auto-updated) |

---

## Tech Stack

- **Scraping:** Python + BeautifulSoup (TOI RSS feeds)
- **AI Summarization:** BART (facebook/bart-large-cnn) via HuggingFace Inference API
- **Automation:** GitHub Actions (free, cron schedule)
- **Hosting:** GitHub Pages (free, static)
- **Total cost: $0**
