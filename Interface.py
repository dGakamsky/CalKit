# the UI responsible for the file reader
import tkinter.messagebox
from tkfilebrowser import askopenfilename
from tkinter import *
from CalKit import CalKit, plotck
from Library import Library
import easygui as e
import os


# retrieves the list of Calibration Kits (ck's) from the library
def load_ck_list(lib):
    return lib.get_ck_list()


# saves to the .pkl file, functions via append
def save_file(library, ck):
    print(type(ck))  # for testing
    # adds kit to library
    library.library = ck
    ck.print()  # for testing
    library.dump_ck_list()  # calls the library to dump to the pickle file
    for i in library.get_ck_list():  # testing function to validate what was printed
        i.print()


class StartUi:
    cklist = []
    lib = Library()
    namelabel = ""

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.show_page_widgets()
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        self.populatecklist()
        # print(StartUi.cklist)
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
                i.print()
        return StartUi.cklist

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
        _class(self.win)


class NewKitUi(StartUi):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Load New Calkit")
        self.master.geometry("500x500")
        self.namelabel = tkinter.StringVar(self.master)
        self.namelabel.set("No kit name selected")
        self.kit = CalKit()
        self.name = ""
        self.filename = ""
        self.type = ""

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.master, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        label = tkinter.Label(self.master, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                                padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Deuterium", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Tungsten", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        self.label = tkinter.Label(self.master, text="no file selected")
        self.label.grid(row=3, column=0, ipadx=5, ipady=5)
        b = tkinter.Button(self.master, text="browse files",
                           command=lambda: self.open_file_browser())  # searches files for input file
        b.grid(row=3, column=1, ipadx=5, ipady=5)
        self.b2 = tkinter.Button(self.master, text="select file", state=DISABLED,
                                 command=lambda: self.open_file(self.filename, self.name,
                                                                self.kit))  # reads
        # the file
        self.b2.grid(row=3, column=2, ipadx=5, ipady=5)
        # text entry box
        label = tkinter.Label(self.master, text="Enter name of calibration kit:").grid(row=2, column=0, sticky=W,
                                                                                       padx=10, pady=10, ipadx=5,
                                                                                       ipady=5)
        e = tkinter.Entry(self.master)
        e.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        e.focus_set()
        f = tkinter.Button(self.master, text="save name", command=lambda: self.callback(e))  # name input
        f.grid(row=2, column=2, ipadx=5, ipady=5)
        self.c = tkinter.Button(self.master, text="save",
                                state=DISABLED,
                                command=lambda: save_file(StartUi.lib, self.kit))  # saves the file to the .pkl file
        # given
        self.c.grid(row=4, column=1, pady=50, ipadx=5, ipady=5)
        self.quit_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=5, column=1)

    def close_window(self):
        self.master.destroy()

    def callback(self, e):
        self.name = e.get()
        if self.filename != "" and self.type != "":
            self.b2["state"] = NORMAL
        self.changetext()
        print("Name set to: " + self.name)  # print is for validation
        return self.name

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)

    def open_file(self, filename, name, kit):
        kit.name = name  # sets the name
        # this check method is probably very inefficient, but I was unable to get the methods to work by passing the
        # type in
        if self.type == "d":  # sets the type of the scan
            kit.add_scan(filename, "d")
        if self.type == "t":
            kit.add_scan(filename, "t")
        if self.type == "d":  # has the kit plot the material corresponding to the type
            plotck(kit.d)
        if self.type == "t":
            plotck(kit.t)
        # checks whether or not to enable saving the file
        if self.type != "" and self.name != "":
            self.c["state"] = NORMAL

    def set_type(self, t):
        self.type = t
        # checks for the presence of a name and filename, and if found enables loading the scandata
        if self.name != "" and self.filename != "":
            self.b2["state"] = NORMAL
        return self.type

    def open_file_browser(self):
        filename = askopenfilename(initialdir="/Users/David/PycharmProjects/CalKit",
                                   title="Select file",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        if filename != "":  # if a file is selected then the filename property is set to it
            self.label.config(text="selected file: " + os.path.basename(filename))
            return filename


class LoadKitUi(StartUi):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Load New Calkit")
        self.master.geometry("500x500")
        self.namelabel = ""
        self.namelabel = tkinter.StringVar()
        self.namelabel.set("No kit name selected")
        self.kit = CalKit()
        self.name = ""
        self.filename = ""
        self.type = ""

    def show_page_widgets(self):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(root)
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.master, textvariable=StartUi.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        label = tkinter.Label(self.master, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                                padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Deuterium Scan", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Tungsten Scan", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        label = tkinter.Label(self.master, text="Select file with update data :").grid(row=2, column=0, sticky=W,
                                                                                       padx=10, pady=10, ipadx=5,
                                                                                       ipady=5)
        b = tkinter.Button(self.master, text="browse files",
                           command=lambda: self.open_file_browser())  # searches files for input file
        b.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.b2 = tkinter.Button(self.master, text="select file", state=DISABLED,
                                 command=lambda: self.open_file(self.filename, self.name, self.kit))  # reads
        # the file
        self.b2.grid(row=2, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        options = StartUi.cklist
        if not options:
            options = ["empty"]
        self.label = tkinter.Label(self.master, text="Selected calibration kit :")
        self.label.grid(row=4, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        question_menu = tkinter.OptionMenu(self.master, self.value_inside, *options)
        question_menu.grid(row=4, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        submit_button = tkinter.Button(self.master, text='Submit',
                                       command=lambda: self.select_existing_file(StartUi.lib))
        submit_button.grid(row=4, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        self.c = tkinter.Button(self.master, text="save",
                                state=DISABLED,
                                command=lambda: save_file(
                                    self.lib, self.kit))  # saves the file to the .pkl file given the input parameters
        self.c.grid(row=6, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.quit_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=7, column=1, padx=10, pady=10, ipadx=5, ipady=5)

    def close_window(self):
        self.master.destroy()

    def open_file(self, filename, name, kit):
        kit.name = name  # sets the name
        # this check method is probably very inefficient, but I was unable to get the methods to work by passing the
        # type in
        if self.type == "d":  # sets the type of the scan
            kit.add_scan(filename, "d")
        if self.type == "t":
            kit.add_scan(filename, "t")
        if self.type == "d":  # has the kit plot the material corresponding to the type
            plotck(kit.d)
        if self.type == "t":
            plotck(kit.t)
        # checks whether or not to enable saving the file
        if self.type != "" and self.name != "":
            self.c["state"] = NORMAL

    def set_type(self, t):
        self.type = t
        # checks for the presence of a name and filename, and if found enables loading the scandata
        if self.name != "" and self.filename != "":
            self.b2["state"] = NORMAL
        return self.type

    def open_file_browser(self):
        filename = askopenfilename(initialdir="/Users/David/PycharmProjects/CalKit",
                                   title="Select file",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        if filename != "":  # if a file is selected then the filename property is set to it
            self.filename = filename
            return filename

    # the command that responds to the dropdown menu
    def select_existing_file(self, lib):
        self.name = self.value_inside.get()  # sets the name of the current kit to the selected kit
        print(self.name)  # for validation
        self.changetext()
        library = lib.library
        print(library)  # fpr validation
        # Sets the current kit data equal to the kit data from the selected kit
        self.kit = library[self.name]
        self.kit.t = library[self.name].t
        self.kit.d = library[self.name].d
        # plots the selected kits data if appropriate
        if self.type == "t":
            plotck(library[self.name].t)
        if self.type == "d":
            plotck(library[self.name].d)
        self.label.config(text="selected calibration kit: " + self.name)
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)


class SaveKitUi(StartUi):
    def __init__(self, master):
        super().__init__(master)
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

    def show_page_widgets(self):
        "A frame with a button to quit the window"
        self.value_inside = tkinter.StringVar(root)
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.master, textvariable=StartUi.namelabel)
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
        options = StartUi.cklist
        if not options:
            options = ["empty"]
        question_menu = tkinter.OptionMenu(self.master, self.value_inside, *options)
        question_menu.grid(row=2, column=1)
        submit_button = tkinter.Button(self.master, text='Submit',
                                       command=lambda: self.select_existing_file(StartUi.lib))
        submit_button.grid(row=2, column=2)
        self.export_button = tkinter.Button(self.master, text="export", state=DISABLED,
                                            command=lambda: self.export_file(StartUi.lib))
        self.export_button.grid(row=4, column=1)
        self.quit_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=5, column=1)

    def close_window(self):
        self.master.destroy()

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
            self.kit.t = library[self.name].t
            self.kit.d = library[self.name].d
        except KeyError:
            e.msgbox("You must select a calibration kit to export")
        # plots the selected kits data if appropriate
        if self.type == "t":
            plotck(library[self.name].t)
        if self.type == "d":
            plotck(library[self.name].d)
        if self.name != "" and self.type != "":
            self.export_button["state"] = NORMAL
        self.label.config(text="selected calibration kit: " + self.name)
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)

    def export_file(self, lib):
        library = lib.library
        if self.type == "t":
            library[self.name].print_to_file(library[self.name].t)
        if self.type == "d":
            library[self.name].print_to_file(library[self.name].d)


# where everything is called from
root = tkinter.Tk()
app = StartUi(root)
root.mainloop()
