import streamlit as st
import pandas as pd
import plotly.express as px

def render(df_filtered):
    st.title(" Financial Analysis")

    # Display key financial metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
    col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.2f}")
    col3.metric("Total Orders", df_filtered['Order ID'].nunique())
    col4.metric("Avg. Profit per Order", f"${(df_filtered['Profit'].sum() / df_filtered['Order ID'].nunique()):,.2f}")

    st.markdown("---")
    st.subheader(" Monthly Sales and Profit Trend")

    # Convert order dates and group by month-end
    df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
    monthly = df_filtered.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales", "Profit"]].sum().reset_index()
    monthly["Month"] = monthly["Order Date"].dt.strftime("%Y-%m")

    # Line chart of monthly sales and profit
    st.line_chart(monthly.set_index("Month")[["Sales", "Profit"]])

    st.markdown("---")
    st.subheader("Profit by Sub Category")

    # Bar chart: Total profit per sub-category
    profit_by_sub = df_filtered.groupby("Sub-Category")["Profit"].sum().sort_values()
    st.bar_chart(profit_by_sub)


    st.markdown("---")
    st.subheader("Top 10 Sub-Categories by Sales")

    # Bar chart: Top 10 sub-categories by total sales
    top_sub = df_filtered.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_sub)

    st.subheader("Monthly Sales Trend")

    # Line chart: Monthly sales (alternative view)
    monthly_sales = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)
    st.line_chart(monthly_sales)

    st.subheader("Heatmap: Region × Category (Interactive)")

    # Create heatmap of sales by region and category
    heatmap_data = df_filtered.pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum", fill_value=0).reset_index()
    melted = heatmap_data.melt(id_vars="Region", var_name="Category", value_name="Sales")

    fig = px.density_heatmap(
        melted,
        x="Category",
        y="Region",
        z="Sales",
        color_continuous_scale="Blues",
        text_auto=True,
        title="Sales Heatmap by Region and Category"
    )
    st.plotly_chart(fig, use_container_width=True, key="region_category_heatmap")

    st.markdown("---")
    st.subheader("Low-Profit Products (Below 5 SAR)")

    # Identify products with total profit below threshold
    low_profit_products = df_filtered[df_filtered["Profit"] < 5]
    if not low_profit_products.empty:
        top_low = (
            low_profit_products
            .groupby("Product Name")["Profit"]
            .sum()
            .sort_values()
            .head(5)
        )
        st.info("These products have very low profit (less than 5 USD):")
        st.table(top_low.reset_index().rename(columns={"Profit": "Total Profit"}).style.format({"Total Profit": "${:,.2f}"}))
    else:
        st.success("Great! All products are above the low-profit threshold")
