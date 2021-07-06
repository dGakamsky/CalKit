# the mathematical operations happen here
import numpy as np
from scipy.interpolate import UnivariateSpline


# generates a univariate spline
def getspline(data):
    spl_list = []
    for i in range(len(data["data"])):
        x = data["data"][i][0]
        y = data["data"][i][1]
        new_y = normalize(y)
        spl = UnivariateSpline(x, new_y)
        spl.set_smoothing_factor(
            0.00001)  # low smoothing factor means that it serves as a close representation of the original data
        spl_list.append(spl)
    return spl_list


# normalizes the data for the Y axis for more effective plotting
def normalize(l):
    norm = (l - np.min(l)) / (np.max(l) - np.min(l))
    return norm
