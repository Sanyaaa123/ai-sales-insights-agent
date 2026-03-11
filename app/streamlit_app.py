import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# -----------------------------------
# OpenAI Client
# -----------------------------------

client = OpenAI()

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Sales Insights Dashboard",
    layout="wide"
)

st.title("📊 AI Sales Insights Dashboard")

# -----------------------------------
# File Upload
# -----------------------------------

uploaded_file = st.file_uploader("Upload Sales Dataset", type=["csv"])

# -----------------------------------
# If file uploaded
# -----------------------------------

if uploaded_file is not None:

    # Load dataset
    df = pd.read_csv(uploaded_file, encoding="latin1")

    # Clean column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    st.success("Dataset uploaded successfully!")

    # -----------------------------------
    # KPI METRICS
    # -----------------------------------

    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_name"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Total Orders", total_orders)
    col4.metric("Customers", total_customers)

    st.divider()

    # -----------------------------------
    # Revenue by Region
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Region")

        region_sales = (
            df.groupby("region")["sales"]
            .sum()
            .reset_index()
        )

        fig = px.bar(region_sales, x="region", y="sales", color="region")

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------
    # Revenue by Category
    # -----------------------------------

    with col2:
        st.subheader("Revenue by Category")

        category_sales = (
            df.groupby("category")["sales"]
            .sum()
            .reset_index()
        )

        fig = px.bar(category_sales, x="category", y="sales", color="category")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------------------
    # Monthly Sales Trend
    # -----------------------------------

    st.subheader("Monthly Sales Trend")

    df["order_date"] = pd.to_datetime(df["order_date"])

    monthly_sales = (
        df.groupby(df["order_date"].dt.to_period("M"))["sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)

    fig = px.line(monthly_sales, x="order_date", y="sales", markers=True)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------------------
    # Top Customers
    # -----------------------------------

    st.subheader("Top 10 Customers")

    top_customers = (
        df.groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(top_customers, use_container_width=True)

    st.divider()

    # -----------------------------------
    # Profit by Category
    # -----------------------------------

    st.subheader("Profit by Category")

    profit_category = (
        df.groupby("category")["profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(profit_category, x="category", y="profit", color="category")

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------------------
    # AI BUSINESS INSIGHTS
    # -----------------------------------

    st.subheader("🤖 AI Business Insights")

    summary = df.describe().to_string()

    if st.button("Generate AI Insights"):

        prompt = f"""
You are a business analyst.

Analyze this sales dataset summary and provide key insights and recommendations.

Dataset summary:
{summary}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        insights = response.choices[0].message.content

        st.write(insights)

    st.divider()

    # -------------------------------------------------
# AI DATA ANALYST CHATBOT
# -------------------------------------------------

st.divider()
st.subheader("🤖 AI Data Analyst")

question = st.text_input("Ask anything about the dataset")

if question:

    prompt = f"""
You are a senior data analyst.

A pandas dataframe named df is already loaded.

Columns:
{list(df.columns)}

User question:
{question}

Rules:

1. Use pandas to analyze the data
2. Store final answer in variable called result
3. If visualization is useful, create a plotly chart called fig
4. Do NOT explain anything
5. Only return Python code
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.choices[0].message.content

    code = code.replace("```python", "").replace("```", "")

    try:

        local_vars = {"df": df, "px": px, "pd": pd}

        exec(code, {}, local_vars)

        if "fig" in local_vars:
            st.plotly_chart(local_vars["fig"], use_container_width=True)

        if "result" in local_vars:
            st.write(local_vars["result"])

    except Exception as e:

        st.error("AI generated invalid code")

        st.code(code)
# -----------------------------------
# If no file uploaded
# -----------------------------------

else:
    st.info("Upload a sales dataset to start analysis.")

