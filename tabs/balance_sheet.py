import streamlit as st
import pandas as pd

def render(df_filtered):
    st.title("📘 Balance Sheet")

    # حساب الأصول (Assets)
    cash = df_filtered["Sales"].sum() * 0.2  # نفترض 20% من المبيعات نقدية حالياً
    accounts_receivable = df_filtered["Sales"].sum() * 0.5  # 50% مبيعات لم تُستلم بعد
    inventory = df_filtered["Sales"].sum() * 0.3  # قيمة البضاعة المتبقية تمثل 30%

    assets = {
        "Cash": round(cash, 2),
        "Accounts Receivable": round(accounts_receivable, 2),
        "Inventory": round(inventory, 2)
    }

    # حساب الخصوم (Liabilities)
    accounts_payable = df_filtered["Sales"].sum() * 0.2  # التزامات قصيرة
    short_term_loans = 30000  # قرض افتراضي

    liabilities = {
        "Accounts Payable": round(accounts_payable, 2),
        "Short-Term Loans": short_term_loans
    }

    # حقوق الملكية (Equity)
    total_assets = sum(assets.values())
    total_liabilities = sum(liabilities.values())
    owner_equity = 50000  # رأس المال الأساسي
    retained_earnings = total_assets - total_liabilities - owner_equity

    equity = {
        "Owner's Equity": owner_equity,
        "Retained Earnings": round(retained_earnings, 2)
    }

    # عرض الأصول
    st.subheader("🏦 Assets")
    df_assets = pd.DataFrame(list(assets.items()), columns=["Asset", "Value (SAR)"])
    st.table(df_assets)

    # عرض الخصوم
    st.subheader("💳 Liabilities")
    df_liabilities = pd.DataFrame(list(liabilities.items()), columns=["Liability", "Value (SAR)"])
    st.table(df_liabilities)

    # عرض حقوق الملكية
    st.subheader("📈 Equity")
    df_equity = pd.DataFrame(list(equity.items()), columns=["Equity", "Value (SAR)"])
    st.table(df_equity)

    # التحقق من التوازن
    st.markdown("---")
    total_equity = sum(equity.values())

    st.metric("Total Assets", f"{total_assets:,.2f} SAR")
    st.metric("Total Liabilities + Equity", f"{total_liabilities + total_equity:,.2f} SAR")

    if round(total_assets, 2) == round(total_liabilities + total_equity, 2):
        st.success("✅ Balance Sheet is Balanced!")
    else:
        st.error("⚠️ Balance Sheet is NOT Balanced!")
