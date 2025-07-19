# Import necessary libraries and modules
import streamlit as st
import pandas as pd

# Import custom functions for loading data and applying sidebar filters
from data.load_data import load_data
from filters.sidebar_filters import apply_filters

# Import tab modules (each represents a section of the dashboard)
from tabs import (
    business_overview,
    financial_analysis,
    customer_analysis,
    recommendations,
    data_cleaning,
)
from tabs.prediction import sales_prediction

# Configure the Streamlit app page
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("Superstore Sales Performance Dashboard")

# Load the cleaned dataset and cleaning log
df, cleaning_log_df = load_data()

# Apply sidebar filters to the dataset (e.g., by region, category, date)
df_filtered = apply_filters(df)

# Define the main navigation tabs for the dashboard
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Business Overview",              # tab0: High-level KPIs and summary
    "Financial Analysis",             # tab1: Trends, margins, and profitability
    "Customer Analysis",              # tab2: Insights into customer behavior
    "Sales Forecasting",              # tab3: Future sales predictions (Prophet)
    "Smart Business Recommendations", # tab4: AI-driven suggestions and insights
    "Data Cleaning Overview"          # tab5: Data quality and processing log
])

# Render each tab by calling the appropriate function
with tab0:
    business_overview.render(df_filtered)

with tab1:
    financial_analysis.render(df_filtered)

with tab2:
    customer_analysis.render(df_filtered, cleaning_log_df)

with tab3:
    sales_prediction.render(df_filtered)

with tab4:
    recommendations.render(df_filtered)

with tab5:
    data_cleaning.render(df_filtered, cleaning_log_df)
