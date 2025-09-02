import requests
import feedparser 
import pandas

def fetch_news (query : str = "Inteligência Artificial Piauí", limit: int = 15):
  url_base = "https://news.google.com/rss/search"
  params = {
    "q": query,
    "hl": "pt-BR",
    "gl": "BR",
    "ceid": "BR:pt-419"
  }

  response = requests.get(url_base, params=params, timeout=10)
  response.raise_for_status()

  feed = feedparser.parse(response.content)

  if feed.bozo:
    raise Exception("Erro ao analisar o feed RSS.")

  if not feed.entries:
    raise Exception("Nenhuma notícia encontrada para a consulta fornecida.")

  new_list = []
  for entry in feed.entries[:limit]:
    new_list.append({
      "title": entry.get("title", ""),
      "link": entry.get("link", ""),
      "pubDate": entry.get("published", ""),
      "description": entry.get("description", ""),
    })


  df = pandas.DataFrame(new_list)
  return df
  

