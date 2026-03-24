import urllib.request
  import xml.etree.ElementTree as ET                                                                           
  import json                                                                                                  
  from datetime import datetime, timezone
                                                                                                               
  WHITELIST = [   
      'oil', 'crude', 'market', 'stock', 'fed', 'federal reserve', 'rate',
      'trade', 'tariff', 'inflation', 'gdp', 'recession', 'bond', 'treasury',
      'dollar', 'yuan', 'gold', 'commodity', 'energy', 'opec', 'economy', 'economic',                          
      'iran', 'china', 'russia', 'ukraine', 'taiwan', 'war', 'sanction',
      'ceasefire', 'nato', 'military', 'nuclear', 'hormuz',                                                    
      'trump', 'congress', 'white house', 'debt', 'shutdown', 'budget',
  ]                                                                                                            
                  
  FEEDS = [                                                                                                    
      'https://feeds.reuters.com/reuters/topNews',
      'https://feeds.reuters.com/reuters/businessNews',
  ]

  def is_relevant(title, desc):                                                                                
      text = (title + ' ' + desc).lower()
      return any(kw in text for kw in WHITELIST)                                                               
                  
  articles = []
  seen = set()

  for url in FEEDS:
      if len(articles) >= 10:
          break
      try:
          req = urllib.request.urlopen(url, timeout=15)                                                        
          tree = ET.fromstring(req.read())
          channel = tree.find('channel')                                                                       
          if channel is None:
              continue
          for item in channel.findall('item'):
              title = item.findtext('title', '')                                                               
              link = item.findtext('link', '')
              desc = item.findtext('description', '')                                                          
              pub_date = item.findtext('pubDate', '')
              if link in seen:
                  continue
              seen.add(link)
              if is_relevant(title, desc):                                                                     
                  articles.append({
                      'source': 'Reuters',                                                                     
                      'title': title,
                      'link': link,
                      'summary': desc[:500],
                      'pubDate': pub_date,
                  })                                                                                           
              if len(articles) >= 10:
                  break                                                                                        
      except Exception as e:
          print(f'Failed {url}: {e}')

  with open('reuters.json', 'w', encoding='utf-8') as f:                                                       
      json.dump({
          'updated': datetime.now(timezone.utc).isoformat(),                                                   
          'articles': articles
      }, f, ensure_ascii=False, indent=2)

  print(f'Saved {len(articles)} Reuters articles')
