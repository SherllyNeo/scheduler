import pandas as pd
import math

class lower_bound_confidence_estimate:
  def __init__(self,df):
    self.df = df

  def get_time_deltas(self):
    deltas = self.df['EndDatetime']-self.df['BeginDatetime']
    seconds_deltas = deltas
    self.df['seconds_deltas'] = seconds_deltas.dt.total_seconds()

  def filter_deltas(self,_activity):
    activity_rows = self.df.copy()[self.df.activity == _activity]
    deltas_for_activity = activity_rows.seconds_deltas
    return deltas_for_activity

  def estimate_for_each(self):
    estimation_dict = dict()
    for activity in self.df.activity.unique():
      deltas_for_activity = self.filter_deltas(activity)
      estimation_dict[activity] = deltas_for_activity.mean() - (deltas_for_activity.std(ddof=0)/math.sqrt(len(deltas_for_activity)))
    return estimation_dict


  def main(self):
    self.get_time_deltas()
    activity_dict = self.estimate_for_each()
    return activity_dict
