import json, re, urllib.request
from datetime import datetime, timedelta, timezone

URL = "https://ix.cnn.io/data/truth-social/truth_archive.json"
HOURS_BACK = 30

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
posts = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))

cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
recent = []
for p in posts:
    try:
        dt = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
        if dt >= cutoff:
            content = re.sub(r"<[^>]+>", "", p.get("content", "")).strip()
            recent.append({"id": p.get("id", ""), "created_at": p["created_at"], "content": content, "url": p.get("url", "")})
    except (KeyError, ValueError):
        continue

output = {"updated": datetime.now(timezone.utc).isoformat(), "posts": recent}
with open("truthsocial.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(recent)} posts")
