#!/bin/python3

from sys import argv

def compute(goal, liste, index, lenght, current):
    my_print(f"{goal=}, {current=}")
    if current > goal:
        return False
    if index == lenght:
        return current ==  goal
    plus = compute(goal, liste, index +1, lenght, current + int(liste[index])) 
    if plus:
        return True
    fois = compute(goal, liste, index +1, lenght, current * int(liste[index]))
    if fois : 
        return fois
    concat = compute(goal, liste, index +1, lenght, int(str(current)+(liste[index])))
    return concat


def my_print(*args, **kwargs):
    global silent
    if silent: print(*args, **kwargs)
if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read().strip()
silent = int(argv[2]) 
tot = 0
for line in x.split("\n"):
    goal = int(line.split(":")[0])
    liste = str(line.split(":")[1])
    liste= liste.split()
    taille = len(liste)
    if compute(goal, liste, 0, taille, 0):
        tot += goal
print(tot, "ici")
