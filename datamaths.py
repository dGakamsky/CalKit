# the mathematical operations happen here
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.optimize import fmin
from matplotlib import pyplot as plt

# generates a univariate spline
import outputer


def getspline(data):
    spl_list = []
    print(data)
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
    norm = l / (np.max(l) - np.min(l))
    return norm


def scale_scan(scan1, scan2):
    indexed_a_x, indexed_b_x, indexed_a_y, indexed_b_y = get_intersections(scan1, scan2)
    factor = get_rsd(indexed_b_y, indexed_a_y)
    scan_mod_data = scan_scaled(scan1, factor)
    scan_mod = (scan_mod_data, "scaled scan")
    scan1 = [scan1, "scan 1"]
    scan2 = [scan2, "scan 2"]
    connected_scan_manual = [connect_scans_manual(scan1, scan2, 350), "connected scan manual"]
    connected_scan_auto = [connect_scans_auto(scan1[0], scan2[0], 10), "connected scan auto"]
    scans = (scan1, scan2, scan_mod, connected_scan_manual, connected_scan_auto)
    outputer.plot_scans(scans)


def get_intersections(scan1, scan2):
    del scan2[1][-1]
    del scan2[0][-1]
    scan1_x = scan1[0]
    scan2_x = scan2[0]
    intersection = set(scan1_x).intersection(scan2_x)
    intersection = sorted(intersection)
    indices_a_x = [scan1[0].index(x) for x in intersection]
    indices_b_x = [scan2[0].index(x) for x in intersection]
    indexed_a_x = []
    indexed_b_x = []
    indexed_a_y = []
    indexed_b_y = []
    for i in indices_a_x:
        indexed_a_y.append(scan1[1][i])
    for i in indices_b_x:
        indexed_b_y.append(scan2[1][i])
    for i in indices_a_x:
        indexed_a_x.append(scan1[0][i])
    for i in indices_b_x:
        indexed_b_x.append(scan2[0][i])
    return indexed_a_x, indexed_b_x, indexed_a_y, indexed_b_y


def get_rsd(x, y):
    # rstd_norm(0, x,y)
    y2 = fmin(func=rstd_norm, x0=1, args=(x, y))
    # print(y2[0])
    new_y = []
    for i in range(len(y)):
        new_y.append(y[i] * y2[0])
    return y2[0]


def rstd_norm(k_scaling, intensities_scan1, intensities_scan2):
    rstd_norm_var = []
    lists = zip(intensities_scan1, intensities_scan2)
    for list1_i, list2_i in lists:
        rstd_norm_var.append((list1_i - list2_i * k_scaling) ** 2 / list1_i)
    var = np.sum(rstd_norm_var)
    return var


def plot(x, y, text):
    plt.plot(x, y, label=text)


def scan_scaled(scan, scaler):
    scan_x = scan[0]
    mod_y = []
    for i in range(len(scan[1])):
        mod_y.append(scan[1][i] * scaler)
    scan_mod = [scan_x, mod_y]
    return scan_mod


def connect_scans_manual(scan_mod, scan2, point):
    new_scan = [[], []]
    scan_mod = scan_mod[0]
    scan2 = scan2[0]
    if check_index(scan_mod, point) and check_index(scan2, point):
        index1 = check_index(scan_mod, point)
        index2 = check_index(scan2, point)
        scaler = scan2[1][index2] / scan_mod[1][index1]
        scan_mod_scaled = [[], []]
        for i in range(len(scan_mod[1][0:index1])):
            scan_mod_scaled[0].append(scan_mod[0][i])
            scan_mod_scaled[1].append(scan_mod[1][i] * scaler)
        new_scan[0] = (scan_mod_scaled[0][0:index1] + scan2[0][index2 + 1:-1])
        new_scan[1] = (scan_mod_scaled[1][0:index1] + scan2[1][index2 + 1:-1])
    else:
        outputer.error_message("index for overlap missing")
    return new_scan


def check_index(scan, point):
    try:
        if scan[0].index(point):
            return scan[0].index(point)
    except:
        return False


def connect_scans_auto(scan_mod, scan2, threshold):
    indexed_a_x, indexed_b_x, indexed_a_y, indexed_b_y = get_intersections(scan_mod, scan2)
    difference = []
    within_threshhold = []
    scan_mod_scaled = [[], []]
    new_scan = [[], []]
    for i in range(len(indexed_a_x)):
        difference.append(indexed_b_y[i] - indexed_a_y[i])
    for var in difference:
        if var <= threshold:
            within_threshhold.append(var)
    if not within_threshhold:
        outputer.error_message("no index found within threshold")
    else:
        point = difference.index(min(within_threshhold))
        index1 = scan_mod[0].index(indexed_a_x[point])
        index2 = scan2[0].index(indexed_b_x[point])
        scaler = indexed_b_y[point] / indexed_a_y[point]
        for i in range(len(scan_mod[0][0:index1])):
            scan_mod_scaled[0].append(scan_mod[0][i])
            scan_mod_scaled[1].append(scan_mod[1][i] * scaler)
        new_scan[0] = (scan_mod_scaled[0][0:index1] + scan2[0][index2 + 1:-1])
        new_scan[1] = (scan_mod_scaled[1][0:index1] + scan2[1][index2 + 1:-1])
    #print(new_scan)
    return new_scan
