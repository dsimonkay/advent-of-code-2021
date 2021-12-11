#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
MIN_ENERGY_LEVEL = 0
MAX_ENERGY_LEVEL = 9
ROWS = None
COLS = None

def get_non_flashed_but_charged_cells(board, flashed):
    """
    Check whether the board contains cell which are charged (over the max energy level)
    but have not yet flashed.
    """
    global ROWS, COLS, MAX_ENERGY_LEVEL
    cells = []
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] > MAX_ENERGY_LEVEL and not flashed[i][j]:
                cells.append((i, j))

    return cells


def increase_energy_levels_around(board, row, col):
    """
    Calculate the effect of a flashing taking place at [row, col].
    """
    global ROWS, COLS
    for i in [row - 1, row, row + 1]:
        if i < 0 or i == ROWS:
            continue

        for j in [col - 1, col, col + 1]:
            if (i != row or j != col) and j >= 0 and j < COLS:
                board[i][j] += 1


# Read the input and prepare the variable holding the data
board = []
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        state_row = [int(x) for _, x in enumerate(line)]
        board.append(state_row)

ROWS = len(board)
COLS = len(board[0])  # Hello, input validation

# Process the data
first_synchronized_step = None
step = 0
while not first_synchronized_step:
    step += 1
    flashed = [[False for _ in range(COLS)] for _ in range(ROWS)] 

    # Increase the counters
    for i in range(ROWS):
        for j in range(COLS):
            board[i][j] += 1

    # Keep on flashing until saturation
    while cells := get_non_flashed_but_charged_cells(board, flashed):
        for (i, j) in cells:
            flashed[i][j] = True
            increase_energy_levels_around(board, i, j)

    # Reset the flashed cells and check for a synchronized flashing event
    all_flashed = True
    for i in range(ROWS):
        for j in range(COLS):
            all_flashed = all_flashed and flashed[i][j]
            if board[i][j] > MAX_ENERGY_LEVEL:
                board[i][j] = MIN_ENERGY_LEVEL

    if all_flashed:
        first_synchronized_step = step

print(f"\nThe first step at which all the octopusses flash: {first_synchronized_step}")
