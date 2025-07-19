import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

def render(df):
    st.header(" Sales Forecasting")

    if 'Order Date' not in df.columns or 'Sales' not in df.columns:
        st.warning("Data must contain 'Order Date' and 'Sales' columns.")
        return

    # Sidebar filters
    st.sidebar.markdown("###  Filter Forecast by")
    region = st.sidebar.selectbox("Region", options=["All"] + sorted(df['Region'].dropna().unique().tolist()))
    category = st.sidebar.selectbox("Category", options=["All"] + sorted(df['Category'].dropna().unique().tolist()))
    future_months = st.sidebar.slider("📆 Months to Predict", min_value=1, max_value=12, value=3)

    # Apply filters
    df_filtered = df.copy()
    if region != "All":
        df_filtered = df_filtered[df_filtered["Region"] == region]
    if category != "All":
        df_filtered = df_filtered[df_filtered["Category"] == category]

    if df_filtered.shape[0] < 10:
        st.warning(" Not enough data points after filtering. Please adjust the filters.")
        return

    # Prepare monthly sales data
    df_filtered['Order Date'] = pd.to_datetime(df_filtered['Order Date'])
    monthly_df = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_df['Order Date'] = monthly_df['Order Date'].dt.to_timestamp()
    monthly_df = monthly_df.sort_values('Order Date')

    prophet_df = monthly_df.rename(columns={"Order Date": "ds", "Sales": "y"})
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=future_months, freq='MS')
    forecast = model.predict(future)

    # Plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prophet_df['ds'], y=prophet_df['y'], name='Actual Sales', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast', mode='lines', line=dict(dash='dash')))
    fig.update_layout(title=' Monthly Sales Forecast (Prophet)', xaxis_title='Date', yaxis_title='Sales')

    st.plotly_chart(fig, use_container_width=True)

    # Forecast Table
    forecast_df = forecast[['ds', 'yhat']].tail(future_months)
    forecast_df.rename(columns={"ds": "Date", "yhat": "Predicted Sales"}, inplace=True)

    st.markdown("###  Forecast Table")
    st.dataframe(forecast_df)

    csv = forecast_df.to_csv(index=False).encode()
    st.download_button("⬇ Download Forecast as CSV", data=csv, file_name='forecast.csv', mime='text/csv')
