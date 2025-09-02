import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

from src import fetcher
from src import processor
from src import sentiment_analyzer

st.set_page_config(page_title="Dashboard AI Piauí", layout="wide")
st.title("Dashboard: Notícias sobre Inteligência Artificial no Piauí")

# --- Passo 1: Coletar notícias ---
st.sidebar.header("Configurações")
num_news = st.sidebar.slider("Número de notícias", min_value=5, max_value=50, value=15, step=5)

try:
    df_raw = fetcher.fetch_news(limit=num_news)
except Exception as e:
    st.error(f"Erro ao buscar notícias: {e}")
    st.stop()

# --- Passo 2: Processar notícias ---
try:
    df_processed = processor.process_news_dataframe(df_raw)
except Exception as e:
    st.warning(f"Nenhuma notícia válida: {e}")
    st.stop()

# --- Passo 3: Analisar sentimento ---
df_sentiment, sentiment_summary = sentiment_analyzer.analyze_sentiment(df_processed)

# --- Passo 4: Exibir gráfico de pizza ---
st.subheader("Distribuição de Sentimentos")
fig_pie = px.pie(
    sentiment_summary, 
    names="Sentimento", 
    values="Quantidade",
    color="Sentimento", 
    color_discrete_map={"Positivo": "green", "Negativo": "red", "Neutro": "gray"}
)
st.plotly_chart(fig_pie, use_container_width=True)

# --- Passo 5: Nuvem de palavras ---
st.subheader("Nuvem de palavras")
# Usar função do processor que retorna lista limpa de palavras
words = processor.extract_words(df_processed)
frequencies = processor.get_word_frequencies(words)

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis"
).generate_from_frequencies(frequencies)

fig, ax = plt.subplots(figsize=(12,6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# --- Passo 6: Tabela interativa ---
st.subheader("Notícias Processadas e Classificadas")
st.dataframe(df_sentiment)

# --- Passo 7 (opcional): filtro por sentimento ---
st.subheader("Filtrar notícias por sentimento")
sentiment_filter = st.multiselect(
    "Selecione o(s) sentimento(s) para exibir:",
    options=["Positivo", "Negativo", "Neutro"],
    default=["Positivo", "Negativo", "Neutro"]
)

df_filtered = df_sentiment[df_sentiment["Sentimento"].isin(sentiment_filter)]
st.dataframe(df_filtered)