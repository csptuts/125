import streamlit as st
import datetime
import time
import textwrap

def get_unixts(dmy,dfW_0):
    # dfW = st.session_state.dfW_0
    lst=textwrap.wrap(dmy,2)
    d=int(lst[0])
    m=int(lst[1])
    y=int("20"+lst[2])
    date_time = datetime.datetime(y, m, d)
    ut=time.mktime(date_time.timetuple())
    df_closest5 = dfW_0.iloc[(dfW_0['UNIXTS']-ut).abs().argsort()[:8]]
    sorted_df = df_closest5.sort_values(by=['UNIXTS'], ascending=True)
    # sorted_df=sorted_df[["TS-GMT","UNIXTS"]]
    # sorted_df['TS_diff'] = sorted_df['UNIXTS'].diff()
    return sorted_df
    
