# Dashboard de Análise de Notícias sobre Inteligência Artificial no Piauí

Este projeto é um **dashboard interativo** desenvolvido com **Streamlit**, que coleta, processa e analisa notícias relacionadas à Inteligência Artificial no estado do Piauí.  
O sistema realiza **classificação de sentimento**, gera **nuvens de palavras**, gráficos de **distribuição de sentimentos** e **tendência de publicações por mês**.  

---

## Tecnologias Utilizadas
- [Python 3.12+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [Pandas](https://pandas.pydata.org/)  
- [Matplotlib](https://matplotlib.org/)  
- [Plotly](https://plotly.com/python/)  
- [WordCloud](https://github.com/amueller/word_cloud)  

---

## Pré-requisitos
Antes de começar, certifique-se de ter instalado:
- **Python 3.12 ou superior**
- **pip** (gerenciador de pacotes do Python)
- **virtualenv** (recomendado)

---

## Estrutura do Projeto
```bash
  Teste_Sia/
  ├── app.py                  # Dashboard principal (Streamlit)
  ├── requirements.txt        # Lista de dependências do projeto
  ├── src/
  │   ├── fetcher.py          # Módulo de busca de notícias
  │   ├── processor.py        # Processamento e limpeza dos textos
  │   └── sentiment_analyzer.py  # Análise de sentimentos
  └── README.md
```

---

## Funcionalidades

- 🔎 Busca automática de notícias sobre IA no Piauí  
- 📅 Filtros por data e sentimento  
- 📊 Gráfico de pizza com distribuição de sentimentos  
- ☁️ Nuvem de palavras gerada a partir das notícias processadas  
- 📈 Gráfico de linha mostrando o número de notícias publicadas por mês  
- 📑 Tabela interativa com as notícias classificadas  

---

## Setup e Execução do Projeto
1. Clone o repositório:

```bash
  git clone https://github.com/LuizAndreR/Teste_Sia.git
```

2. Entre na pasta do projeto:
```bash
  cd Teste_Sia
```

3. Crie um ambiente virtual:
```bash
  python -m venv venv
```

4. Ative o ambiente virtual:

  Windows:
  ```bash
    venv\Scripts\activate
  ```

  Linux/macOS:
  ```bash
    source venv/bin/activate
  ```

5. Instale as dependências:
```bash
  pip install -r requirements.txt
```

6. Execute o dashboard:

```bash
  streamlit run app.py
```

7. O dashboard estará disponível em:

```bash
  http://localhost:8501
```

