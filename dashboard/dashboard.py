# Import library yang akan digunakan

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper Function untuk setiap analysis

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").agg({
        "customer_id": "nunique",
    })
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystate_df


def create_monthly_orders_df(df):
    monthly_orders_df = df.groupby('order_month').agg({'order_id': 'count', 'price': 'sum'}).reset_index()
    monthly_orders_df['order_month_str'] = monthly_orders_df['order_month'].astype(str)
    return monthly_orders_df


def create_order_product_highest_income_df(df):
    result_order_product_highest_income_df = df.groupby(by="product_category_name_english").agg({
        "order_id": "nunique",
        "price": "sum"
    }).sort_values(by="price", ascending=False)
    result_order_product_highest_income_df = result_order_product_highest_income_df.head(5)
        
    return result_order_product_highest_income_df


def create_order_product_lowest_income_df(df):
    result_order_product_lowest_income_df = df.groupby(by="product_category_name_english").agg({
        "order_id": "nunique",
        "price": "sum"
    }).sort_values(by="price", ascending=True)
    result_order_product_lowest_income_df = result_order_product_lowest_income_df.head(5)
        
    return result_order_product_lowest_income_df


def create_order_product_highest_sales_df(df):
    result_order_product_highest_sales_df = df.groupby(by="product_category_name_english").agg({
        "order_id": "nunique",
        "price": "sum"
    }).sort_values(by="order_id", ascending=False)
    result_order_product_highest_sales_df = result_order_product_highest_sales_df.head(5)

    return result_order_product_highest_sales_df

def create_order_product_lowest_sales_df(df):
    result_order_product_lowest_sales_df = df.groupby(by="product_category_name_english").agg({
        "order_id": "nunique",
        "price": "sum"
    }).sort_values(by="order_id", ascending=True)
    result_order_product_lowest_sales_df = result_order_product_lowest_sales_df.head(5)

    return result_order_product_lowest_sales_df




# Load data
all_df = pd.read_csv("../dashboard/all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df.sort_values(by="order_delivered_carrier_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_delivered_carrier_date"].min()
max_date = all_df["order_delivered_carrier_date"].max()

with st.sidebar:   
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_delivered_carrier_date"] >= str(start_date)) & 
                (all_df["order_delivered_carrier_date"] <= str(end_date))]

# st.dataframe(main_df)

# Menyiapkan data frame yang akan digunakan untuk visualisaasi

bystate_df = create_bystate_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
highest_income_product_df = create_order_product_highest_income_df(main_df)
lowest_income_product_df = create_order_product_lowest_income_df(main_df)
highest_sales_product_df = create_order_product_highest_sales_df(main_df)
lowest_sales_product_df = create_order_product_lowest_sales_df(main_df)



st.header('Analisa Data E-Commerce Public Dataset Oleh Charles')
st.subheader('Monthly Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_df.order_id.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(monthly_orders_df.price.sum(), "BRL", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df['order_month_str'],
    monthly_orders_df['order_id'],
    marker='o', 
    linewidth=2,
    color="#000000"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel('Order Month', fontsize=15)
ax.set_ylabel('Order Count', fontsize=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

st.pyplot(fig)


# Produk dengan penghasilan tertinggi dan terendah
st.subheader("Highest and Lowest Income Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

plot_highest = highest_income_product_df.plot(kind='barh', y='price', color='skyblue', legend=False, ax=ax[0])

ax[0].set_xlabel('Total Penghasilan', fontsize=30)
ax[0].set_ylabel('Kategori Produk')
ax[0].set_title('Produk Penghasilan Tertinggi', loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)


plot_highest = lowest_income_product_df.plot(kind='barh', y='price', color='skyblue', legend=False, ax=ax[1])

ax[1].set_xlabel('Total Penghasilan', fontsize=30)
ax[1].set_ylabel('Kategori Produk')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()

ax[1].set_title('Produk Penghasilan Terendah', loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)


st.pyplot(fig)


# Produk dengan penjualan tertinggi dan terendah
st.subheader("Highest and Lowest Sales Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

plot_highest = highest_sales_product_df.plot(kind='barh', y='price', color='skyblue', legend=False, ax=ax[0])

ax[0].set_xlabel('Total Penjualan', fontsize=30)
ax[0].set_ylabel('Kategori Produk')
ax[0].set_title('Produk Penjualan Tertinggi', loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)


plot_highest = lowest_sales_product_df.plot(kind='barh', y='price', color='skyblue', legend=False, ax=ax[1])

ax[1].set_xlabel('Total Penjualan', fontsize=30)
ax[1].set_ylabel('Kategori Produk')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()

ax[1].set_title('Produk Penjualan Terendah', loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)


st.pyplot(fig)


# Distribusi Customer Berdasarkan state
st.subheader("Distribusi Customer Berdasarkan State")
fig, ax = plt.subplots(figsize=(16, 8))
colors_ = ["#72BCD4"]
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel('Total Customer', fontsize=15)
ax.set_ylabel('State', fontsize=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

st.pyplot(fig)
