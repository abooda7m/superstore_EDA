import streamlit as st
from sklearn.linear_model import LinearRegression
import pandas as pd

def render(df_filtered):
    st.subheader(" Smart Business Recommendations")

    low_sales_product = df_filtered[df_filtered["Region"] == "West"].groupby("Product Name")["Sales"].sum().sort_values().head(1)
    top_category = df_filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False).idxmax()
    product_sales = df_filtered.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
    product_cumsum = product_sales.cumsum() / product_sales.sum()
    pareto_cut = product_cumsum[product_cumsum <= 0.8]
    top_customers = df_filtered.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(2).index.tolist()

    monthly_sales = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
    monthly_sales["Order Date"] = pd.to_datetime(monthly_sales["Order Date"])
    monthly_sales["Month_Num"] = range(len(monthly_sales))

    model = LinearRegression()
    model.fit(monthly_sales[["Month_Num"]], monthly_sales[["Sales"]])
    next_month_df = pd.DataFrame({"Month_Num": [monthly_sales["Month_Num"].max() + 1]})
    prediction = model.predict(next_month_df)[0][0]

    st.markdown("###  Key Insights for Management")
    if not low_sales_product.empty:
        st.write(f"📉 Product with lowest sales in West: `{low_sales_product.index[0]}` (${low_sales_product.values[0]:,.2f})")
    else:
        st.warning(" No sales data for the West region with current filters.")
    st.write(f"Top performing category: `{top_category}`")
    st.write(f"Pareto Principle: {len(pareto_cut)} products contribute to 80% of revenue")
    st.write(f"Top customers: {', '.join(top_customers)}")
    st.write(f"Predicted sales next month: **${prediction:,.2f}**")

    st.success("Use these insights to adjust inventory, target top customers, and improve regional strategies.")

    st.markdown("###  Auto-Marketing Suggestions")
    df_filtered["Month"] = df_filtered["Order Date"].dt.to_period("M")
    trend = df_filtered.groupby(["Month", "Category"])["Sales"].sum().unstack().fillna(0)

    last_month = df_filtered["Order Date"].max().to_period("M")
    prev_month = (df_filtered["Order Date"].max() - pd.DateOffset(months=1)).to_period("M")

    if last_month in trend.index and prev_month in trend.index:
        st.info(" Category Growth (Last Month vs Previous):")
        
        def safe_growth(curr, prev):
            if prev == 0 and curr == 0:
                return 0
            elif prev == 0:
                return None  # Unknown or infinity
            else:
                return ((curr - prev) / prev) * 100

        for cat in trend.columns:
            curr_val = trend.loc[last_month, cat]
            prev_val = trend.loc[prev_month, cat]
            change = safe_growth(curr_val, prev_val)
            
            if change is None:
                st.info(f" Cannot calculate growth for `{cat}` – No sales in previous month.")
            elif change > 5:
                st.success(f"📈 Increase in `{cat}`: {change:.2f}% – Consider boosting ads or upselling!")
            elif change < -5:
                st.warning(f"📉 Drop in `{cat}`: {change:.2f}% – Consider discount campaigns or stock review.")
            else:
                st.info(f" Stable performance in `{cat}`: {change:.2f}%")
