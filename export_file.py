import tkinter
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import outputer
from Ei_ref_scan import EiRefScan


class SaveKitUi:
    def __init__(self, master, library, permission):
        self.permission = permission
        self.master = master
        self.master.title("Export Calkit Scan")
        self.master.geometry("1200x500")
        self.namelabel = ""
        self.namelabel = tkinter.StringVar()
        self.ei = EiRefScan()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.eidict = {}
        self.dropdownlist = []
        self.library = library
        self.x_start = tkinter.StringVar()
        self.x_end = tkinter.StringVar()
        self.steps = tkinter.StringVar()
        self.eilist = self.populateeilist()
        self.show_page_widgets(self.master)

    def show_page_widgets(self, root):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(root)
        self.master_frame = tkinter.Frame(self.master, height=500, width=700)
        self.master_frame.grid()
        self.master_frame.grid_propagate(False)
        self.select_frame = tkinter.Frame(self.master_frame)
        self.export_frame = tkinter.Frame(self.master_frame)
        self.entry_frame = tkinter.Frame(self.master_frame)
        self.export_frame.grid(row=2)
        self.label = tkinter.Label(self.select_frame, text="Selected EI reference compound: ", width=25)
        self.label.grid(row=0, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        options = self.dropdownlist
        if not options:
            options = ["empty"]
        question_menu = tkinter.OptionMenu(self.select_frame, self.value_inside, *options,
                                           command=lambda x=None: self.select_existing_file())
        question_menu.config(width=10)
        question_menu.grid(row=0, column=1, sticky="ew")
        self.export_button = tkinter.Button(self.export_frame, text="export", state=DISABLED,
                                            command=lambda: self.export_file(
                                                self.library))
        self.export_button.grid(row=4, column=0, padx=50, pady=50, ipadx=5, ipady=5)
        self.select_frame.grid(row=0)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=1)
        self.canvas._tkcanvas.grid(row=0, column=1)
        tkinter.Label(self.entry_frame, text="name:", width=25).grid(row=0, column=0, sticky=W,
                                                                     padx=10, pady=10, ipadx=5,
                                                                     ipady=5)
        self.save_name = tkinter.Label(self.entry_frame, text="")
        self.save_name.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.save_name.focus_set()
        self.addfields()

        self.save_file_button = tkinter.Button(self.export_frame, text="save",
                                               state=DISABLED,
                                               command=lambda: self.save_file(self.ei))
        # since on
        if self.permission == "developer":
            self.save_file_button.grid(row=4, column=1, padx=50, pady=50, ipadx=5, ipady=5)

    def populateeilist(self):
        self.eilist = ["empty"]  # default necessary for when/if the file being read from is empty
        if self.library.get_ei_list():
            self.eilist = []  # removes the placeholder value
            for i in self.library.get_ei_list():  # populates the dropdown
                self.eilist.append(i.key)
                self.eidict[i.name] = i.key
                self.dropdownlist.append(i.name)
                i.print()
        return self.eilist

    # loads the data fields a certain way depending on what the current permission is
    def addfields(self):
        if self.permission == "user":
            self.addlabels()
        if self.permission == "developer":
            self.addentries()

    # developers have the ability to edit the data in the library, so editable entries are created
    def addentries(self):
        self.chemicalfield = tkinter.Entry(self.entry_frame)
        self.chemicalfield.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.chemicalfield.focus_set()
        self.chemical_label = tkinter.Label(self.entry_frame, text="Product name")
        self.chemical_label.grid(row=1, column=0, sticky=W, padx=5, pady=10, ipadx=5, ipady=5)
        self.typefield = tkinter.Entry(self.entry_frame)
        self.typefield.grid(row=2, column=1, padx=10, pady=5, ipadx=5, ipady=5)
        self.typefield.focus_set()
        self.type_label = tkinter.Label(self.entry_frame, text="Sample type")
        self.type_label.grid(row=2, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield = tkinter.Entry(self.entry_frame)
        self.rangefield.grid(row=3, column=1, padx=10, pady=5, ipadx=5, ipady=5)
        self.rangefield.focus_set()
        self.range_label = tkinter.Label(self.entry_frame, text="Emission range from")
        self.range_label.grid(row=3, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield_to = tkinter.Entry(self.entry_frame)
        self.rangefield_to.grid(row=3, column=3, padx=10, pady=5, ipadx=5, ipady=5)
        self.rangefield_to.focus_set()
        self.range_label_to = tkinter.Label(self.entry_frame, text="to")
        self.range_label_to.grid(row=3, column=2, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyfield = tkinter.Entry(self.entry_frame)
        self.qyfield.grid(row=4, column=1, padx=10, pady=5, ipadx=5, ipady=5)
        self.qyfield.focus_set()
        self.qy_label = tkinter.Label(self.entry_frame, text="Quantum Yield Emission range from")
        self.qy_label.grid(row=4, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyfield_to = tkinter.Entry(self.entry_frame)
        self.qyfield_to.grid(row=4, column=3, padx=10, pady=5, ipadx=5, ipady=5)
        self.qyfield_to.focus_set()
        self.qy_label_to = tkinter.Label(self.entry_frame, text="t0")
        self.qy_label_to.grid(row=4, column=2, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyvaluefield = tkinter.Entry(self.entry_frame)
        self.qyvaluefield.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyvaluefield.focus_set()
        self.qy_label = tkinter.Label(self.entry_frame, text="QY")
        self.qy_label.grid(row=5, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.entry_frame.grid(row=1, column=0)

    # if the permission is user, non editable labels are created
    def addlabels(self):
        self.chemicalfield = tkinter.Label(self.entry_frame, text="", width=10)
        self.chemicalfield.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.chemicalfield.focus_set()
        self.chemical_label = tkinter.Label(self.entry_frame, text="Product name", width=25)
        self.chemical_label.grid(row=1, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.typefield = tkinter.Label(self.entry_frame, text="", width=10)
        self.typefield.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.typefield.focus_set()
        self.type_label = tkinter.Label(self.entry_frame, text="Sample type", width=25)
        self.type_label.grid(row=2, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield = tkinter.Label(self.entry_frame, text="", width=10, height=2)
        self.rangefield.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield.focus_set()
        self.range_label = tkinter.Label(self.entry_frame, text="Reference Emission range from", width=25)
        self.range_label.grid(row=3, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield_to = tkinter.Label(self.entry_frame, text="", width=1, height=2)
        self.rangefield_to.grid(row=3, column=3, padx=5, pady=5, ipadx=5, ipady=5)
        self.rangefield_to.focus_set()
        self.range_label_to = tkinter.Label(self.entry_frame, text="to", width=10)
        self.range_label_to.grid(row=3, column=2, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyfield = tkinter.Label(self.entry_frame, text="", width=10, height=2)
        self.qyfield.grid(row=4, column=1, padx=10, pady=5, ipadx=5, ipady=5)
        self.qyfield.focus_set()
        self.qy_label = tkinter.Label(self.entry_frame, text="Quantum Yield Emission range from", width=25)
        self.qy_label.grid(row=4, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyfield_to = tkinter.Label(self.entry_frame, text="", width=10, height=2)
        self.qyfield_to.grid(row=4, column=3, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyfield_to.focus_set()
        self.qy_label_to = tkinter.Label(self.entry_frame, text="to", width=10)
        self.qy_label_to.grid(row=4, column=2, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyvaluefield = tkinter.Label(self.entry_frame, text="", width=10)
        self.qyvaluefield.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.qyvaluefield.focus_set()
        self.lifetime_label = tkinter.Label(self.entry_frame, text="QY", width=25)
        self.lifetime_label.grid(row=5, column=0, sticky=W, padx=5, pady=5, ipadx=5, ipady=5)
        self.entry_frame.grid(row=1, column=0)

    def set_type(self, t):
        self.type = t
        self.plot_file()

    def plot_file(self):
        library = self.library.library
        try:
            outputer.plot_ei(library[self.name].spline, self.subplot)
        except KeyError:
            outputer.error_message("please select a material before selecting a file")
        self.canvas.draw()
        self.export_button["state"] = NORMAL
        self.save_file_button["state"] = NORMAL
        self.set_vars()
        return self.name, self.ei

    # the command that responds to the dropdown menu
    def select_existing_file(self):
        dropdown = self.value_inside.get()
        key = self.eidict[dropdown]
        self.name = key  # sets the name of the current kit to the selected kit
        library = self.library.library
        # Sets the current kit data equal to the kit data from the selected kit
        try:
            self.ei = library[self.name]
            self.plot_file()
        except KeyError:
            outputer.error_message("You must select an EI scan to export")

    def export_file(self, lib):
        library = lib.library
        outputer.print_to_file(self.ei.name, library[self.name])

    def set_vars(self):
        self.save_name["text"] = self.ei.name
        if self.permission == "developer":
            self.set_entries()
        else:
            self.chemicalfield["text"] = self.ei.product_name
            self.typefield["text"] = self.ei.sample_type
            self.rangefield["text"] = self.ei.ref_emission_range[0]
            self.rangefield_to["text"] = self.ei.ref_emission_range[1]
            self.qyfield["text"] = self.ei.qy_emission_range[0]
            self.qyfield_to["text"] = self.ei.qy_emission_range[1]
            self.qyvaluefield["text"] = self.ei.qy

    def set_entries(self):
        self.chemicalfield.delete(0, END)
        self.typefield.delete(0, END)
        self.rangefield.delete(0, END)
        self.rangefield_to.delete(0, END)
        self.qyfield.delete(0, END)
        self.qyfield_to.delete(0, END)
        self.qyvaluefield.delete(0, END)
        self.chemicalfield.insert(10, self.ei.product_name)
        self.typefield.insert(10, self.ei.sample_type)
        self.rangefield.insert(10, self.ei.ref_emission_range[0])
        self.rangefield_to.insert(10, self.ei.ref_emission_range[1])
        self.qyfield.insert(10, self.ei.qy_emission_range[0])
        self.qyfield_to.insert(10, self.ei.qy_emission_range[1])
        self.qyvaluefield.insert(10, self.ei.qy)

    def save_file(self, ei):
        ei.product_name = self.chemicalfield.get()
        ei.sample_type = self.typefield.get()
        ref = str(self.rangefield.get()) + " " + str(self.rangefield_to.get())
        ei.ref_emission_range = ref
        qyem = str(self.qyfield.get()) + " " + str(self.qyfield_to.get())
        ei.qy_emission_range = qyem
        ei.qy = self.qyvaluefield.get()
        self.library.library = ei
        outputer.dump_ei_list(self.library)
