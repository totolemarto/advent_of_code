#!/bin/python3
with open("star1","r") as f:
    x = f.read()

def reboot():
    global cur, elem,a,b
    a = b = None
    cur = 0
    if elem == "m":
        cur = 1

cur = 0
a = b = None
tot = 0
for elem in x:
    if cur == 0:
        if elem == "m":
            cur = 1
            continue
    if cur == 1:
        if elem == "u":
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
print(tot)
