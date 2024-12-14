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
    already_see.append(cur_pos)
    dep = []
    z = 0
    for i,elem in enumerate(movement):
        tmp = [ cur_pos[0] + elem[0], cur_pos[1] + elem[1] ] 
        retour = is_same(mat, cur_pos, tmp, already_see)
        if retour == 1:
            already_see = (decoupe_zone(mat, tmp, already_see ))
            dep.append(tmp)
    return already_see



def calcul_perimetre(zone):
    result = []

    for elem in zone:
        if [elem[0] - 1, elem[1]] not in zone:
            result.append(  [elem[0] - 1, elem[1], 0])      
        if [elem[0] + 1, elem[1]] not in zone:
            result.append(  [elem[0] + 1, elem[1], 1])      
        if [elem[0] , elem[1] - 1] not in zone:
            result.append(  [elem[0] , elem[1] - 1 , 2])      
        if [elem[0] , elem[1] + 1] not in zone:
            result.append(  [elem[0] , elem[1] + 1, 3 ])      
    my_print(result)
    peri = result
    result = []
    i = 0
    already_done = []
    for elem in peri:
        y,x,orient = elem    
        flag = 0
        for elem_2 in peri:
            if elem_2[2] != orient:
                continue
            if orient < 2:
                if elem_2[0] == y and (elem_2[1]  == x + 1 or elem_2[1]  == x - 1 ) : 
                    if elem_2 in already_done or elem in already_done:
                        already_done.append(elem_2)
                        flag = 2
                    else:
                        if flag != 2:
                            already_done.append(elem_2)
                            flag = 1
            else:
                if elem_2[1] == x and (elem_2[0]  == y + 1 or elem_2[0]  == y - 1 ) : 
                    if elem_2 in already_done or elem in already_done:
                        already_done.append(elem_2)
                        flag = 2
                    else:
                        if flag != 2:
                            already_done.append(elem_2)
                            flag = 1
        if flag != 2:
            result.append(elem)
    my_print("à la fin")
    my_print(len(result), result)
    result = len(result)
    return result
    

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
    zonebis = sorted(zone, key=lambda e: (e[0],e[1]))
    my_print(zonebis)

    my_print(zone, "hye")
    perimetre = calcul_perimetre(zonebis)
    my_print("aire = ", len(zone))
    my_print("perimetre = ", perimetre)
    tot += (perimetre * (len(zone)))

print(tot)
