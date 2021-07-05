# the mathematical operations happen here
from Reader import scan_to_dict
import numpy as np
from scipy.interpolate import UnivariateSpline


# "subcontractor" of Calkit, returns dictionary
def read(filename):
    filecontent = scan_to_dict(filename)
    return filecontent


# generates a univariate spline
def getspline(data):
    x = data["data"][0][0]
    y = data["data"][0][1]
    new_y = normalize(y)
    spl = UnivariateSpline(x, new_y)
    spl.set_smoothing_factor(
        0.00001)  # low smoothing factor means that it serves as a close representation of the original data
    return spl


# normalizes the data for the Y axis for more effective plotting
def normalize(l):
    norm = (l - np.min(l)) / (np.max(l) - np.min(l))
    return norm
