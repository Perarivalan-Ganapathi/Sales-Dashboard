# Mini Streamlit Project

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime #, timedelta - if required

# Page Configuration
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# Footer function
def footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #111;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #333;
        }
        </style>
        <div class="footer">
            <p>Developed by Perarivalan Ganapathi |  📧 <a href="mailto:perarivalang164@gmail.com" style="color: #f0f0f0;">perarivalang164@gmail.com</a> | 🌐 <a href="https://www.linkedin.com/in/perarivalan-ganapathi?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BsWYYgbyUSQ6l63dAYGMEmQ%3D%3D" style="color: #f0f0f0;">LinkedIn</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# import dataset
d=pd.read_csv("sales1.csv")

# Data cleaning, transforming and manipulation
d['Quantity']=d.groupby('Product')['Product'].transform('count')
d['Totalsales']=(d['Quantity'] * d['Price'])
d['Date']=pd.to_datetime(d['Date'])
d['Month']=d['Date'].dt.month_name()
d['Month&Year']=d['Date'].dt.to_period('M').astype(str)

# Title for streamlit Interface
st.title('Sales_Dashboard')
# Totalsales in metric - looks like a card view in Power BI
st.metric("Total Sales in INR", value=d['Totalsales'].sum())
# Sales data preview for reference
st.subheader('Data_Preview')
st.dataframe(d.drop_duplicates(subset=['Product']).drop(columns=['PayMode','Month','Month&Year']))

# Adding multiselect filter by city that will sort all charts according to the city
f1=st.multiselect('Select City to filter sales', options=d['City'].unique())
f2=d[d['City'].isin(f1)]

if f1:
    f2=d[d['City'].isin(f1)]
else:
    f2=d

# Adding Bar_chart to see the totalsales by product 
st.subheader('Overall_Sales_by_Cities')
fig=px.bar(f2, x='Product', y='Totalsales', color='Quantity')
plt.xticks(rotation=45)
st.plotly_chart(fig)

# Pie_Chart to analyse the Payment mode #Cash #Card #UPI
st.subheader('Payment Details')
paymod=f2['PayMode'].value_counts().reset_index()
paymod.columns=['Mode', 'Percent']

fig_pie = px.pie(paymod, names='Mode', values='Percent', title='Mode Of Payment',
                 color_discrete_sequence=px.colors.diverging.PiYG,
                 labels={'Percent': 'Number of Transactions'},
                 hole=0.2,
                 hover_data=['Percent'])
st.plotly_chart(fig_pie)

# Line_chart for Monthly sales Analysis
monthly_rev=f2.groupby('Month')['Totalsales'].sum().reset_index()

fig,ax = plt.subplots()
sns.set_style('darkgrid')
sns.lineplot(data=monthly_rev, x='Month', y='Totalsales', markers='o', color='darkblue', ax=ax)
plt.xticks(rotation=45)
st.subheader('Month wise sales flow')
st.pyplot(fig)

# Pair_plot for Numerical columns to analyse the deep insight
num_col=st.multiselect('Select the Fields for deep insight', options=d.select_dtypes(include=['int64','float64']).columns)

if len(num_col)>1:
    fig=px.scatter_matrix(d, title='Sales Flow Insight', dimensions=num_col, color='Product')
    fig.update_traces(text=20, textsrc='outside')
    st.plotly_chart(fig)
elif len(num_col)<1:
    st.plotly_chart(fig)
    

# Create a download button by streamlit to download the filtered data in CSV Formate
st.subheader('Download Filtered Data')
csv=f2.to_csv(index=False)
st.download_button(
    label='Download CSV File',
    data=csv,
    file_name='Filtered_Sales_CSV',
    mime='text/csv')

# Call footer
footer()


