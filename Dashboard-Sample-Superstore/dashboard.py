import streamlit as st
import pandas as pd
import plotly.express as px
import os  # Untuk mengecek keberadaan file

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Superstore Dashboard", page_icon="📊")

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data():
    file_path = "Sample-Superstore.csv"  # Sesuaikan dengan nama file yang benar

    # Cek apakah file ada
    if not os.path.exists(file_path):
        st.error(f"File {file_path} tidak ditemukan! Pastikan sudah diunggah atau tersedia di repository GitHub.")
        return pd.DataFrame()  # Mengembalikan dataframe kosong jika file tidak ditemukan

    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    return df.dropna()

# Load data
df = load_data()

# Pastikan data tidak kosong sebelum melanjutkan
if df.empty:
    st.stop()  # Hentikan eksekusi jika data tidak tersedia

# Sidebar untuk filter
with st.sidebar:
    st.image("images/unikom.png", width=150)
    st.image("images/kelompok6.png", width=150)
    st.markdown("## Filter Data")

    regions = df["Region"].dropna().unique()
    selected_regions = st.multiselect("Pilih Region", regions, default=regions)

    categories = df["Category"].dropna().unique()
    selected_categories = st.multiselect("Pilih Kategori", categories, default=categories)

# Filter data berdasarkan pilihan sidebar
filtered_df = df[df["Region"].isin(selected_regions) & df["Category"].isin(selected_categories)]

# Menampilkan data yang difilter
st.write("### Data yang Difilter")
st.dataframe(filtered_df)

# Visualisasi Data
st.write("## Visualisasi Data")

# Total Penjualan
total_sales = filtered_df["Sales"].sum()
st.metric(label="Total Penjualan", value=f"${total_sales:,.2f}")

# Total Profit
total_profit = filtered_df["Profit"].sum()
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")

# Grafik Penjualan per State
sales_by_state = filtered_df.groupby("State")["Sales"].sum().reset_index()
fig_sales = px.bar(sales_by_state, x="State", y="Sales", title="Penjualan per State", color="Sales")
st.plotly_chart(fig_sales, use_container_width=True)

# Grafik Profit dan Discount
fig_profit_discount = px.scatter(filtered_df, x="Discount", y="Profit", color="Category",
                                 title="Profit vs Discount", size="Sales", hover_data=["State"])
st.plotly_chart(fig_profit_discount, use_container_width=True)

# Grafik Pie Kategori
sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig_pie = px.pie(sales_by_category, names="Category", values="Sales", title="Distribusi Penjualan per Kategori")
st.plotly_chart(fig_pie, use_container_width=True)

# Grafik Tren Penjualan
sales_trend = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()
fig_trend = px.line(sales_trend, x="Order Date", y="Sales", title="Tren Penjualan")
st.plotly_chart(fig_trend, use_container_width=True)
