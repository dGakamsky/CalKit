from tkfilebrowser import askopenfilename
import outputer
from CalKit import CalKit, plot_ck
from Interface import StartUi
import os

class NewKitUi(StartUi):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Load New Calkit")
        self.master.geometry("500x500")
        self.namelabel = tkinter.StringVar(self.master)
        self.namelabel.set("No kit name selected")
        self.make_calibration_kit()
        self.name = ""
        self.filename = ""
        self.type = ""
        self.file_loaded = False

    def make_calibration_kit(self):
        self.kit = CalKit()

    def show_page_widgets(self):
        self.frame = tkinter.Frame(self.master)
        self.frame.label = tkinter.Label(self.master, textvariable=self.namelabel)
        self.frame.label.grid()
        self.quit_button = tkinter.Button(
            self.frame, text="close window",
            command=self.close_window)
        self.v = tkinter.StringVar(self.master, "1")
        tkinter.Label(self.master, text="Type of lamp material :").grid(row=1, column=0, sticky=W,
                                                                        padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Deuterium", variable=self.v, value="d",
                            command=lambda: self.set_type_and_validate("d")).grid(row=1, column=1,
                                                                                  padx=10, pady=10, ipadx=5, ipady=5)
        tkinter.Radiobutton(self.master, text="Tungsten", variable=self.v, value="t",
                            command=lambda: self.set_type_and_validate("t")).grid(row=1, column=2,
                                                                                  padx=10, pady=10, ipadx=5, ipady=5)
        self.label = tkinter.Label(self.master, text="no file selected")
        self.label.grid(row=3, column=0, ipadx=5, ipady=5)
        browse_button = tkinter.Button(self.master, text="browse files",
                                       command=lambda: self.open_file_browser())  # searches files for input file
        browse_button.grid(row=3, column=1, ipadx=5, ipady=5)
        # b.config(style="awdark.style.Menubutton")
        self.select_file = tkinter.Button(self.master, text="select file", state=DISABLED,
                                          command=lambda: self.open_file(self.filename, self.name,
                                                                         self.kit))  # reads
        # the file
        self.select_file.grid(row=3, column=2, ipadx=5, ipady=5)
        # text entry box
        tkinter.Label(self.master, text="Enter name of calibration kit:").grid(row=2, column=0, sticky=W,
                                                                               padx=10, pady=10, ipadx=5,
                                                                               ipady=5)
        save_name = tkinter.Entry(self.master)
        save_name.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        save_name.focus_set()
        f = tkinter.Button(self.master, text="save name", command=lambda: self.callback(save_name))  # name input
        f.grid(row=2, column=2, ipadx=5, ipady=5)
        self.save_file = tkinter.Button(self.master, text="save",
                                        state=DISABLED,
                                        command=lambda: outputer.save_file(StartUi.lib,
                                                                  self.kit))  # saves the file to the .pkl file
        # given
        self.save_file.grid(row=4, column=1, pady=50, ipadx=5, ipady=5)
        self.quit_button.pack(fill=tkinter.X, pady=50, ipadx=10, ipady=10)
        self.frame.grid(row=5, column=1)

    def close_window(self):
        self.master.destroy()

    def callback(self, e):
        self.name = e.get()
        if self.filename != "" and self.type != "":
            self.select_file["state"] = NORMAL
        self.change_text()
        print("Name set to: " + self.name)  # print is for validation
        return self.name

    def change_text(self):
        self.namelabel.set("current kit name: " + self.name)

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
        if self.type != "" and self.name != "":
            self.save_file["state"] = NORMAL

    def set_type_and_validate(self, t):
        self.type = t
        # checks for the presence of a name and filename, and if found enables loading the scandata
        self.validate()
        return self.type

    def validate(self):
        if self.name != "" and self.filename != "" and self.type != "":
            self.select_file["state"] = NORMAL
        if self.file_loaded:
            self.save_file["state"] = NORMAL

    def open_file_browser(self):
        filename = askopenfilename(initialdir="/Users/David/PycharmProjects/CalKit",
                                   title="Select file",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        if filename != "":  # if a file is selected then the filename property is set to it
            self.label.config(text="selected file: " + os.path.basename(filename))
            if self.type != "":
                self.select_file["state"] = NORMAL
            print(filename)
            self.filename = filename
            return self.filename