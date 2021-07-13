# the UI responsible for the file reader
import tkinter.messagebox
from tkfilebrowser import askopenfilename
from tkinter import *
import new_calkit
from CalKit import CalKit, plot_ck
from Library import Library
import easygui as e
import os
import outputer
from tkinter import ttk
from ttkthemes import themed_tk as theme


# retrieves the list of Calibration Kits (ck's) from the library
from export_file import SaveKitUi
from load_calkit import LoadKitUi


def load_ck_list(lib):
    return lib.get_ck_list()


class StartUi:
    lib = Library()
    namelabel = ""

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.show_page_widgets()
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        self.populatecklist()
        # creates the "box" for the ui
        self.window = master
        # Dictionary to create multiple buttons
        root.title("CalKit Calibration")
        load_ck_list(self.lib)  # loads the list of stored calkits

    def populatecklist(self):
        StartUi.cklist = ["empty"]  # default necessary for when/if the file being read from is empty
        if self.lib.get_ck_list():
            StartUi.cklist = []  # removes the placeholder value
            for i in self.lib.get_ck_list():  # populates the dropdown
                StartUi.cklist.append(i.name)
                # i.print()
        return StartUi.cklist

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.master.title("Calibration Kit Interface")
        self.create_button("Create new Calibration Kit", new_calkit.NewKitUi)
        self.create_button("Update Existing Calibration Kit", LoadKitUi)
        self.create_button("Export existing Calibration kit", SaveKitUi)
        self.frame.pack()

    def create_button(self, text, _class):
        """Button that creates a new window"""
        tkinter.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class)).pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)

    def new_window(self, _class):
        self.win = tkinter.Toplevel(self.master)
        _class(self.win)

# where everything is called from
root = tkinter.Tk()
app = StartUi(root)
root.mainloop()

# root.tk.call('lappend', 'auto_path', 'E:/awthemes - 10.4.0')
# root.tk.call('package', 'require', 'awdark.tcl')
