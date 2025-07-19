import streamlit as st
import pandas as pd
from data.load_data import load_data
from filters.sidebar_filters import apply_filters

from tabs import (
    business_overview,
    financial_analysis,
    customer_analysis,
    recommendations,
)
from tabs.prediction import sales_prediction

st.set_page_config(page_title=" Superstore Sales Dashboard", layout="wide")
st.title(" Superstore Sales Performance Dashboard")

df, cleaning_log_df = load_data()

df_filtered = apply_filters(df)

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    " Business Overview",              # tab0
    " Financial Analysis",             # tab1
    " Customer Analysis",              # tab2
    " Smart Business Recommendations", # tab3
    " Sales Forecasting",              # tab4
])

with tab0:
    business_overview.render(df_filtered)

with tab1:
    financial_analysis.render(df_filtered)

with tab2:
    customer_analysis.render(df_filtered , cleaning_log_df)

with tab3:
    recommendations.render(df_filtered)

with tab4:
    sales_prediction.render(df_filtered)

