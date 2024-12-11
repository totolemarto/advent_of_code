#!/bin/python3

from sys import argv

def my_print(*args, **kwargs):
    global silent
    if silent: print(*args, **kwargs)
if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read().strip()
silent = int(argv[2]) 

line = x.split()
my_print(line)

for _ in range(25):
    new = []
    my_print(line)
    for elem in line:
        if int(elem) == 0:
            new.append("1")

        elif len(elem) % 2 == 0:
            j = len(elem) // 2
            new.append(str(int(elem[:j])))
            try:
                x = int(elem[j:])
            except:
                x = 0
            new.append(str(x))
        else:
            new.append(str(int(elem) * 2024))
    line = new
my_print(line)
print(len(line))
