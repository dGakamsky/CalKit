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
        self.file_loaded = False

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
        tkinter.Label(self.master, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                        padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Deuterium Scan", variable=self.v, value="d",
                            command=lambda: self.set_type("d")).grid(row=1, column=1,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Tungsten Scan", variable=self.v, value="t",
                            command=lambda: self.set_type("t")).grid(row=1, column=2,
                                                                     padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Label(self.master, text="Select file with update data :").grid(row=3, column=0, sticky=W,
                                                                               padx=10, pady=10, ipadx=5,
                                                                               ipady=5)
        browse_file = tkinter.Button(self.master, text="browse files",
                                     command=lambda: self.open_file_browser())  # searches files for input file
        browse_file.grid(row=3, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.select_file = tkinter.Button(self.master, text="select file", state=DISABLED,
                                          command=lambda: self.open_file(self.filename, self.name, self.kit))  # reads
        # the file
        self.select_file.grid(row=3, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        options = StartUi.cklist
        if not options:
            options = ["empty"]
        self.label = tkinter.Label(self.master, text="Selected calibration kit :")
        self.label.grid(row=2, column=0, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        question_menu = tkinter.OptionMenu(self.master, self.value_inside, *options)
        question_menu.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        submit_button = tkinter.Button(self.master, text='Submit',
                                       command=lambda: self.select_existing_file(StartUi.lib))
        submit_button.grid(row=2, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        self.save_file = tkinter.Button(self.master, text="save",
                                        state=DISABLED,
                                        command=lambda: save_file(
                                    self.lib, self.kit))  # saves the file to the .pkl file given the input parameters
        self.save_file.grid(row=6, column=1, padx=10, pady=10, ipadx=5, ipady=5)
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
            plot_ck(kit.materials["d"])
        if self.type == "t":
            kit.add_scan(filename, "t")
            plot_ck(kit.materials["t"])
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
            plot_ck(library[self.name].materials["t"])
        if self.type == "d":
            plot_ck(library[self.name].materials["d"])
        self.label.config(text="Selected calibration kit: " + self.name)
        return self.name, self.kit  # returns the kit

    def changetext(self):
        self.namelabel.set("current kit name: " + self.name)