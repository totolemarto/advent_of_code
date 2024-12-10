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


my_print(x)
j = []
is_file = 1
maxi = 0

for i in range(len(x)):
    if is_file:
            
        for _ in range(int(x[i])):
            j.append(str(maxi))
        maxi+= 1
        if i == 0:
            deb = int(x[i])
    else:
        for _ in range(int(x[i])):
            j.append("A")
    is_file = 1 - is_file

maxi = maxi - 1

my_print(maxi)
my_print(j)
my_print("len de j : ", len(j))

while maxi != 0 :
    pos = j.index(str(maxi))
    my_print(pos, j[pos], j )
    taille = 0
    for x in range(pos, len(j)):
        if j[x] == str(maxi):
            taille+= 1
        else:
            break
    taille2 = 0
    good_index = -1
    for x in range(pos):
        if j[x] == "A":
            taille2+= 1
        else:
            taille2 = 0
        if taille2 >= taille:
            good_index = x - taille2 + 1
            break
    my_print("sur maxi ", maxi ,"la taille c'est ", taille, "et taille2 c'est : ", taille2)
    if good_index == -1:
        maxi-=1
        continue
    for x in range(good_index, good_index + taille):
        j[x] = str(maxi)
    for x in range(pos, pos+taille):
        j[x] = "A"
    maxi -= 1


tot = 0


for i, elem in enumerate(j):
    if elem == "A":
        continue
    tot += int(elem) * i

print(tot)


