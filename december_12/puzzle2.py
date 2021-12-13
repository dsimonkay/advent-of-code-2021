#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input_test_2.txt"
START = "start"
END = "end"


def is_eligible(path, node):
    """
    Checks whether a specific node can be appended to the path considering whether it's not yet on it
    or it is already there exactly once and no other lowercase node appears twice on the path.
    """
    result = node not in path
    if path.count(node) == 1:
        result = True
        for x in path:
            if x.islower() and path.count(x) == 2:
                result = False
                break

    return result


# Read the input and prepare the variable holding the data
graph = {START: []}

print("Using input file:", INPUT_FILE)
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        (from_node, to_node) = line.split("-")
        if from_node not in graph and from_node != END:
            graph[from_node] = []

        if to_node not in graph and to_node != END:
            graph[to_node] = []

        # Assuming no "start-end" or "end-start" input

        if to_node == START:
            graph[START].append(from_node)
        elif from_node == END:
            graph[to_node].append(END)
        else:
            graph[from_node].append(to_node)
            if from_node != START and to_node != END:
                graph[to_node].append(from_node)

# Process the data
found_path_count = 0
stack = [([], START)]
while stack:
    (path, node) = stack.pop()
    growing_path = path + [node]

    # Check for victory
    if node == END:
        # print(found_path_count, growing_path)
        found_path_count += 1
        continue

    # Otherwise put every considerable subsequent node in the graph to the stack
    for next_node in graph[node]:

        # This node can be visited any number of times (=large cave, basic case) OR
        # dealing with an eligible small cave
        if next_node.isupper() or is_eligible(growing_path, next_node):
            stack.append((growing_path, next_node))


print(graph)
print(f"\nNumber of distinct paths found: {found_path_count}")
