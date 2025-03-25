import streamlit as st
import pandas as pd
from streamlit_shortcuts import button, add_keyboard_shortcuts

from files.wops import get_unixts
from files.coredf import get_df25, get_df125
import files.sessionvars
from files.plotlyfig import chart_25, show_initial_chart

# st.title('Hello')
with st.sidebar:
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

with st.sidebar:
    with st.form("my_form"):
        st.write("Inside the form")
        d = st.text_input("Enter date")
        m = st.text_input("Enter month")
        y = st.text_input("Enter Year")
        

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(d,m,y)
            d=int(d)
            m=int(m)
            y=int(y)
            sorted_df=get_unixts(d,m,y,dfW)
            sorted_df1=sorted_df[["TS-GMT","UNIXTS"]]
            st.dataframe(sorted_df1)





with st.sidebar:
    with st.form("my_form-1"):
        st.write("Inside the form")
        wk_unxts = st.text_input("Enter UNIXTS")
        

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(wk_unxts)
            wk_unxts=int(wk_unxts)
            df25=get_df25(wk_unxts,df25_0)
            df125=get_df125(wk_unxts,df125_0)
            plot_data=pd.merge_asof(df25,df125,left_index=True,right_index=True)
            plot_data['60rsi'] = 60
            plot_data['40rsi'] = 40
            unique_values = plot_data['IsoWeekNum'].unique()
            st.write(unique_values)
            wa=unique_values[0]
            wb=unique_values[1]
            grp=plot_data.groupby('IsoWeekNum')
            grpa=grp.get_group(wa)
            grpb=grp.get_group(wb)
            ia=grpa.index[0]
            ib=grpb.index[0]
            if ia>ib:
                st.session_state.df1=grpb
                st.session_state.df2=grpa
            else:
                st.session_state.df1=grpa
                st.session_state.df2=grpb
            st.session_state.switch ='show'
            # st.session_state.df25=get_df25(wk_unxts,df25_0)
            # st.session_state.df125=get_df125(wk_unxts,df125_0)
            # sorted_df1=sorted_df[["TS-GMT","UNIXTS"]]
            # st.dataframe(sorted_df1)




# if st.button("Initialise"):
#     # st.dataframe(st.session_state.df1)
#     # st.dataframe(st.session_state.df2)
#     fig=chart_25(st.session_state.df1)
#     st.plotly_chart(fig)

def greet():
    st.session_state.total_rows= len(st.session_state.df2)
    # st.write(st.session_state.total_rows)
    st.session_state.row_num = st.session_state.row_num + 1
    if st.session_state.row_num <= st.session_state.total_rows:
        sliced_df = st.session_state.df2.head(st.session_state.row_num)
        plot_df=pd.concat([st.session_state.df1,sliced_df], axis=0)
        last_row = sliced_df.iloc[-1]
        rsi=last_row.get(key = 'RSI') 
        st.write(rsi)
        fig=chart_25(plot_df)
        st.plotly_chart(fig)
    else:
       if st.button("Reset"):
           st.session_state.row_num=0

button("Forward", "ArrowRight", greet)

# if st.button("Forward" , ):
#     # st.dataframe(st.session_state.df1)
#     # st.dataframe(st.session_state.df2)
#     # fig=chart_25(st.session_state.df1)
#     # st.plotly_chart(fig)
#     st.write('Hello')
#     st.session_state.total_rows= len(st.session_state.df2)
#     st.write(st.session_state.total_rows)
#     st.session_state.row_num = st.session_state.row_num + 1
#     if st.session_state.row_num <= st.session_state.total_rows:
#         sliced_df = st.session_state.df2.head(st.session_state.row_num)
#         plot_df=pd.concat([st.session_state.df1,sliced_df], axis=0)
#         fig=chart_25(plot_df)
#         st.plotly_chart(fig)
#     else:
#         st.stop()


with st.container():
    if st.session_state.switch =='show':
        show_initial_chart()
        st.session_state.switch ='hide'


with st.sidebar:
    if st.button("Reset"):
       st.session_state.row_num=0 
