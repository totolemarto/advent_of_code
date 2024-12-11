from collections import defaultdict, deque

def parse_input(page_ordering_rules, updates):
    # Create the graph from the page ordering rules
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

def is_ordered(update, graph, in_degree):
    # Check if an update is in the correct order
    page_index = {page: idx for idx, page in enumerate(update)}
    
    for x in graph:
        for y in graph[x]:
            # If the rule x|y is violated, return False
            if page_index.get(x, -1) > page_index.get(y, -1):
                return False
    return True

def topological_sort(update, graph, in_degree):
    # Perform a topological sort using Kahn's algorithm
    # Start with nodes that have no incoming edges (in_degree 0)
    queue = deque([page for page in update if in_degree[page] == 0])
    sorted_pages = []
    
    while queue:
        node = queue.popleft()
        sorted_pages.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If all pages are not sorted, return None (indicating a cycle, which shouldn't happen here)
    if len(sorted_pages) == len(update):
        return sorted_pages
    return None

def solve_part_two(page_ordering_rules, updates):
    # Parse the input
    graph, in_degree, all_pages, updates = parse_input(page_ordering_rules, updates)
    
    # List to store the middle page numbers from correctly ordered updates
    middle_pages = []
    
    for update in updates:
        if not is_ordered(update, graph, in_degree):
            # If the update is not ordered, topologically sort it
            sorted_update = topological_sort(update, graph, in_degree)
            if sorted_update:
                # Find the middle page number of the sorted update
                middle_pages.append(sorted_update[len(sorted_update) // 2])
    
    # Return the sum of the middle page numbers from correctly ordered updates
    return sum(middle_pages)

# Example usage
page_ordering_rules = [
    "47|53", "97|13", "97|61", "97|47", "75|29", "61|13", "75|53", 
    "29|13", "97|29", "53|29", "61|53", "97|53", "61|29", "47|13", 
    "75|47", "97|75", "47|61", "75|61", "47|29", "75|13", "53|13"
]

updates = [
    [75, 47, 61, 53, 29],
    [97, 61, 53, 29, 13],
    [75, 29, 13],
    [75, 97, 47, 61, 53],
    [61, 13, 29],
    [97, 13, 75, 29, 47]
]

# Solve part two
print(solve_part_two(page_ordering_rules, updates))  # Output should be 123 (for part two)

