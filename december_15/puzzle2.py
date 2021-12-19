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


# Read the input
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        costs_row = [int(x) for _, x in enumerate(line)]
        costs.append(costs_row)

# Blow up the input
costs = multiply_input(costs, 5)

total_costs = [[0 for _ in row] for row in costs]

NR_OF_ROWS = len(costs)
NR_OF_COLS = len(costs[0])
START = (0, 0)
GOAL = (NR_OF_ROWS - 1, NR_OF_COLS - 1)

# Easy hack: getting to the top right corner does not cost anything
costs[0][0] = 0

explored_cells = []
frontier = [START]

C = 100 / (NR_OF_ROWS * NR_OF_COLS)

while frontier:
    elapsed = time.time() - START_TIME
    map_discovered_percent = (len(explored_cells) + len(frontier)) * C
    print(f"Elapsed time: {int(elapsed / 60)} minutes {(elapsed % 60):.2f} seconds   Map discovered: {map_discovered_percent:.2f} %   ", end="\r")

    min_cost_estimate = 999999
    picked_cell = None
    for cell in frontier:
        (i, j) = cell
        # g(cell) = total_costs[i][j]
        # h(cell) = (NR_OF_ROWS - 1 - i) + (NR_OF_COLS - 1 - j), but we don't need the constant parts
        # as this expression will be calculated for each cell equally and only to compare it against other cells
        cost_estimate = total_costs[i][j] - i - j
        if cost_estimate < min_cost_estimate:
            picked_cell = cell
            min_cost_estimate = cost_estimate

    (row, col) = picked_cell

    # Exit condition
    if picked_cell == GOAL:
        print("\nFound", GOAL)
        break

    # Investigate possible candidates to visit from the picked cell
    for candidate in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
        (i, j) = candidate
        if i < 0 or i == NR_OF_ROWS or j < 0 or j == NR_OF_COLS or candidate in explored_cells:
            continue

        # picked cell total cost + candidate cell entering cost
        candidate_total_cost = total_costs[row][col] + costs[i][j]

        # We can finally add the cell to the frontier
        if candidate not in frontier:
            frontier.append(candidate)

        # Register the cost (or adjust it in case we've just found a cheaper way to the candidate)
        if total_costs[i][j] == 0 or total_costs[i][j] > candidate_total_cost:
            total_costs[i][j] = candidate_total_cost

    # Remove the processed cell from the frontier and add it to the discovered ones
    frontier.remove(picked_cell)
    explored_cells.append(picked_cell)


print(f"\nTotal lowest risk level on the shortest path: {total_costs[NR_OF_ROWS - 1][NR_OF_COLS - 1]}")
