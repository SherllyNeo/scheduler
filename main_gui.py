import os
import time
from main import main_function
from icecream import ic
import _thread
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
from log_file import log_files
from set_valid_times import time_setter
from pandastable import Table, TableModel, config
log_files().check_exist()
def make_default_json():
    main_ok_defaults = dict(main_ok=1)
    with open("./main_ok.json","w+") as writer:
        writer.write(str(main_ok_defaults))
        print("written default values to main_ok.json",str(main_ok_defaults))



if not os.path.isfile("./main_ok.json"):
    ic("not found main_ok so making")
    make_default_json()

LARGEFONT =("Verdana", 35)
BOLDERFONT = ("verdana",16)
class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Settings, History):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        start_page_log_controller = log_files()
        global main_label
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text ="Scheduler by Sherlly", font = LARGEFONT)

        def stop_main():
            global main_label
            main_label.config(text="ending scheduler and cleaning up",font=BOLDERFONT)
            with open("./main_ok.json","w+") as writer:
                main_ok_defaults = {"main_ok":0}
                writer.write(str(main_ok_defaults))
            log_files().set_inactive()
            log_files().dirty_to_clean()

        def start_main():
            global main_label
            main_label.config(text="started scheduler",font=BOLDERFONT)
            _thread.start_new_thread(main_function,())
        def restart_main():
             stop_main()
             start_main()
        def destory_window():
            global app
            app.destroy()

        main_label = ttk.Label(self,text="Press start scheduler")
        main_label.config(font=BOLDERFONT)
        main_label.grid(row=1,column=2)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        settings_button = Button(self, text = "Settings", command = lambda: controller.show_frame(Settings))

        start_button = ttk.Button(self, text = "Start Scheduler", command = start_main)

        end_button = ttk.Button(self, text = "Stop Scheduler", command = stop_main)

        edit_history_button = ttk.Button(self, text = "Edit History", command = lambda: controller.show_frame(History))

        quit_button = ttk.Button(self,text="Exit",command=destory_window)

        start_button.grid(row = 1, column = 1, padx = 10, pady = 10)
        end_button.grid(row = 1, column = 3, padx = 10, pady = 10)

        settings_button.grid(row = 2, column = 1, padx = 10, pady = 10)

        edit_history_button.grid(row = 2, column = 3, padx = 10, pady = 10)

        quit_button.grid(row = 3, column = 2, padx = 10, pady = 10)

        last_activity_label = Label(self,text="blank",font=BOLDERFONT)
        last_activity_label.grid(row = 2, column = 2, padx = 10, pady = 10)
        def update():
            last_activity = start_page_log_controller.get_last_activity()
            last_activity_label.config(text=f"last activity was: {last_activity}",font=BOLDERFONT)
            self.after(1000, update)
        self.after(1000,update)


class Settings(tk.Frame):

    def __init__(self, parent, controller):

        global input_end
        global input_start
        global monday_val
        global tuesday_val
        global wednesday_val
        global thursday_val
        global friday_val
        global saturday_val
        global sunday_val
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Settings", font = LARGEFONT)
        label.grid(row = 0, column = 3, padx = 10, pady = 10)
        def stop_main():
            with open("./main_ok.json","w+") as writer:
                main_ok_defaults = {"main_ok":0}
                writer.write(str(main_ok_defaults))
            log_files().set_inactive()
            log_files().dirty_to_clean()

        def start_main():
            _thread.start_new_thread(main_function,())
        def restart_main():
             stop_main()
             start_main()


        monday_val = tk.IntVar(value=1)
        monday_button = tk.Checkbutton(self, text='monday',variable=monday_val, onvalue=1, offvalue=0)
        monday_button.grid(row = 1, column = 1, padx = 10, pady=10)

        tuesday_val = tk.IntVar(value=1)
        tuesday_button = tk.Checkbutton(self, text='tuesday',variable=tuesday_val, onvalue=1, offvalue=0)
        tuesday_button.grid(row = 1, column = 2, padx = 10, pady=10)


        wednesday_val = tk.IntVar(value=1)
        wednesday_button = tk.Checkbutton(self, text='wednesday',variable=wednesday_val, onvalue=1, offvalue=0)
        wednesday_button.grid(row = 1, column = 3, padx = 10, pady=10)


        thursday_val = tk.IntVar(value=1)
        thursday_button = tk.Checkbutton(self, text='thursday',variable=thursday_val, onvalue=1, offvalue=0)
        thursday_button.grid(row = 1, column = 4, padx = 10, pady=10)


        friday_val = tk.IntVar(value=1)
        friday_button = tk.Checkbutton(self, text='friday',variable=friday_val, onvalue=1, offvalue=0)
        friday_button.grid(row = 1, column = 5, padx = 10, pady=10)


        saturday_val = tk.IntVar()
        saturday_button = tk.Checkbutton(self, text='saturday',variable=saturday_val, onvalue=1, offvalue=0)
        saturday_button.grid(row = 1, column = 6, padx = 10, pady=10)


        sunday_val = tk.IntVar()
        sunday_button = tk.Checkbutton(self, text='sunday',variable=sunday_val, onvalue=1, offvalue=0)
        sunday_button.grid(row = 1, column = 7, padx = 10, pady=10)

        input_label = ttk.Label(self,text="start hour: eg 7")
        input_label.grid(row = 2, column = 2, padx = 10, pady = 10)
        input_start = ttk.Entry(self)
        input_start.insert(0,"0")
        input_start.grid(row = 2, column = 3, padx = 10, pady = 10)
        input_start.focus_set()

        input_end_label = ttk.Label(self,text="end hour: eg 17")
        input_end_label.grid(row = 3, column = 2, padx = 10, pady = 10)
        input_end = ttk.Entry(self)
        input_end.insert(0,"24")
        input_end.grid(row = 3, column = 3, padx = 10, pady = 10)
        input_end.focus_set()

        def use_selection():
            global input_end
            global input_start
            global monday_val
            global tuesday_val
            global wednesday_val
            global thursday_val
            global friday_val
            global saturday_val
            global sunday_val

            start_time_val = input_start.get()
            end_time_val = input_end.get()

            time_setter(
            monday_val.get(),
            tuesday_val.get(),
            wednesday_val.get(),
            thursday_val.get(),
            friday_val.get(),
            saturday_val.get(),
            sunday_val.get(),
            start_time_val,
            end_time_val)

        quit_button = ttk.Button(self, text ="Back to main menu (quit)",
                            command = lambda : controller.show_frame(StartPage))

        quit_button.grid(row = 4, column = 2, padx = 10, pady = 10)

        quit_button = ttk.Button(self, text ="Back to main menu (save and exit)",
                            command = lambda : [use_selection(),restart_main(),controller.show_frame(StartPage)])

        quit_button.grid(row = 4, column = 3, padx = 10, pady = 10)



# third window frame page2
class History(tk.Frame):
    def __init__(self, parent, controller):
        log_files().check_exist()

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="History", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Back to main menu",
                            command = lambda : controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button1.grid(row = 3, column = 2, padx = 10, pady = 10)
        def update():
            f = Frame(self)
            f.grid(row=2,column=2,padx=10,pady=10)
            df = pd.read_csv("./log_files/log_files_cleaned/clean_logs.csv")
            pt = Table(f, dataframe=df,
                                    showtoolbar=False, showstatusbar=True)
            pt.show()
            #set some options
            options = {'colheadercolor':'green','floatprecision': 5}
            config.apply_options(options, pt)
            pt.show()
            self.after(10000,update)
        self.after(1,update)


# Driver Code
app = tkinterApp()

app.mainloop()
