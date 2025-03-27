import streamlit as st
import pandas as pd 

data = {
"UNIXTS":[1672406700,1672408200,1672409700,1672411200,1672412700],
"Open":[18195.65,18196.8,18198.65,18174,18087.2],
"High":[18218.4,18201.95,18199.85,18206.7,18120.1],
"Low":[18193.85,18164.95,18162.7,18080.9,18081.05],
"Close":[18197.05,18199.45,18173.95,18088.05,18117.05],
"SMA50":[18121.58,18124.46,18127.08,18128.28,18129.21],
"TS-GMT":["Fri Dec 30 2022 13:25:00","Fri Dec 30 2022 13:50:00","Fri Dec 30 2022 14:15:00","Fri Dec 30 2022 14:40:00","Fri Dec 30 2022 15:05:00"],
"IsoWeekNum":[52,52,52,52,52],
"RSI":[52.36,52.36,52.36,52.36,52.36],
"PP":[18025.68,18025.68,18025.68,18025.68,18025.68],
"R1":[18270.92,18270.92,18270.92,18270.92,18270.92],
"S1":[17578.87,17578.87,17578.87,17578.87,17578.87],
"R2":[18717.73,18717.73,18717.73,18717.73,18717.73],
"S2":[17333.63,17333.63,17333.63,17333.63,17333.63],
"40rsi":[40,40,40,40,40],
"60rsi":[60,60,60,60,60]
}

df0 = pd.DataFrame(data)




if 'df1' not in st.session_state:
    st.session_state.df1 = df0

empty_df = pd.DataFrame(columns = ['TS-GMT'])

if 'weekly_df_subset' not in st.session_state:
    st.session_state.weekly_df_subset = empty_df

if 'df2' not in st.session_state:
    st.session_state.df2 = 0    

if 'row_num' not in st.session_state:
    st.session_state.row_num = 0


# if 'switch' not in st.session_state:
#     st.session_state.switch = 'hide'

if 'total_rows' not in st.session_state:
    st.session_state.total_rows = 0

if 'dfW_0' not in st.session_state:
    st.session_state.dfW_0 = 0

if 'df125_0' not in st.session_state:
    st.session_state.df125_0 = 0

if 'df25_0' not in st.session_state:
    st.session_state.df25_0 = 0        
