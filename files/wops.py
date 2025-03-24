import datetime
import time

def get_unixts(d,m,y,dfW):
    
    date_time = datetime.datetime(y, m, d)
    ut=time.mktime(date_time.timetuple())
    df_closest5 = dfW.iloc[(dfW['UNIXTS']-ut).abs().argsort()[:8]]
    sorted_df = df_closest5.sort_values(by=['UNIXTS'], ascending=True)
    sorted_df=sorted_df[["TS-GMT","UNIXTS"]]
    sorted_df['TS_diff'] = sorted_df['UNIXTS'].diff()
    return sorted_df
    
