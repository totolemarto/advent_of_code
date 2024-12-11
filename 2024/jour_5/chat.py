#!/bin/python3

from sys import argv
from collections import defaultdict, deque

# Function to parse the input
def parse_input(page_ordering_rules, updates):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_pages = set()

    for rule in page_ordering_rules:
        x, y = map(int, rule.split('|'))
        graph[x].append(y)
        in_degree[y] += 1
        if x not in in_degree:
            in_degree[x] = 0
        all_pages.update([x, y])

    return graph, in_degree, all_pages, updates

# Function to check if the update is ordered
def is_ordered(update, graph, in_degree):
    page_index = {page: idx for idx, page in enumerate(update)}
    
    for x in graph:
        for y in graph[x]:
            if page_index.get(x, -1) > page_index.get(y, -1):
                return False
    return True

# Function to perform topological sort
def topological_sort(update, graph, in_degree):
    queue = deque([page for page in update if in_degree[page] == 0])
    sorted_pages = []

    while queue:
        node = queue.popleft()
        sorted_pages.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(sorted_pages) == len(update):
        return sorted_pages
    return None

# Main function to solve part two of the puzzle
def solve_part_two(page_ordering_rules, updates):
    graph, in_degree, all_pages, updates = parse_input(page_ordering_rules, updates)
    
    middle_pages = []
    
    for update in updates:
        if not is_ordered(update, graph, in_degree):
            sorted_update = topological_sort(update, graph, in_degree)
            if sorted_update:
                middle_pages.append(sorted_update[len(sorted_update) // 2])
    
    return sum(middle_pages)

# Initialization based on file input
if len(argv) != 2:
    print(f"usage : {argv[0]} <fichier>")
    exit(1)

with open(argv[1], "r") as f:
    x = f.read().splitlines()

# Splitting the input into page ordering rules and updates
separator_index = x.index('')
page_ordering_rules = x[:separator_index]
updates = [list(map(int, line.split(','))) for line in x[separator_index + 1:]]

# Solve part two
print(solve_part_two(page_ordering_rules, updates))  # Output should be the correct sum for part two

