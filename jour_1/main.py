#!/bin/python3

with open("star1","r") as f:
    i = f.read()
l1 = []
l2 = []
for elem in i.split("\n")[:-1]:
    l1.append(int(elem.split()[0]))
    l2.append(int(elem.split()[1]))
x = 0
l1.sort()
l2.sort()
for i in range(len(l1)):
    x += abs(l2[i] - l1[i])
print(x)
tot = 0
for i in l1:
    tot += i*l2.count(i) 

print(tot)
