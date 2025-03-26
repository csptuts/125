import streamlit as st
import pandas as pd

def uploader():
    uploaded_files = st.file_uploader(
        "Choose a CSV file", accept_multiple_files=True
    )
    for uploaded_file in uploaded_files:
        # bytes_data = uploaded_file.read()
        # st.write("filename:", uploaded_file.name)
        # st.write(bytes_data)
        if uploaded_file.name == "weekly.csv":
            # uploaded_file.seek(0)
            dfW = pd.read_csv(uploaded_file)
            # st.dataframe(dfW)
        if uploaded_file.name == "125m.csv":
            # uploaded_file.seek(0)
            df125_0 = pd.read_csv(uploaded_file)
            # st.dataframe(df125_0)
        if uploaded_file.name == "25m.csv":
            # uploaded_file.seek(0)
            df25_0 = pd.read_csv(uploaded_file)
            # st.dataframe(df25_0)
