import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import easygui as e


# exports a single scan as a txt file
def print_to_file(name, mat):
    y = []
    path = "C://Users//David//PycharmProjects//CalKit//exports"
    filename = (name + "_export.txt")
    fullpath = os.path.join(path, filename)
    file = open(fullpath, "w+")
    # delimiter is set to space, this could be changed later
    file.writelines("labels" + ", " + name + "\n")
    # generates the data for the file
    end = int(mat.x_end)
    start = int(mat.x_start)
    step = int(mat.step)
    steps = int((end - start) / step) + 1
    x = np.linspace(start, end, num=steps)
    for i in range(len(mat.spline)):
        spl = mat.spline[i]
        y.append(spl(x))
    # prints the data in procedurally
    for i in range(len(x)):
        file.write(str(x[i]) + ",")
        for j in range(len(y)):
            temp = str(y[j][i])
            file.write(temp + ",")
        file.write("\n")


# saves to the .pkl file, functions via append
def save_file(library, ck, name):
    # adds kit to library
    if type(name) != str:
        ck.name = name.get()
    library.library = ck
    ck.print()  # for testing
    dump_ck_list(library)  # calls the library to dump to the pickle file
    for i in library.get_ck_list():  # testing function to validate what was printed
        i.print()


# dumps the library to the .pkl
def dump_ck_list(self):
    with open("cklib.pkl", "wb") as openfile:
        pickle.dump(self.library, openfile)


def plot_ck(mat, plt):
    if len(mat.spline) != 0:
        plt.clear()
        for i in range(len(mat.spline)):
            x = []
            y = []
            date = "no date loaded"
            if mat.date is not None:
                date = mat.date
            text_title = str("scan created date: " + str(date))
            end = int(mat.x_end)
            start = int(mat.x_start)
            step = mat.step
            steps = int((end - start) / step)  # determines the number of data-points
            x = np.linspace(mat.x_start, mat.x_end,
                            num=steps)  # extrapolates the X axis based on the start, stop and number of data-points
            try:
                spl = mat.spline[i]
                y = spl(x)  # gets the Y axis data
                plt.set(xlabel="Wavelength, nm", ylabel="Intensity, a.u.", title=text_title)
                plt.plot(x, y)  # plots it
            except TypeError:
                error_message("This calibration kit does not have a scan of the selected type stored")
        plt.grid()
    else:
        error_message("This calibration kit does not have a scan of the selected type stored")


def error_message(text):
    e.msgbox(text)


def plot_scans(scans):
    for scan in scans:
        plt.plot(scan[0][0], scan[0][1], label=scan[1])
    plt.legend()
    plt.show()
