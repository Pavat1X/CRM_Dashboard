import streamlit as st
import pandas as pd

st.title('Dashboard')
with st.sidebar:
    email_health = st.file_uploader('Upload health drip data', type=['csv'], key='email_h')
    email_beauty = st.file_uploader('Upload beauty drip data', type=['csv'], key='email_b')
    email_dental = st.file_uploader('Upload dental drip data', type=['csv'], key='email_d')
    #email_vaccine = st.file_uploader('Upload vaccine drip data', type=['csv'], key='email_v')
    #email_checkup = st.file_uploader('Upload checkup drip data', type=['csv'], key='email_c')
    #email_food = st.file_uploader('Upload food drip data', type=['csv'], key='email_f')
    ga_data = st.file_uploader('Upload GA4 data', type=['csv'], key='ga')


if (email_health is not None) and (email_beauty is not None) and (email_dental is not None) and (ga_data is not None):
    segmentation = st.selectbox('segment', ['health', 'beauty', 'dental'])
    select_two, select_three = st.columns(2)
    ga = pd.read_csv(ga_data)
    ga.rename(columns = {'Event campaign name': 'campaign'}, inplace = True)
    #if segmentation:
        #data_file_name = "email_%s" %segmentation
        #data = pd.read_csv(data_file_name)
        #ga = ga[ga['campaign'].str.contains(segmentation)]

    if segmentation == 'health':
        data = pd.read_csv(email_health)
        ga = ga[ga['campaign'].str.contains('health')]
    elif segmentation == 'dental':
        data = pd.read_csv(email_dental)
        ga = ga[ga['campaign'].str.contains('dental')]
    elif segmentation == 'beauty':
        data = pd.read_csv(email_beauty)
        ga = ga[ga['campaign'].str.contains('beauty')]
    #elif segmentation == 'vaccine':
        #data = pd.read_csv(email_vaccine)
        #ga = ga[ga['campaign'].str.contains('vaccine')]
    #elif segmentation == 'checkup':
        #data = pd.read_csv(email_checkup)
        #ga = ga[ga['campaign'].str.contains('checkup')]
    #elif segmentation == 'food':
        #data = pd.read_csv(email_food)
        #ga = ga[ga['campaign'].str.contains('food')]
    else:
        st.text('no file uploaded')
    ga = ga.reset_index()
    ga = ga.drop('index', axis = 1)
    ga.columns = ga.columns.str.lower()
    ga['source / medium'] = ga['source / medium'].str.replace(" ","")
    ga.columns = ga.columns.str.replace(" ", "")

    emails = list(dict.fromkeys(data['Email Subject']))
    for i in emails:
        if pd.isnull(i) == True:
            emails.remove(i)


    date_series = list(dict.fromkeys(data['Date']))
    for i in date_series:
        if pd.isnull(i) == True:
            date_series.remove(i)

    dates = select_two.selectbox('pick the start date (period 1)', date_series)
    dates_two = select_three.selectbox('pick the end date (period 1)', date_series)
    st.caption('pick dates to compare')
    select_four, select_five = st.columns(2)
    dates_three = select_four.selectbox('pick the start date (period 2)', date_series, key='seconddate')
    dates_four = select_five.selectbox('pick the end date (period 2)', date_series, key='thirddate')


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

    compare_data = data.copy()
    compare_data = compare_data[['Email Subject', 'Date', 'Total Opens', 'Total Clicks', 'Delivered']]
    compare_data = compare_data.dropna()
    compare_data = compare_data.set_index('Date')
    compare_data = compare_data.loc[dates_three:dates_four]
    compare_data = compare_data.groupby('Email Subject', as_index=False).sum()
    compare_data['Cumulative Open Rate'] = compare_data['Total Opens'] / compare_data['Delivered']
    compare_data['Cumulative Click Rate'] = compare_data['Total Clicks'] / compare_data['Delivered']
    compare_data['Click Through Rate'] = compare_data['Total Clicks'] / compare_data['Total Opens']
    compare_data = compare_data[['Email Subject', 'Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']]
    compare_data['drip_tags'] = compare_data['Email Subject'].map(lambda x: email_drip[x])
    compare_data = compare_data[
        ['Email Subject', 'drip_tags', 'Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']]
    #st.dataframe(pres_data)
    #st.dataframe(compare_data)

    diff_matrix = pres_data[['Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']].subtract(compare_data[['Cumulative Open Rate', 'Cumulative Click Rate', 'Click Through Rate']], axis=1)
    #st.dataframe(diff_matrix)



    #st.dataframe(pres_data)
    ga = ga.rename(columns={'source/medium': 'drip_tags'})
    final_data = pd.merge(pres_data, ga, on='drip_tags')
    final_data = final_data.drop(columns=['campaign'])
    final_data['Cumulative Open Rate'] = (100 * final_data['Cumulative Open Rate']).round(2).astype(str)+"%"
    final_data['Cumulative Click Rate'] = (100 * final_data['Cumulative Click Rate']).round(2).astype(str)+"%"
    final_data['Click Through Rate'] = (100 * final_data['Click Through Rate']).round(2).astype(str)+"%"

    pres_data['Cumulative Open Rate'] = (100 * pres_data['Cumulative Open Rate']).round(2).astype(str)+"%"
    pres_data['Cumulative Click Rate'] = (100 * pres_data['Cumulative Click Rate']).round(2).astype(str) + "%"
    pres_data['Click Through Rate'] = (100 * pres_data['Click Through Rate']).round(2).astype(str) + "%"

    pres_data ['delta Open Rate'] = diff_matrix['Cumulative Open Rate']
    pres_data['delta Click Rate'] = diff_matrix['Cumulative Click Rate']
    pres_data['delta CTR'] = diff_matrix['Click Through Rate']
    pres_data = pres_data[['Email Subject', 'drip_tags', 'Cumulative Open Rate', 'delta Open Rate',
                             'Cumulative Click Rate', 'delta Click Rate', 'Click Through Rate', 'delta CTR']]


    final_data['delta Open Rate'] = diff_matrix['Cumulative Open Rate']
    final_data['delta Click Rate'] = diff_matrix['Cumulative Click Rate']
    final_data['delta CTR'] = diff_matrix['Click Through Rate']
    final_data = final_data[['Email Subject', 'drip_tags', 'Cumulative Open Rate', 'delta Open Rate',
                             'Cumulative Click Rate', 'delta Click Rate', 'Click Through Rate', 'delta CTR', 'sessions',
                             'conversions']]
    st.dataframe(final_data)
    st.caption('all drips')
    st.dataframe(pres_data)


    download = final_data.to_csv().encode('utf-8')

    st.download_button('download data', download,
                       "dashboard_data_%s.csv" %segmentation, "text/csv")