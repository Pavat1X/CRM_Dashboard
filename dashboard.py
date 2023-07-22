import streamlit as st
import pandas as pd

st.title('Dashboard')
with st.sidebar:
    email_health = st.file_uploader('Upload health drip data', type=['csv'], key='email_h')
    email_beauty = st.file_uploader('Upload beauty drip data', type=['csv'], key='email_b')
    email_dental = st.file_uploader('Upload dental drip data', type=['csv'], key='email_d')
    ga_data = st.file_uploader('Upload GA4 data', type=['csv'], key='ga')

select_one, select_two, select_three, select_four = st.columns(4)
segmentation = select_one.selectbox('segment', ['health', 'beauty', 'dental'])
if segmentation == 'health':
    data = pd.read_csv(email_health)
elif segmentation == 'dental':
    data = pd.read_csv(email_dental)
elif segmentation == 'beauty':
    data = pd.read_csv(email_beauty)
else:
    st.text('no file uploaded')

if data is not None:
    emails = list(dict.fromkeys(data['Email Subject']))
    for i in emails:
        if pd.isnull(i) == True:
            emails.remove(i)

    email_name = select_two.selectbox('email subjects', emails)

    date_series = list(dict.fromkeys(data['Date']))
    for i in date_series:
        if pd.isnull(i) == True:
            date_series.remove(i)

    dates = select_three.selectbox('pick the start date', date_series)
    dates_two = select_four.selectbox('pick the end date', date_series)


    pres_data = data.copy()
    pres_data = pres_data.drop(['Date Set Live', 'Automation ID', 'Automation Name', 'Email Number'], axis=1)
    pres_data = pres_data.dropna()
    pres_data_date = pres_data['Date']
    pres_data = pres_data.drop('Date', axis=1)
    pres_data.insert(loc = 1, column='Date', value=pres_data_date)
    pres_data = pres_data.set_index("Email Subject")
    pres_data = pres_data.loc[email_name]
    pres_data = pres_data.reset_index()
    pres_data = pres_data.set_index('Date')
    pres_data = pres_data.loc[dates:dates_two]
    pres_data = pres_data.drop('Email Subject', axis = 1)
    pres_data = pres_data[['Requests', 'Delivered', 'Unique Opens', 'Cumulative Unique Open Rate',
    'Unique Clicks', 'Cumulative Unique Click Rate', 'Spam Reports', 'Unsubscribes']]
    st.dataframe(pres_data)