def fix_format(filename):
    f = open(filename, "r")
    lines = f.read().splitlines()
    print(lines)
    f2 = open(filename, "w")
    for line in lines:
        f2.write(line + ",\n")




