#!/bin/python3

from sys import argv


if len(argv) != 2 :
    print(f"usage : {argv[0]} <fichier>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read()

def construit_ligne(good_order, line2, line, good_len, current,pos_line = 0, finish = 0):
    global i
    if i == good_len + 1: 
        return line2
    while good_order[current] == []:
        if current in line2: 
            return line2
        line2.append(current)
        i += 1
        if i == good_len + 1 or finish:
            return line2
        pos_line += 1
        current = line[pos_line]
    to_do = []
    for elem in good_order[current]:
        to_do.append([elem, good_order[elem]])
    to_do = sorted(to_do, key=lambda lenght: len(lenght[1]))
    new_to_do = []
    j = 0
    while  j < len(to_do) :
        new_to_do_tmp = []
        x = j + 1
        new_to_do_tmp.append(to_do[j])
        while x < len(to_do) and len(to_do[j][1]) == len(to_do[x][1]):
            new_to_do_tmp.append(to_do[x])
            x += 1
        new_to_do += sorted( new_to_do_tmp, key = lambda order : line.index(order[0])) # preserve original order of element in line
        j = x
    to_do = new_to_do
    for elem in to_do:
        if elem in line2:continue
        line2=  construit_ligne(good_order, line2, line, good_len, elem[0],pos_line + 1, finish = 1)
        if i == good_len + 1: 
            return line2
    
    if current not in line2:
        line2.append(current)
        i += 1
    if i == good_len + 1 or finish: 
        return line2
    while line[pos_line] in line2:
        pos_line+=1
    return construit_ligne(good_order, line2, line, good_len, line[pos_line], pos_line)


def is_good(union, line,test):
    flag2=0
    i = 0
    elem = line[0]
    good_order = {}
    while 1:
        intersect = []
        if elem in union.keys():
            if not test:
                intersect = [ x for x in union[elem] if x in line[i+1:]] 
                if intersect != [] : 
                    flag2=1
            else:
                intersect = [ x for x in union[elem] if x in line] 
        good_order[elem] = intersect
        i += 1
        if i == len(line):
            break
        elem = line[i]
    return flag2, good_order

union = {}
mat = []
flag = 1
sume = 0
for line in x.split("\n"):
    if flag and not "|" in line : # get the empty line between rules and pages 
        flag = 0
        continue
    if flag:
        x, y = line.split("|")
        if y not in union.keys():
            union[y]= [x]
        else:
            union[y].append(x)
    else:
        line = line.split(",")
        flag2, _ = is_good(union, line, 0)
        if not flag2:continue 
        _, good_order = is_good( union, line, 1)
        good_len = len(line)//2 
        i = 0
        line2 = construit_ligne(good_order, [] , line, good_len, line[0])    
        sume += int(line2[good_len])
print(sume)
