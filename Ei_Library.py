# stores the calibration kits in a dictionary, responsible for collecting the various calibration kits
import pickle


class Library:

    def __init__(self):
        # library of calibration kits
        self._library = {}

    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, ei):
        self._library[ei.key] = ei

    # reads the .pkl file for the stored calibration kits, reads until EoF
    def get_ei_list(self):
        ei_list = []  # list within which the calibration kits are stored
        with open("eilib.pkl", "rb") as openfile:
            while True:
                try:
                    lib = pickle.load(openfile)  # reads the library stored within the file
                    for key, item in lib.items():  # reads through the library (its a dictionary class object)
                        self.library = item  # gets the "data" part of the dictionary and adds it into the usable
                        # item = [key, item]
                        ei_list.append(item)  # adds the item to the list of stored calkits
                except EOFError:
                    break
        return ei_list  # returns a list containing the un-pickled calibration kits
