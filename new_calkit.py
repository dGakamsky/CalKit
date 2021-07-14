# class responsible for creating the page that saves a new calibration kit to the library
import tkinter
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkfilebrowser import askopenfilename
from tkinter import *
from CalKit import CalKit
import os
import os.path, time
import outputer
import datetime
import pathlib


class NewKitUi():
    def __init__(self, master, library):
        self.master = master
        self.master.title("Load New Calkit")
        self.master.geometry("1000x500")
        self.namelabel = tkinter.StringVar(self.master)
        self.namelabel.set("No kit name selected")
        self.make_calibration_kit()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.file_loaded = False
        self.library = library
        self.time = ""
        self.show_page_widgets()

    def make_calibration_kit(self):
        self.kit = CalKit()

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.frame, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        tkinter.Label(self.frame, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                       padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.frame, text="Deuterium", variable=self.v, value="d",
                            command=lambda: self.set_type_and_validate("d")).grid(row=1, column=1,
                                                                                  padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.frame, text="Tungsten", variable=self.v, value="t",
                            command=lambda: self.set_type_and_validate("t")).grid(row=1, column=2,
                                                                                  padx=10, pady=10, ipadx=5, ipady=5)
        self.label = tkinter.Label(self.frame, text="no file selected")
        self.label.grid(row=3, column=0, ipadx=5, ipady=5)
        self.browse_button = tkinter.Button(self.frame, text="browse files", state=DISABLED,
                                            command=lambda: self.open_file_browser())  # searches files for input file
        self.browse_button.grid(row=3, column=1, ipadx=5, ipady=5)
        # text entry box
        tkinter.Label(self.frame, text="Enter name of calibration kit:").grid(row=2, column=0, sticky=W,
                                                                              padx=10, pady=10, ipadx=5,
                                                                              ipady=5)
        save_name = tkinter.Entry(self.frame)
        save_name.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        save_name.focus_set()
        self.save_file = tkinter.Button(self.frame, text="save",
                                        state=DISABLED,
                                        command=lambda: outputer.save_file(self.library,
                                                                           self.kit, save_name))  # saves the file to
        # the .pkl file given
        self.save_file.grid(row=4, column=1, pady=50, ipadx=5, ipady=5)
        self.quit_button.grid(row=6, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=0, column=0)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)

    def close_window(self):
        self.master.destroy()

    def set_time(self, time):
        self.time = time
        return self.time

    def change_text(self):
        self.namelabel.set("current kit name: " + self.name)

    # opens the selected file and loads it into the "material" container, plots it for reference
    def open_file(self, filename, kit):
        fname = pathlib.Path(filename)
        date = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
        kit.add_scan(filename, self.type, date)
        outputer.plot_ck(kit.materials[self.type], self.subplot)
        self.canvas.draw()
        # checks whether or not to enable saving the file
        self.file_loaded = True

    # sets the type of the current scan
    def set_type_and_validate(self, t):
        self.type = t
        # checks for the presence of a name and filename, and if found enables loading the scandata
        self.browse_button["state"] = NORMAL
        return self.type

    def open_file_browser(self):
        filename = askopenfilename(initialdir="/Users/David/PycharmProjects/CalKit/scans",
                                   title="Select file",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        if filename != "":  # if a file is selected then the filename property is set to it
            self.label.config(text="selected file: " + os.path.basename(filename))
            self.filename = filename
            self.open_file(self.filename, self.kit)
            self.save_file["state"] = NORMAL
