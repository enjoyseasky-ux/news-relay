  #!/usr/bin/env python3                                                                                                     
  """             
  抓取 Trump Truth Social 帖子 (via CNN archive)，筛选最近24h，写入 truthsocial.json
  """                                                                                                                        
                                                                                                                             
  import json                                                                                                                
  import re                                                                                                                  
  import urllib.request
  from datetime import datetime, timedelta, timezone

  URL = "https://ix.cnn.io/data/truth-social/truth_archive.json"                                                             
  OUTPUT = "truthsocial.json"
  HOURS_BACK = 30                                                                                                            
                  
  def fetch():
      req = urllib.request.Request(URL, headers={
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"                                       
      })
      with urllib.request.urlopen(req, timeout=30) as resp:                                                                  
          return json.loads(resp.read().decode("utf-8"))                                                                     
   
  def main():                                                                                                                
      posts = fetch()
      cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)                                                      
      recent = [] 
      for p in posts:                                                                                                        
          try:
              dt = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))                                            
              if dt >= cutoff:
                  content = p.get("content", "")                                                                             
                  content = re.sub(r"<[^>]+>", "", content).strip()
                  recent.append({                                                                                            
                      "id": p.get("id", ""),                                                                                 
                      "created_at": p["created_at"],
                      "content": content,                                                                                    
                      "url": p.get("url", ""),                                                                               
                      "replies_count": p.get("replies_count", 0),
                      "reblogs_count": p.get("reblogs_count", 0),                                                            
                      "favourites_count": p.get("favourites_count", 0),                                                      
                  })
          except (KeyError, ValueError):                                                                                     
              continue                                                                                                       
   
      output = {                                                                                                             
          "updated": datetime.now(timezone.utc).isoformat(),
          "posts": recent,                                                                                                   
      }
      with open(OUTPUT, "w", encoding="utf-8") as f:                                                                         
          json.dump(output, f, ensure_ascii=False, indent=2)

      print(f"Saved {len(recent)} posts in last {HOURS_BACK}h, saved to {OUTPUT}")                                           
   
  if __name__ == "__main__":                                                                                                 
      main()  
