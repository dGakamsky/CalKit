from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from outputer import save_file
import tkinter
import tkinter.messagebox
from tkfilebrowser import askopenfilename
from tkinter import *
from CalKit import CalKit
import outputer
import datetime
import pathlib



class LoadKitUi():
    def __init__(self, master, library):
        # super().__init__(master)
        self.master = master
        self.master.title("Load New Calkit")
        self.master.geometry("1000x500")
        self.namelabel = ""
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        self.kit = CalKit()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.file_loaded = False
        self.library = library
        self.cklist = self.populatecklist()
        self.show_page_widgets()

    def show_page_widgets(self):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(self.master)
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.frame, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        tkinter.Label(self.frame, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                        padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.frame, text="Deuterium Scan", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.frame, text="Tungsten Scan", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Label(self.frame, text="Select file with update data :").grid(row=3, column=0, sticky=W,
                                                                               padx=10, pady=10, ipadx=5,
                                                                               ipady=5)
        self.browse_file = tkinter.Button(self.frame, text="browse files", state=DISABLED,
                                     command=lambda: self.open_file_browser())  # searches files for input file
        self.browse_file.grid(row=3, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        options = self.cklist
        if not options:
            options = ["empty"]
        self.label = tkinter.Label(self.frame, text="Selected calibration kit :")
        self.label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        question_menu = tkinter.OptionMenu(self.frame, self.value_inside, *options,
                                           command=lambda x=None: self.select_existing_file(self.library))
        question_menu.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.save_file = tkinter.Button(self.frame, text="save",
                                        state=DISABLED,
                                        command=lambda: save_file(
                                            self.library,
                                            self.kit))  # saves the file to the .pkl file given the input parameters
        self.save_file.grid(row=6, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.quit_button.grid(pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)

    def close_window(self):
        self.master.destroy()

    def populatecklist(self):
        self.cklist = ["empty"]  # default necessary for when/if the file being read from is empty
        if self.library.get_ck_list():
            self.cklist = []  # removes the placeholder value
            for i in self.library.get_ck_list():  # populates the dropdown
                self.cklist.append(i.name)
                # i.print()
        return self.cklist

    def open_file(self, filename, kit):
        # this check method is probably very inefficient, but I was unable to get the methods to work by passing the
        # type in
        fname = pathlib.Path(filename)
        date = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
        kit.add_scan(filename, self.type, date)
        outputer.plot_ck(kit.materials[self.type], self.subplot)
        self.file_loaded = True
        # checks whether or not to enable saving the file
        self.validate()

    def validate(self):
        if self.name != "" and self.filename != "" and self.type != "":
            self.select_file["state"] = NORMAL
        if self.file_loaded:
            self.save_file["state"] = NORMAL

    def set_type(self, t):
        self.type = t
        # checks for the presence of a name and filename, and if found enables loading the scandata
        if self.name != "" and self.filename != "":
            self.select_file["state"] = NORMAL
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

    # the command that responds to the dropdown menu
    def select_existing_file(self, lib):
        self.name = self.value_inside.get()  # sets the name of the current kit to the selected kit
        self.changetext()
        library = lib.library
        # fpr validation
        # Sets the current kit data equal to the kit data from the selected kit
        self.kit = library[self.name]
        self.kit.materials["t"] = library[self.name].materials["t"]
        self.kit.materials["d"] = library[self.name].materials["d"]
        # plots the selected kits data if appropriate

        outputer.plot_ck(library[self.name].materials[self.type], self.subplot)
        self.canvas.draw()
        self.label.config(text="Selected calibration kit: " + self.name)
        self.browse_file["state"] = NORMAL
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)
