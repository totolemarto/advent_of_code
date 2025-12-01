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

tot = 0

for elem in x.split("\n"):
    r = 0
    line = elem.split("x")
    mini = int(line[0]) * int(line[1])
    for i in range(3):
        size =int(line[i]) *  int(line[(i+1) % 3])
        r += 2 * size
        if size < mini:
            mini = size
    tot += r + mini
print(tot)
