import pandas as pd
from datetime import timedelta
from icecream import ic


class clean_df:

  def __init__(self,df: pd.DataFrame,mod_time: int):
    self.df = df
    self.mod_time = mod_time

  def pass_over_new(self,df_: pd.DataFrame) -> pd.DataFrame:
    """ passes over every row and ensures that the end of the last activity is the start of the next activity """
    for i,row in df_.iterrows():
        try:
          if df_.at[i,'EndDatetime'] != df_.at[i+1,'BeginDatetime']:
            df_.at[i,'EndDatetime'] = df_.at[i+1,'BeginDatetime']
        except:
          df_.at[i,'EndDatetime'] = df_.at[i,'EndDatetime'] + timedelta(seconds=self.mod_time)
    return df_


  def clean_dataframe(self) -> pd.DataFrame:
    """ a beautiful cleaning function that will merge consecutive activities to reduce redundancy """
    df = self.df
    df['datetime'] = pd.to_datetime(df['datetime'])
    group_term = ([(df.activity != df.activity.shift()).cumsum()])
    consec = pd.DataFrame({'BeginDatetime' : df.groupby(group_term).datetime.first(),
                  'EndDatetime' : df.groupby(group_term).datetime.last(),
                  'activity' : df.groupby(group_term).activity.first()}).reset_index(drop=True)
    df_consec = self.pass_over_new(consec)
    return df_consec
