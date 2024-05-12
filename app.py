

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


@st.cahce_data
def load_data():
    Olist = pd.read_csv('./datasets/List of Orders.csv')
    Detail = pd.read_csv('./datasets/Order Details.csv')
    data = Olist.merge(Detail, on='Order ID')

    return data

def preproc():
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d-%m-%Y')
    data['year'] = data['Order Date'].dt.year
    data['month'] = data['Order Date'].dt.month
    data['yearmonth'] = data['Order Date'].astype('str').str.slice(0,7)

    return df

def line_chart(data, x, y, title):
    df = data.groupby(x).agg({y: 'sum'}).reset_index()
    fig = px.line(df, x=x, y=y, title=title)
    fig.show()

    return fig

def bar_chart(data, x, y, color=None):
    if color is not None:
        index = [x, color]
    else:
        index = x

    df = data.pivot_table(index=index, values=y, aggfunc='sum').reset_index()
    fig = px.bar(df, x=x, y=y, color=color)
    fig.show()

    return fig

def heatmap(data, z, title):
    df = data.pivot_table(index= ['State', 'Sub-Category'], values=['Quantity', 'Amount', 'Profit'], aggfunc='sum').reset_index()
    fig = px.density_heatmap(df, x='State', y='Sub-Category', z=z, title=title)
    fig.show()

    return fig


if __name__ == "__main__":
    st.titile('E-Commerce data analysis')
    st.write('Visualization dashboard')

    data = load_data()
    data = preproc()

st.subheader('Monthly Sales Quantity Analysis')
with st.form('form', clear_on_submit = True):
    col1, col2 = st.columns(2)
    submitted1 = col1.form_submit_button('Quantity graph')
    submitted2 = col2.form_submit_button('Amount graph')

    if submitted1:
        df1, fig1 = line_chart(data, 'yearmonth', 'Quantity', 'Sales Quantity by month')
        st.dataframe(df1.T)
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    elif submitted2:
        df2, fig2 = line_chart(data, 'yearmonth', 'Amount', 'Sales Amount by month')
        st.dataframe(df2.T)
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


st.subheader('Sales Quantity by Item')
col1, col2 = st.columns(2)
with col1:
    col1.subheader("Sales Quantity by Category")
    fig3 = bar_chart(data, 'Category', 'Quantity')
    st.plotly_chart(fig3, them=streamlit", use_container_width=True)
with col2:
    col2.subheader("Stackted bar chart by Monthly/Category")
    fig4 = bar_chart(data, 'yearmonth', 'Quantity', 'Category')
    st.plotly_chart(fig4, them=streamlit", use_container_width=True)


st.subheader('Main Selling Products by State')
tab1, tab2 = st.tabs(["Quantity heat map", "Amount heat map"])
with tab1:
    fig5 = heatmap(data, 'Quantity', 'Quantity heat map')
    st.plotly_chart(fig5, them=streamlit", use_container_width=True)
with tab2:
    fig6 = heatmap(data, 'Amount', 'Amount heat map')
    st.plotly_chart(fig6, them=streamlit", use_container_width=True)
    
