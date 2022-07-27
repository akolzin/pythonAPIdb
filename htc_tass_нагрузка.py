import fileinput
import sys

# for line in fileinput.FileInput("C:\\Users\\akolzin\\Downloads\\Лист1 — копия.csv",inplace=1):
#     if line.rstrip():
#         print(line)

# string = open('C:\\Users\\akolzin\\Downloads\\Лист1 — копия.csv').readlines()
#
# for i in string:
#     if not i.isspace():
#         print(i.replace('\n', ''))

# with open("C:\\Users\\akolzin\\Downloads\\Лист1 — копия.csv","r") as f:
#     for line in f:
#         if not line.isspace():
#             sys.stdout.write(line)

# with open("C:\\Users\\akolzin\\Downloads\\Лист1 — копия1.csv", "r") as f:
#     print("".join(line for line in f if not line.isspace()))

with open('C:\\Users\\akolzin\\Downloads\\Лист1 — копия1.csv', 'r') as inf:
    for line in inf:
        if line.strip():
            print(line)
with open('C:\\Users\\akolzin\\Downloads\\Лист1 — копия1.csv', 'r') as inf, open('outfile.txt', 'w') as out:
    for line in inf:
        if line.strip():
            out.write(line)