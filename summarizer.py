# -*- coding: utf-8 -*-
"""
summarizer.py - News Summarizer via Hugging Face Inference API
SDP Project: Multi-Model News Article Summarization

Uses HuggingFace's free cloud API to run BART summarization.
NO local model download needed (works perfectly on GitHub Actions).

Requires env variable:  HF_TOKEN  (your HuggingFace API token)
Get free token at: https://huggingface.co/settings/tokens

Input:  scraped_news.json
Output: summarized_news.json
"""

import json
import logging
import time
import re
import os
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")

HF_TOKEN   = os.environ.get("HF_TOKEN", "")
API_URL    = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
INPUT_FILE  = "scraped_news.json"
OUTPUT_FILE = "summarized_news.json"
MODEL_NAME  = "facebook/bart-large-cnn (HuggingFace API)"

SUMMARY_MIN = 40
SUMMARY_MAX = 130


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()


def summarize_via_api(text):
    """Call HuggingFace Inference API to summarize text."""
    if not HF_TOKEN:
        logging.warning("HF_TOKEN not set - using first 2 sentences as fallback")
        sentences = text.split(". ")
        return ". ".join(sentences[:2]).strip() + "."

    headers = {"Authorization": "Bearer " + HF_TOKEN}
    payload = {
        "inputs": text[:1024],
        "parameters": {
            "min_length": SUMMARY_MIN,
            "max_length": SUMMARY_MAX,
            "do_sample":  False,
        }
    }

    # Retry up to 3 times (model may be loading on first call)
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if r.status_code == 503:
                wait = r.json().get("estimated_time", 20)
                logging.info("  Model loading, waiting %ss..." % int(wait))
                time.sleep(min(wait, 30))
                continue
            r.raise_for_status()
            result = r.json()
            if isinstance(result, list) and result:
                return result[0].get("summary_text", "").strip()
        except Exception as e:
            logging.warning("  API attempt %d failed: %s" % (attempt + 1, e))
            time.sleep(5)

    # Final fallback: return first 2 sentences
    sentences = text.split(". ")
    return ". ".join(sentences[:2]).strip() + "."


def main():
    if not Path(INPUT_FILE).exists():
        logging.error("ERROR: %s not found. Run scraper.py first." % INPUT_FILE)
        return

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    articles = data.get("articles", [])
    logging.info("Loaded %d articles" % len(articles))

    if HF_TOKEN:
        logging.info("Using HuggingFace Inference API (BART)")
    else:
        logging.warning("No HF_TOKEN - summaries will be truncated text")

    results = []
    for i, article in enumerate(articles, 1):
        title = article.get("title", "Untitled")
        body  = article.get("full_text", "") or article.get("description", "")
        body  = clean_text(body)
        logging.info("[%d/%d] Summarizing: %s" % (i, len(articles), title[:55]))

        t0 = time.time()
        if len(body.split()) < 30:
            summary = body
        else:
            summary = summarize_via_api(body)
        elapsed = round(time.time() - t0, 2)

        results.append({
            "category":  article.get("category", ""),
            "title":     title,
            "url":       article.get("url", ""),
            "published": article.get("published", ""),
            "image_url": article.get("image_url", ""),
            "summary":   summary,
            "model":     MODEL_NAME,
            "time_sec":  elapsed,
        })
        logging.info("  Done in %ss" % elapsed)
        time.sleep(1)  # be polite to the API

    output = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model":        MODEL_NAME,
        "total":        len(results),
        "articles":     results,
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    logging.info("Saved %d summaries to %s" % (len(results), OUTPUT_FILE))
    logging.info("=== Done ===")


if __name__ == "__main__":
    logging.info("=== Summarizer Started ===")
    main()
