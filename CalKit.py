# class that stores the calibration kit name and the data for its relevant t and d scans, which are stored as two
# instances of the Material class the class also handles the creation of the material classes and acts as a
# "subcontractor" of interface for the purpose of getting the data from a file
import Reader
import datamaths
from material import Lamp_Material
import numpy as np
import matplotlib.pyplot as plt
import easygui as e





def plotck(mat):
    if len(mat.spline) != 0:
        plt.figure()
        for i in range(len(mat.spline)):
            x = []
            y = []
            end = mat.x_end[i]
            start = mat.x_start[i]
            step = mat.step
            steps = int((end - start) / step)  # determines the number of data-points
            x = np.linspace(mat.x_start, mat.x_end,
                            num=steps)  # extrapolates the X axis based on the start, stop and number of data-points
            try:
                spl = mat.spline[i]
                y = spl(x)  # gets the Y axis data
                plt.plot(x, y)  # plots it
            except TypeError:
                e.msgbox("This calibration kit does not have a scan of the selected type stored")
        plt.show()
    else:
        e.msgbox("This calibration kit does not have a scan of the selected type stored")


class CalKit:

    def __init__(self):
        self._name = ""
        self.d = Lamp_Material("d")
        self.t = Lamp_Material("t")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    # receives a filename and type when called, then passes that onto a reader which returns data
    def add_scan(self, filename, m):
        read = Reader.scan_to_dict(filename)
        spl = datamaths.getspline(read)  # creates a spline object based on the data
        # passes the spline into the appropriate type of Material
        for i in range(len(spl)):
            if m == "t":
                print(spl)
                self.t.spline = spl[i]
            if m == "d":
                self.d.spline = spl[i]

    # function that plots the data in a material passed in as parameter

    # this method is purely for testing purposes, prints out the calkit and some data from its two materials
    def print(self):
        print(type(self))
        print(self.name)
        print(type(self.d))
        print("d scan")
        self.d.print()
        print(type(self.t))
        print("t scan")
        self.t.print()
        print("end of calkit")

    # exports a single scan as a txt file
    def print_to_file(self, mat):
        file = open("file" + self.name + "export.txt", "w+")
        # delimiter is set to space, this could be changed later
        file.writelines("labels" + "/s" + self.name + "\n")
        # generates the data for the file
        end = mat.x_end
        start = mat.x_start
        step = mat.step
        steps = int((end[0] - start[0]) / step)
        x = np.linspace(mat.x_start[0], mat.x_end[0],
                        num=steps)
        for i in range(len(mat.spline)) :
            spl = mat.spline[i]
            y = []
            y.append(spl(x))
        # prints the data in procedurally
        for i in range(len(x)):
            file.write(str(x[i]) + "/s")
            for j in range(len(y)):
                file.write(str(y[j]) + "/s")
            file.write("/n")
