import pandas as pd
import re

import fetcher

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_news_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    
    df_copy = df.copy()

    rename_map = {
        "title": "Título",
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
        "Título",
        "Descrição",
        "Link"
    ]

    df_copy = df_copy[final_columns]

    return df_copy