#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
START = 'start'
END = 'end'

# Read the input and prepare the variable holding the data
graph = {}
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        (from_node, to_node) = line.split("-")
        if from_node not in graph:
            graph[from_node] = []

        if to_node not in graph and to_node != END:
            graph[to_node] = []

        graph[from_node].append(to_node)

        if from_node != START and to_node != END:
            graph[to_node].append(from_node)

# Process the data
path_count = 0
stack = [([], START)]
while stack:
    (path, node) = stack.pop()

    # Check for victory
    if node == END:
        path_count += 1
        # print(path + [END])
        continue

    # Otherwise put every subsequent node in the graph to the stack
    # ...except for those small caves we have already encountered so far along the way
    for next_node in graph[node]:
        if next_node.isupper() or next_node not in path:
            stack.append((path + [node], next_node)) 

print(f"\nNumber of paths found: {path_count}")
