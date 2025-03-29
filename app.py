import streamlit as st
import pandas as pd
from streamlit_shortcuts import button, add_keyboard_shortcuts
import datetime
import time
import textwrap
import plotly.graph_objects as go
from plotly.subplots import make_subplots

empty_df = pd.DataFrame(columns = ['TS-GMT'])

if 'weekly_df_subset' not in st.session_state:
    st.session_state.weekly_df_subset = empty_df

if 'dfPrevWk' not in st.session_state:
    st.session_state.dfPrevWk = 0

if 'dfCurrentWk' not in st.session_state:
    st.session_state.dfCurrentWk = 0    

if 'row_num' not in st.session_state:
    st.session_state.row_num = 0

if 'total_rows' not in st.session_state:
    st.session_state.total_rows = 0


def get_unixts(dmy,dfW_0):
    lst=textwrap.wrap(dmy,2)
    d=int(lst[0])
    m=int(lst[1])
    y=int("20"+lst[2])
    date_time = datetime.datetime(y, m, d)
    ut=time.mktime(date_time.timetuple())
    df_closest5 = dfW_0.iloc[(dfW_0['UNIXTS']-ut).abs().argsort()[:8]]
    sorted_df = df_closest5.sort_values(by=['UNIXTS'], ascending=True)
    return sorted_df
    
    
def get_df25(wk_unxts, df25_0):
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df25 = df25_0[(df25_0['UNIXTS'] >= minus) & (df25_0['UNIXTS'] < plus)]
  df25.set_index('UNIXTS', inplace=True)
  return df25

def get_df125(wk_unxts, df125_0):
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df125 = df125_0[(df125_0['UNIXTS'] >= minus) & (df125_0['UNIXTS'] < plus)]
  df125.set_index('UNIXTS', inplace=True)
  df125=df125[["RSI", "PP", "R1", "S1", "R2", "S2", ]]
  df125_cp = df125.copy()
  df125_cp['RSI'] = df125_cp['RSI'].shift(1)
  df125=df125_cp.copy()
  df125.dropna(inplace=True)
  return df125
    
    
    
def chart_25(df):
    
  
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0.01,
                        row_heights=[1,0.1]
    )

 
    fig.add_trace(go.Candlestick(x=df['TS-GMT'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], 
                name="OHLC"),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['PP'],
                             marker=dict(color='black',size=8),
                             mode="markers",
                             name="PP"),
                            row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['R1'],
                             marker=dict(color='orange',size=8),
                             mode="markers",
                             name="R1"),
                             row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['R2'],
                             marker=dict(color='orange',size=8),
                             mode="markers",
                             name="R2"),
                             row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['S1'],
                             marker=dict(color='green',size=8),
                             mode="markers",
                             name="S1"),
                             row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['S2'],
                             marker=dict(color='green',size=8),
                             mode="markers",
                             name="S2"),
                             row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['SMA50'],
                             marker=dict(color='blue',size=4),
                             name="SMA50"),
                             row=1, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['RSI'],
                             marker=dict(color='blue',size=4),
                             mode="markers",
                             name="RSI"),
                             row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['60rsi'],
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=2, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['40rsi'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=2, col=1)
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(height=800, width=1200)
    fig.update_yaxes(dtick=100)
    fig.update_layout(showlegend=False)

    return fig



with st.sidebar:
    uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            if uploaded_file.name == "weekly.csv":
                dfW_0 = pd.read_csv(uploaded_file)
            if uploaded_file.name == "125m.csv":
                df125_0 = pd.read_csv(uploaded_file)
            if uploaded_file.name == "25m.csv":
                df25_0 = pd.read_csv(uploaded_file)

with st.sidebar:
    with st.form("date_input"):
        dmy = st.text_input("Enter date - in ddmmyy format")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            weekly_df_subset=get_unixts(dmy, dfW_0)
            st.session_state.weekly_df_subset = weekly_df_subset
        

with st.sidebar:
    with st.form("Create Dropdown"):
        dfy=st.session_state.weekly_df_subset
        selected_dt = st.selectbox('Select Week:', dfy[["TS-GMT"]])
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            dt_str=str(selected_dt)
            dfx=st.session_state.weekly_df_subset.loc[st.session_state.weekly_df_subset['TS-GMT'] == dt_str]
            last_row = dfx.iloc[-1]
            wk_unxts=last_row.get(key = 'UNIXTS')
            
            wk_unxts=int(wk_unxts)
            df25=get_df25(wk_unxts, df25_0)
            df125=get_df125(wk_unxts, df125_0)
            plot_data=pd.merge_asof(df25,df125,left_index=True,right_index=True)
            plot_data['60rsi'] = 60
            plot_data['40rsi'] = 40
            unique_values = plot_data['IsoWeekNum'].unique()
            wa=unique_values[0]
            wb=unique_values[1]
            grp=plot_data.groupby('IsoWeekNum')
            grpa=grp.get_group(wa)
            grpb=grp.get_group(wb)
            ia=grpa.index[0]
            ib=grpb.index[0]
            if ia>ib:
                st.session_state.dfPrevWk=grpb
                st.session_state.dfCurrentWk=grpa
            else:
                st.session_state.dfPrevWk=grpa
                st.session_state.dfCurrentWk=grpb
            
def initialise():
    if st.session_state.row_num < 1:
        fig=chart_25(st.session_state.dfPrevWk)
        st.plotly_chart(fig)
        
with st.sidebar:
    button("Init", "Ctrl+ArrowRight", initialise)


def simulate():
    st.session_state.total_rows= len(st.session_state.dfCurrentWk)
    st.session_state.row_num = st.session_state.row_num + 1
    if st.session_state.row_num <= st.session_state.total_rows:
        sliced_df = st.session_state.dfCurrentWk.head(st.session_state.row_num)
        plot_df=pd.concat([st.session_state.dfPrevWk,sliced_df], axis=0)
        last_row = sliced_df.iloc[-1]
        rsi=last_row.get(key = 'RSI') 
        st.write(rsi)
        fig=chart_25(plot_df)
        st.plotly_chart(fig)
        
with st.sidebar:
    button("Forward", "ArrowRight", simulate)


with st.sidebar:
    if st.button("Reset"):
        
        empty_df = pd.DataFrame(columns = ['TS-GMT'])
        if 'weekly_df_subset' not in st.session_state:
            st.session_state.weekly_df_subset = empty_df
        else:
            st.session_state.weekly_df_subset = empty_df

        if 'dfPrevWk' not in st.session_state:
            st.session_state.dfPrevWk = 0
        else:
            st.session_state.dfPrevWk = 0

        if 'dfCurrentWk' not in st.session_state:
            st.session_state.dfCurrentWk = 0
        else:
            st.session_state.dfCurrentWk = 0

        if 'row_num' not in st.session_state:
            st.session_state.row_num = 0
        else:
            st.session_state.row_num=0 

        if 'total_rows' not in st.session_state:
            st.session_state.total_rows = 0
        else:
            st.session_state.total_rows = 0
