import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

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


def show_initial_chart():
    fig=chart_25(st.session_state.df1)
    st.plotly_chart(fig)
