import os
import time
from main import main_function
from icecream import ic
import _thread
from settings import settings_gui
from edit_history import editor
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
from log_file import log_files
def make_default_json():
    main_ok_defaults = dict(main_ok=1)
    with open("./main_ok.json","w+") as writer:
        writer.write(str(main_ok_defaults))
        print("written default values to main_ok.json",str(main_ok_defaults))



if not os.path.isfile("./main_ok.json"):
    ic("not found main_ok so making")
    make_default_json()












LARGEFONT =("Verdana", 35)

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

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text ="Scheduler by Sherlly", font = LARGEFONT)

        # putting the grid in its place by using
        # grid
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
        def destory_window():
            global app
            app.destroy()

        label.grid(row = 0, column = 4, padx = 10, pady = 10)

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

# second window frame page1
class Settings(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Settings", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Back to main menu",
                            command = lambda : controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)




# third window frame page2
class History(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="History", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Back to main menu",
                            command = lambda : controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)


# Driver Code
app = tkinterApp()

app.mainloop()
