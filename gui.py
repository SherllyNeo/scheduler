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
    user_input = str()
    side_root = Tk()

    # specify size of window.
    side_root.geometry("250x170")

    def get_activity():
        global e
        global user_input
        string = e.get()
        user_input = string
    def no_activity():
        global user_inpit
        user_input = "nothing"

    def close_windows():
        global side_root
        side_root.destroy()

    # Create label
    l = Label(side_root, text = "Please answer, what you are currently doing?")
    l.config(font =("Courier", 14))

    # Create button for next text
    confirm_activity_button = Button(side_root, text = "Confirm current activity", command = lambda:[get_activity(),close_windows()])

    # Create an Exit button.
    exit_button = Button(side_root, text = "Exit - no activity",
            command = lambda: [no_activity(),close_windows()])

    l.pack()
    e = Entry(side_root)
    e.pack()
    e.focus_set()
    confirm_activity_button.pack()
    exit_button.pack()

    side_root.mainloop()

    ic(user_input)
    return user_input
