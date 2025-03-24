def get_df25(wk_unxts,df25):
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df25 = df25[(df25['UNIXTS'] >= minus) & (df25['UNIXTS'] < plus)]
  df25.set_index('UNIXTS', inplace=True)
  return df25

def get_df125(wk_unxts,df125):
  plus=wk_unxts+604800
  minus=wk_unxts-604800
  df125 = df125[(df125['UNIXTS'] >= minus) & (df125['UNIXTS'] < plus)]
  df125.set_index('UNIXTS', inplace=True)
  df125=df125[["RSI", "PP", "R1", "S1", "R2", "S2", ]]
  df125_cp = df125.copy()
  df125_cp['RSI'] = df125_cp['RSI'].shift(1)
  df125=df125_cp.copy()
  df125.dropna(inplace=True)
  return df125
