import streamlit as st

st.title('CRM Dashboard')

email_health = st.file_uploader('Upload health drip file', type=['csv'], key='email_h')
email_beauty = st.file_uploader('Upload beauty drip file', type=['csv'], key='email_b')
email_dental = st.file_uploader('Upload dental drip file', type=['csv'], key='email_d')
ga_data = st.file_uploader('Upload a CSV file', type=['csv'], key='ga')

if email_health is not None:
    st.session_state['email_health'] = email_health.getvalue().decode('utf-8')
if email_beauty is not None:
    st.session_state['email_beauty'] = email_beauty.getvalue().decode('utf-8')
if email_dental is not None:
    st.session_state['email_dental'] = email_dental.getvalue().decode('utf-8')
if ga_data is not None:
    st.session_state['ga_data'] = ga_data.getvalue().decode('utf-8')