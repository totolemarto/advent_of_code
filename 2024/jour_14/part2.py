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

mat = x.split("\n")
lines = len(mat)

def get_current_y(line, number = 1):
    line = line.split("=")
    return int(line[number].split(",")[1].split()[0])

def get_current_x(line, number = 1):
    line = line.split("=")
    return int(line[number].split(",")[0])
tot = 0
robots = []

for line in mat:
    cur_x = get_current_x(line, 1)
    cur_y = get_current_y(line, 1)
    move_x = get_current_x(line, 2)
    move_y = get_current_y(line, 2)
    my_print(cur_x,cur_y,move_x,move_y)
    robots.append([cur_x,cur_y,move_x,move_y])


line =  103
columns =  101

for k in range(100000):
    for elem in robots:
        elem[0] += elem[2] 
        elem[0] = elem[0] % columns
        elem[1] += elem[3] 
        elem[1] = elem[1] % line
    tmp = sorted(robots, key = lambda valeur: (valeur[0], valeur[1]))
    max_line = 0
    cur_line = 0
    for i,elem in enumerate(tmp):
        if i == 0 :
            continue
        if elem[0] == tmp[i - 1][0] and elem[1] == tmp[i - 1][1] + 1:
            cur_line += 1
        else:
            if cur_line > max_line:
                max_line = cur_line
                good = elem[0]
            cur_line = 0
    my_print(k, max_line)
    if max_line < 8 :
        continue
    my_print(max_line)
    for i in range(line):
        for j in range(columns):
            flag = 0
            for elem in robots:
                if j == elem[0] and i == elem[1]:
                    flag = 1
            if flag:
                print("X", end= "")
            else:
                print(".", end="")
        print()
    print(k + 1)
    input() ## use to see the tree :)
