# 📊 Superstore Sales Performance Dashboard

This interactive business intelligence dashboard provides a comprehensive analysis of Superstore sales data using **Streamlit**, **Plotly**, and **Prophet**.  
It empowers decision-makers with key metrics, visualizations, and AI-driven recommendations.

---

## 🚀 Features

- ✅ **Business Overview**: KPIs, category/region analysis, top/bottom product insights  
- 💰 **Financial Analysis**: Sales & profit trends, profit margins, low-profit products  
- 👥 **Customer Analysis**: Top customers, sales trends by segment, average sales per customer  
- 📈 **Sales Forecasting**: Future sales prediction using Prophet  
- 💡 **Smart Business Recommendations**: Automated strategic suggestions using business rules  
- 🧹 **Data Cleaning Overview**: Data quality stats and log of cleaning operations

---

## 🧱 Project Structure

```
full_project/
│
├── landingPage.py              # Main entry point of the app
├── requirements.txt            # Required packages
│
├── data/
│   ├── superstore_raw.csv      # Original dataset
│   ├── load_data.py            # Data loading and preprocessing logic
│
├── filters/
│   └── sidebar_filters.py      # Sidebar filters for Region, Category, Date
│
├── pages/
│   └── home.py                 # Welcome page (optional)
│
├── tabs/
│   ├── business_overview.py    # Executive summary and KPIs
│   ├── financial_analysis.py   # Profitability and category performance
│   ├── customer_analysis.py    # Customer behavior insights
│   ├── prediction/
│   │   └── sales_prediction.py # Prophet forecasting model
│   ├── recommendations.py      # Smart business insights
│   └── data_cleaning.py        # Cleaning report
```

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/full_project.git
cd full_project
```

### 2. Create and activate a virtual environment (using `uv`)

```bash
uv venv venv
venv\Scripts\activate  # on Windows
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run landingPage.py
```

The dashboard will open in your browser at `http://localhost:8501`.

---

## 📦 Dependencies

- streamlit
- pandas
- plotly
- prophet

---

## 📊 Dataset Info

- Source: `superstore_raw.csv`  
- Contains order-level data including:
  - Sales, Profit, Category, Region
  - Customer names, Order dates, Product names
  - Shipping duration (calculated)

---

## 📍 Notes

- This dashboard is modular and easy to extend with new tabs or features.
- Forecasting is handled using **Facebook Prophet**.
- Data quality insights are logged in the `cleaning_log_df`.

---


