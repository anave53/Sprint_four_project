import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Read the dataset and remove missing values
vehicles_df = pd.read_csv('vehicles_us.csv')
vehicles_df.dropna()

#Remove outliers
numeric_cols = vehicles_df.select_dtypes(include=['int64', 'float64']).columns

Q1 = vehicles_df[numeric_cols].quantile(0.25)
Q3 = vehicles_df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

non_outliers = ((vehicles_df[numeric_cols] >= lower_bound) & (vehicles_df[numeric_cols] <= upper_bound))

vehicles_processed = vehicles_df[non_outliers.all(axis=1)]

print(vehicles_processed)


st.header('Car Listing Analysis')
st.write('Comparing the listings of old cars vs new cars')

scatterplot = st.checkbox('Scatterplot')
histogram = st.checkbox('Histogram')    

if scatterplot:
    st.write('Scatterplot')
    fig_one = px.scatter(vehicles_processed, x='model_year', y='price', title='Car Age vs. Price')  
    st.plotly_chart(fig_one)    
else:
    st.write('Histogram')
    fig_two = px.histogram(vehicles_processed, x='price', title='Distribution of Car Prices')
    st.plotly_chart(fig_two)    
