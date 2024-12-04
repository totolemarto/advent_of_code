#!/bin/python3

from sys import argv
if len(argv) != 2 :
    print(f"usage : {argv[0]} <fichier>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()
mat = []
for line in x.split("\n"):
    mat.append( list(line) )
number = 0
height = len(mat) - 1
weight = len(mat[0])
for i in range(height):
    for j in range(weight):
        if i >= 3 :
            if mat[i][j] == "X" and mat[i - 1][j] == "M" and mat[i - 2][j] == "A" and mat[i - 3][j] == "S": number+=1
        if j >= 3 :
            if mat[i][j] == "X" and mat[i][j - 1] == "M" and mat[i][j - 2] == "A" and mat[i][j - 3] == "S": number+=1
        if i + 3 < height:
            if mat[i][j] == "X" and mat[i + 1][j] == "M" and mat[i + 2][j] == "A" and mat[i + 3][j] == "S": number+=1
        if j + 3 < weight:
            if mat[i][j] == "X" and mat[i][j + 1] == "M" and mat[i][j + 2] == "A" and mat[i][j + 3] == "S": number+=1
        if i >= 3 and j >= 3 :
            if mat[i][j] == "X" and mat[i - 1][j - 1] == "M" and mat[i - 2][j - 2] == "A" and mat[i - 3][j - 3] == "S": number+=1
        if i + 3 < height and j + 3 < weight :
            if mat[i][j] == "X" and mat[i + 1][j + 1] == "M" and mat[i + 2][j + 2] == "A" and mat[i + 3][j + 3] == "S": number+=1
        if i >= 3 and j + 3 < weight:
            if mat[i][j] == "X" and mat[i - 1][j + 1] == "M" and mat[i - 2][j + 2] == "A" and mat[i - 3][j + 3] == "S": number+=1
        if i + 3 < height and j >= 3 :
            if mat[i][j] == "X" and mat[i + 1][j - 1] == "M" and mat[i + 2][j - 2] == "A" and mat[i + 3][j - 3] == "S": number+=1


print(number)        
