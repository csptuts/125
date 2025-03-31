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
  df125_0.rename(columns={'RSI': 'RSI125'}, inplace=True)
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df125 = df125_0[(df125_0['UNIXTS'] >= minus) & (df125_0['UNIXTS'] < plus)]
  df125.set_index('UNIXTS', inplace=True)
  df125=df125[["RSI125", "PP", "R1", "S1", "R2", "S2", ]]
  df125_cp = df125.copy()
  df125_cp['RSI125'] = df125_cp['RSI125'].shift(1)
  df125=df125_cp.copy()
  df125.dropna(inplace=True)
  return df125

def get_df75(wk_unxts, df75_0):
  df75_0.rename(columns={'RSI': 'RSI75'}, inplace=True)
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df75 = df75_0[(df75_0['UNIXTS'] >= minus) & (df75_0['UNIXTS'] < plus)]
  df75.set_index('UNIXTS', inplace=True)
  df75=df75[["RSI75", "Delta"]]
  df75_cp = df75.copy()
  df75_cp['RSI75'] = df75_cp['RSI75'].shift(1)
  df75=df75_cp.copy()
  df75.dropna(inplace=True)
  return df75    
    
    
def chart_25(df):
    
    #get last row in Data Frame as df
    last_row = df.iloc[-1:]
    #get last row in Data Frame as Series
    last_row_s = df.iloc[-1]
    
    last_rsi_75 =last_row_s.get(key = 'RSI75')
    last_rsi_125 =last_row_s.get(key = 'RSI125')
    # last_pp =last_row.get(key = 'PP')
    # last_r1 =last_row.get(key = 'R1')
    # last_r2 =last_row.get(key = 'R2')
    # last_s1 =last_row.get(key = 'S1')
    # last_s2 =last_row.get(key = 'S2')
    last_close =last_row_s.get(key = 'Close')
    last_delta = last_row_s.get(key= "Delta")

    fig = make_subplots(rows=4, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        row_heights=[1,0.2,0.2,0.2]
    )

 
    fig.add_trace(go.Candlestick(x=df['TS-GMT'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], 
                name="OHLC"),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=last_row['TS-GMT'],# if you use last_row['TS-GMT'] you will get last value
                             y=last_row['Close'],
                             marker=dict(color='black',size=8),
                             mode="text",
                             textfont=dict(color='black', size=12),
                             textposition='top right',
                             text=last_close,
                             name="Close"),
                             row=1, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['PP'],
                             marker=dict(color='black',size=8),
                             mode="markers",
                             name="PP"),
                            row=1, col=1)
    
    # fig.add_trace(go.Scatter(x=df['TS-GMT'],
    #                          y=last_pp,
    #                          marker=dict(color='black',size=8),
    #                          mode="markers+text",
    #                          name="PPtext"),
    #                         row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['R1'],
                             marker=dict(color='orange',size=8),
                             mode="markers",
                             name="R1"),
                             row=1, col=1)
    
    # fig.add_trace(go.Scatter(x=df['TS-GMT'],
    #                          y=last_r1,
    #                          marker=dict(color='orange',size=8),
    #                          mode="markers+text",
    #                          name="R1text"),
    #                          row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['R2'],
                             marker=dict(color='orange',size=8),
                             mode="markers",
                             name="R2"),
                             row=1, col=1)
    
    # fig.add_trace(go.Scatter(x=df['TS-GMT'],
    #                          y=last_r2,
    #                          marker=dict(color='orange',size=8),
    #                          mode="markers+text",
    #                          name="R2text"),
    #                          row=1, col=1)
    
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
                             y=df['RSI75'],
                             marker=dict(color='darkturquoise',size=4),
                             mode="lines+markers",
                             name="RSI75"),
                             row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=last_row['RSI75'],
                             marker=dict(color='red',size=2),
                             mode="text",
                             text=last_rsi_75,
                             textfont=dict(color='black', size=12),
                             textposition='middle center',
                             name="RSI75text"),
                             row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['60rsi'],
                             line=dict(color='firebrick', width=0.5,dash='dash')),
    row=2, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['40rsi'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=2, col=1)
    
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['RSI125'],
                             marker=dict(color='crimson',size=4),
                             mode="lines+markers",
                             name="RSI125"),
                             row=3, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=last_row['RSI125'],
                             marker=dict(color='red',size=2),
                             mode="text",
                             text=last_rsi_125,
                             textfont=dict(color='black', size=12),
                             textposition='middle center',
                             name="RSI125text"),
                             row=3, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['60rsi'],
                             line=dict(color='aquamarine', width=1,dash='dash')),
    row=3, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['40rsi'], 
                             line=dict(color='aquamarine', width=1,dash='dash')),
    row=3, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['Delta'],
                             marker=dict(color='blue',size=4),
                             mode="lines+markers",
                             name="Delta"),
                             row=4, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=last_row['Delta'],
                             marker=dict(color='red',size=2),
                             mode="text",
                             text=last_delta,
                             textfont=dict(color='black', size=12),
                             textposition='middle center',
                             name="lastDelta"),
                             row=4, col=1)
    
    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['10p'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=4, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['10m'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=4, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['20p'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=4, col=1)

    fig.add_trace(go.Scatter(x=df['TS-GMT'],
                             y=df['20m'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=4, col=1)

    fig.update_yaxes(title_text="RSI 75", row=2, col=1)
    fig.update_yaxes(title_text="RSI 125", row=3, col=1)
    fig.update_yaxes(title_text="Delta", row=4, col=1)

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
            if uploaded_file.name == "75m.csv":
                df75_0 = pd.read_csv(uploaded_file)    

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
            df75=get_df75(wk_unxts, df75_0)

            plot_data_0=pd.merge_asof(df25,df125,left_index=True,right_index=True)
            plot_data=pd.merge_asof(plot_data_0,df75,left_index=True,right_index=True)
            # st.dataframe(plot_data)
            plot_data['60rsi'] = 60
            plot_data['40rsi'] = 40
            plot_data['20p'] = 20
            plot_data['10p'] = 10
            plot_data['10m'] = -10
            plot_data['20m'] = -20
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
        # last_row = sliced_df.iloc[-1]
        # rsi=last_row.get(key = 'RSI') 
        # st.write(rsi)
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
