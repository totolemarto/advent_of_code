#!/bin/python3
from sys import argv
import hashlib

def my_print(*args, **kwargs):
    global silent
    if silent: print(*args, **kwargs)
if len(argv) != 3  :
    print(f"usage : {argv[0]} <fichier> <debug>")
    exit(1)
with open(argv[1],"r") as f:
    x = f.read().strip()

def test(text):
    if len(text) < 5 : return 1
    for i in range(5):
        if text[i] != "0":
            return 1
    return 0


md5_hash = text= ""
for i in range(99999999999):
    text = x + str(i)
    text = hashlib.md5((text.encode())).hexdigest()
    if not test(text):
        break
print(i, text)
