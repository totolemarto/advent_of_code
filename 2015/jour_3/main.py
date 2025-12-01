#!/bin/python3
from sys import argv
from copy import deepcopy
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
already_see = [[0,0]]
cur = [0,0]
for elem in x:
    if elem == "^":
        cur[0] -= 1
    elif elem == "<":
        cur[1] -= 1
    elif elem == ">":
        cur[1] += 1
    elif elem == "v":
        cur[0] += 1
    else:
        continue
    if cur not in already_see:
            already_see.append(deepcopy(cur))
print(len(already_see)) 
