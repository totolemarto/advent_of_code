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
for i in range(1, height - 1):
    for j in range(1, weight - 1):
        count = 0
        if (mat[i][j] != "A"):
            continue

        top_left = mat[i - 1][j - 1]
        top_right = mat[i - 1][j + 1]
        bottom_right = mat[i + 1][j + 1]
        bottom_left = mat[i + 1][j - 1]
        
        if top_left == "M" and bottom_right == "S":
            count = 1
        if bottom_right == "M" and top_left == "S":
            count += 1
        if bottom_left == "M" and top_right == "S":
            count += 1
        if top_right == "M" and bottom_left == "S":
            count += 1
        if count > 1:
            number += 1


print(number)        
