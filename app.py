import streamlit as st
import pandas as pd

bar = st.sidebar.radio("Navigation",['Home', 'Result'])

if bar == 'Home' :
    st.header('JEC RESULT ANALYSIS')

if bar == 'Result' :
    data = pd.read_csv('sorted_data.csv')
    option = st.selectbox('See Performance', ['See Your Performance','Search by Roll No', 'Search by Rank'])
    
    if option == 'Search by Roll No':
        st.info('Enter Enrolment No. to search result without space and in capital letter')
        enrolment_no = st.text_input('Enter Your Enrolment No')
        student = data[data['Enrolment No'] == enrolment_no]
        st.success(f'''**Name** : {student['Branch']}''')

# yet to complete frontend