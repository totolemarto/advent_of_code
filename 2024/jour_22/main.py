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


def compute_secret_number(init : int) -> int :
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
    return init

tot = 0
flag = False
i = 0
for line in mat:
    tot += compute_secret_number(int(line)) 
print(tot)
