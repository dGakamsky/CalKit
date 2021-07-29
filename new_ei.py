# class responsible for creating the page that saves a new calibration kit to the library
import tkinter
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkfilebrowser import askopenfilename
from tkinter import *

import editor
from CalKit import CalKit
import os
import os.path, time
import outputer
import datetime
import pathlib
from Ei_ref_scan import EiRefScan


class NewKitUi:
    def __init__(self, master, library):
        self.namelabel = None
        self.ei = EiRefScan()
        self.master = master
        self.master.title("Create new EI scan")
        self.master.geometry("1000x1000")
        fields = "name", "chemical name", "sample type", "emission range", "quantum yield", "lifetime"
        self.product_name = ""
        self.filename = ""
        self.sample_type = ""
        self.emission_range = ""
        self.qy = ""
        self.lifetime = ""
        self.spline = ""
        self.file_loaded = False
        self.library = library
        self.show_page_widgets()

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.entryframe = tkinter.Frame(self.frame)
        self.label = tkinter.Label(self.frame, text="no file selected")
        self.label.grid(row=3, column=0, ipadx=5, ipady=5)
        self.browse_button = tkinter.Button(self.frame, text="browse files",
                                            command=lambda: self.open_file_browser())  # searches files for input file
        self.browse_button.grid(row=3, column=1, ipadx=5, ipady=5)
        self.save_file_button = tkinter.Button(self.frame, text="save",
                                        state=DISABLED,
                                        command=lambda: self.save_file(self.ei))  # saves the file to
        # the .pkl file given
        self.save_file_button.grid(row=4, column=1, pady=50, ipadx=5, ipady=5)
        self.frame.grid(row=0, column=0)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)
        tkinter.Label(self.entryframe, text="Enter name of EI scan:").grid(row=0, column=0, sticky=W,
                                                                           padx=10, pady=10, ipadx=5,
                                                                           ipady=5)
        self.save_name = tkinter.Entry(self.entryframe)
        self.save_name.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.save_name.focus_set()
        self.chemicalfield = tkinter.Entry(self.entryframe)
        self.chemicalfield.grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.chemicalfield.focus_set()
        self.chemical_label = tkinter.Label(self.entryframe, text="Enter name of chemical")
        self.chemical_label.grid(row=1, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.typefield = tkinter.Entry(self.entryframe)
        self.typefield.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.typefield.focus_set()
        self.type_label = tkinter.Label(self.entryframe, text="Enter sample type")
        self.type_label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.rangefield = tkinter.Entry(self.entryframe)
        self.rangefield.grid(row=3, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.rangefield.focus_set()
        self.range_label = tkinter.Label(self.entryframe, text="Enter Emission range")
        self.range_label.grid(row=3, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.qyfield = tkinter.Entry(self.entryframe)
        self.qyfield.grid(row=4, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.qyfield.focus_set()
        self.qy_label = tkinter.Label(self.entryframe, text="Enter Quantum Yield")
        self.qy_label.grid(row=4, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.lifetimefield = tkinter.Entry(self.entryframe)
        self.lifetimefield.grid(row=5, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.lifetimefield.focus_set()
        self.lifetime_label = tkinter.Label(self.entryframe, text="Enter lifetime")
        self.lifetime_label.grid(row=5, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.entryframe.grid(row=1, column=0)

    def close_window(self):
        self.master.destroy()

    def change_text(self):
        self.namelabel.set("current EI name: " + self.product_name)

    # opens the selected file and loads it into the "material" container, plots it for reference
    def plot_file(self, filename, ei):
        fname = pathlib.Path(filename)
        ei.add_scan(fname)
        outputer.plot_ei(ei.spline, self.subplot)
        self.canvas.draw()
        # checks whether or not to enable saving the file
        self.file_loaded = True

    def open_file_browser(self):
        filename = askopenfilename(initialdir="/Users/David/PycharmProjects/EI ref/scans",
                                   title="Select file",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        if filename != "":  # if a file is selected then the filename property is set to it
            self.label.config(text="selected file: " + os.path.basename(filename))
            self.filename = filename
            editor.fix_format(filename)
            filename = self.filename + " modified"
            self.plot_file(filename, self.ei)
            self.save_file_button["state"] = NORMAL

    def save_file(self, ei):
        ei.name = self.save_name.get()
        ei.product_name = self.chemicalfield.get()
        ei.sample_type = self.typefield.get()
        ei.emission_range = self.rangefield.get()
        ei.qy = self.qyfield.get()
        ei.lifetime = self.lifetimefield.get()
        ei.print()
        self.library.library = ei
        outputer.dump_ei_list(self.library)
