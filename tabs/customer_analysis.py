import streamlit as st
import pandas as pd

def render(df_filtered , cleaning_log):
    st.subheader(" Customer Insights")

    total_customers = df_filtered["Customer Name"].nunique()
    avg_sales_per_customer = df_filtered.groupby("Customer Name")["Sales"].sum().mean()
    col1, col2 = st.columns(2)
    col1.metric("Total Customers", total_customers)
    col2.metric("Avg Sales per Customer", f"${avg_sales_per_customer:,.2f}")

    st.subheader("Top 10 Customers by Sales")
    top_customers = df_filtered.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_customers)

    st.subheader(" Customer Sales Trend Over Time")
    sales_over_time = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum()
    sales_over_time.index = sales_over_time.index.astype(str)
    st.line_chart(sales_over_time)

    st.subheader(" Sales by Customer Segment")
    seg = df_filtered.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
    st.bar_chart(seg)

    st.subheader(" Top 5 Customers (Names + Total Sales)")
    top_5_customers = (
        df_filtered.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.table(top_5_customers.style.format({"Sales": "${:,.2f}"}))
    
