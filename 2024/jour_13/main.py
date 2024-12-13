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
        for i in range(101):
            if (goal_x - (xA * i )) % xB == 0 and (goal_y - (yA * i )) % yB == 0:
                if   ((goal_x - (xA * i ) ) // xB) == ((goal_y - (yA * i ) ) // yB)  :
                    iok = ((goal_y - (yA * i ) ) // yB)
                    if iok <= 100:                   
                        print(f" sur {line=} {i*xA + iok * xB=} {i*yA + iok * yB=} ")
                        tot += (3*i) + ((goal_x - (xA * i ) ) // xB)          
                        print(tot)
                        break
    
    if "A" in line:
        xA = get_x(line)
        yA = get_y(line)
    if "B:" in line:
        xB = get_x(line)
        yB = get_y(line)
print(tot)
