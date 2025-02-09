import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Superstore Dashboard", page_icon="📊")

@st.cache_data
def load_data():
    df = pd.read_csv("sample-superstore.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

with st.sidebar:
    st.image("images/unikom.png", width=150)
    st.image("images/kelompok6.png", width=450)
    st.markdown("## Filter Data")  
    regions = df["Region"].unique()
    selected_regions = st.multiselect("Pilih Region", regions, default=regions)
    categories = df["Category"].unique()
    selected_categories = st.multiselect("Pilih Kategori", categories, default=categories)

filtered_df = df[(df["Region"].isin(selected_regions)) & (df["Category"].isin(selected_categories))]
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

st.title("📊 Superstore Dashboard")
st.markdown("### Analisis Penjualan dan Profit")

col1, col2 = st.columns(2)
col1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
col2.metric(label="Total Profit", value=f"${total_profit:,.2f}")

st.subheader("Total Penjualan berdasarkan Negara")
sales_by_state = filtered_df.groupby("State")["Sales"].sum().reset_index()
fig_sales = px.bar(sales_by_state, x="State", y="Sales", title="Total Penjualan per Negara", color="Sales", color_continuous_scale="Blues")
st.plotly_chart(fig_sales, use_container_width=True)

st.subheader("Profit vs Discount")
fig_profit_discount = px.scatter(filtered_df, x="Discount", y="Profit", color="Category", size="Sales", title="Profit vs Discount", hover_data=["State"])
st.plotly_chart(fig_profit_discount, use_container_width=True)

st.subheader("Distribusi Penjualan per Kategori Produk")
sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig_pie = px.pie(sales_by_category, values="Sales", names="Category", title="Distribusi Penjualan per Kategori", hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Tren Penjualan Bulanan")
sales_trend = filtered_df.groupby("Month")["Sales"].sum().reset_index()
fig_trend = px.line(sales_trend, x="Month", y="Sales", title="Tren Penjualan Bulanan", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("📊 Data Sample")
st.dataframe(filtered_df.head(10))

st.markdown("---")
st.markdown("📌 **Dashboard ini dikembangkan oleh Kelompok 6 | Universitas Komputer Indonesia (UNIKOM)**")
