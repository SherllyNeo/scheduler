from icecream import ic
import tkinter as tk
from tkinter import ttk
from tkinter import *


ic.enable()

def call_gui():
    global e
    global side_root
    global user_input
    global side_root
    global user_estimate
    global est_e
    user_input = str()
    side_root = Tk()
    user_estimate = None

    # specify size of window.
    side_root.geometry("900x200")

    def get_activity():
        global e
        global user_input
        user_input = e.get()
    def no_activity():
        global user_input
        user_input = "nothing"

    def close_windows():
        global side_root
        side_root.destroy()
    def get_user_est():
        global est_e 
        global user_estimate
        user_estimate = est_e.get()


    # Create label
    l = Label(side_root, text = "Please answer, what you are currently doing?")
    l.config(font =("Courier", 14))

    # Create button for next text
    confirm_activity_button = Button(side_root, text = "Confirm current activity", command = lambda:[get_activity(),get_user_est(),close_windows()])

    # Create an Exit button.
    exit_button = Button(side_root, text = "Exit - no activity",
            command = lambda: [no_activity(),close_windows()])

    l.grid(row=0,columns=1,padx=10,pady=10)
    e = Entry(side_root)
    e.grid(row=1,column=1,padx=10,pady=10)
    e.focus_set()
    e.insert(0, 'activity_name_goes_here')
    confirm_activity_button.grid(row=3,column=0,padx=10,pady=10)
    exit_button.grid(row=3,column=2,padx=10,pady=10)
    est_e = Entry(side_root)
    est_e.grid(row=2,column=1,padx=10,pady=10)
    side_root.mainloop()

    ic(user_input,user_estimate)
    if user_estimate == '':
        user_estimate = False
    return user_input,user_estimate
