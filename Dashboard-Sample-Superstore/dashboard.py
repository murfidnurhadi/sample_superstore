import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Superstore Dashboard", page_icon="📊")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    file_id = "1g-haOdl4urid7IrPmu0w-1oBe6E0Su7l"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "sample-superstore.csv"

    try:
        gdown.download(url, output, quiet=False)
        try:
            df = pd.read_csv(output)
        except pd.errors.ParserError:
            df = pd.read_csv(output, delimiter=";")

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
        return df
    except Exception as e:
        st.error(f"Gagal mengunduh atau membaca file CSV dari Google Drive: {e}")
        return pd.DataFrame()

# Load dataset
df = load_data()

# Sidebar untuk filter
with st.sidebar:
    st.image("https://raw.githubusercontent.com/murfidnurhadi/sample_superstore/main/images/unikom.png", width=150)
    st.image("https://raw.githubusercontent.com/murfidnurhadi/sample_superstore/main/images/kelompok6.png", width=450)
    st.markdown("## Filter Data")  

    # Filter Region
    regions = df["Region"].unique()
    selected_regions = st.multiselect("Pilih Region", regions, default=regions)

    # Filter Kategori
    categories = df["Category"].unique()
    selected_categories = st.multiselect("Pilih Kategori", categories, default=categories)

    # Filter Kategori untuk Tren Penjualan
    selected_trend_category = st.selectbox("Pilih Kategori Tren Penjualan", ["Semua"] + list(categories))

# Filter data berdasarkan pilihan user
filtered_df = df[(df["Region"].isin(selected_regions)) & (df["Category"].isin(selected_categories))]

# Hitung Total Sales & Profit
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

# Tampilan utama dashboard
st.title("📊 Superstore Dashboard")
st.markdown("### Analisis Penjualan dan Profit")

# Menampilkan Total Sales dan Profit
col1, col2 = st.columns(2)
col1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
col2.metric(label="Total Profit", value=f"${total_profit:,.2f}")

# Grafik Penjualan per Negara (State)
st.subheader("Total Penjualan berdasarkan Negara")
sales_by_state = filtered_df.groupby("State")["Sales"].sum().reset_index()
fig_sales = px.bar(sales_by_state, x="State", y="Sales", title="Total Penjualan per Negara", 
                   color="Sales", color_continuous_scale="Blues")
st.plotly_chart(fig_sales, use_container_width=True)

# Scatter Plot Profit vs Discount
st.subheader("Profit vs Discount")
fig_profit_discount = px.scatter(filtered_df, x="Discount", y="Profit", color="Category", 
                                 size="Sales", title="Profit vs Discount", hover_data=["State"])
st.plotly_chart(fig_profit_discount, use_container_width=True)

# Menampilkan jumlah total transaksi per kategori
st.subheader("Total Jumlah Transaksi per Kategori")
category_counts = filtered_df["Category"].value_counts().reset_index()
category_counts.columns = ["Category", "Total Transactions"]
st.table(category_counts)

# Visualisasi Total Transaksi per Kategori
fig_category_count = px.bar(category_counts, x="Category", y="Total Transactions", 
                            title="Total Transaksi per Kategori", color="Total Transactions", 
                            color_continuous_scale="Viridis")
st.plotly_chart(fig_category_count, use_container_width=True)

# Pie Chart Distribusi Penjualan per Kategori
st.subheader("Distribusi Penjualan per Kategori Produk")
sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig_pie = px.pie(sales_by_category, values="Sales", names="Category", 
                 title="Distribusi Penjualan per Kategori", hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)

# **Tren Penjualan Bulanan Sesuai Filter Kategori**
st.subheader("Tren Penjualan Bulanan per Kategori")

# Jika "Semua" dipilih, tampilkan semua kategori
if selected_trend_category == "Semua":
    sales_trend = filtered_df.groupby(["Month", "Category"])["Sales"].sum().reset_index()
    fig_trend = px.line(sales_trend, x="Month", y="Sales", color="Category", 
                        title="Tren Penjualan Bulanan (Semua Kategori)", markers=True)
else:
    sales_trend = filtered_df[filtered_df["Category"] == selected_trend_category].groupby("Month")["Sales"].sum().reset_index()
    fig_trend = px.line(sales_trend, x="Month", y="Sales", title=f"Tren Penjualan Bulanan ({selected_trend_category})", markers=True)

st.plotly_chart(fig_trend, use_container_width=True)

# Tampilkan Data Sample
st.subheader("📊 Data Sample")
st.dataframe(filtered_df.head(10))

# Footer
st.markdown("---")
st.markdown("📌 **Dashboard ini dikembangkan oleh Kelompok 6 | Universitas Komputer Indonesia (UNIKOM)**")
