import tkinter
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

import outputer
from CalKit import CalKit
import easygui as e


class SaveKitUi():
    def __init__(self, master,library):
        #super().__init__(master)
        self.master = master
        self.master.title("Save Calkit Scan")
        self.master.geometry("1000x500")
        self.namelabel = ""
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        self.kit = CalKit()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.library = library
        self.cklist = self.populatecklist()
        self.show_page_widgets(self.master)


    def show_page_widgets(self, root):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(root)
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.frame, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        label = tkinter.Label(self.frame, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                                padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.frame, text="Deuterium Scan", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1)
        tkinter.Radiobutton(self.frame, text="Tungsten Scan", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2)
        self.label = tkinter.Label(self.frame, text="Selected calibration kit: ")
        self.label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        options = self.cklist
        if not options:
            options = ["empty"]
        question_menu = tkinter.OptionMenu(self.frame, self.value_inside, *options,
                                           command=lambda x=None: self.select_existing_file(self.library))
        question_menu.grid(row=2, column=1)
        self.export_button = tkinter.Button(self.frame, text="export", state=DISABLED,
                                            command=lambda: self.export_file(self.library, stepfield))
        self.export_button.grid(row=4, column=1)
        self.quit_button.grid(pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=0, column=0)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)
        stepfield = tkinter.Entry(self.frame)
        stepfield.grid(row=5, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        stepfield.focus_set()



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

    def set_type(self, t):
        self.type = t
        return self.type

    # the command that responds to the dropdown menu
    def select_existing_file(self, lib):
        self.name = self.value_inside.get()  # sets the name of the current kit to the selected kit
        print(self.name)  # for validation
        self.changetext()
        library = lib.library
        print(library)  # fpr validation
        # Sets the current kit data equal to the kit data from the selected kit
        try:
            self.kit = library[self.name]
            self.kit.materials["d"] = library[self.name].materials["d"]
            self.kit.materials["t"] = library[self.name].materials["t"]
        except KeyError:
            e.msgbox("You must select a calibration kit to export")
        # plots the selected kits data if appropriate
        outputer.plot_ck(library[self.name].materials[self.type], self.subplot)
        self.canvas.draw()
        if self.name != "" and self.type != "":
            self.export_button["state"] = NORMAL
        self.label.config(text="selected calibration kit: " + self.name)
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)

    def export_file(self, lib, step):
        library = lib.library
        library[self.name].materials[self.type].step = step.get()
        outputer.print_to_file(self.name, library[self.name].materials[self.type])
