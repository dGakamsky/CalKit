import CalKit
import numpy as np
import pickle
import os

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
    end = mat.x_end
    start = mat.x_start
    step = mat.step
    steps = int((end[0] - start[0]) / step) + 1
    x = np.linspace(mat.x_start[0], mat.x_end[0],
                    num=steps)
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
def save_file(library, ck):
    print(type(ck))  # for testing
    # adds kit to library
    library.library = ck
    ck.print()  # for testing
    dump_ck_list(library)  # calls the library to dump to the pickle file
    for i in library.get_ck_list():  # testing function to validate what was printed
        i.print()


# dumps the library to the .pkl
def dump_ck_list(self):
    with open("cklib.pkl", "wb") as openfile:
        pickle.dump(self.library, openfile)
