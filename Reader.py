# this method turns the data in a given input file into a dictionary where the key is the first entry in a line for
# the header, and "data" for the numerical data
import os
import re
from detect_delimiter import detect


# takes a filename as input
def scan_to_dict(fn):
    dictionary = {}
    f = open(fn, "r")
    x_axis_list = []
    y_axis_list = []
    short_header = False
    scans, checklist = getscans(fn, x_axis_list, y_axis_list)
    title_length = get_title_length(f, checklist)
    # resets the reader to the start of the file and prepares to read into the dictionary
    f.seek(0, 0)
    # skips the title
    for j in range(title_length):
        line = f.readline()
    # inputs the label into the dictionary
    linetodict(f, dictionary, scans)
    line = f.readline()  # reads an extra line forwards
    if re.match("\d",
                line):  # if the header is short then the next line will contain digits at the start owing to it
        # being numerical
        short_header = True  # shortheader is set to true
        # reads the data into the dictionary
        column = line.split(detect(line))  # breaks the line up
        for j in range(scans):  # reads the data into the arrays created for each scan
            i = j
            if column[
                1 + j] != " ":  # iterates through the number of scans, only scans in if there is appropriate Y data
                # (skips over blank entries)
                x_axis_list[i].append(float(column[0]))  # x axis is always the same
                y_axis_list[i].append(float(column[1 + j]))  # gives the proper Y axis
        read_data(f, scans, x_axis_list, y_axis_list, dictionary)
    # adds the remaining header lines into the header
    if not short_header:
        for j in range(19):
            linetodict(f, dictionary, scans)
        # skips a line if the header is long
        line = f.readline()
        # reads the data into a list which is in turn added into the dictionary under the key of "data"
        read_data(f, scans, x_axis_list, y_axis_list, dictionary)
    return dictionary


def read_data(file, scans, x_axis_list, y_axis_list, dictionary):
    # used to store the numerical data
    data_list = []
    # repeats the process for each subsequent line of data until EOF
    for line in file:
        line = line.strip()
        column = line.split(detect(line))
        for j in range(scans):
            i = j
            if column[1 + j] != " ":
                x_axis_list[i].append(float(column[0]))
                y_axis_list[i].append(float(column[1 + j]))

    for j in range(scans):
        i = j
        data_list.append([x_axis_list[i], y_axis_list[i]])
    dictionary["data"] = data_list
    return dictionary


# sends the binary reader to the end of the file, where it will check the number of separate columns to determine
# the number of scans
def getscans(fn, x_axis_list, y_axis_list):
    f3 = open(fn, "rb")
    f3.seek(-2, os.SEEK_END)
    while f3.read(1) != b'\n':
        f3.seek(-2, os.SEEK_CUR)
    line = f3.readline().decode()
    line.strip()
    checklist = line.split(detect(line))
    scans = ((
                 len(checklist)) - 2)  # number is based on number of "columns" when you break up the file via
    # delimiter - the number of "fixed" columns
    # makes the necessary number of arrays to store the data
    for i in range(scans):
        i = []
        x_axis_list.append(i)
    for i in range(scans):
        i = []
        y_axis_list.append(i)
    return scans, checklist


def linetodict(f, dictionary, scans):
    line = f.readline()
    line = line.strip()
    column = line.split(detect(line))
    line_data = []
    for i in range(scans):
        line_data.append(column[1 + i])
        dictionary[column[0]] = line_data
    return dictionary


def get_title_length(f, checklist):
    title_length = 0
    for line in f.readlines():
        if len(line.split(detect(line))) == (len(checklist)):
            break
        else:
            title_length = title_length + 1
    return title_length
