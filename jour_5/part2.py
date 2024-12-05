#!/bin/python3

from sys import argv


if len(argv) != 2 :
    print(f"usage : {argv[0]} <fichier>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()

# 5524 > too low

def construit_ligne(good_order, line2, line, good_len, current,pos_line = 0, finish = 0):
    global i

    print(f" on m'appelle sur {i=} et {line2=} et {good_len=} et {pos_line=}")
    if i == good_len + 1: 
        return line2
    while good_order[current ] == []:
        if current in line2: 
            return line2
            input("je suis dans la fun")
        line2.append(current)
        i += 1
        if i == good_len + 1 or finish:
            return line2
        pos_line += 1
        current = line[pos_line]
    mini = 0
    to_do = []
    for elem in good_order[current]:
        to_do.append([elem, good_order[elem]])

    to_do = sorted(to_do, key=lambda lenght: len(lenght[1]))
    print(f"{to_do=}")
    new_to_do = []
    j = 0
    tmpi = i
    while  j < len(to_do) :
        new_to_do_tmp = []
        x = j + 1
        new_to_do_tmp.append(to_do[j])
        while x < len(to_do) and len(to_do[j][1]) == len(to_do[x][1]):
            new_to_do_tmp.append(to_do[x])
            x += 1
        new_to_do_tmp = sorted( new_to_do_tmp, key = lambda order : line.index(order[0]))
        print(new_to_do_tmp)
        new_to_do+= new_to_do_tmp # preserve original order
        j = x
    to_do = new_to_do
    print(f"{to_do=}")
    for elem in to_do:
        if elem in line2:continue
        line2=  construit_ligne(good_order, line2, line, good_len, elem[0],pos_line + 1, finish = 1)
        if i == good_len + 1: 
            return line2
    
    if current not in line2:
        line2.append(current)
        i += 1
    tmpi += 1
    #breakpoint()
    if i == good_len + 1 or finish: 
        return line2
    while line[pos_line] in line2:
        pos_line+=1
    return construit_ligne(good_order, line2, line, good_len, line[pos_line], pos_line)


union = {}
mat = []
flag = 1
sume = 0
for line in x.split("\n"):
    if flag and not "|" in line : 
        flag = 0
        continue
    if flag:
        x, y = line.split("|")
        if y not in union.keys():
            union[y]= [x]
        else:
            union[y].append(x)
    else:
        flag2=0
        line = line.split(",")
        if line[0] == '':
            break
        i = 0
        elem = line[0]
        good_order = {}
        while 1:
            #            print(i, elem)
            if elem in union.keys():
                intersect = [ x for x in union[elem] if x in line[i+1:]] 
                if intersect != [] :
                    flag2=1
                print(elem, intersect)
            else:
                intersect = []
            good_order[elem] = intersect
            if intersect != []:
                print( elem,intersect)
                flag2=1
                print("ça pete")
            i += 1
            if i == len(line):
                break
            elem = line[i]
        if not flag2:continue 
        i = 0
        elem = line[0]
        good_order = {}
        while 1:
            if elem in union.keys():
                intersect = [ x for x in union[elem] if x in line] 
            else:
                intersect = []
            good_order[elem] = intersect
            i += 1
            if i == len(line):
                break
            elem = line[i]
        print(good_order)
        good_len = len(line)//2 if len(line) % 2 == 1 else len(line) // 2 - 1
        line2 = []
        i = 0
        print("valeuur de line :",line)
        line2 = construit_ligne(good_order, line2, line, good_len, line[0])    
        i = 0
        elem = line2[0]
        good_order = {}
        while 1:
            #            print(i, elem)
            if elem in union.keys():
                intersect = [ x for x in union[elem] if x in line2[i + 1:]] 
            else:
                intersect = []
            good_order[elem] = intersect
            if intersect != []:
                print( elem,intersect)
                flag2=1
                print(line)
                print(line2)
                input("pourquoi ça a valide") 
            i += 1
            if i == len(line2):
                break
            elem = line2[i]
        print(line2, good_len)
        print("je rajoute donc", line2[good_len])
        sume += int(line2[good_len])
print(sume)
