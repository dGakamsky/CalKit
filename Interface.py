# the UI responsible for the file reader
import tkinter.messagebox
from tkinter import *
from Library import Library

# retrieves the list of Calibration Kits (ck's) from the library
from export_file import SaveKitUi
from load_calkit import LoadKitUi
from new_calkit import NewKitUi

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
        # creates the "box" for the ui
        self.window = master
        # Dictionary to create multiple buttons
        root.title("CalKit Calibration")
        load_ck_list(self.lib)  # loads the list of stored calkits

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.master.title("Calibration Kit Interface")
        self.create_button("Create new Calibration Kit", NewKitUi)
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
        _class(self.win, StartUi.lib)


# where everything is called from
root = tkinter.Tk()
app = StartUi(root)
root.mainloop()

# root.tk.call('lappend', 'auto_path', 'E:/awthemes - 10.4.0')
# root.tk.call('package', 'require', 'awdark.tcl')
