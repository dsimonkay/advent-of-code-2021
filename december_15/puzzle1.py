#!/usr/bin/env python3

from os import remove
import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
NR_OF_ROWS = None
NR_OF_COLS = None

costs = []
total_costs = []

def g(cell):
    """
    Calculate the total cost value for a given cell
    """
    global total_costs
    (i, j) = cell

    return total_costs[i][j]


def h(cell):
    """
    Calculate the heuristic value for a given cell
    """
    global NR_OF_ROWS, NR_OF_COLS
    (i, j) = cell

    return (NR_OF_ROWS - 1 - i) + (NR_OF_COLS - 1 - j)


def add_to_frontier(frontier, from_cell, to_cell):
    """
    Add a candidate to the frontier
    """
    global total_costs, costs
    assert from_cell in frontier

    (from_i, from_j) = from_cell
    (to_i, to_j) = to_cell

    frontier.append(to_cell)
    total_costs[to_i][to_j] = total_costs[from_i][from_j] + costs[to_i][to_j]


def remove_from_frontier(frontier, cell, discovered_cells):
    """
    Removes a cell from the frontier and adds it to the discovered cells
    """
    frontier.remove(cell)
    discovered_cells.append(cell)


# Read the input
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        costs_row = [int(x) for _, x in enumerate(line)]
        costs.append(costs_row)
        total_costs.append([0 for x in costs_row])

total_costs = [[0 for x in row] for row in costs]

NR_OF_ROWS = len(costs)
NR_OF_COLS = len(costs[0])
START = (0, 0)
GOAL = (NR_OF_ROWS - 1, NR_OF_COLS - 1)

# Easy hack: getting to the top right corner does not cost anything
costs[0][0] = 0

# The first two cells we add to the frontier are hardcoded
discovered_cells = []
frontier = [START]
add_to_frontier(frontier, START, (0, 1))
add_to_frontier(frontier, START, (1, 0))
remove_from_frontier(frontier, START, discovered_cells)

while not GOAL in frontier:
    min_cost_estimate = 999999
    picked_cell = None
    for cell in frontier:
        cost_estimate = g(cell) + h(cell)
        if cost_estimate < min_cost_estimate:
            picked_cell = cell
            min_cost_estimate = cost_estimate

    assert picked_cell
    (row, col) = picked_cell

    # Investigate possible candidates to visit from the picked cell
    for candidate in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
        (i, j) = candidate
        if i < 0 or i == NR_OF_ROWS or j < 0 or j == NR_OF_COLS or candidate in discovered_cells or candidate in frontier:
            continue

        # We can finally add the cell to the frontier
        add_to_frontier(frontier, picked_cell, candidate)

    remove_from_frontier(frontier, picked_cell, discovered_cells)

print(f"\nTotal lowest risk level on the shortest path: {total_costs[NR_OF_ROWS - 1][NR_OF_COLS - 1]}")
