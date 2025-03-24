import streamlit as st

if 'df1' not in st.session_state:
    st.session_state.df1 = 0

if 'df2' not in st.session_state:
    st.session_state.df2 = 0    

if 'row_num' not in st.session_state:
    st.session_state.row_num = 0


if 'switch' not in st.session_state:
    st.session_state.switch = 'hide'

if 'total_rows' not in st.session_state:
    st.session_state.total_rows = 0
