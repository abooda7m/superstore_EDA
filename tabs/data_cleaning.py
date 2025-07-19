import streamlit as st
import pandas as pd
import io

def render(df, cleaning_log_df):
    # Set the title of the page
    st.header("🧹 Data Cleaning Overview")

    # 1️⃣ Show dataset structure and missing values in a summary table
    st.subheader("📄 Dataset Info")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum(),
        "Data Type": df.dtypes,
        "Missing": df.isnull().sum(),
        "% Missing": (df.isnull().mean() * 100).round(2)
    }).reset_index(drop=True)

    st.dataframe(info_df, use_container_width=True)

    # 2️⃣ Show statistical summary of numeric columns
    st.subheader("📊 Descriptive Statistics")
    st.dataframe(df.describe(include="number"), use_container_width=True)

    # 3️⃣ Display the number of dropped and imputed rows
    st.subheader("🧾 Cleaning Summary")

    if "__Action__" in cleaning_log_df.columns:
        # Count dropped rows (due to missing critical values)
        dropped_rows = cleaning_log_df["__Action__"].str.contains("Dropped", na=False).sum()
        # Count imputed rows (total cleaned rows minus dropped)
        imputed_rows = len(cleaning_log_df) - dropped_rows
    else:
        dropped_rows = 0
        imputed_rows = 0

    st.markdown(f"""
        - ✅ **Total rows after cleaning:** `{len(df):,}`
        - ❌ **Dropped rows (missing critical fields):** `{dropped_rows}`
        - 🩹 **Imputed rows (missing non-critical values):** `{imputed_rows}`
    """)

    # 4️⃣ Show detailed cleaning log
    st.subheader("📝 Cleaning Log")

    if not cleaning_log_df.empty:
        log_view = cleaning_log_df.drop(columns=["Profit", "Shipping Duration"], errors="ignore")
        st.dataframe(log_view, use_container_width=True)
        st.caption("This log shows rows that were either dropped or had missing values imputed.")
    else:
        st.success("No rows were modified or dropped.")
