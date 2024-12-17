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
flag = 0
i = 0
move = ""
A=0
B=0
C=0
result = []
programme = ""
for line in mat:
    if "A" in line: 
        A = int(line.split(":")[1])
    if "B" in line: 
        B = int(line.split(":")[1])
    if "C" in line: 
        C = int(line.split(":")[1])
    if "P" in line: 
        programme = line.split(":")[1][1:]
programme = programme.split(",")
print(A,B,C,programme)

true_ope = 0
i = 0
while i != len(programme):
    ope = int(programme[i + 1])
    if ope == 4:
        true_ope = A
    elif ope == 5:
        true_ope = B
    elif ope == 6:
        true_ope = C
    else:
        true_ope = ope
    my_print(A,B,C)
    my_print(programme[i], ope, true_ope)
    match (programme[i]):
        case "0":
            A = int(A / (2** true_ope) ) 
        case "1":
            B = B ^  ope
        case "2":
            B = true_ope % 8
        case "3":
            if A != 0:
                i = ope - 2
        case "4":
            B = B ^ C
        case "5":
            result += str(true_ope%8)
        case "6":
            B = int(A / (2**true_ope)) 
        case "7":
            C = int(A / (2 ** true_ope)) 
    i+= 2
print(A,B,C, result)
print(",".join(result))
