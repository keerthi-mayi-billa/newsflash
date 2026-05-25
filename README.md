<div align="center">

<!-- BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=E8C547&height=200&section=header&text=NewsFlash&fontSize=80&fontColor=0b0b0b&fontAlignY=38&desc=AI-Powered%20News%20Summarization&descAlignY=58&descSize=22&descColor=0b0b0b" width="100%"/>

<br/>

<!-- BADGES -->
[![GitHub Actions](https://img.shields.io/badge/Auto--Updated-Daily-E8C547?style=for-the-badge&logo=githubactions&logoColor=black)](https://github.com/keerthi-mayi-billa/newsflash/actions)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20On-GitHub%20Pages-E8C547?style=for-the-badge&logo=github&logoColor=black)](https://keerthi-mayi-billa.github.io/newsflash/)
[![Python](https://img.shields.io/badge/Python-3.11-E8C547?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![HuggingFace](https://img.shields.io/badge/Model-BART%20Large%20CNN-E8C547?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/facebook/bart-large-cnn)
[![License](https://img.shields.io/badge/License-MIT-E8C547?style=for-the-badge)](LICENSE)

<br/>

**A fully automated, AI-powered news aggregation and summarization platform.**  
Scrapes Times of India daily · Summarizes with BART · Publishes automatically via GitHub Actions.  
*Zero manual work. Every day. For free.*

<br/>

[🌐 **View Live Website**](https://keerthi-mayi-billa.github.io/newsflash/) &nbsp;·&nbsp;
[📋 **Report Bug**](https://github.com/keerthi-mayi-billa/newsflash/issues) &nbsp;·&nbsp;
[💡 **Request Feature**](https://github.com/keerthi-mayi-billa/newsflash/issues)

</div>

---

## 📸 Preview

<div align="center">
<img src="https://i.imgur.com/placeholder.png" alt="NewsFlash Preview" width="90%" style="border-radius:12px;"/>
<p><i>NewsFlash — dark themed, card-based news UI with AI summaries and text-to-speech</i></p>
</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Summarization** | Every article summarized using Facebook's BART-large-CNN model |
| 🕐 **Daily Auto-Update** | GitHub Actions scrapes and summarizes fresh news at 6:00 AM IST every day |
| 🔊 **Text-to-Speech** | Listen to any article summary with one click using Web Speech API |
| 📰 **9 News Categories** | Top Stories, India, World, Tech, Business, Sports, Science, Education, Entertainment |
| 🔍 **Live Search** | Instantly filter articles by keyword across all categories |
| 📱 **Fully Responsive** | Works seamlessly on desktop, tablet, and mobile |
| 🌐 **Always Public** | Hosted free on GitHub Pages — shareable with anyone, anywhere |
| ⚡ **Zero Cost** | 100% free — GitHub Actions + GitHub Pages + HuggingFace free tier |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY AUTOMATION PIPELINE                     │
│                  GitHub Actions · 6:00 AM IST                   │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│   scraper.py    │ ───▶ │  summarizer.py   │ ───▶ │  GitHub Pages Live  │
│                 │      │                  │      │                     │
│ TOI RSS Feeds   │      │ HuggingFace API  │      │  index.html         │
│ 9 Categories    │      │ BART-large-CNN   │      │  summarized_news    │
│ ~36 Articles    │      │ ~130 word summry │      │  .json              │
└─────────────────┘      └──────────────────┘      └─────────────────────┘
          │                      │                          │
          ▼                      ▼                          ▼
  scraped_news.json    summarized_news.json      Public Website URL
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Web Scraping** | BeautifulSoup4 + Requests + TOI RSS Feeds |
| **AI Model** | `facebook/bart-large-cnn` via HuggingFace Inference API |
| **Frontend** | Vanilla HTML5 + CSS3 + JavaScript (no frameworks) |
| **Automation** | GitHub Actions (cron schedule) |
| **Hosting** | GitHub Pages |
| **Audio** | Web Speech API (browser built-in, no library needed) |

</div>

---

## 📁 Project Structure

```
newsflash/
│
├── 📄 scraper.py                    # Scrapes TOI RSS feeds (9 categories)
├── 📄 summarizer.py                 # Summarizes via HuggingFace BART API
├── 📄 requirements.txt              # Python dependencies
│
├── 📂 docs/                         # GitHub Pages served folder
│   ├── 🌐 index.html                # Main website (UI)
│   └── 📊 summarized_news.json      # Latest news data (auto-updated daily)
│
└── 📂 .github/
    └── 📂 workflows/
        └── ⚙️  daily_update.yml     # GitHub Actions automation workflow
```

---

## 🚀 How It Works

```
1. Every day at 6:00 AM IST ──▶ GitHub Actions wakes up automatically

2. Runs scraper.py ────────────▶ Fetches latest headlines from 9 TOI RSS feeds
                                  Extracts: title, image, URL, full article text

3. Runs summarizer.py ─────────▶ Sends each article to HuggingFace BART API
                                  Gets back: clean 2-3 sentence AI summary

4. Commits to GitHub ──────────▶ Updates docs/summarized_news.json in repo

5. GitHub Pages updates ───────▶ Website is live with today's news within minutes

6. User visits website ────────▶ Sees latest summarized news, can listen via TTS
```

---

## ⚙️ Setup & Deployment

### Prerequisites
- GitHub account (free)
- HuggingFace account (free)

### Step 1 — Fork or Clone This Repo
```bash
git clone https://github.com/keerthi-mayi-billa/newsflash.git
cd newsflash
```

### Step 2 — Get HuggingFace API Token
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to **Settings → Access Tokens → New token**
3. Name: `newsflash` | Type: **Read**
4. Copy the `hf_...` token

### Step 3 — Add Token to GitHub Secrets
```
GitHub Repo → Settings → Secrets and variables → Actions → New secret
Name:  HF_TOKEN
Value: hf_your_token_here
```

### Step 4 — Enable GitHub Pages
```
GitHub Repo → Settings → Pages
Source: Deploy from branch
Branch: main  |  Folder: /docs
```

### Step 5 — Trigger First Run
```
GitHub Repo → Actions → Daily News Update → Run workflow
```

Your site will be live at `https://YOUR-USERNAME.github.io/newsflash/` 🎉

---

## 🏃 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your HuggingFace token
set HF_TOKEN=hf_your_token_here     # Windows
export HF_TOKEN=hf_your_token_here  # Mac/Linux

# Step 1: Scrape news
python scraper.py

# Step 2: Summarize articles
python summarizer.py

# Step 3: Open the website
# Open docs/index.html in your browser
```

---

## 📊 News Categories Covered

<div align="center">

🏆 Top Stories &nbsp;|&nbsp; 🇮🇳 India &nbsp;|&nbsp; 🌍 World &nbsp;|&nbsp; 💻 Technology &nbsp;|&nbsp; 💼 Business

⚽ Sports &nbsp;|&nbsp; 🔬 Science &nbsp;|&nbsp; 🎓 Education &nbsp;|&nbsp; 🎬 Entertainment

</div>

---

## 🤖 AI Model Details

| Property | Value |
|---|---|
| **Model** | `facebook/bart-large-cnn` |
| **Type** | Abstractive Text Summarization |
| **Parameters** | 406 Million |
| **Training Data** | CNN / DailyMail news dataset |
| **Summary Length** | 40–130 tokens per article |
| **Inference** | HuggingFace Inference API (cloud, free tier) |

**Why BART?**  
BART (Bidirectional and Auto-Regressive Transformer) is specifically fine-tuned on news articles from CNN and DailyMail, making it ideal for summarizing news content. It generates abstractive summaries — rephrasing and condensing information rather than just extracting sentences.

---

## 👨‍💻 Author

<div align="center">

**Keerthi Mayi Billa**  
Senior Design Project — Multi-Model News Article Summarization  

[![GitHub](https://img.shields.io/badge/GitHub-keerthi--mayi--billa-E8C547?style=flat-square&logo=github&logoColor=black)](https://github.com/keerthi-mayi-billa)

</div>

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=E8C547&height=100&section=footer&fontColor=0b0b0b" width="100%"/>

**⭐ Star this repo if you found it useful!**

*Built with ❤️ for Senior Design Project*

</div>
