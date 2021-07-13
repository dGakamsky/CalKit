import tkinter
import tkinter.messagebox
from tkinter import *

import outputer
from CalKit import CalKit, plot_ck
import easygui as e


class SaveKitUi():
    def __init__(self, master,library):
        #super().__init__(master)
        self.master = master
        self.master.title("Save Calkit Scan")
        self.master.geometry("500x500")
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
        self.frame.label = tkinter.Label(self.master, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        label = tkinter.Label(self.master, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                                padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Deuterium Scan", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1)
        tkinter.Radiobutton(self.master, text="Tungsten Scan", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2)
        self.label = tkinter.Label(self.master, text="Selected calibration kit: ")
        self.label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        options = self.cklist
        if not options:
            options = ["empty"]
        question_menu = tkinter.OptionMenu(self.master, self.value_inside, *options)
        question_menu.grid(row=2, column=1)
        submit_button = tkinter.Button(self.master, text='Submit',
                                       command=lambda: self.select_existing_file(self.library))
        submit_button.grid(row=2, column=2)
        self.export_button = tkinter.Button(self.master, text="export", state=DISABLED,
                                            command=lambda: self.export_file(self.library))
        self.export_button.grid(row=4, column=1)
        self.quit_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=5, column=1)

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
        plot_ck(library[self.name].materials[self.type])
        if self.name != "" and self.type != "":
            self.export_button["state"] = NORMAL
        self.label.config(text="selected calibration kit: " + self.name)
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)

    def export_file(self, lib):
        library = lib.library
        outputer.print_to_file(self.name, library[self.name].materials[self.type])
