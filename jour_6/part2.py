#!/bin/python3

from sys import argv

def my_print(*args, **kwargs):
    global silent
    if silent: print(*args, **kwargs)
if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()
silent = int(argv[2]) 
mat = []
i = 0
for line in x.split("\n"):
    mat.append(list(line))
    if '^' in line:
        pos = [i, line.index('^')]
        pos2 = [i, line.index('^')]
    i+=1
mat2 = mat
height = len(mat) - 1
width = len(mat[0])
move = [[-1,0],[0,1],[1,0],[0,-1]]
mat[pos[0]][pos[1]] = "X"
cur = 0
while 1:
    new = [pos[0] +move[cur][0], pos[1] + move[cur][1]]
    if new[0] < 0 or new[0] >= height or new[1] < 0 or new[1] >= width:
        break
    if mat[new[0]][new[1]] != "#":
        mat[new[0]][new[1]] = 'X'
        pos = new
    else:
        cur = (cur + 1) % 4
print(sum(x.count('X') for x in mat))
to_do = []
for i in range (height):
    for j in range(width):
        if mat[i][j] == 'X':
            to_do.append([i,j])
tot = 0
for elem in to_do:
    cur = 0
    mat[elem[0]][elem[1]] = "#"    
    already_see = []
    pos = pos2
    while 1:
        new = [pos[0] +move[cur][0], pos[1] + move[cur][1]]
        my_print(already_see, new + move[cur], new + move[cur] in already_see)
        if new + move[cur] in already_see:
            tot +=1
            break
        if new[0] < 0 or new[0] >= height or new[1] < 0 or new[1] >= width:
            break
        if mat[new[0]][new[1]] != "#":
            mat[new[0]][new[1]] = 'X'
            pos = new
            already_see.append(pos+ move[cur])
        else:
            cur = (cur + 1) % 4
    mat[elem[0]][elem[1]] = "."    
print(tot)
# 2537 -> toohigh
