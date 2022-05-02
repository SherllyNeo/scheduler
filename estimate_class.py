import pandas as pd
import math

class lower_bound_confidence_estimate:
  def __init__(self,df):
    self.df = df

  def get_time_deltas(self):
    """ gets the lengths of time for every activity in the logs """
    deltas = self.df['EndDatetime']-self.df['BeginDatetime']
    seconds_deltas = deltas
    self.df['seconds_deltas'] = seconds_deltas.dt.total_seconds()

  def filter_deltas(self,_activity: str) -> pd.DataFrame:
    """ filters the deltas so that we only view the records for the activity we are trying to estimate a length for """
    activity_rows = self.df.copy()[self.df.activity == _activity]
    deltas_for_activity = activity_rows.seconds_deltas
    return deltas_for_activity

  def estimate_for_each(self) -> dict:
    """ for every activity we estimate how long it will take based on past records using the lower bound of the 95% confidence interval and then construct a dictionary for each activity and it's estimate """
    estimation_dict = dict()
    for activity in self.df.activity.unique():
        deltas_for_activity = self.filter_deltas(activity)
        est = deltas_for_activity.mean() - (deltas_for_activity.std(ddof=0)/math.sqrt(len(deltas_for_activity)))
        if (est<15) | len(deltas_for_activity)<5:
            est = 15
        estimation_dict[activity] = est
    return estimation_dict


  def main(self) -> dict:
    """ main function to make estimates for activities """
    self.get_time_deltas()
    activity_dict = self.estimate_for_each()
    return activity_dict
