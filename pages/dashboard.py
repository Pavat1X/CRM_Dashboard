import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO


st.title('Dashboard')

with st.sidebar:

    segment_selector = st.selectbox('select the segment of emails that you want to view',
                                    ['health', 'beauty', 'dental'])

    if segment_selector == 'health':
        if 'email_health' in st.session_state:
            data = pd.read_csv(StringIO(st.session_state['email_data']))
        else:
            print("No file uploaded")
    elif segment_selector == 'dental':
        if 'email_dental' in st.session_state:
            data = pd.read_csv(StringIO(st.session_state['email_dental']))
        else:
            print("No file uploaded")
    elif segment_selector == 'beauty':
        if 'email_beauty' in st.session_state:
            data = pd.read_csv(StringIO(st.session_state['email_beauty']))

    if data is not None:
        ## Creating keys
        emails = list(dict.fromkeys(data['Email Subject']))
        for i in emails:
            if pd.isnull(i) == True:
                emails.remove(i)
        columns_list = ['Email Subject', 'Requests', 'Delivered', 'Unique Opens', 'Cumulative Unique Open Rate',
                        'Unique Clicks',
                        'Cumulative Unique Click Rate', 'Spam Reports', 'Unsubscribes']
        columns_list_two = ['Requests', 'Delivered', 'Unique Opens', 'Cumulative Unique Open Rate',
                            'Unique Clicks', 'Cumulative Unique Click Rate', 'Spam Reports', 'Unsubscribes']
        ## UI components
    selection = st.selectbox('select the email that you want to view', emails)

    show_button = st.button('view data')

    if 'ga_data' in st.session_state:
        ga_data = pd.read_csv(StringIO(st.session_state['ga_data']))

## represent data - will add time series later after figuring out how to get the latest data from sendgrid

if show_button:
    serve_data = data[columns_list]
    serve_data['Cumulative Unique Open Rate'] = \
        serve_data['Cumulative Unique Open Rate'].str.rstrip("%").astype(float) / 100
    serve_data['Cumulative Unique Click Rate'] = \
        serve_data['Cumulative Unique Click Rate'].str.rstrip("%").astype(float) / 100
    serve_data = serve_data.groupby('Email Subject')[columns_list_two].sum()
    show_data = serve_data.loc[selection]
    col1, col2, col3 = st.columns(3)
    col1.metric('Delivered', show_data['Delivered'])
    col2.metric('Cumulative Unique Open Rate', show_data['Cumulative Unique Open Rate'])
    col3.metric('Cumulative Unique Click Rate', show_data['Cumulative Unique Click Rate'])
    st.dataframe(show_data)