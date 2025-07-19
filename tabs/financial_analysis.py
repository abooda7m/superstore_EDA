import streamlit as st
import pandas as pd
import plotly.express as px

def render(df_filtered):
    st.title(" Financial Analysis")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
    col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.2f}")
    col3.metric("Total Orders", df_filtered['Order ID'].nunique())
    col4.metric("Avg. Profit per Order", f"${(df_filtered['Profit'].sum() / df_filtered['Order ID'].nunique()):,.2f}")

    st.markdown("---")
    st.subheader(" Monthly Sales and Profit Trend")

    df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
    monthly = df_filtered.groupby(pd.Grouper(key="Order Date", freq="ME"))[["Sales", "Profit"]].sum().reset_index()
    monthly["Month"] = monthly["Order Date"].dt.strftime("%Y-%m")

    st.line_chart(monthly.set_index("Month")[["Sales", "Profit"]])

    st.markdown("---")
    st.subheader("Profit by Sub Category")

    profit_by_sub = df_filtered.groupby("Sub-Category")["Profit"].sum().sort_values()
    st.bar_chart(profit_by_sub)

    st.markdown("---")
    st.subheader("Profit Margin by Category")

    category_data = df_filtered.groupby("Category")[["Sales", "Profit"]].sum()
    category_data["Profit Margin (%)"] = (category_data["Profit"] / category_data["Sales"]) * 100
    st.dataframe(category_data.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Profit Margin (%)": "{:.2f}%"}))

    st.markdown("---")
    st.subheader("Top 10 Sub-Categories by Sales")
    top_sub = df_filtered.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_sub)

    st.subheader("Monthly Sales Trend")
    monthly_sales = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)
    st.line_chart(monthly_sales)

    st.subheader("Heatmap: Region × Category (Interactive)")
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
    st.subheader(" Loss-Making Products")
    loss_products = df_filtered[df_filtered["Profit"] < 0]
    if not loss_products.empty:
        top_losses = loss_products.groupby("Product Name")["Profit"].sum().sort_values().head(5)
        st.warning("These products generated losses:")
        st.table(top_losses.reset_index().rename(columns={"Profit": "Total Loss"}).style.format({"Total Loss": "${:,.2f}"}))
    else:
        st.success("No products with negative profit!")

    st.markdown("---")
    st.subheader("Low-Profit Products (Below 5 SAR)")
    low_profit_products = df_filtered[df_filtered["Profit"] < 5]
    if not low_profit_products.empty:
        top_low = (
            low_profit_products
            .groupby("Product Name")["Profit"]
            .sum()
            .sort_values()
            .head(5)
        )
        st.info("These products have very low profit (less than 5 SAR):")
        st.table(top_low.reset_index().rename(columns={"Profit": "Total Profit"}).style.format({"Total Profit": "${:,.2f}"}))
    else:
        st.success("Great! All products are above the low-profit threshold ")
