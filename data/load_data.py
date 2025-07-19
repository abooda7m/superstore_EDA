# load_data.py

import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import os

@st.cache_data(ttl=900)
def load_data():
    # Load data from CSV file 
    file_path = os.path.join(os.path.dirname(__file__), 'superstore_sales.csv')
    df_raw = pd.read_csv(file_path)

    # Replace "None", "nan", None with np.nan
    df_raw.replace(["None", "nan", None], np.nan, inplace=True)

    # Convert columns to proper formats
    df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"], errors='coerce', dayfirst=True)
    df_raw["Ship Date"] = pd.to_datetime(df_raw["Ship Date"], errors='coerce', dayfirst=True)

    df_raw["Sales"] = pd.to_numeric(df_raw["Sales"], errors="coerce")

    # Copy raw data for cleaning
    df_clean = df_raw.copy()
    logs = []

    # 🔴 Drop rows with missing Sales ONLY
    critical = ["Sales"]
    dropped = df_clean[df_clean[critical].isna().any(axis=1)]
    if not dropped.empty:
        dropped["__Action__"] = "Dropped due to missing Sales"
        logs.append(dropped)
    df_clean.dropna(subset=critical, inplace=True)

    # 🩹 Impute missing Order Date using Ship Date - 2 days
    mask_missing_order = df_clean["Order Date"].isna() & df_clean["Ship Date"].notna()
    df_clean.loc[mask_missing_order, "Order Date"] = df_clean["Ship Date"] - pd.Timedelta(days=2)
    if mask_missing_order.sum() > 0:
        affected = df_clean[mask_missing_order].copy()
        affected["__Action__"] = "Order Date Imputed: Ship Date - 2 days"
        logs.append(affected)

    # Impute other missing values (non-critical)
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

    # Derive new columns
    df_clean["Shipping Duration"] = (df_clean["Ship Date"] - df_clean["Order Date"]).dt.days
    df_clean["Profit"] = df_clean["Sales"] * 0.3

    final_log = pd.concat(logs) if logs else pd.DataFrame()
    return df_clean, final_log
