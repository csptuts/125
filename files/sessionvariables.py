import streamlit as st
st.set_page_config(layout="wide")

# Start and end dates
if 'start_date' not in st.session_state:
    st.session_state.start_date = 0

if 'end_date' not in st.session_state:
    st.session_state.end_date = 0

####  row indexes #####



if 'end_idx' not in st.session_state:
    st.session_state.end_idx = 0

if 'first_idx' not in st.session_state:
    st.session_state.first_idx = 0

###### counters #########
# counter variable
if 'counter_list' not in st.session_state:
    st.session_state.counter_list = 0

# Initialize the current index
if "counter_clicks" not in st.session_state:
    st.session_state.counter_clicks = 0

# # Initialize the current index
if "datetime_counter" not in st.session_state:
    st.session_state.datetime_counter = 0




# trimmed dataframes with rows dropped when start date and end dates are provided 
if 'base_df' not in st.session_state:
    st.session_state.base_df = 0

if 'sliced_df' not in st.session_state:
    st.session_state.sliced_df = 0    

if 'stp' not in st.session_state:
    st.session_state.stp = 0
