import streamlit as st
import pandas as pd
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'stp' not in st.session_state:
    st.session_state.stp = 0    
import files.sessionvariables
from files.dfops import rename_columns, split_timestamp_column, add_columns
from files.dfops import trim_df,reset_idex,get_row_numbers
from files.plotlyfig import chart_rsi
from files.generateui import slice_df, get_text_data
from files.counter import make_date_range_list, move_counter


with st.sidebar:
    
    uploaded_file_W = st.file_uploader("Upload W data file")
    
    if uploaded_file_W is not None:
        dfW = pd.read_csv(uploaded_file_W)

with st.sidebar:
    
    uploaded_file_125 = st.file_uploader("Upload 125 data file")
    
    if uploaded_file_125 is not None:
        df125 = pd.read_csv(uploaded_file_125)


with st.sidebar:
    
    uploaded_file_25 = st.file_uploader("Upload 25 data file")
    
    if uploaded_file_25 is not None:
        df25 = pd.read_csv(uploaded_file_25)

with st.sidebar:
    with st.form("my_form"):
        st.write("Inside the form")
        dd = st.text_input("Insert a number", value=None, placeholder="Type a date...")
        mm = st.text_input("Insert a number", value=None, placeholder="Type a month...")
        yy = st.text_input("Insert a number", value=None, placeholder="Type a year...")
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(dd,mm,yy)
    st.write("Outside the form")

# with st.sidebar:
    
#     uploaded_file = st.file_uploader("Upload 125min data file")
    
#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
        
#         df=rename_columns(df)
#         df=split_timestamp_column(df)
#         df=add_columns(df)
        
# with st.sidebar:
#     with st.form("Please Enter Dates"):
        
#         start_date = st.date_input("Start Date",value=None)
#         end_date = st.date_input("End Date",value=None)

#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit")
#         if submitted:
#             st.session_state.start_date = start_date
#             st.session_state.end_date = end_date

#             df=trim_df(df)
#             df=reset_idex(df)
#             st.session_state.base_df = df
#             make_date_range_list(df)
           

if st.button('Start Simulation'):
    move_counter()
    slice_df()
    if st.session_state.stp == 0:
        original_timestamp,rsi_value,current_time, market_condition = get_text_data()
        col1, col2 = st.columns([4, 1])
        fig=chart_rsi()
        with col1:
            st.plotly_chart(fig)
        with col2:
            st.metric("Date", original_timestamp)
            st.metric("Current Time", current_time)
            st.metric("RSI Value", rsi_value)
            st.metric("Market Condition", market_condition)
    else:
        st.header("End Date reached. Start Over")    
