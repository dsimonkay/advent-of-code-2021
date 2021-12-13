#!/usr/bin/env python3

import sys


def is_allowed(path, node):
    result = node not in path
    if path.count(node) == 1:
        # Make sure that no other small cave appears twice in the list
        other_small_cave_visited_twice = [True for x in path if x.islower() and path.count(x) == 2]
        result = not other_small_cave_visited_twice

    return result


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input_test.txt"
START = 'start'
END = 'end'

# Read the input and prepare the variable holding the data
graph = {
    START: []
}
print("Using input file:", INPUT_FILE)
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        (from_node, to_node) = line.split("-")
        print(line)
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

print(graph)
# graph = {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'b': ['A', 'd', 'end'], 'c': ['A'], 'd': ['b']}

# Process the data
found_path_count = 0
stack = [([], START, None)]
while stack:
    (path, node, twice_visitable_node_decided) = stack.pop()

    # Check for victory
    if node == END:
        # print(found_path_count, path + [node])
        found_path_count += 1
        continue

    # Otherwise put every considerable subsequent node in the graph to the stack
    growing_path = path + [node]
    for next_node in graph[node]:

        if next_node == END:
            # We are always happy to put the END node to the stack
            stack.append((growing_path, next_node, twice_visitable_node_decided))

        elif next_node.isupper():
            # Basic case: this node can be visited any times
            stack.append((growing_path, next_node, twice_visitable_node_decided))

        elif next_node.islower() and is_allowed(path, next_node):
            stack.append((growing_path, next_node, next_node))

        # elif next_node.islower():
        #     # Dealing with small caves

        #     if not twice_visitable_node_decided:
        #         if next_node not in path:
        #             # Branching out: we can continue with the undefined node for double visibility
        #             # in case we haven't seen this node yet
        #             stack.append((growing_path, next_node, None))

        #         # ...or allocate the double visibility option for this node
        #         else:
        #             stack.append((growing_path, next_node, next_node))

        #     elif (next_node not in path) or \
        #          (next_node == twice_visitable_node_decided and path.count(next_node) == 1):
        #         # Either all is fine, as this is a small cave we're encountering for the first time OR
        #         # we have already encountered this one, but we are allowed to visit it for a second time
        #         stack.append((growing_path, next_node, twice_visitable_node_decided))


print(f"\nNumber of distinct paths found: {found_path_count}")
