# DECISIONS

## 1. Por que escolhemos a abordagem de regras para análise de sentimento?
Optado por uma abordagem baseada em regras, utilizando listas de palavras positivas e negativas, porque:
- É simples e rápida de implementar para um projeto inicial.
- Não exige treinamento de modelos nem grandes volumes de dados.
- Permite explicabilidade completa de como cada notícia é classificada.

## 2. Como lidamos com possíveis erros ou falta de notícias no feed RSS?
- Tratamento de exceções foi implementado durante a coleta do feed RSS (usando `requests` e `feedparser`).
- Mensagens de erro amigáveis são exibidas no dashboard caso o feed esteja indisponível ou não haja notícias.
- A execução é interrompida de forma segura para evitar resultados inconsistentes.

## 3. Por que escolhemos Streamlit para o dashboard?
- Streamlit permite criar dashboards interativos de forma rápida e simples.
- Suporta integração com gráficos do Plotly e visualizações como Nuvem de Palavras.
- Facilita a inclusão de filtros e seletores diretamente na interface.

## 4. Como organizamos e processamos os dados?
- As notícias são processadas para limpar texto, remover links e tags HTML.
- Colunas relevantes são renomeadas e datas convertidas para datetime.
- A classificação de sentimentos é adicionada e resumos são gerados para gráficos.

## 5. Como tratamos visualizações e interatividade?
- Filtros de data e sentimento permitem que o usuário selecione o conjunto de notícias desejado.
- A tabela de notícias pode ser ordenada por data ou sentimento.
- Gráficos incluem: Nuvem de Palavras, Pizza de Sentimentos e Linha de notícias por mês.

## 6. Quais partes do código tiveram auxílio de IA?
- Comentários detalhados explicando cada função.
- Organização, classificação de dados e layout do dashboard.
- Algumas sugestões de design e estrutura do código.
- Algumas duvidas sobre o uso correto de bibliotecas 
