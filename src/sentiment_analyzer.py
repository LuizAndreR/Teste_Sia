import pandas as pd
import re
import json

# --- Função para carregar as palavras positivas e negativas a partir do JSON ---
def open_json():
    global PALAVRAS_POSITIVAS, PALAVRAS_NEGATIVAS
    with open("words_feeling.json", "r", encoding="utf-8") as f:
        palavras = json.load(f)

    PALAVRAS_POSITIVAS = set(palavras["positivas"])  # Lista de palavras positivas
    PALAVRAS_NEGATIVAS = set(palavras["negativas"])  # Lista de palavras negativas

# --- Função para limpar e transformar o texto em tokens (lista de palavras) ---
def clean_and_text(text: str) -> list:
    if not isinstance(text, str):
        return []
    text = text.lower()  # Deixa tudo minúsculo
    text = re.sub(r'[^a-záéíóúâêôãõç\s]', '', text)  # Remove caracteres especiais
    text = text.split()  # Divide em palavras
    return text

# --- Função para classificar sentimento com base nas contagens ---
def classify_sentiment(pos_count: int, neg_count: int) -> str:
    if pos_count > neg_count:
        return "Positivo"
    elif neg_count > pos_count:
        return "Negativo"
    else:
        return "Neutro"

# --- Função principal de análise de sentimento ---
def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    
    df_copy = df.copy()  # Trabalha em uma cópia

    # Cria coluna auxiliar juntando título + descrição para análise
    df_copy['Texto completo'] = df_copy['Titulo'].fillna('') + ". " + df_copy['Descrição'].fillna('')

    sentimentos = []  # Lista para armazenar os resultados

    open_json()  # Carrega palavras positivas e negativas

    # Percorre cada notícia
    for text in df_copy['Texto completo']:  
        tokens = clean_and_text(text)  # Limpa e quebra o texto em palavras
        pos_count = sum(1 for word in tokens if word in PALAVRAS_POSITIVAS)  # Conta palavras positivas
        neg_count = sum(1 for word in tokens if word in PALAVRAS_NEGATIVAS)  # Conta palavras negativas

        sentimentos.append(classify_sentiment(pos_count, neg_count))  # Classifica

    # Adiciona coluna final de sentimento
    df_copy['Sentimento'] = sentimentos

    # Remove coluna auxiliar
    df_copy.drop(columns=['Texto completo'], inplace=True)

    # Gera resumo (quantidade de cada tipo de sentimento)
    resumo = df_copy['Sentimento'].value_counts().reset_index()
    resumo.columns = ['Sentimento', 'Quantidade']

    return df_copy, resumo
