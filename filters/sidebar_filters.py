# This is filters/sidebar_filters.py

import streamlit as st
import pandas as pd

def apply_filters(df):
    st.sidebar.header("🔎 Filters")

    if "selected_region" not in st.session_state:
        st.session_state["selected_region"] = df["Region"].dropna().unique().tolist()
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = df["Category"].dropna().unique().tolist()
    if "date_range" not in st.session_state:
        st.session_state["date_range"] = [df["Order Date"].min(), df["Order Date"].max()]

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.clear()
        st.rerun()

    selected_region = st.sidebar.multiselect("Select Region", df["Region"].dropna().unique(), default=st.session_state["selected_region"])
    if len(selected_region) == 0:
        st.sidebar.warning("⚠️ You must select at least one Region.")
        selected_region = st.session_state["selected_region"]
    else:
        st.session_state["selected_region"] = selected_region

    selected_category = st.sidebar.multiselect("Select Category", df["Category"].dropna().unique(), default=st.session_state["selected_category"])
    if len(selected_category) == 0:
        st.sidebar.warning("⚠️ You must select at least one Category.")
        selected_category = st.session_state["selected_category"]
    else:
        st.session_state["selected_category"] = selected_category

    date_range = st.sidebar.date_input("Select Date Range", value=st.session_state["date_range"])
    st.session_state["date_range"] = date_range

    return df[
        (df["Region"].isin(selected_region)) &
        (df["Category"].isin(selected_category)) &
        (df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]

