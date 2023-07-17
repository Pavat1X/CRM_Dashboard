import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Email Automation Dashboard')

upload = st.file_uploader("Upload a CSV file", type='csv')
if upload is not None:
    data = pd.read_csv(upload)

## removing duplicates
emails = list(dict.fromkeys(data['Email Number']))

## wrangling metrics

metrics_list = ['requests', 'delivered', 'unique opens',
'cumulative unique open rate', 'unique clicks', 'cumulative unique click rate','spam reports','unsubscribes',
'conversion']

selection = st.selectbox('select the email number that you want to view', emails)

show_button = st.button('view data')

## represent data - will add time series later after figuring out how to get the latest data from sendgrid

if show_button:
	serve_data = data.loc[selection, metrics_list]
	print(serve_data)