# class that stores the calibration kit name and the data for its relevant t and d scans, which are stored as two
# instances of the Material class the class also handles the creation of the material classes and acts as a
# "subcontractor" of interface for the purpose of getting the data from a file
import Reader
import datamaths
from material import Lamp_Material
import numpy as np
import matplotlib.pyplot as plt
import easygui as e


def plot_ck(mat):
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
        self.materials = {"d": Lamp_Material("d"), "t": Lamp_Material("t")}

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
                self.materials["t"].spline = spl[i]
            if m == "d":
                self.materials["d"].spline = spl[i]

    # function that plots the data in a material passed in as parameter

    # this method is purely for testing purposes, prints out the calkit and some data from its two materials
    def print(self):
        print(type(self))
        print(self.name)
        print(type(self.materials["d"]))
        print("d scan")
        self.materials["d"].print()
        print(type(self.materials["t"]))
        print("t scan")
        self.materials["t"].print()
        print("end of calkit")

