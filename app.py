import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Email Automation Dashboard')

with st.sidebar:
	upload = st.file_uploader("Upload a CSV file", type='csv')
	if upload is not None:
		data = pd.read_csv(upload)
	## Creating keys
	emails = list(dict.fromkeys(data['Email Number']))
	for i in emails:
		if pd.isnull(i) == True:
			emails.remove(i)
	columns_list = ['Date Set Live', 'Requests', 'Delivered', 'Unique Opens', 'Cumulative Unique Open Rate',
					'Unique Clicks',
					'Cumulative Unique Click Rate', 'Spam Reports', 'Unsubscribes']
	## UI components
	selection = st.selectbox('select the email number that you want to view', emails)

	show_button = st.button('view data')

    ## represent data - will add time series later after figuring out how to get the latest data from sendgrid

if show_button:
    serve_data = data[columns_list]
    show_data = serve_data.loc[serve_data['Date Set Live'] == selection + " TOTAL"]
    col1, col2, col3 = st.columns(3)
    col1.metric('Unique Opens', show_data['Unique Opens'])
    col2.metric('Unique Clicks', show_data['Unique Clicks'])
    col3.metric('Unsubscribes', show_data['Unsubscribes'])
    st.dataframe(show_data)