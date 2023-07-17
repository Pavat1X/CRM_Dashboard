import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Email Automation Dashboard')

upload = st.file_uploader("Upload a CSV file", type='csv')
if upload is not None:
    data = pd.read_csv(upload)


