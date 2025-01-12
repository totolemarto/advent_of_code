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


def get_number_in_columns(mat :list[str]) -> list[int]:
    number_line = len(mat)
    number_columns = len(mat[0])
    result = [0] *number_columns
    for j in range(number_columns):
        tot = 0
        for i in range(number_line):
            if mat[i][j] == "#":
                tot+= 1
        result[j] = tot
    return result
        


mat = x.split("\n\n")
dico = {}
flag = 0
to_do = []
key= []
lock = []
i = 0
key_columns = []
lock_columns = []
for matrice in mat:
    if not "#" in matrice[0]:
        key.append(i)
        number_line = len(matrice.split("\n"))
        number_columns = len(matrice.split("\n")[0])
        key_columns.append(get_number_in_columns(matrice.split("\n")))
    else:
        lock.append(i)
        lock_columns.append(get_number_in_columns(matrice.split("\n")))
    i+= 1
result = []
to_print = 0
for keys in key_columns:
    for locks in lock_columns:
        flag = 0
        for i in range(number_columns):
            if keys[i] + locks[i] > number_line:
                flag = 1
        if not flag:
            result.append([keys,locks])
            to_print += 1
my_print(result)
print(to_print)

