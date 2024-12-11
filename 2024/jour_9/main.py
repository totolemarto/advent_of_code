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
t = []
is_file = 1
curr = 0
for i in range(len(x)):
    if is_file:
        for _ in range(int(x[i])):
            t.append(str(curr))
        curr+= 1
        if i == 0:
            deb = int(x[i])
    else:
        for _ in range(int(x[i])):
            t.append("A")
    is_file = 1 - is_file
my_print(curr)
my_print(t)
j = t
my_print(j)
curr = len(j) - 1
my_print("len de j : ", len(j))
while curr  > deb :
    my_print(deb, curr, j[curr])
    while j[deb ] != "A":
        deb+= 1
    if  j[curr] != "A":
        my_print("ç passeé")
        tmp = j[curr]
        j[curr] = j[deb]
        j[deb] = tmp
        deb+= 1
    curr-=1
tot = 0
flag = 0
if silent:
    for i, elem in enumerate(j):
        if elem == "A" and not flag:
            flag = 1
        if flag and elem != "A":
            flag += 1
    print(flag)
gap = 0
for i, elem in enumerate(j):
    if elem == "A":
        gap -=1
        continue
    tot += int(elem) * (i+gap)

print(tot)
