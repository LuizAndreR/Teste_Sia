import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

from src import fetcher
from src import processor
from src import sentiment_analyzer

# Configurações iniciais do app
st.set_page_config(page_title="Analisador de Notícias", layout="wide")
st.title("Analisador de Notícias sobre Inteligência Artificial no Piauí")

# --- Sidebar: configuração de busca ---
st.sidebar.header("Configurações de Busca")
# Slider para escolher o número de notícias que serão buscadas
num_news = st.sidebar.slider("Número de notícias", min_value=5, max_value=50, value=15, step=5)

# --- Coleta de notícias ---
try:
  df_raw = fetcher.fetch_news(limit=num_news)  # Busca notícias via função fetcher
except Exception as e:
  st.error(f"Erro ao buscar notícias: {e}")
  st.stop()

# --- Processamento das notícias ---
try:
  df_processed = processor.process_news_dataframe(df_raw)  # Limpa e organiza as notícias
except Exception as e:
  st.warning(f"Nenhuma notícia válida: {e}")
  st.stop()

# --- Análise de sentimento ---
df_sentiment, sentiment_summary = sentiment_analyzer.analyze_sentiment(df_processed)

# Converte a coluna de data para datetime
df_sentiment["Data de Publicação"] = pd.to_datetime(df_sentiment["Data de Publicação"])

# --- Filtros de visualização ---
st.subheader("Filtros de visualização")
col_date_start, col_date_end, col_sentiment = st.columns(3)

# Filtro de datas
with col_date_start:
  start_date = st.date_input("Data inicial", df_sentiment["Data de Publicação"].min().date())
with col_date_end:
  end_date = st.date_input("Data final", df_sentiment["Data de Publicação"].max().date())

# Filtro de sentimentos
with col_sentiment:
  selected_sentiments = st.multiselect(
    "Sentimento",
    options=["Positivo", "Negativo", "Neutro"],
    default=["Positivo", "Negativo", "Neutro"]
  )

# Aplica os filtros de data e sentimento
df_filtered = df_sentiment[
  (df_sentiment["Data de Publicação"].dt.date >= start_date) &
  (df_sentiment["Data de Publicação"].dt.date <= end_date) &
  (df_sentiment["Sentimento"].isin(selected_sentiments))
]

# --- Tabela de Notícias ---
st.subheader("Tabela de Notícias")

# Opções de ordenação
available_cols = df_filtered.columns.tolist()
sort_options = {}

if "Data de Publicação" in available_cols:
  sort_options["Data de Publicação (mais recente)"] = ("Data de Publicação", False)
  sort_options["Data de Publicação (mais antiga)"] = ("Data de Publicação", True)

if "Titulo" in available_cols:  # Ajuste se o nome da coluna for diferente
  sort_options["Título (A-Z)"] = ("Titulo", True)
  sort_options["Título (Z-A)"] = ("Titulo", False)

# Aplica ordenação escolhida
if sort_options:
  sort_choice = st.selectbox("Ordenar por:", list(sort_options.keys()))
  sort_col, ascending = sort_options[sort_choice]
  df_filtered_sorted = df_filtered.sort_values(by=sort_col, ascending=ascending)
  st.dataframe(df_filtered_sorted)
else:
  st.dataframe(df_filtered)

# --- Visualizações ---
st.subheader("Visualizações")
col1, col2 = st.columns([2, 1])

# --- Nuvem de Palavras ---
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

# --- Gráfico de Pizza (Distribuição de Sentimentos) ---
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

# --- Gráfico de Linha (Quantidade de Notícias por Mês) ---
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

# --- Rodapé com aviso sobre limitações e uso de IA ---
st.markdown("---")  # Linha separadora
st.markdown(

  """"
  <div style="font-size:15px; color:white;">
  ⚠️ Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos.<br>
  ℹ️ Alguns códigos, como os comentários detalhados explicando cada função, organização e classificação dos dados e o design do dashboard, foram desenvolvidos com auxílio de modelos de IA.
  </div>
  """,

  unsafe_allow_html=True
)
