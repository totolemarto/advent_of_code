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

dico = {}

def compute(rang, courant):
    if rang == 75 :
        return 1
    
    if courant+"A"+str(rang) in dico.keys():
        return dico[courant + "A" + str(rang)]
    
    if int(courant) == 0:    
        to_do = ["1"]    
    elif len(courant) % 2 == 0:
        j = len(courant) // 2
        a = (str(int(courant[:j])))
        try :
            b = int(courant[j:])
        except:
            b = 0
        to_do=[a,str(b)]
    else:
        to_do = [str(int(courant) * 2024)]
    
    x = 0
    for elem in to_do:
        x += compute(rang + 1, elem)
    dico[courant + "A" + str(rang)] = x

    return x




line = x.split()
my_print(line)
tot = 0
for salut in line:
    tot += compute(0, salut)
print(tot)
