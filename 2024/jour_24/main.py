#!/bin/python3

from sys import argv
from copy import deepcopy

def my_print(*args, **kwargs): 
    if silent: print(*args, **kwargs)

if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)

with open(argv[1],"r") as f:
    x = f.read().strip()
silent = int(argv[2]) 

mat = x.split("\n")
dico = {}
flag = 0
to_do = []
for line in mat:
    my_print(line)
    if not line or flag:
        if not flag:
            my_print(dico)
            flag = 1
            continue
        to_do.append(line)

    else:
        dico[line.split(":")[0]] = int(line.split(":")[1])
result = 0
while len(to_do) != 0:
    to_stay = []
    cur = deepcopy(to_do)
    for line in cur :
        op1 = line.split(" ")[0]
        op2 = line.split(" ")[2]
        if op1 not in dico.keys() or op2 not in dico.keys():
            to_stay.append(line)
            continue
        if "AND" in line:
            result = dico[op1] & dico[op2]
        if "OR" in line:
            result = dico[op1] | dico[op2]
        if "XOR" in line:
            result = dico[op1] ^ dico[op2]
        dico[line.split("->")[1][1:]] = result
    to_do = deepcopy(to_stay)
my_print(dico)
result = []
for elem in dico.keys():
    if elem[0] == "z":
        result.append(elem)
result.sort()
result.reverse()
string = ""
for elem in result:
    my_print(dico[elem], end="")
    string += str(dico[elem])
print("\n",int(string, 2))



