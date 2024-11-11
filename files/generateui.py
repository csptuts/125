import streamlit as st
import pandas as pd
import numpy as np

def slice_df():
    
    df=st.session_state.base_df
    sliced_df=df.loc[df['DateTime'] <= st.session_state.datetime_counter]
    
    st.session_state.sliced_df =sliced_df

def candle_start_end(hhmmss):
    if hhmmss == '09:15:00':
        hhmmss = '11:20:00'
    elif hhmmss == '11:20:00':
        hhmmss = '13:25:00'
    elif hhmmss == '13:25:00':
        hhmmss = '15:30:00'    

    return hhmmss

def rsi_strength(rsi):
    rsi =float(rsi)
    if 40 <= rsi <= 60:
        condition='Sideways'
    if rsi > 60:
        condition='Bullish'    
    if rsi > 70:
        condition='Strong Bullish'
    if rsi > 80:
        condition='Over Bought'
    if rsi < 40:
        condition='Bearish'
    if rsi < 30:
        condition='Strong Bearish'
    if rsi < 20:
        condition='Over Sold'
    
    return condition

def get_text_data():
    
    df=st.session_state.sliced_df.tail(1)

    st.dataframe(df)
    original_timestamp=str(df.iloc[0]['OriginalTimeStamp'])
    original_timestamp = original_timestamp[:15]
    
    rsi_value = str(df.iloc[0]['RSI']) 
    market_condition = rsi_strength(rsi_value)
    candle_start_time=str(df.iloc[0]['Time'])
    current_time = candle_start_end(candle_start_time)

    return original_timestamp,rsi_value,current_time, market_condition 

    
