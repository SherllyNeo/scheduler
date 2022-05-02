from datetime import datetime,date,timedelta
import ast
PATH_TO_TIMES = r'./log_files/valid_times/valid_times.json'

def mapper(day_of_week):
    """ a small function to map the day of the week to it's number """
    lut_weekday = {
            'monday':0,
            'tuesday':1,
            'wednesday':2,
            'thursday':3,
            'friday':4,
            'saturday':5,
            'sunday':6,
            }
    return lut_weekday[day_of_week]

def filter_dict_for_valid_days(dic: dict(),dict_key: str) -> bool:
    """ a function used to filter out the valid days: 1 means valid, 0 means not """
    if dic[dict_key] == 1:
        return True
    else:
        return False

def valid_time() -> bool:
    """ uses above helper functions and data about todays date to find if the current time is valid for not """
    dt = date.today()
    today_from_midnight = (datetime.combine(dt, datetime.min.time()))
    now = datetime.today()
    day_today = now.weekday()
    dictionary = dict()
    with open(PATH_TO_TIMES,"r") as reader:
        dictionary = ast.literal_eval(reader.read())


    #the worst wrriten code of my life
    valid_days = list(map(mapper,list(filter(lambda dict_key: filter_dict_for_valid_days(dictionary,dict_key),dictionary))))
    valid_start_hour = today_from_midnight + timedelta(hours=float(dictionary['start_time']))
    valid_end_hour = today_from_midnight + timedelta(hours=float(dictionary['end_time']))
    if (day_today in valid_days) and (valid_start_hour<=now<=valid_end_hour):
        return True
    else:
        return False
