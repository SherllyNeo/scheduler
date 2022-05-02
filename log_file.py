import pandas as pd
import os.path
from icecream import ic
from datetime import datetime, timedelta
import math
import numpy as np
import clean
import estimate_class
from pathlib import Path

#debug mode is ic.enable() which will print out all the ic statements
ic.enable()



class log_files:

    def __init__(self):
        """ init with useful paths and variables that are needed in the class scope """
        self.path_to_dirty_logs =  r"log_files/log_files/logs.csv"
        self.path_to_clean_logs =  r"log_files/log_files_cleaned/clean_logs.csv"
        self.dirty_logs = pd.DataFrame({'activity':[],'datetime':[]})
        self.clean_logs = pd.DataFrame({'activity':[],'BeginDatetime':[],'EndDatetime':[]})
        self.est = dict()
        self.def_time = 1

    def refresh_logs(self):
        """ refreshes the log dataframes so that estimates are accurate """
        date_parser = lambda date: pd.to_datetime(date)
        self.dirty_logs = pd.read_csv(self.path_to_dirty_logs).dropna()
        self.clean_logs = pd.read_csv(self.path_to_clean_logs).dropna()
        self.dirty_logs['datetime'] = pd.to_datetime(self.dirty_logs['datetime'])
        self.clean_logs['BeginDatetime'] = pd.to_datetime( self.clean_logs['BeginDatetime'] )
        self.clean_logs['EndDatetime'] = pd.to_datetime( self.clean_logs['EndDatetime'] )


    def check_exist(self):
        """ Checks that the log_files and exists and makes them if they do not """

        path_to_valid_times = r"./log_files/valid_times/valid_times.json"

        if not os.path.exists(r"./log_files"):
            os.makedirs(r"./log_files")

        if not os.path.exists(r"./log_files/log_files"):
            os.makedirs(r"./log_files/log_files")

        if not os.path.exists(r"./log_files/log_files_cleaned"):
            os.makedirs(r"./log_files/log_files_cleaned")

        if not os.path.exists(r"./log_files/valid_times"):
            os.makedirs(r"./log_files/valid_times")

        if not os.path.isfile(path_to_valid_times):

            valid_times = dict(monday=1,tuesday=1,wednesday=1,thursday=1,friday=1,saturday=1,sunday=1,start_time="0",end_time="24")


            with open(path_to_valid_times,"w+") as writer:
                writer.write(str(valid_times))
                ic("added default valid times to logs")



        if not os.path.isfile(self.path_to_dirty_logs):
            ic("dirty logs don't exist!")
            df_dirty_log = pd.DataFrame({'datetime':[],'activity':[]})
            df_dirty_log.to_csv(self.path_to_dirty_logs,index=False)
            ic("saved a blank dirty log file")

        if not os.path.isfile(self.path_to_clean_logs):
            ic("clean logs don't exist!")
            df_clean_log = pd.DataFrame({'activity':[],'BeginDatetime':[],'EndDatetime':[]})
            df_clean_log.to_csv(self.path_to_clean_logs,index=False)
            ic("saved a blank clean log file")

        self.refresh_logs()
        if len(self.dirty_logs) == 0:
            ic("currently no logs, some features may not work")


    def print_logs(self):
        """ displays datafrane logs """
        print(self.dirty_logs)
        print(self.clean_logs)

    def add_log_to_file(self,activity: str):
        """ adds and activity to the dirty log file and refreshes the logs """
        new_row = pd.DataFrame({

                'datetime':[datetime.now()],
                'activity':[activity]

                })
        ic(f"concating {new_row}")
        dirty_logs = pd.concat([self.dirty_logs,new_row])
        dirty_logs.to_csv(self.path_to_dirty_logs,index=False)
        self.refresh_logs()

    def set_inactive(self):
        """ used when the time is invalid - sets the inactive activity """
        last_activity = str()
        try:
            last_activity = self.dirty_logs.tail(1)['activity'].values[0]
        except:
            last_activity = ""
        if last_activity == "inactive":
            return
        else:
            self.add_log_to_file("inactive")

    def find_consecutive_values(self,df: pd.DataFrame) -> pd.DataFrame:
        """ calls the dataframe cleaning function that turns the two column time series long format into a 3 column wide format to easily find how long each task took in the past """
        cleaner = clean.clean_df(df,self.def_time)
        consec_frame = cleaner.clean_dataframe()
        ic(f"when cleaning dirty logs produced {consec_frame}")

        return consec_frame


    def dirty_to_clean(self):

        """ unoptimised - would be more efficient to only clean the section since it was last called.
            turns dirty logs into clean logs using the find_consecutive_values method and saves them to the cleaned log folder
        """
        ic("CLEANING DIRTY LOGS INTO CLEAN")
        cleaned_dataframe = self.find_consecutive_values(self.dirty_logs)
        cleaned_dataframe.to_csv(self.path_to_clean_logs,index=False)
        self.refresh_logs

    def make_activity_dict(self,df_: pd.DataFrame) -> dict:
        """ turns the clean logs file into a dictionary of activities and their estimate length """
        estimator = estimate_class.lower_bound_confidence_estimate(df_)
        activity_time_est = estimator.main()
        activity_time_est['inactive'] = 15
        activity_time_est['nothing'] = 15
        ic(activity_time_est)
        with open(r"activity.json","w+") as w:
            w.write(str(activity_time_est))
        return activity_time_est

    def get_last_activity(self) -> str:
        self.check_exist()
        last_activity = str()
        try:
            last_activity = self.dirty_logs.tail(1)['activity'].values[0]
        except:
            last_activity  = "nothing"
        return last_activity

    def check_if_something_is_happening(self) -> bool:
        """ checks if an activity is currently happening by looking at the last activity and adding on a time estimate if it exists or an arbitary amount of time if it does not """
        if len(self.dirty_logs) == 0:
            return False


        last_activity = self.dirty_logs.tail(1)['activity'].values[0]
        last_time_recorded = pd.to_datetime(self.dirty_logs.tail(1)['datetime']).values[0].astype('M8[ms]').astype('O')

        self.refresh_logs()
        activity_dict = self.make_activity_dict(self.clean_logs)

        ic(last_activity,activity_dict)
        if last_activity in activity_dict:
            ic("activity has been found previously")
            end_of_task_est = timedelta(seconds = activity_dict[last_activity])+last_time_recorded
            if not datetime.now()>=end_of_task_est:
                ic(f"current activity has an estimate of {activity_dict[last_activity]} seconds")
                ic(f"currently there is an activity going on that will end at {end_of_task_est}")
                return True
            else:
                ic("currently there is no activity going on")
                return False


        else:
            ic("this activity is new")
            end_of_task_est = timedelta(seconds = self.def_time)+last_time_recorded
            if not datetime.now()>=end_of_task_est:
                ic(f"currently there is an activity going on that will end at {end_of_task_est}")
                return True
            else:
                ic("currently there is no activity going on")
                return False
