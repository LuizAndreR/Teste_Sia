import pandas as pd
import re
from html import unescape
from collections import Counter

def clean_text(text: str) -> str:
  if not isinstance(text, str):
    return ""
  text = unescape(text)
  text = re.sub(r'http\S+|www\.\S+', '', text)
  text = re.sub(
    r'\b(?:https?://|www\.)\S+|(?:\S+\.(?:com|org|net|gov|gov\.br|edu|edu\.br))\b', 
    '', 
    text, 
    flags=re.IGNORECASE
  ) 
  text = re.sub(r'<.*?>', '', text)
  text = re.sub(r'\s+', ' ', text).strip()
  return text

def process_news_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  if df.empty:
    return df
  
  df_copy = df.copy()

  rename_map = {  
    "title": "Titulo",
    "link": "Link",
    "pubDate": "Data de Publicação",
    "description": "Descrição"
  }
  
  df_copy.rename(columns=rename_map, inplace=True)

  df_copy["Data de Publicação"] = pd.to_datetime(df_copy["Data de Publicação"], errors='coerce', utc=True)
  df_copy.dropna(subset=["Data de Publicação"], inplace=True)
  df_copy.sort_values(by="Data de Publicação", ascending=False, inplace=True)
  df_copy["Data de Publicação"] = df_copy["Data de Publicação"].dt.strftime('%d/%m/%Y %H:%M:%S')  

  df_copy["Descrição"] = df_copy["Descrição"].apply(clean_text)
  df_copy.dropna(subset=["Descrição"], inplace=True)
  df_copy = df_copy[df_copy["Descrição"] != ""]

  if df_copy.empty:
      raise Exception("Nenhuma notícia com uma descrição válida foi encontrada.")
  
  final_columns = [
    "Data de Publicação",
    "Titulo",
    "Descrição",
    "Link"
  ]

  df_copy = df_copy[final_columns]

  return df_copy

STOPWORDS_PT = {
  "a", "o", "as", "os", "um", "uma", "uns", "umas",
  "de", "do", "da", "dos", "das",
  "em", "no", "na", "nos", "nas",
  "e", "que", "que", "por", "com", "para", "se", "ao", "à",
  "mais", "não", "ou", "como", "já", "são", "foi", "ser", "uso", "rafael", 
}

def extract_words(df: pd.DataFrame, column: str = "Descrição") -> list:

  all_text = " ".join(df[column].dropna().tolist()).lower()

  all_text = re.sub(r'[^a-záéíóúâêôãõç\s]', '', all_text)
  words = all_text.split()
  words = [word for word in words if word not in STOPWORDS_PT and len(word) > 2]
  return words

def get_word_frequencies(words: list) -> dict:

  return dict(Counter(words))