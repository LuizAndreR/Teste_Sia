import pandas as pd
import re
from html import unescape
from collections import Counter

# --- Função para processar o DataFrame de notícias ---
def process_news_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  if df.empty:
    return df
  
  df_copy = df.copy()  # Trabalha em uma cópia para não alterar o original

  # Renomeia colunas para português
  rename_map = {  
    "title": "Titulo",
    "link": "Link",
    "pubDate": "Data de Publicação",
    "description": "Descrição"
  }
  df_copy.rename(columns=rename_map, inplace=True)

  # Converte datas para datetime e mantém apenas válidas
  df_copy["Data de Publicação"] = pd.to_datetime(df_copy["Data de Publicação"], errors='coerce', utc=True)
  df_copy.dropna(subset=["Data de Publicação"], inplace=True)
  df_copy.sort_values(by="Data de Publicação", ascending=False, inplace=True)  # Ordena da mais recente para a mais antiga
  df_copy["Data de Publicação"] = df_copy["Data de Publicação"].dt.strftime('%d/%m/%Y %H:%M:%S')  # Formata a data

  # Limpa descrições
  df_copy["Descrição"] = df_copy["Descrição"].apply(clean_text)
  df_copy.dropna(subset=["Descrição"], inplace=True)
  df_copy = df_copy[df_copy["Descrição"] != ""]  # Remove linhas sem descrição válida

  # Se depois de tudo não sobrar nada, gera erro
  if df_copy.empty:
    raise Exception("Nenhuma notícia com uma descrição válida foi encontrada.")
  
  # Mantém apenas colunas finais relevantes
  final_columns = [
    "Data de Publicação",
    "Titulo",
    "Descrição",
    "Link"
  ]
  df_copy = df_copy[final_columns]

  return df_copy

# --- Função para limpar o texto de uma notícia ---
def clean_text(text: str) -> str:
  if not isinstance(text, str):
      return ""
  text = unescape(text)  # Converte entidades HTML (&amp; -> &)
  text = re.sub(r'http\S+|www\.\S+', '', text)  # Remove URLs simples
  text = re.sub(  # Remove links mais complexos (https, .com, .gov etc)
    r'\b(?:https?://|www\.)\S+|(?:\S+\.(?:com|org|net|gov|gov\.br|edu|edu\.br))\b', 
    '', 
    text, 
    flags=re.IGNORECASE
  )
  text = re.sub(r'<.*?>', '', text)  # Remove tags HTML
  text = re.sub(r'\s+', ' ', text).strip()  # Remove espaços extras
  return text



# --- Lista de stopwords em português ---
STOPWORDS_PT = {
  "a", "o", "as", "os", "um", "uma", "uns", "umas",
  "de", "do", "da", "dos", "das",
  "em", "no", "na", "nos", "nas",
  "e", "que", "que", "por", "com", "para", "se", "ao", "à",
  "mais", "não", "ou", "como", "já", "são", "foi", "ser", "uso" 
}

# --- Função para extrair palavras relevantes de uma coluna do DataFrame ---
def extract_words(df: pd.DataFrame, column: str = "Descrição") -> list:
  all_text = " ".join(df[column].dropna().tolist()).lower()  # Junta todas as descrições em um texto só
  all_text = re.sub(r'[^a-záéíóúâêôãõç\s]', '', all_text)  # Remove caracteres especiais
  words = all_text.split()  # Quebra em palavras
  # Remove stopwords e palavras curtas (<=2 caracteres)
  words = [word for word in words if word not in STOPWORDS_PT and len(word) > 2]
  return words

# --- Função para contar a frequência de cada palavra ---
def get_word_frequencies(words: list) -> dict:
  return dict(Counter(words))
