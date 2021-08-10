import Reader
import datamaths

file1 = "Corr Factor (D) Visible PMT_test_.txt"
file2 = "modified.txt"

files = [file1, file2]
dataset = []


def getreader(filename):
    read = Reader.scan_to_dict(filename)
    data = [read["data"][0][0], read["data"][0][1]]
    dataset.append(data)


def main():
    for file in files:
        getreader(file)
    datamaths.scale_scan(dataset[0], dataset[1])


main()
