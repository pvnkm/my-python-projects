import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

class SalesDashboard:
    def __init__(self,df):
        self.df=df

    def filter_data(self,region,product):
        return self.df[(self.df['Region'].isin(region) & self.df['Product'].isin(product))]
    
    def calculate_kpis(self,df_filtered):
        total_sales = (df_filtered["Quantity"]*df_filtered['Price']).sum()
        total_quantity = df_filtered['Quantity'].sum()
        unique_products = df_filtered["Product"].nunique()
        return total_sales,total_quantity,unique_products
    
    def get_sales_over_time(self,df_filtered):
        df_filtered["Sales"] = df_filtered["Quantity"] * df_filtered["Price"]
        return df_filtered.groupby("Date")[["Sales"]].sum().reset_index()
    
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df =pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx','.xls'):
            df =pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Upload a CSV or Excel file")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
    
def display_kpis(total_sales,total_quantity,unique_products):
    col1,col2,col3=st.columns(3)
    col1.metric("Total Sales",f"${total_sales:,.2f}")
    col2.metric("Total Quantity",total_quantity)
    col3.metric("Unique Products",unique_products)

#Streamlit App layout
st.set_page_config(page_title='🛍️ Sales Dashboard',page_icon='bar_Chart',layout='wide')
st.title(':bar_chart: Sales Dashboard')

#Sidebar Upload file section
st.sidebar.header("📁 Upload Sales Data")
uploaded_file = st.sidebar.file_uploader("Choose a Csv or Excel",type=["xlsx","csv","xls"])

#load data

if uploaded_file:
    df = load_data(uploaded_file)
    #sidebar filteres
    region = st.sidebar.multiselect("Select the Region: ",df['Region'].unique(),default=df['Region'].unique())
    product = st.sidebar.multiselect("Select the Product: ",df['Product'].unique(),default=df['Product'].unique())

    #Dashboard Object

    dashboard = SalesDashboard(df)
    

    #Data Filtering
    df_filtered = dashboard.filter_data(region,product)

    #KPI Calculation
    total_sales,total_quantity,unique_products = dashboard.calculate_kpis(df_filtered)

        
    #Visualization
    st.subheader("📦 Sales by Product")
    product_sales = df_filtered.groupby("Product")[["Quantity"]].sum().reset_index()
    st.bar_chart(product_sales.set_index("Product"))

    st.subheader("📈 Sales Over Time")
    sales_over_time = dashboard.get_sales_over_time(df_filtered)
    fig = px.line(sales_over_time,x="Date",y="Sales",title="Sales Trend")
    st.plotly_chart(fig,use_container_width=True)

    #View Rawdata
    with st.expander("🧾 View Raw Data"):
        st.dataframe(df_filtered)

    #Download Filtered Data
    csv = df_filtered.to_csv(index=False).encode('utf=8')
    st.download_button("Download Filtered Data",csv,"filtered_sales.csv","text/csv")

else:
     st.warning("No data loaded. Please upload a valid sales file.")


