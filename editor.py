file2 = "Corr Factor (T) Visible PMT_test_.txt"

f = open(file2, "r")
lines = f.read().splitlines()
print(lines)
f2 =open("modified.txt", "w")

for line in lines:
    f2.write(line+",\n")

