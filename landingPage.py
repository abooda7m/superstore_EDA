import streamlit as st

st.set_page_config(
    page_title="Superstore EDA | Sales Analytics",
    page_icon="🛒",
    layout="centered"
)

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#4CAF50;'>Welcome to Superstore EDA</h1>
        <h3>An Interactive Exploratory Data Analysis Dashboard</h3>
        <p style='max-width: 600px; margin: auto; font-size: 18px; color: gray;'>
            This platform allows you to explore historical sales data, uncover customer insights, analyze financial trends, and generate smart business recommendations — all in one interactive dashboard.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Launch Dashboard"):
        st.switch_page("pages/home.py")
