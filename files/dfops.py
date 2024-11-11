import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta

def rename_columns(df):
    
    df.rename(columns={'Date': 'OriginalTimeStamp'}, inplace=True)

    df.rename(columns={ df.columns[5]: "RSI" }, inplace=True)
    df.rename(columns={ df.columns[6]: "SMA21" }, inplace=True)

    return df


def split_timestamp_column(df):

    df['SplitOriginalTimeStamp'] = df['OriginalTimeStamp'].map(lambda a: a.split())
    df['OriginalTimeStamp'] = df['OriginalTimeStamp'].str.replace(' GMT+0530 (India Standard Time)', '')
    
    return df

def add_columns(df):
    
    df['DayofWeek']=df['SplitOriginalTimeStamp'].map(lambda x:x[0]) 
    df['FullDate'] = df['SplitOriginalTimeStamp'].map(lambda x:x[1]+x[2]+x[3])  
    df["FullDate"] =  pd.to_datetime(df["FullDate"], format="%b%d%Y")
    df['FullDate'] = df['FullDate'].dt.date

    df['Time'] = df['SplitOriginalTimeStamp'].map(lambda x:x[4])
    df['DateTime'] = df['SplitOriginalTimeStamp'].map(lambda x:x[1]+'-'+x[2]+'-'+x[3]+' ' +x[4])
    df['DateTime'] =  pd.to_datetime(df["DateTime"], format="%b-%d-%Y %H:%M:%S")


    df['60rsi'] = 60
    df['40rsi'] = 40
    
    return df


def trim_df(df):

    df_a=df.loc[df['FullDate'] <= st.session_state.end_date] 
    rows_start=st.session_state.start_date + timedelta(days=-45)
    df=df_a.loc[df_a['FullDate'] > rows_start]
    
    return df


def reset_idex(df):
    df.reset_index(inplace=True)
    return df




def get_row_numbers(df):
    filter_in_df = df[(df['FullDate'] == st.session_state.start_date) & (df['Time'] == '09:15:00') ]
    st.session_state.start_idx = filter_in_df.index.to_list()[0]
    filter_in_df=df.tail(1)
    st.session_state.end_idx = filter_in_df.index.to_list()[0]

    st.session_state.first_idx = 1
