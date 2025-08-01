import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})

st.title('Population of Canada')
st.markdown(f'CSV file can be found [here]({URL})')
with st.expander('View data'):
    st.dataframe(df)
with st.form('date'):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Start date')
        qstart = st.selectbox('Quarter', ('Q1', 'Q2', 'Q3', 'Q4'), 2)
        ystart = st.slider('Year', 1991, 2023, 1991)
    with col2:
        st.subheader('End date')
        qend = st.selectbox('Quarter', ('Q1', 'Q2', 'Q3', 'Q4'), 0)
        yend = st.slider('Year', 1991, 2023, 2023)
    location = st.selectbox('Location', df.columns[1:])
    st.form_submit_button('Analyze')
start = f'{qstart} {ystart}'
end = f'{qend} {yend}'
tab1, tab2 = st.tabs(('Population change', 'Compare'))
with tab1:
    st.subheader(f'Population change from {start} to {end}')
    col1, col2 = st.columns(2)
    start_pop = df.loc[df['Quarter'] == start, location].item()
    end_pop = df.loc[df['Quarter'] == end, location].item()
    delta = end_pop - start_pop
    with col1:
        st.metric(start, start_pop)
        st.metric(end, end_pop, delta)
    start_idx = df[df['Quarter'] == start].index[0]
    end_idx = df[df['Quarter'] == end].index[0]
    sub_df = df.loc[start_idx:end_idx]
    fig, ax = plt.subplots()
    ax.plot(sub_df['Quarter'], sub_df[location])
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_xticks([sub_df.at[start_idx, 'Quarter'], sub_df.at[end_idx, 'Quarter']])
    fig.autofmt_xdate()
    with col2:
        st.pyplot(fig)
with tab2:
    st.subheader('Compare with other locations')
    targets = st.multiselect('Choose other locations', df.columns[1:], location)
    fig, ax = plt.subplots()
    for target in targets:
        ax.plot(sub_df['Quarter'], sub_df[target])
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_xticks([sub_df.at[start_idx, 'Quarter'], sub_df.at[end_idx, 'Quarter']])
    fig.autofmt_xdate()
    st.pyplot(fig)