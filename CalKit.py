# class that stores the calibration kit name and the data for its relevant t and d scans, which are stored as two
# instances of the Material class the class also handles the creation of the material classes and acts as a
# "subcontractor" of interface for the purpose of getting the data from a file
import Reader
import datamaths


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
    def add_scan(self, filename, material, time):
        read = Reader.scan_to_dict(filename)
        spl = datamaths.getspline(read)  # creates a spline object based on the data
        # passes the spline into the appropriate type of Material
        self.materials[material].date = time
        self.materials[material].spline = spl

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
