import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def render(df_filtered):
    st.title(" Business Overview")

    # Executive KPIs summary section
    st.subheader(" Executive Summary")

    # Calculate high-level metrics
    total_sales = df_filtered["Sales"].sum()
    total_profit = df_filtered["Profit"].sum()
    total_orders = df_filtered["Order ID"].nunique()
    avg_shipping = df_filtered["Shipping Duration"].mean()
    avg_sale = df_filtered["Sales"].mean()
    max_sale = df_filtered["Sales"].max()

    # Prepare KPI values to be displayed
    kpis = [
        {"title": "Total Sales", "value": f"${total_sales:,.2f}"},
        {"title": "Total Profit (Est.)", "value": f"${total_profit:,.2f}"},
        {"title": "Total Orders", "value": total_orders},
        {"title": "Avg. Shipping Days", "value": f"{int(avg_shipping)} days"},
        {"title": "Average Sale", "value": f"${avg_sale:,.2f}"},
        {"title": "Max Sale", "value": f"${max_sale:,.2f}"},
    ]

    # Custom HTML to render KPIs in styled boxes
    html_kpis = """
    <style>
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .kpi-card {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 20px;
            height: 100px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .kpi-title {
            color: #ccc;
            font-size: 16px;
            margin-bottom: 8px;
        }
        .kpi-value {
            color: #4FC3F7;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    <div class="kpi-container">
    """

    # Loop over KPIs and generate HTML blocks
    for kpi in kpis:
        html_kpis += f"""
        <div class="kpi-card">
            <div class="kpi-title">{kpi['title']}</div>
            <div class="kpi-value">{kpi['value']}</div>
        </div>
        """

    html_kpis += "</div>"

    # Render the KPI HTML using Streamlit components
    components.html(html_kpis, height=400, scrolling=True)

    st.markdown("---")

    # Region-level sales summary
    st.subheader(" Sales by Region")
    st.bar_chart(df_filtered.groupby("Region")["Sales"].sum())

    # Category-level sales summary
    st.subheader(" Sales by Category")
    st.bar_chart(df_filtered.groupby("Category")["Sales"].sum())

    # Top 3 best-selling products
    st.markdown("### Top 3 Products by Sales")
    top_products = df_filtered.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(3)
    st.table(top_products.reset_index().rename(columns={"Sales": "Total Sales"}).style.format({"Total Sales": "${:,.2f}"}))

    # Bottom 3 worst-selling products
    st.markdown("### Bottom 3 Products by Sales")
    bottom_products = df_filtered.groupby("Product Name")["Sales"].sum().sort_values().head(3)
    st.table(bottom_products.reset_index().rename(columns={"Sales": "Total Sales"}).style.format({"Total Sales": "${:,.2f}"}))
