#!/bin/python3
with open("star1","r") as f:
    x = f.read()

def reboot():
    global cur, elem,a,b
    a = b = None
    cur = 0
    if elem == "m":
        cur = 1
    if elem == 'd':
        cur = 6 
cur = 0
a = b = None
tot = 0
flag = 0
for elem in x:
    print(elem, end = "")
    if cur == 0: 
        if elem == "m" and not flag:
            cur = 1
            continue
        if elem == "d":
            cur = 6
            continue
    if cur == 1 :
        if elem == "u" and not flag:
            cur = 2
            continue
        reboot()
        continue
    if cur == 2:
        if elem == "l":
            cur = 3
            continue
        reboot()
        continue
    if cur == 3:
        if elem == "(":
            cur = 4
            continue
        reboot()
        continue
    if cur == 4:
        try :
            elem = int(elem)
            if a == None:
                a = 0
            a = a*10 + elem
            cur = 4
            continue
        except:
            if elem == ',' and a != None:
                cur = 5
                continue
            reboot()
            continue
    if cur == 5:
        try :
            elem = int(elem)
            if b == None:
                b = 0
            b = b*10 + elem
            cur = 5
            continue
        except:
            if elem == ')' and a != None and b != None:
                cur = 0
                tot += (a*b)
                a = b = None
                continue
            reboot()
            continue
    if cur == 6:
        if elem == "o":
            cur = 7
            continue
        reboot()
        continue
    if cur == 7:
        print("dans 7 :", elem)
        if elem == "(":
            cur = 8
            continue
        if elem == "n":
            cur = 9
            continue
        reboot()
        continue
    if cur == 8:
        if elem == ")":
            cur = 0
            flag = 0
            continue
        reboot()
        continue
    if cur == 9:
        print("dans 9 :", elem)
        if elem == "'":
            cur = 10
            continue
        reboot()
        continue
    if cur == 10:
        if elem == "t":
            cur = 11
            continue
        reboot()
        continue
    if cur == 11:
        if elem == "(":
            cur = 12
            continue
        reboot()
        continue
    if cur == 12:
        if elem == ")":
            cur = 0
            flag = 1
            continue
        reboot()
        continue
    print(flag)
print(tot)
