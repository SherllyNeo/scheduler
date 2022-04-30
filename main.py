from log_file import log_files
import time
from valid_timer import valid_time
from icecream import ic

ic.enable()

GLOBAL_LOGS = log_files()

def start_thread():
    log_control = log_files()
    log_control.check_exist()
    time.sleep(1)
    if log_control.check_if_something_is_happening():
        return
    else:
        current_activity = input("what are you doing?\n")
        log_control.add_log_to_file(current_activity)
        log_control.refresh_logs()
        log_control.dirty_to_clean()

while True:
    GLOBAL_LOGS.check_exist()
    time.sleep(1)
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
