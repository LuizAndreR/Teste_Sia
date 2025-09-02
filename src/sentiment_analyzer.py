import pandas as pd
import re
import json

def open_json():
  global PALAVRAS_POSITIVAS, PALAVRAS_NEGATIVAS
  with open("words_feeling.json", "r", encoding="utf-8") as f:
    palavras = json.load(f)

  PALAVRAS_POSITIVAS = set(palavras["positivas"])
  PALAVRAS_NEGATIVAS = set(palavras["negativas"])

def clean_and_text(text: str) -> list:
  if not isinstance(text, str):
    return []
  text = text.lower()
  text = re.sub(r'[^a-záéíóúâêôãõç\s]', '', text)
  text = text.split()
  return text

def classify_sentiment(pos_count: int, neg_count: int) -> str:
  if pos_count > neg_count:
    return "Positivo"
  elif neg_count > pos_count:
    return "Negativo"
  else:
    return "Neutro"

def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
  if df.empty:
    return df
  
  df_copy = df.copy()

  df_copy['Texto completo'] = df_copy['Titulo'].fillna('') + ". " + df_copy['Descrição'].fillna('')

  sentimentos = []

  open_json()

  for text in df_copy['Texto completo']:  
    tokens = clean_and_text(text)
    pos_count = sum(1 for word in tokens if word in PALAVRAS_POSITIVAS)
    neg_count = sum(1 for word in tokens if word in PALAVRAS_NEGATIVAS)

    sentimentos.append(classify_sentiment(pos_count, neg_count))

  # Mantém apenas a classificação final
  df_copy['Sentimento'] = sentimentos

  # Remove a coluna auxiliar
  df_copy.drop(columns=['Texto completo'], inplace=True)

  resumo = df_copy['Sentimento'].value_counts().reset_index()
  resumo.columns = ['Sentimento', 'Quantidade']

  return df_copy, resumo
