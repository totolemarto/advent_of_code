#!/bin/python3
from sys import argv
import heapq

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


def manhattan_heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def get_f_score(g, h):
    return g + h

def is_legal_move(map,lines, columns, to_do):
    y,x = to_do
    if x < 0 or y < 0 or y >= lines or x >= columns:
        return 0
    return map[y][x] == "."

def a_star(map, start, end, lines, columns):
    deplacements = [ [0,1] ,[-1,0], [0,-1], [1,0]]
    open_list = []
    heapq.heappush(open_list, (0, start))  
    came_from = {}  
    g_scores = {str(start): 0}  
    f_scores = {str(start): manhattan_heuristic(start, end)}  
    while open_list:
        _, current = heapq.heappop(open_list)
        if list(current) == end:
            path = []
            while str(current) in came_from:
                path.append(list(current))
                current = came_from[str(current)]
            path.append(start)
            my_print(path)
            return path 
        for move in deplacements:
            to_do = (current[0] + move[0], current[1] + move[1])
            if is_legal_move(map, lines, columns, to_do):
                score_g = g_scores[str(current)] + 1
                if str(to_do) not in g_scores or score_g < g_scores[str(to_do)]:
                    came_from[str(to_do)] = current
                    g_scores[str(to_do)] = score_g
                    h_score = manhattan_heuristic(to_do, end)
                    f_score = get_f_score(score_g, h_score)
                    f_scores[str(to_do)] = f_score
                    heapq.heappush(open_list, (f_score, to_do))
    return [0]

lines = 71
columns = 71
map = []
for _ in range(lines):
    liste = ["." for _ in range(columns)]
    map.append(liste)

exit_point = [70,70]
begin_point = [0,0]
i = 0

for line in mat:
    i+= 1
    if i <= 1024 :
        continue
    x,y = line.split(",")
    map[int(y)][int(x)] = "#"
    l = list(a_star(map, begin_point, exit_point, lines,columns))
    if l == [0]:
        print(x,y)
        exit(2)

