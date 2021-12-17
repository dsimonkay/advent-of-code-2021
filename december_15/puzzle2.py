#!/usr/bin/env python3

import sys
import time


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
START_TIME = time.time()
NR_OF_ROWS = None
NR_OF_COLS = None

costs = []
total_costs = []

def multiply_input(input, times):
    """
    Place the input as a tile 'times' times next to and below itself as described in the task briefing.
    """
    # Multiply the input table horizontally
    for row in input:
        row_copy = row.copy()
        for i in range(1, times):
            row += [(x + i) if x + i < 10 else (x + i + 1) % 10 for x in row_copy]

    # Multiply the multiplied rows vertically.
    # Works only for multipliers up to 10!!
    input_copy = input.copy()
    for i in range(1, times):
        for row in input:
            input_copy.append([(x + i) if x + i < 10 else (x + i + 1) % 10 for x in row])

    return input_copy


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

# Blow up the input
costs = multiply_input(costs, 5)

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

step = 0
total_cells = NR_OF_ROWS * NR_OF_COLS

while not GOAL in frontier:
    step += 1
    elapsed = time.time() - START_TIME
    print(f"[Step #{step}] Elapsed time: {elapsed:.2f} seconds   Map discovered: {(len(discovered_cells) + len(frontier)) * 100 / total_cells} %    ", end="\r")

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

    # Remove the processed cell from the frontier and add it to the discovered ones
    remove_from_frontier(frontier, picked_cell, discovered_cells)


print(f"\nTotal lowest risk level on the shortest path: {total_costs[NR_OF_ROWS - 1][NR_OF_COLS - 1]}")
