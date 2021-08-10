# the UI responsible for the file reader
import tkinter.messagebox
from tkinter import *

import outputer
from Ei_Library import Library

# retrieves the list of Calibration Kits (ck's) from the library
from export_file import SaveKitUi



def load_ck_list(lib):
    return lib.get_ei_list()


class StartUi:
    lib = Library()
    namelabel = ""

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.show_page_widgets()
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        # creates the "box" for the ui
        self.window = master
        self.permission = "user"
        # Dictionary to create multiple buttons
        root.title("EI Calibration")
        load_ck_list(self.lib)  # loads the list of stored calkits

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.master.title("EI Scan Interface")
        self.create_button("Browse EI scan library", SaveKitUi)
        self.passwordentry = tkinter.Entry(self.frame)
        self.passwordentry.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10, side=RIGHT)
        self.password_button = tkinter.Button(self.frame,
                                              text="enter developer password",
                                              command=lambda: self.set_permission())
        self.password_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10, side=LEFT)
        self.frame.pack()

    def create_button(self, text, _class):
        """Button that creates a new window"""
        tkinter.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class)).pack(fill=tkinter.X, pady=100, ipadx=10, ipady=10)

    def set_permission(self):
        text = self.passwordentry.get()
        if text == "password":
            self.permission = "developer"
            self.passwordentry.pack_forget()
            self.password_button.pack_forget()
            tkinter.Label(text="developer permission granted").pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        else:
            outputer.error_message("your password was incorrect")

    def new_window(self, _class):
        self.win = tkinter.Toplevel(self.master)
        _class(self.win, StartUi.lib, self.permission)


# where everything is called from
root = tkinter.Tk()
app = StartUi(root)
root.mainloop()


