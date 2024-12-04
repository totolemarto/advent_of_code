#!/bin/python3
from copy import deepcopy
def test( elem, deb, order):
    for i in range(deb + 1, len(elem)):
        num = int(elem[i])
        if order == "p": 
            if int(elem[i-1]) + 3 < num  or int(elem[i-1]) >= num :
                return 0
        elif order == "m":
            if int(elem[i-1]) - 3 > num or  int(elem[i-1]) <= num:
                return 0
        if i == len(elem) - 1:
            return 1

def myprint(elem):
    for i in elem:
        print(i, end= " ")
    print()

def vote_order(a,b):
    return 1 if a < b else -1 if a > b else 0

with open("star1","r") as f:
    i = f.read()
tot = 0
for elem in i.split("\n")[:-1]:
    elem = elem.split()
    casse  = 0
    for i,num in enumerate(elem):
        num=int(num)
        if i == len(elem) - 1:
            tot += 1
            myprint(elem)
            break
        if i == 0 :
            vote = vote_order(int(elem[i+1]), num)
            vote += vote_order(int(elem [i+2]), int(elem[i+1]))
            vote += vote_order(int(elem [i+3]), int(elem[i+2]))
            if vote > 0:
                order = "m"
            elif vote < 0:
                order = "p"
            else: 
                break
        else:
            if order == "p" and (int(elem[i-1]) + 3 < num  or int(elem[i-1]) >= num ):
                casse = 1
            elif order == "m" and ( int(elem[i-1]) - 3 > num or  int(elem[i-1]) <= num ):
                casse = 1
            if casse:
                tmp2 = deepcopy(elem)
                tmp2[i] = tmp2[i-1]
                if test(tmp2, i, order):
                    tot += 1
                    myprint(elem)
                    break
                else:
                    if i > 1:
                        if order == "p" and (int(elem[i-2]) >=  int(elem[i])  or int(elem[i]) >= int(elem[i-2]) + 3 )  or  order == "m" and (int(elem[i-2]) <= int(elem[i]) or int(elem[i]) <= int(elem[i-2]) - 3) :
                            break
                    if test(elem, i, order):
                        tot +=1
                        myprint(elem)
                        break
                    else:
                        break
print(tot)
