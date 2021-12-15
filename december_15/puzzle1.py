#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
NR_OF_ROWS = None
NR_OF_COLS = None

costs = []
total_costs = []

def g(cell):
    global total_costs
    (i, j) = cell
    return total_costs[i][j]

def h(cell):
    global NR_OF_ROWS, NR_OF_COLS
    (i, j) = cell
    return (NR_OF_ROWS - 1 - i) + (NR_OF_COLS - 1 - j)

# # Read the input
# with open(INPUT_FILE, "r") as infile:
#     while line := infile.readline().rstrip():
#         costs_row = [int(x) for _, x in enumerate(line)]
#         costs.append(costs_row)
#         total_costs.append([0 for x in costs_row])

costs = [
    [0, 1, 6, 3, 7, 5, 1, 7, 4, 2],
    [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
    [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
    [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
    [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
    [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
    [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
    [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
    [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
    [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]]

total_costs = [[0 for x in row] for row in costs]

NR_OF_ROWS = len(costs)
NR_OF_COLS = len(costs[0])
TARGET = (NR_OF_ROWS - 1, NR_OF_COLS - 1)

# Easy hack: getting to the top right corner does not cost anything
costs[0][0] = 0
total_costs[0][1] = costs[0][1]
total_costs[1][0] = costs[1][0]


total_path_cost = None
discovered_cells = [(0, 0)]
frontier = [(0, 1), (1, 0)]
log = []

for step in range(300):

    print(f"\n--------------------------\nstep #{step}\nfrontier: {frontier}")
    min_cost = 999999
    picked_cell = None
    for cell in frontier:
        print(f"  cell({cell[0]}, {cell[1]}) -- g: {g(cell)}   h: {h(cell)}   g+h: {g(cell) + h(cell)}")
        if g(cell) + h(cell) < min_cost:
            picked_cell = cell
            min_cost = g(cell) + h(cell)

    (row, col) = picked_cell
    log.append((picked_cell, costs[row][col]))
    cell_cost = total_costs[row][col]

    print("elem to pick from frontier:", picked_cell, "  cell cost:", cell_cost)
    if picked_cell == TARGET:
        print("Victory!")
        total_path_cost = cell_cost
        break

    # Investigate possible candidates
    for (i, j) in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
        print(f"    checking candidate ({i}, {j})...", end="")
        # or (i, j) in frontier
        if i < 0 or i == NR_OF_ROWS or j < 0 or j == NR_OF_COLS or (i, j) in discovered_cells:
            print(" - not passed")
            continue

        print("OK")
        # Total cost of reaching the candidate
        total_cost = cell_cost + costs[i][j]
        frontier.append((i, j))
        total_costs[i][j] = total_cost

    frontier.remove(picked_cell)
    discovered_cells.append(picked_cell)


print()
vis = [["." for x in row] for row in costs]
for i, ((row, col), cost) in enumerate(log):
    # print(f"#{i+1}: {log_entry}")
    vis[row][col] = str(cost)

for i, row in enumerate(vis):
    for j, value in enumerate(row):
        print(value, end="")
    print()        

print(costs)

print(f"\nTotal lowest risk level on the shortest path: {total_cost}")
