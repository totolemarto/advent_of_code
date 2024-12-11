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
    line = list(map(int,elem.split("x")))
    line.sort()
    for i in range(2):
        size =line[i]
        tot += 2 * size
    tot += (line[0] * line[1] * line[2])
print(tot)
