from icecream import ic
path = "./log_files/valid_times"



#toy function to add the dictionary of allowed times - sort of acts like settings


def time_setter(monday_val,tuesday_val,wednesday_val,thursday_val,friday_val,saturday_val,sunday_val,start_time_val,end_time_val):
    valid_times = dict(monday=monday_val,tuesday=tuesday_val
            ,wednesday=wednesday_val
            ,thursday=thursday_val,friday=friday_val,saturday=saturday_val,sunday=sunday_val,start_time=start_time_val,end_time=end_time_val)

    ic(f"written {valid_times} to json")
    with open(path+"/valid_times.json","w+") as writer:
        writer.write(str(valid_times))
        print("written valid time to logs")
