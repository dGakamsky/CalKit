import tkinter
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import outputer
from CalKit import CalKit


class SaveKitUi():
    def __init__(self, master, library):
        self.master = master
        self.master.title("Export Calkit Scan")
        self.master.geometry("1000x500")
        self.namelabel = ""
        self.namelabel = tkinter.StringVar()
        self.kit = CalKit()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.library = library
        self.x_start = tkinter.StringVar()
        self.x_end = tkinter.StringVar()
        self.steps = tkinter.StringVar()
        self.cklist = self.populatecklist()
        self.show_page_widgets(self.master)

    def show_page_widgets(self, root):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(root)
        self.master_frame = tkinter.Frame(self.master, height=500, width=500)
        self.master_frame.grid()
        self.master_frame.grid_propagate(0)
        self.select_frame = tkinter.Frame(self.master_frame)
        self.export_frame = tkinter.Frame(self.master_frame)
        self.export_frame.grid(row=1)
        self.v = tkinter.StringVar(self.master, "1")
        label = tkinter.Label(self.select_frame, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                                      padx=10, pady=10, ipadx=5,
                                                                                      ipady=5)
        self.d_type = tkinter.Radiobutton(self.select_frame, text="Deuterium Scan", variable=self.v, value="d",
                                          state=DISABLED,
                                          command=lambda: self.set_type("d"))
        self.d_type.grid(row=1, column=1)
        self.t_type = tkinter.Radiobutton(self.select_frame, text="Tungsten Scan", variable=self.v, value="t",
                                          state=DISABLED,
                                          command=lambda: self.set_type("t"))
        self.t_type.grid(row=1, column=2)
        self.label = tkinter.Label(self.select_frame, text="Selected calibration kit: ")
        self.label.grid(row=0, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        options = self.cklist
        if not options:
            options = ["empty"]
        question_menu = tkinter.OptionMenu(self.select_frame, self.value_inside, *options,
                                           command=lambda x=None: self.select_existing_file())
        question_menu.grid(row=0, column=1)
        self.export_button = tkinter.Button(self.export_frame, text="export", state=DISABLED,
                                            command=lambda: self.export_file(
                                                self.library, stepfield, startfield, stopfield))
        self.export_button.grid(row=4, column=1)
        self.select_frame.grid(row=0)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)
        stepfield = tkinter.Entry(self.export_frame)
        stepfield.grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        stepfield.focus_set()
        self.step_label = tkinter.Label(self.export_frame, text="Enter step size (leave empty for default 1) :")
        self.step_label.grid(row=1, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        startfield = tkinter.Entry(self.export_frame)
        startfield.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        startfield.focus_set()
        self.start_label = tkinter.Label(self.export_frame, text="X axist start")
        self.start_label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        stopfield = tkinter.Entry(self.export_frame)
        stopfield.grid(row=3, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        stopfield.focus_set()
        self.stop_label = tkinter.Label(self.export_frame, text="X axis end")
        self.stop_label.grid(row=3, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)


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
        self.plot_file()

    def plot_file(self):
        library = self.library.library
        try:
            outputer.plot_ck(library[self.name].materials[self.type], self.subplot)
        except KeyError:
            outputer.error_message("please select a material before selecting a file")
        self.canvas.draw()
        self.export_button["state"] = NORMAL
        self.set_vars()

        return self.name, self.kit

    # the command that responds to the dropdown menu
    def select_existing_file(self):
        self.name = self.value_inside.get()  # sets the name of the current kit to the selected kit
        library = self.library.library
        # Sets the current kit data equal to the kit data from the selected kit
        try:
            self.kit = library[self.name]
            self.kit.materials["d"] = library[self.name].materials["d"]
            self.kit.materials["t"] = library[self.name].materials["t"]
        except KeyError:
            outputer.error_message("You must select a calibration kit to export")
        self.d_type["state"] = NORMAL
        self.t_type["state"] = NORMAL
        if self.type != "":
            self.plot_file()

    def export_file(self, lib, step, start, stop):
        library = lib.library
        if step.get() != "":
            library[self.name].materials[self.type].step = step.get()
        if start.get() != "":
            library[self.name].materials[self.type].x_start = start.get()
        if stop.get() != "":
            library[self.name].materials[self.type].x_end = stop.get()
        outputer.print_to_file(self.name, library[self.name].materials[self.type])

    def set_vars(self):
        self.label.config(
            text="selected calibration kit: " + self.name)
        self.start_label.config(
            text="Enter X axis start(leave empty for default of " + str(self.kit.materials[self.type].x_start) + ")")
        self.stop_label.config(
            text="Enter X axis start(leave empty for default of " + str(self.kit.materials[self.type].x_end) + ")")
