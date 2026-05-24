# -*- coding: utf-8 -*-
"""
scraper.py - Times of India News Scraper
Fetches latest news from TOI RSS feeds.
Output: scraped_news.json
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

RSS_FEEDS = {
    "Top Stories":  "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "India":        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "World":        "https://timesofindia.indiatimes.com/rssfeeds/296589298.cms",
    "Technology":   "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
    "Business":     "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
    "Sports":       "https://timesofindia.indiatimes.com/rssfeeds/4719161.cms",
    "Science":      "https://timesofindia.indiatimes.com/rssfeeds/1898458.cms",
    "Education":    "https://timesofindia.indiatimes.com/rssfeeds/913168846.cms",
    "Entertainment":"https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",
}

MAX_ARTICLES_PER_FEED = 4
ARTICLE_FETCH_DELAY   = 1.0
REQUEST_TIMEOUT       = 12
OUTPUT_FILE           = "scraped_news.json"


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r
    except requests.RequestException as e:
        logging.warning("Failed to fetch %s: %s" % (url, e))
        return None


def get_link_from_item(item):
    link_tag = item.find("link")
    if link_tag:
        text = link_tag.get_text(strip=True)
        if text.startswith("http"):
            return text
        sib = link_tag.next_sibling
        if sib and str(sib).strip().startswith("http"):
            return str(sib).strip()

    guid = item.find("guid")
    if guid:
        text = guid.get_text(strip=True)
        if text.startswith("http"):
            return text

    raw = str(item)
    urls = re.findall(r'https://timesofindia\.indiatimes\.com/[^\s<>"\']+', raw)
    if urls:
        for u in urls:
            if "articleshow" in u:
                return u.rstrip("/")
        return urls[0].rstrip("/")
    return ""


def parse_rss(category, rss_url):
    logging.info("Fetching RSS [%s]" % category)
    r = fetch(rss_url)
    if not r:
        return []

    soup = BeautifulSoup(r.content, "xml")
    items = soup.find_all("item")[:MAX_ARTICLES_PER_FEED]
    articles = []

    for item in items:
        title     = item.find("title")
        pub_date  = item.find("pubDate")
        desc      = item.find("description")
        image_tag = item.find("media:content") or item.find("enclosure")
        image_url = image_tag.get("url", "") if image_tag else ""
        article_url = get_link_from_item(item)
        title_text  = title.get_text(strip=True) if title else ""
        if not title_text:
            continue

        articles.append({
            "category":    category,
            "title":       title_text,
            "url":         article_url,
            "published":   pub_date.get_text(strip=True) if pub_date else "",
            "description": desc.get_text(strip=True)     if desc     else "",
            "image_url":   image_url,
            "full_text":   "",
        })

    logging.info("  Parsed %d articles from [%s]" % (len(articles), category))
    return articles


def fetch_article_text(url):
    if not url:
        return ""
    r = fetch(url)
    if not r:
        return ""

    soup = BeautifulSoup(r.text, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    containers = [
        soup.find("div", class_="_s30J"),
        soup.find("div", class_="article_content"),
        soup.find("div", class_="Normal"),
        soup.find("div", {"id": "article-content"}),
        soup.find("article"),
    ]
    for container in containers:
        if container:
            paras = container.find_all("p")
            text  = " ".join(p.get_text(" ", strip=True) for p in paras)
            if len(text) > 200:
                return text

    paras = soup.find_all("p")
    return " ".join(p.get_text(" ", strip=True) for p in paras if len(p.get_text(strip=True)) > 40)


def scrape_all():
    all_articles = []
    for category, rss_url in RSS_FEEDS.items():
        stubs = parse_rss(category, rss_url)
        for stub in stubs:
            logging.info("  Fetching text: %s" % stub["title"][:55])
            stub["full_text"] = fetch_article_text(stub["url"])
            if len(stub["full_text"]) < 200:
                stub["full_text"] = stub["description"]
            time.sleep(ARTICLE_FETCH_DELAY)
        all_articles.extend(stubs)
    logging.info("Total articles scraped: %d" % len(all_articles))
    return all_articles


def save(articles):
    payload = {
        "scraped_at": datetime.now().isoformat(),
        "total":      len(articles),
        "articles":   articles,
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f, indent=2)
    logging.info("Saved %d articles to %s" % (len(articles), OUTPUT_FILE))


if __name__ == "__main__":
    logging.info("=== TOI Scraper Started ===")
    articles = scrape_all()
    save(articles)
    logging.info("=== Done ===")
