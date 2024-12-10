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


def is_good(x , y , val_actu, mat, not_available):
    if x < 0 or x >= l or y < 0 or y >= c: 
        return 0
    my_print( f"{mat[x][y]=} dans is_good")
    return mat[x][y] == str(val_actu + 1) 


def parcours( val_actu : int , pos_x, pos_y, move, mat, deja_vu):
    if val_actu == 9 :
        my_print(f"trouvé un 9 avec {pos_x=} et {pos_y=}")
        return 1, [pos_x,pos_y]
    tot = 0
    my_print(f"je rentre sur {val_actu=} sur {pos_x=} {pos_y=}")
    for elem in move:
        if is_good(pos_x + elem[0] , pos_y + elem[1] , val_actu, mat, deja_vu):
            tmp, tmp_2 = parcours(val_actu + 1 , pos_x + elem[0], pos_y + elem[1], move, mat, deja_vu)
            tot+=tmp
            deja_vu.append(tmp_2)
    return tot, deja_vu


tot = 0

pos_deb = []
letters = {}
my_print(x)
t = []
is_file = 1
curr = 0
l = len(mat) 
c = len(mat[0])
for i in range(l):
    for j in range(c):
        if mat[i][j] == "0":
            pos_deb.append([i,j])
my_print(pos_deb)
move = [ [-1,0],[1,0],[0,-1],[0,1] ]
tot = 0
for elem in pos_deb:
    tmp,_ = parcours( 0 , elem[0], elem[1], move, mat, [])
    tot += tmp
print(tot)
