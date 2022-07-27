import fileinput
import sys

# Вариант 1 - удаление пустых строк в файле
# for line in fileinput.FileInput("C:\\Users\\akolzin\\Downloads\\Лист1 — копия.csv",inplace=1):
#     if line.rstrip():
#         print(line)

# Вариант 2 - удаление пустых строк в файле
with open('C:\\Users\\akolzin\\Downloads\\Лист1 — копия1.csv', 'r') as inf:
    for line in inf:
        if line.strip():
            print(line)
with open('C:\\Users\\akolzin\\Downloads\\Лист1 — копия1.csv', 'r') as inf, open('outfile.txt', 'w') as out:
    for line in inf:
        if line.strip():
            out.write(line)