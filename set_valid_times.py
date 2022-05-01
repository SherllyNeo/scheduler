path = "./log_files/valid_times"


#toy function to add the dictionary of allowed times - sort of acts like settings


def set_valid_timer():
    valid_times = dict(monday=0,tuesday=0,wednesday=1,thursday=1,friday=0,saturday=1,sunday=0,start_time="7",end_time="23")
    with open(path+"/valid_times.json","w") as writer:
        writer.write(str(valid_times))
        print("written valid time to logs")


set_valid_timer()
