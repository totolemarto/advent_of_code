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
map = []
flag = 0
i = 0
move = ""

def possible(map: list[list[str]], deplacement :list[int] , pos_debut : list[int], lines, columns):
    new_pos =[ pos_debut[0] + deplacement[0],pos_debut[1] + deplacement[1]]
    y,x = new_pos
    if y < 0 or y >= lines or x < 0 or x >= columns:
        return map, pos_debut
    if map[y][x] == "#":
        return map, pos_debut
    if map[y][x] == ".":
        map[y][x] = "@"
        map[pos_debut[0]][pos_debut[1]] = "."
        pos_debut = [y,x]
        return map, pos_debut
    ## on est sur le cas ou il y a une boite devant
    i = y
    j = x
    my_print(lines,columns)
    while i != -1 and j != -1 and map[i][j] != "." :
        if map[i][j] == "#":
            i = -1
            j = -1
            break
        i+= deplacement[0]
        j+= deplacement[1]
        my_print(i,j)
    my_print(i,j)
    if i != -1 and j != -1 :
        if i != pos_debut[0]:
            for k in range(i, pos_debut[0], -deplacement[0]):
                map[k][j] = map[k - deplacement[0]][j]

        else:
            for k in range(j, pos_debut[1] , -deplacement[1]):
                map[i][k ] = map[i][k - deplacement[1]]
        map[pos_debut[0]][pos_debut[1]] = "."
        return map, [pos_debut[0] + deplacement[0] , pos_debut[1] + deplacement[1]]
    else:
        return map, pos_debut
    


pos_debut = [0,0]
for line in mat:
    if line == "":
        flag = 1
        continue
    if not flag:
        map.append(list(line))
        if "@" in line:
            pos_debut = [i, line.index("@")]
        i+= 1
    else:
        move += str(line)
my_print(move)
for line in map:
    my_print("".join(line))
my_print(pos_debut)
deplacement = {"^": [-1,0], "<":[0,-1], ">":[0,1], "v":[1,0]}
lines = len(map)
columns = len(map[0])

for current_move in move:
    map, pos_debut = possible(map, deplacement[current_move], pos_debut, lines,columns)
    for line in map:
        my_print("".join(line))
tot = 0
for y in range(lines):
    for x in range(columns):
        if map[y][x] == "O":
            tot += y *100 + x
print(tot)
