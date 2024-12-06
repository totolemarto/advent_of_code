#!/bin/python3

from sys import argv


if len(argv) != 2 :
    print(f"usage : {argv[0]} <fichier>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()
mat = []
i = 0
for line in x.split("\n"):
    mat.append(list(line))
    if '^' in line:
        pos = [i, line.index('^')]
    i+=1

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
