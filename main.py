from log_file import log_files
import time
from valid_timer import valid_time
from icecream import ic
import gui
import sys
import ast

ic.enable()

GLOBAL_LOGS = log_files()

def user_wants_to_stop():
    main_ok_dict = {"main_ok":1}
    with open(r"./main_ok.json","r+") as reader:
        okay_or_no = ast.literal_eval(reader.read())

    if okay_or_no['main_ok'] == 0:
        with open(r"./main_ok.json","w") as writer:
            writer.write(str(main_ok_dict))
        return True
    else:
        return False

def start_thread():
    log_control = log_files()
    log_control.check_exist()
    time.sleep(2)
    if log_control.check_if_something_is_happening():
        return
    else:
        current_activity,user_estimate = gui.call_gui()
        
        ic(current_activity)
        log_control.add_log_to_file(current_activity)
        log_control.refresh_logs()
        log_control.dirty_to_clean()
        if user_estimate:
            with open(r"user_activity.json","w+") as w:
                user_est = {current_activity:user_estimate}
                w.write(str(user_est))
        

def main_function():
    while True:
        if user_wants_to_stop():
            sys.exit("quitting")
        GLOBAL_LOGS.check_exist()
        ic("checking")

        if valid_time():
            ic("starting checker")
            start_thread()
        else:
            ic("invalid time: appending no-task to datetime")
            log_control = log_files()
            log_control.refresh_logs()
            log_control.set_inactive()
            log_control.dirty_to_clean()
