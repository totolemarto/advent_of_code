#!/bin/python3

from sys import argv
import sympy as sp

mul_a,mul_b = sp.symbols('x y', positive = True, integer = True)

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

def get_y(line, sep="+"):
    line = line.split(sep)
    return int(line[2])

def get_x(line, sep = "+"):
    line = line.split(sep)
    return int(line[1].split(",")[0])
tot = 0
for line in mat:
    if line == "":continue
    if "Prize" in line:
        goal_x = get_x(line, "=")
        goal_y = get_y(line, "=")
        goal_x += 10000000000000
        goal_y += 10000000000000
        eq1 = sp.Eq(mul_a * xA + mul_b * xB, goal_x)
        eq2 = sp.Eq(mul_a * yA + mul_b * yB , goal_y)

        solutions = sp.solve((eq1, eq2), (mul_a, mul_b))
        my_print(solutions)
        try:
            tot += (solutions[mul_a] * 3)
            tot += solutions[mul_b]
        except:
            continue
    
    if "A" in line:
        xA = get_x(line)
        yA = get_y(line)
    if "B:" in line:
        xB = get_x(line)
        yB = get_y(line)
print(tot)
