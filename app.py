import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

from src import fetcher
from src import processor
from src import sentiment_analyzer

st.set_page_config(page_title="Analisador de Notícias", layout="wide")
st.title("Analisador de Notícias sobre Inteligência Artificial no Piauí")

st.sidebar.header("Configurações de Busca")
num_news = st.sidebar.slider("Número de notícias", min_value=5, max_value=50, value=15, step=5)

try:
  df_raw = fetcher.fetch_news(limit=num_news)
except Exception as e:
  st.error(f"Erro ao buscar notícias: {e}")
  st.stop()

try:
  df_processed = processor.process_news_dataframe(df_raw)
except Exception as e:
  st.warning(f"Nenhuma notícia válida: {e}")
  st.stop()

df_sentiment, sentiment_summary = sentiment_analyzer.analyze_sentiment(df_processed)

# Converter coluna de data para datetime
df_sentiment["Data de Publicação"] = pd.to_datetime(df_sentiment["Data de Publicação"])

st.subheader("Filtros de visualização")
col_date_start, col_date_end, col_sentiment = st.columns(3)

with col_date_start:
  start_date = st.date_input(
    "Data inicial", df_sentiment["Data de Publicação"].min().date()
  )
with col_date_end:
  end_date = st.date_input(
    "Data final", df_sentiment["Data de Publicação"].max().date()
  )
with col_sentiment:
  selected_sentiments = st.multiselect(
    "Sentimento",
    options=["Positivo", "Negativo", "Neutro"],
    default=["Positivo", "Negativo", "Neutro"]
  )

# Filtrar usando .dt.date
df_filtered = df_sentiment[
  (df_sentiment["Data de Publicação"].dt.date >= start_date) &
  (df_sentiment["Data de Publicação"].dt.date <= end_date) &
  (df_sentiment["Sentimento"].isin(selected_sentiments))
]

st.subheader("Tabela de Notícias")
st.dataframe(df_filtered)

st.subheader("Visualizações")
col1, col2 = st.columns([2, 1])

with col1:
  st.write("Nuvem de Palavras")
  words = processor.extract_words(df_filtered)
  frequencies = processor.get_word_frequencies(words)
  if frequencies:
    wordcloud = WordCloud(
      width=800, height=400, background_color="white", colormap="viridis"
    ).generate_from_frequencies(frequencies)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
  else:
    st.write("Sem palavras para exibir.")

with col2:
  st.write("Distribuição de Sentimentos")
  if not df_filtered.empty:
    summary_filtered = df_filtered["Sentimento"].value_counts().reset_index()
    summary_filtered.columns = ["Sentimento", "Quantidade"]
    fig_pie = px.pie(
      summary_filtered,
      names="Sentimento",
      values="Quantidade",
      color="Sentimento",
      color_discrete_map={"Positivo": "green", "Negativo": "red", "Neutro": "gray"},
      title="Sentimentos das Notícias"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
  else:
    st.write("Sem dados para exibir.")

df_filtered["AnoMes"] = df_filtered["Data de Publicação"].dt.to_period("M").astype(str)
df_monthly = df_filtered.groupby("AnoMes").size().reset_index(name="Quantidade")

fig_line = px.line(
  df_monthly,
  x="AnoMes",
  y="Quantidade",
  title="Quantidade de Notícias por Mês",
  markers=True
)

fig_line.update_layout(
  xaxis_title="Mês", 
  yaxis_title="Quantidade de Notícias"
)

st.plotly_chart(fig_line, use_container_width=True)
