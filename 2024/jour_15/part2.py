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
    liste_boite = [[y,x]]
    if map[y][x] == '[':
        liste_boite.append([y,x+1])
    if map[y][x] == ']':
        liste_boite.append([y,x-1])

    my_print(lines,columns)
    my_print(f"{deplacement=}")

    while True:
        flag2= 0
        for elem in liste_boite:
            nexti,nextj = elem
            nexti+=deplacement[0]
            nextj+=deplacement[1]
            if map[nexti][nextj] == "#":
                return map, pos_debut
            if map[nexti][nextj] == "[":
                if [nexti,nextj] not in liste_boite:
                     liste_boite.append([nexti,nextj])      
                     liste_boite.append([nexti,nextj+1])
                     flag2= 1
            if map[nexti][nextj] == "]":
                if [nexti,nextj] not in liste_boite:
                     liste_boite.append([nexti,nextj])      
                     liste_boite.append([nexti,nextj-1])
                     flag2= 1
        if flag2 == 0:
            break

    my_print(liste_boite)
    if y != pos_debut[0]:
        k = 0
        liste_boite = sorted(liste_boite, key=lambda elem : elem[0])
        if deplacement[0] == -1:
            j = -1
        else:
            liste_boite.reverse()
            j = 1
    else:
        j=0
        liste_boite = sorted(liste_boite, key=lambda elem : elem[1])
        if deplacement[1] == -1:
            k = -1
        else:
            liste_boite.reverse()
            k = 1
    for elem in liste_boite:
        map[elem[0] + j ][elem[1] + k ] = map[elem[0]][elem[1]]
        map[elem[0]][elem[1]] = "."
    map[y][x] = "@"
    map[pos_debut[0]][pos_debut[1]] = "."
    return map, [pos_debut[0] + deplacement[0] , pos_debut[1] + deplacement[1]]
    

mat = x.split("\n")
map = []
flag = 0
i = 0
move = ""
pos_debut = [0,0]
for line in mat:
    if line == "":
        flag = 1
        continue
    if not flag:
        for carac in line:
            if i  >=  len(map) :
                map.append([])
            if carac == "@":
                map[i]+=["@","."]
                pos_debut = [i, map[i].index("@")]
            elif carac == ".":
                map[i]+=[".","."]
            elif carac == "#":
                map[i]+=["#","#"]
            elif carac == "O":
                map[i]+=["[","]"]
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
        if map[y][x] in "[":
            tot += y *100 + x
print(tot)
