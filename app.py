import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Read the dataset and replace missing values
vehicles_df = pd.read_csv('vehicles_us.csv')

vehicles_df['model_year'] = vehicles_df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))

vehicles_df['cylinders'] = vehicles_df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))

def fill_with_median_or_zero(x):
    if x.dropna().empty:  # Check if the group has no non-NaN values
        return x.fillna(0)
    else:
        return x.fillna(x.median())

vehicles_df['odometer'] = vehicles_df.groupby('model_year')['odometer'].transform(fill_with_median_or_zero)

#Remove outliers
def remove_outliers(vehicles_df, column, lower_quantile=0.05, upper_quantile=0.95):
    lower_bound = vehicles_df[column].quantile(lower_quantile)
    upper_bound = vehicles_df[column].quantile(upper_quantile)
    return vehicles_df[(vehicles_df[column] >= lower_bound) & (vehicles_df[column] <= upper_bound)]

vehicles_df = remove_outliers(vehicles_df, 'model_year')
vehicles_df = remove_outliers(vehicles_df, 'price')

#Now I will create a scatterplot and histogram to visualize the data    
st.header('Car Listing Analysis')
st.write('Comparing the listings of old cars vs new cars')

scatterplot = st.checkbox('Scatterplot')
histogram = st.checkbox('Histogram')    

if scatterplot:
    st.write('Scatterplot')
    fig_one = px.scatter(vehicles_df, x='model_year', y='price', title='Car Age vs. Price')  
    st.plotly_chart(fig_one)    
else:
    st.write('Histogram')
    fig_two = px.histogram(vehicles_df, x='price', title='Distribution of Car Prices')
    st.plotly_chart(fig_two)    
