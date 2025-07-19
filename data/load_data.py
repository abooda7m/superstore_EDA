#pull the data, convert date columns, handle missing values, and derive new columns
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import os

@st.cache_data(ttl=900)
def load_data():
    #load data from CSV file 
    file_path = os.path.join(os.path.dirname(__file__), 'superstore_raw.csv')
    df_raw = pd.read_csv(file_path)
    #replace "None", "nan", None to NaN
    df_raw.replace(["None", "nan", None], np.nan, inplace=True)
    #convert to dateTime 
    df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"], errors='coerce')
    df_raw["Ship Date"] = pd.to_datetime(df_raw["Ship Date"], errors='coerce')
    df_raw["Sales"] = pd.to_numeric(df_raw["Sales"], errors="coerce")
    # clean data
    df_clean = df_raw.copy()
    
    logs = []
    critical = ["Sales", "Order Date"]
    dropped = df_clean[df_clean[critical].isna().any(axis=1)]
    if not dropped.empty:
        dropped["__Action__"] = "Dropped due to missing critical fields"
        logs.append(dropped)
    df_clean.dropna(subset=critical, inplace=True)

    for col in df_clean.columns:
        if df_clean[col].isna().sum() == 0:
            continue
        affected = df_clean[df_clean[col].isna()].copy()
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            value = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(value)
            affected["__Action__"] = f"Imputed Median: {value}"
        else:
            value = df_clean[col].mode().iloc[0]
            df_clean[col] = df_clean[col].fillna(value)
            affected["__Action__"] = f"Imputed Mode: '{value}'"
        logs.append(affected)

    df_clean["Shipping Duration"] = (df_clean["Ship Date"] - df_clean["Order Date"]).dt.days
    df_clean["Profit"] = df_clean["Sales"] * 0.3
    final_log = pd.concat(logs) if logs else pd.DataFrame()
    return df_clean, final_log
