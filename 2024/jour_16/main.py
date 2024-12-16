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


def is_legal_move(map,lines, columns, to_do):
    y,x = to_do
    if x < 0 or y < 0 or y >= lines or x >= columns:
        return 0
    return map[y][x] in ".ES"

def is_inside(liste,elem):
    i = 0
    for i in range(len(liste)):
        if liste[i][0] == elem[0] and liste[i][1] == elem[1]:
            if liste[i][2] <= elem[2]:
                return 0
            return 1
    return 0

def not_is_inside_less(liste,elem):
    i = 0
    for i in range(len(liste)):
        if liste[i][0] == elem[0] and liste[i][1] == elem[1]:
            return liste[i][2] > elem[2]
    return 1
def construit_djikstra(map, sortie, cur_pos) -> list[list[int]]:
    deplacements = [ [0,1] ,[-1,0], [0,-1], [1,0]]
    i = 0
    is_done = []
    deja_vu = [cur_pos + [i] + [0] ]
    while cur_pos[0] != sortie[0] or cur_pos[1] != sortie[1]:
        cur_pos = deja_vu.pop(0)
        if is_inside(is_done, cur_pos):
            continue
        is_done.append([cur_pos[0], cur_pos[1], cur_pos[2]])
        for i,elem in enumerate(deplacements):
            y,x = [cur_pos[0] + elem[0], cur_pos[1] + elem[1] ]
            if is_legal_move(map, lines, columns,[y,x]):
                tmp = cur_pos[3]
                if tmp  == i :
                    if not_is_inside_less(is_done, [y,x,cur_pos[2] + 1]):
                        deja_vu.append( [y,x, cur_pos[2] + 1, i ] )
                elif (i + 1) % 4  == tmp or (i - 1) % 4 == tmp:
                    if not_is_inside_less(is_done, [y,x,cur_pos[2] + 1001]):
                        deja_vu.append( [y,x, cur_pos[2] + 1001, i ] )
                else:
                    if not_is_inside_less(is_done, [y,x,cur_pos[2] + 2001]):
                        deja_vu.append( [y,x, cur_pos[2] + 2001, i ] )
        deja_vu = sorted(deja_vu, key=lambda x : x[2])
    return cur_pos[2]


i = 0
pos_debut = [0,0]
sortie = [0,0]
for line in mat:
    map.append(list(line))
    if "S" in line:
        pos_debut = [i, line.index("S")]
    if "E" in line:
        sortie = [i, line.index("E")]
    i+= 1
for line in map:
    my_print("".join(line))
my_print(pos_debut)
my_print(sortie)
deplacements = [ [0,1] ,[-1,0], [0,-1], [1,0]]
lines = len(map)
columns = len(map[0])

x = construit_djikstra(map, sortie, pos_debut)
print(x)
