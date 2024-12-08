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


letters = {}
my_print(x)
x = x.split('\n')
for i in range(len(x)):
    for j in range(len(x[0])):
        curr_carac = x[i][j]
        if curr_carac != '.':
            if curr_carac not in letters.keys():
                letters[curr_carac] = [[i,j]]
            else:
                letters[curr_carac].append([i,j])
my_print(letters)

antinodes = []
for values in letters.values():
    for elem in values:
        for elem2 in values:
            if elem2 == elem: continue
            z = elem2[0] - elem[0]
            k = elem2[1] - elem[1]
            antinodes.append([elem[0] - z, elem[1] - k])
            antinodes.append([elem2[0] + z, elem2[1] + k])
tot = 0
for i in range(len(x)):
    for j in range(len(x[0])):
        if [i,j] in antinodes:
            line = list(x[i])
            line[j] = '#'
            x[i] = "".join(line)
            tot+= 1
for line in x:
    my_print("".join(line))
print(tot, "ici")
