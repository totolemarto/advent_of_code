#!/bin/python3

from sys import argv


if len(argv) != 2 :
    print(f"usage : {argv[0]} <fichier>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()


def find(union, source, but):
    while but in source.keys():
        if union[source] == but:
            return 1
        source = union[source]
    return 0


union = {}
mat = []
flag = 1
sume = 0
for line in x.split("\n"):
    if flag and not "|" in line : 
        flag = 0
        continue
    if flag:
        x, y = line.split("|")
        if y not in union.keys():
            union[y]= [x]
        else:
            union[y].append(x)
    else:
        flag2=1
        line = line.split(",")
        if line[0] == '':
            break
        for i,elem in enumerate(line):
            if elem in union.keys():
                intersect = [ x for x in union[elem] if x in line[i + 1:]] 
            else:
                intersect = []
            print( intersect)
            if intersect != []:
                flag2=0
                break
        if flag2:
            sume += int(line[len(line)//2])
print(sume)
