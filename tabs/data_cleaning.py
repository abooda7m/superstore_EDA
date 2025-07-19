import streamlit as st
import pandas as pd
import io

def render(df, cleaning_log_df):
    st.header("🧹 Data Cleaning Overview")




    # --- 1️⃣ Dataset Summary Table ---
    st.subheader("📄 Dataset Info")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum(),
        "Data Type": df.dtypes,
        "Missing": df.isnull().sum(),
        "% Missing": (df.isnull().mean() * 100).round(2)
    }).reset_index(drop=True)

    st.dataframe(info_df, use_container_width=True)

    
    
    
    
    
    

    # --- 2️⃣ df.describe() ---
    st.subheader("📊 Descriptive Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    # --- 3️⃣ Cleaning Summary ---
    st.subheader("🧾 Cleaning Summary")

    dropped_rows = cleaning_log_df["__Action__"].str.contains("Dropped", na=False).sum()
    imputed_rows = len(cleaning_log_df) - dropped_rows

    st.markdown(f"""
        - ✅ **Total rows after cleaning:** `{len(df):,}`
        - ❌ **Dropped rows (missing critical fields):** `{dropped_rows}`
        - 🩹 **Imputed rows (missing non-critical values):** `{imputed_rows}`
    """)

    # --- 4️⃣ Detailed Log ---
    st.subheader("📝 Cleaning Log")
    if not cleaning_log_df.empty:
        # Drop derived columns just for cleaner view
        log_view = cleaning_log_df.drop(columns=["Profit", "Shipping Duration"], errors="ignore")
        st.dataframe(log_view, use_container_width=True)
        st.caption("This log shows rows that were either dropped or had missing values imputed.")
    else:
        st.success("No rows were modified or dropped.")
