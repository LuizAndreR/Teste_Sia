import requests
import feedparser 
import pandas

# --- Função responsável por buscar notícias no Google News (RSS) ---
def fetch_news(query: str = "Inteligência Artificial Piauí", limit: int = 15):
  # URL base do RSS do Google News
  url_base = "https://news.google.com/rss/search"
  params = {
    "q": query,              # Termo de busca (padrão: "Inteligência Artificial Piauí")
    "hl": "pt-BR",           # Idioma (português Brasil)
    "gl": "BR",              # Região (Brasil)
    "ceid": "BR:pt-419"      # Código de país + idioma
  }

  # Faz a requisição ao Google News RSS
  response = requests.get(url_base, params=params, timeout=10)
  response.raise_for_status()  # Gera erro se a resposta não for bem sucedida (4xx/5xx)

  # Analisa o conteúdo do feed com feedparser
  feed = feedparser.parse(response.content)

  # Verifica se houve erro ao interpretar o feed
  if feed.bozo:
    raise Exception("Erro ao analisar o feed RSS.")

  # Se não houver notícias, retorna erro
  if not feed.entries:
    raise Exception("Nenhuma notícia encontrada para a consulta fornecida.")

  # Extrai as notícias, limitando pela quantidade desejada
  new_list = []
  for entry in feed.entries[:limit]:
    new_list.append({
      "title": entry.get("title", ""),            # Título da notícia
      "link": entry.get("link", ""),              # Link da notícia
      "pubDate": entry.get("published", ""),      # Data de publicação
      "description": entry.get("description", "") # Descrição/resumo
    })

  # Converte a lista em DataFrame pandas
  df = pandas.DataFrame(new_list)
  return df
