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
movement = [[-1,0],[1,0],[0,-1],[0,1]]
lines = len(mat)
columns = len(mat[0])
total_zone = []

def is_same(mat, cur_pos, next_pos, already_see):
    if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= lines or next_pos[1] >= columns :
        return 0
    if next_pos in already_see:
        return -1
    return mat[next_pos[0]][next_pos[1]] == mat[cur_pos[0]][cur_pos[1]]

def decoupe_zone( mat, cur_pos, already_see):
    if cur_pos in already_see:
        return already_see
    if already_see == []:
        already_see.append(0)
    already_see.append(cur_pos)
    for elem in movement:
        tmp = [ cur_pos[0] + elem[0], cur_pos[1] + elem[1] ] 
        retour = is_same(mat, cur_pos, tmp, already_see)
        if retour == 1:
            already_see = (decoupe_zone(mat, tmp, already_see ))
        elif retour == 0:
            already_see[0]+=1
    return already_see

for i in range(lines):
    for j in range(columns):
        flag = 0
        for elem in total_zone:
            if [i,j] in elem:
                flag = 1 
                break
        if not flag:
            total_zone.append(decoupe_zone(mat,[i,j], []))
tot = 0
for zone in total_zone:
    my_print(zone, "hye")
    my_print("aire = ", len(zone) - 1)
    my_print("perimetre = ", zone[0])
    tot += (zone[0] * (len(zone) - 1))

print(tot)
