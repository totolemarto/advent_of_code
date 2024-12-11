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

def compute(rang, parent , courant):
    if rang == 75 :
        return 1
    parent.append(courant)
    
    if courant+"A"+str(rang) in dico.keys():
        return dico[courant + "A" + str(rang)]

    if int(courant) == 0:    
        x = compute(rang + 1, parent, "1")
        dico[courant + "A" + str(rang)] = x

    elif len(courant) % 2 == 0:
        j = len(courant) // 2
        a = (str(int(courant[:j])))
        x = compute(rang + 1, parent, a)
        
        try :
            b = int(courant[j:])
        except:
            b = 0
        
        x += compute(rang + 1, parent, str(b))
        dico[courant + "A" + str(rang)] = x

    else:
        x = compute(rang + 1, parent, (str(int(courant) * 2024))) 
        dico[courant + "A" + str(rang)] = x
    return x




line = x.split()
my_print(line)
tot = 0
for salut in line:
    tot += compute(0, [], salut)
print(tot)
