import streamlit as st
import pandas as pd

st.title('Dashboard')
with st.sidebar:
    email_health = st.file_uploader('Upload health drip data', type=['csv'], key='email_h')
    email_beauty = st.file_uploader('Upload beauty drip data', type=['csv'], key='email_b')
    email_dental = st.file_uploader('Upload dental drip data', type=['csv'], key='email_d')
    ga_data = st.file_uploader('Upload GA4 data', type=['csv'], key='ga')


if (email_health is not None) and (email_beauty is not None) and (email_dental is not None) and (ga_data is not None):
    select_one, select_two, select_three = st.columns(3)
    segmentation = select_one.selectbox('segment', ['health', 'beauty', 'dental'])
    ga = pd.read_csv(ga_data)
    if segmentation == 'health':
        data = pd.read_csv(email_health)
        ga = ga.loc[ga['campaign'] == 'category-lv-1-health']
    elif segmentation == 'dental':
        data = pd.read_csv(email_dental)
        ga = ga.loc[ga['campaign'] == 'category-lv-1-dental']
    elif segmentation == 'beauty':
        data = pd.read_csv(email_beauty)
        ga = ga.loc[ga['campaign'] == 'category-lv-1-beauty']
    else:
        st.text('no file uploaded')
    ga = ga.reset_index()
    ga = ga.drop('index', axis = 1)
    #st.dataframe(ga)


    emails = list(dict.fromkeys(data['Email Subject']))
    for i in emails:
        if pd.isnull(i) == True:
            emails.remove(i)


    date_series = list(dict.fromkeys(data['Date']))
    for i in date_series:
        if pd.isnull(i) == True:
            date_series.remove(i)

    dates = select_two.selectbox('pick the start date', date_series)
    dates_two = select_three.selectbox('pick the end date', date_series)

    drip_tags = [] ##working
    for i in range(1, len(emails) + 1):
        drip_tags.append("drip-%i" %i)

    email_drip = {emails[i]: drip_tags[i] for i in range(len(emails))} ##working

    #ga_drip = {drip_tags[i]: ga['source/medium'][i] for i in range(len(drip_tags))}

    for i in ga.index:
        ga.at[i, 'source/medium'] = ga.at[i, 'source/medium'].replace('email/', '')

    pres_data = data.copy()
    pres_data = pres_data[['Email Subject', 'Date', 'Total Opens', 'Total Clicks', 'Delivered']]
    pres_data = pres_data.dropna()
    pres_data = pres_data.set_index('Date')
    pres_data = pres_data.loc[dates:dates_two]
    pres_data = pres_data.groupby('Email Subject', as_index=False).sum()
    pres_data['Cumulative Open Rate'] = pres_data['Total Opens']/pres_data['Delivered']
    pres_data['Cumulative Click Rate'] = pres_data['Total Clicks']/pres_data['Delivered']
    pres_data['Click Through Rate'] = pres_data['Total Clicks']/pres_data['Total Opens']
    pres_data = pres_data[['Email Subject', 'Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']]
    pres_data['drip_tags'] = pres_data['Email Subject'].map(lambda x: email_drip[x])
    pres_data = pres_data[['Email Subject', 'drip_tags', 'Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']]
    #st.dataframe(pres_data)
    ga = ga.rename(columns={'source/medium': 'drip_tags'})
    final_data = pd.merge(pres_data, ga, on='drip_tags')
    final_data = final_data.drop(columns=['campaign'])
    st.dataframe(final_data)
    #d = final_data['Email Subject']
    #s = final_data['drip_tags']#.loc[dates:dates_two]
    #final_data = final_data.iloc[:, 1:].set_index('source/medium')
    #final_data = final_data.dropna()
    #final_data = final_data.loc[s].reset_index()
    #final_data['Email'] = d
    #final_data = final_data.drop(['drip_tags', 'campaign'], axis=1)
    #final_data = final_data.set_index('Email')
    #st.dataframe(final_data)