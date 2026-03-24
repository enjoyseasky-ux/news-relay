import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timezone

WHITELIST = [
    "oil", "crude", "market", "stock", "fed", "federal reserve", "rate",
    "trade", "tariff", "inflation", "gdp", "recession", "bond", "treasury",
    "dollar", "yuan", "gold", "commodity", "energy", "opec", "economy", "economic",
    "iran", "china", "russia", "ukraine", "taiwan", "war", "sanction",
    "ceasefire", "nato", "military", "nuclear", "hormuz",
    "trump", "congress", "white house", "debt", "shutdown", "budget",
]

# Google News RSS - aggregates Reuters articles
FEEDS = [
    "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
]

def is_relevant(title, desc):
    text = (title + " " + desc).lower()
    return any(kw in text for kw in WHITELIST)

articles = []
seen = set()

headers = {"User-Agent": "Mozilla/5.0"}

for url in FEEDS:
    if len(articles) >= 10:
        break
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15)
        tree = ET.fromstring(resp.read())
        channel = tree.find("channel")
        if channel is None:
            continue
        for item in channel.findall("item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "") or ""
            pub_date = item.findtext("pubDate", "")
            source_el = item.find("source")
            source_name = source_el.text if source_el is not None else ""
            source_url = source_el.get("url", "") if source_el is not None else ""

            # Only keep Reuters articles
            if "reuters" not in source_url.lower() and "reuters" not in source_name.lower():
                continue

            if link in seen:
                continue
            seen.add(link)

            if is_relevant(title, desc):
                articles.append({
                    "source": "Reuters",
                    "title": title,
                    "link": link,
                    "summary": desc[:500],
                    "pubDate": pub_date,
                })
            if len(articles) >= 10:
                break
    except Exception as e:
        print(f"Failed {url}: {e}")

with open("reuters.json", "w", encoding="utf-8") as f:
    json.dump({
        "updated": datetime.now(timezone.utc).isoformat(),
        "articles": articles
    }, f, ensure_ascii=False, indent=2)

print(f"Saved {len(articles)} Reuters articles")
