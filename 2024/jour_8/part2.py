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
letters = {}
my_print(x)
x = x.split('\n')
for i in range(len(x)):
    for j in range(len(x[0])):
        curr_carac = x[i][j]
        if curr_carac != '.':
            letters.setdefault(curr_carac, []).append([i,j])
            tot += 1

my_print(letters)
height = len(x)
widht = len(x[0])
antinodes = []
for values in letters.values():
    for elem in values:
        for elem2 in values:
            if elem2 == elem: continue
            z = elem2[0] - elem[0]
            k = elem2[1] - elem[1]
            for p in range(1, 25) : # 25 is hardcoded but it works becasue puzzle input is not too big
                # to do better we need to compute maximum gap before reach out of area in x
                antinodes.append([elem[0] - (z*p), elem[1] - (k*p)])
                antinodes.append([elem2[0] + (z*p), elem2[1] + (k*p)])

for i in range(len(x)):
    for j in range(len(x[0])):
        if [i,j] in antinodes and x[i][j] == '.':
            x[i] = x[i][:j] + "#" + x[i][j+1:]
            tot+= 1

print(tot, "ici")


if silent:
    for line in x:
        print("".join(line))
