
import streamlit as st
import pandas as pd
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ E-Commerce Customer Segmentation")
st.write("Customer Analysis and Product Recommendation Dashboard")

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Load saved data
@st.cache_data
def load_customer_data():
    path = os.path.join(OUTPUT_DIR, "customer_segments.csv")
    return pd.read_csv(path, index_col=0)

# Dashboard
try:
    rfm = load_customer_data()

    st.subheader("Customer Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", len(rfm))
    col2.metric("Number of Segments", rfm["Cluster"].nunique())
    col3.metric("Average Spending", f"£{rfm['Monetary'].mean():,.2f}")

    st.subheader("Customer Segments")

    st.bar_chart(rfm["Cluster"].value_counts().sort_index())

    st.subheader("Customer RFM Details")
    st.dataframe(rfm, use_container_width=True)

    st.subheader("Cluster Analysis")

    cluster_summary = rfm.groupby("Cluster").agg(
        Customer_Count=("Recency", "count"),
        Average_Recency=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean"),
        Average_Monetary=("Monetary", "mean")
    ).round(2)

    st.dataframe(cluster_summary, use_container_width=True)

    st.success("Dashboard loaded successfully!")

except FileNotFoundError:
    st.error(
        "Customer segmentation file not found. "
        "Please check outputs/customer_segments.csv."
    )

except Exception as e:
    st.error(f"An error occurred: {e}")
