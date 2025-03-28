import streamlit as st
import pandas as pd
from streamlit_shortcuts import button, add_keyboard_shortcuts

import files.sessionvars
from files.wops import get_unixts
from files.coredf import get_df25, get_df125
from files.plotlyfig import chart_25



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
        # st.write("Inside the form")
        dfy=st.session_state.weekly_df_subset
        # st.dataframe(dfy)
        selected_dt = st.selectbox('Select Week:', dfy[["TS-GMT"]])
        # wk_unxts = st.text_input("Enter UNIXTS")
        

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            # st.dataframe(dfy)
            dt_str=str(selected_dt)
            dfx=st.session_state.weekly_df_subset.loc[st.session_state.weekly_df_subset['TS-GMT'] == dt_str]
            last_row = dfx.iloc[-1]
            wk_unxts=last_row.get(key = 'UNIXTS')
            
            # st.write(wk_unxts)
            wk_unxts=int(wk_unxts)
            df25=get_df25(wk_unxts, df25_0)
            df125=get_df125(wk_unxts, df125_0)
            plot_data=pd.merge_asof(df25,df125,left_index=True,right_index=True)
            plot_data['60rsi'] = 60
            plot_data['40rsi'] = 40
            unique_values = plot_data['IsoWeekNum'].unique()
            # st.write(unique_values)
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
            # st.session_state.switch ='show'
            # st.session_state.df25=get_df25(wk_unxts,df25_0)
            # st.session_state.df125=get_df125(wk_unxts,df125_0)
            # sorted_df1=sorted_df[["TS-GMT","UNIXTS"]]
            # st.dataframe(sorted_df1)




def initialise():
    # st.session_state.total_rows= len(st.session_state.df2)
    # st.write(st.session_state.total_rows)
    # st.session_state.row_num = st.session_state.row_num + 1
    if st.session_state.row_num < 1:
        # sliced_df = st.session_state.df2.head(st.session_state.row_num)
        # plot_df=pd.concat([st.session_state.df1,sliced_df], axis=0)
        # last_row = sliced_df.iloc[-1]
        # rsi=last_row.get(key = 'RSI') 
        # st.write(rsi)
        fig=chart_25(st.session_state.dfPrevWk)
        st.plotly_chart(fig)
    # else:
    #     return
        
with st.sidebar:
    button("Init", "Ctrl+ArrowRight", initialise)


# if st.button("Initialise"):
#     # st.dataframe(st.session_state.df1)
#     # st.dataframe(st.session_state.df2)
#     fig=chart_25(st.session_state.df1)
#     st.plotly_chart(fig)

def simulate():
    st.session_state.total_rows= len(st.session_state.dfCurrentWk)
    # st.write(st.session_state.total_rows)
    st.session_state.row_num = st.session_state.row_num + 1
    if st.session_state.row_num <= st.session_state.total_rows:
        sliced_df = st.session_state.dfCurrentWk.head(st.session_state.row_num)
        plot_df=pd.concat([st.session_state.dfPrevWk,sliced_df], axis=0)
        last_row = sliced_df.iloc[-1]
        rsi=last_row.get(key = 'RSI') 
        st.write(rsi)
        fig=chart_25(plot_df)
        st.plotly_chart(fig)
    # else:
    #     return
        
with st.sidebar:
    button("Forward", "ArrowRight", simulate)

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


# with st.container():
#     show_initial_chart()
    
# with st.sidebar:
#     if st.button("Reset"):
#         st.session_state.row_num=0
with st.sidebar:
    if st.button("Reset"):
        
        empty_df = pd.DataFrame(columns = ['TS-GMT'])
        if 'weekly_df_subset' not in st.session_state:
            st.session_state.weekly_df_subset = empty_df

        if 'dfPrevWk' not in st.session_state:
            st.session_state.dfPrevWk = 0

        if 'dfCurrentWk' not in st.session_state:
            st.session_state.dfCurrentWk = 0    

        if 'row_num' not in st.session_state:
            st.session_state.row_num = 0


        # if 'switch' not in st.session_state:
        #     st.session_state.switch = 'hide'

        if 'total_rows' not in st.session_state:
            st.session_state.total_rows = 0

        st.session_state.row_num=0 
