import requests
import feedparser 
import pandas

def fetch_news ():
  url = "https://news.google.com/rss/search?q=inteligência+artificial+no+Piauí&hl=pt-BR&gl=BR&ceid=BR:pt-419"
  response = requests.get(url)
  feed = feedparser.parse(response.content)
  
  new_list = []
  for entry in feed.entries[:15]:
    new_list.append({
       "title": entry.get("title", ""),
      "link": entry.get("link", ""),
      "pubDate": entry.get("pubDate", ""),
      "description": entry.get("description", ""),
    })


  df = pandas.DataFrame(new_list)
  return df

if __name__ == "__main__":
    print(f"Executando teste de busca para:")
    
    df_news = fetch_news()
    
    if not df_news.empty:
        print("\n--- DataFrame Criado com Sucesso (Apenas Colunas Essenciais) ---")
        print("As 5 primeiras linhas:")
        print(df_news.head())
        
        print("\nInformações do DataFrame:")
        df_news.info()

        print("\nMostrando o DateFrame todo")
        print(df_news)
    else:
        print("\nNão foi possível criar o DataFrame.")
  

