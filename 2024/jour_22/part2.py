#!/bin/python3

from sys import argv

def my_print(*args, **kwargs): 
    if silent: print(*args, **kwargs)

if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)

with open(argv[1],"r") as f:
    x = f.read().strip()
silent = int(argv[2]) 

mat = x.split("\n")

def compute_best_sequence(init : int):
    seq = [0,0,0,0]
    already_done = []
    index = 0
    actual = init %10
    cur = init
    for _ in range(2000):
        cur *= 64
        cur = cur ^ init
        init = cur % 16777216
        cur = init // 32
        cur = cur ^ init
        init = cur % 16777216
        cur = init * 2048
        cur = cur ^ init
        init = cur % 16777216
        seq[index] = init % 10 - actual
        index+= 1 
        if index == 4:
            if str(seq) not in already_done:
                dico[str(seq)] += init % 10
                already_done.append(str(seq))
            index = 3
            seq[0] = seq[1]
            seq[1] = seq[2]
            seq[2] = seq[3]
        actual = init % 10
dico = {}
for i1 in range(-9,10,1):
    for i2 in range(-9,10,1):
        for i3 in range(-9,10,1):
            for i4 in range(-9,10,1):
                dico[str([i1,i2,i3,i4])]= 0
for line in mat:
    compute_best_sequence(int(line))
print(max(dico.values()))
