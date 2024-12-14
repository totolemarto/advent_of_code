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

for i in range(100):
    for elem in robots:
        elem[0] += elem[2] 
        elem[0] = elem[0] % columns
        elem[1] += elem[3] 
        elem[1] = elem[1] % line

for i in range(line):
    for j in range(columns):
        flag = 0
        for elem in robots:
            if j == elem[0] and i == elem[1]:
                flag = 1
        if flag:
            my_print("X", end= "")
        else:
            my_print(".", end="")
    my_print()

z=[0,0,0,0]

for elem in robots:
    my_print(elem)
    if elem[0] < columns // 2:
        if elem[1] < line // 2:
            z[0] += 1
        elif elem[1] > line // 2:
            z[1] += 1
        else:
            print(f"ici {elem=}")
    elif elem[0]  > columns // 2 :
        if elem[1] < line // 2:
            z[2] += 1
        elif elem[1] > line // 2 :
            z[3] += 1
        else:
            print(f"ici {elem=}")
    else:
        print(f"ici {elem=}")
print(z)
tot = 1
for elem in z:
    tot *= elem
print(tot)
