import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def chart_rsi():
    df=st.session_state.sliced_df
    df=df.tail(50)
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0.01,
                        row_heights=[1,0.1]
    )
    
    fig.add_trace(
    go.Candlestick(x=df['OriginalTimeStamp'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']),
    row=1, col=1)

    fig.add_trace(go.Scatter(x=df['OriginalTimeStamp'],
                             y=df['SMA21'],
                             line=dict(color='black', width=0.5)
                            ),
    row=1, col=1)

    fig.add_trace(go.Scatter(x=df['OriginalTimeStamp'],
                             y=df['RSI'],
                             line=dict(color='green', width=2)
                            ),
    row=2, col=1)

    fig.add_trace(go.Scatter(x=df['OriginalTimeStamp'],
                             y=df['60rsi'],
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=2, col=1)

    fig.add_trace(go.Scatter(x=df['OriginalTimeStamp'],
                             y=df['40rsi'], 
                             line=dict(color='firebrick', width=1,dash='dash')),
    row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(height=800, width=1200)
    fig.update_yaxes(dtick=100)
    fig.update_layout(showlegend=False)

    return fig
