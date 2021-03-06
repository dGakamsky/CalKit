
class App:

    # init method could use to be cleaned up, but this is where all the various buttons are mapped from and also
    # where the general details of the worked kit are stored in between button calls
    def __init__(self, master):
        # instantiates the library
        self.value_inside = tkinter.StringVar(root)
        self.namelabel = tkinter.StringVar(root)
        self.namelabel.set("No kit name selected")
        self.textlabel = tkinter.Label(master, textvariable=self.namelabel)
        self.textlabel.pack()
        self.lib = Library()
        self.kit = CalKit()
        self.cklist = ["empty"]  # default necessary for when/if the file being read from is empty
        if self.lib.get_ck_list():
            self.cklist = []  # removes the placeholder value
            for i in self.lib.get_ck_list():  # populates the dropdown
                self.cklist.append(i.name)
                i.print()
        # creates the "box" for the ui
        self.name = ""
        self.filename = ""
        self.type = ""
        self.window = master
        self.add_buttons(master)
        # Dictionary to create multiple buttons
        root.title("CalKit Calibration")
        load_ck_list(self.lib)  # loads the list of stored calkits
        mainloop()  # runs the interface

    # opens the file browser
    def add_buttons(self, master):
        # radiobutton that can be used to set the type
        v = tkinter.StringVar(master, "1")
        tkinter.Radiobutton(master, text="Deuterium Scan", variable=v, value="d",
                            command=lambda: self.set_type("d")).pack()
        tkinter.Radiobutton(master, text="Tungsten Scan", variable=v, value="t",
                            command=lambda: self.set_type("t")).pack()
        # function buttons
        b = tkinter.Button(master, text="browse files",
                           command=lambda: self.open_file_browser())  # searches files for input file
        b.pack()
        self.b2 = tkinter.Button(master, text="select file", state=DISABLED,
                                 command=lambda: self.open_file(self.filename, self.name, self.kit))  # reads
        # the file
        self.b2.pack()
        # text entry box
        e = tkinter.Entry(master)
        e.pack()
        e.focus_set()
        f = tkinter.Button(master, text="save text", command=lambda: self.callback(e))  # name input
        f.pack()
        self.c = tkinter.Button(master, text="save file",
                                state=DISABLED,
                                command=lambda: save_file(
                                    self.lib, self.kit))  # saves the file to the .pkl file given the input parameters
        self.c.pack()
        question_menu = tkinter.OptionMenu(master, self.value_inside, *self.cklist)
        question_menu.pack()
        # the command that initiates the selection of the chosen file from the dropdown
        submit_button = tkinter.Button(master, text='Submit', command=lambda: self.select_existing_file(self.lib))
        submit_button.pack()
        # the button that initiates the export of the selected scan
        export_button = tkinter.Button(master, text="export", command=lambda: self.export_file(self.lib))
        export_button.pack()

        # Set the default value of the variable
        self.value_inside.set(self.cklist)

    # sets the type of the scan
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
        return self.name, self.kit  # returns the kit

    # returns input text
    def callback(self, e):
        self.name = e.get()
        print("Name set to: " + self.name)  # print is for validation
        if self.filename != "" and self.type != "":
            self.b2["state"] = NORMAL
        self.changetext()
        return self.name

    # gets passed the filename, library, name and the current kit and populates and adds the scan onto the library
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

    # gets passed the library and exports the data from the currently loaded file by checking for the name
    def export_file(self, lib):
        library = lib.library
        if self.type == "t":
            library[self.name].print_to_file(library[self.name].t)
        if self.type == "d":
            library[self.name].print_to_file(library[self.name].d)

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)

