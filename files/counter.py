import streamlit as st
import pandas as pd

def make_date_range_list(df):
   
    df_subset=df.loc[df['FullDate'] >= st.session_state.start_date]

    st.session_state.counter_list=df_subset['DateTime'].tolist()


def move_counter():
    my_list = st.session_state.counter_list
    st.session_state.datetime_counter = my_list[st.session_state.current_index]
    st.session_state.current_index += 1
