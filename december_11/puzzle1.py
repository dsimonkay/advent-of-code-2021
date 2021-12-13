#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
NR_OF_CYCLES = 100
MIN_ENERGY_LEVEL = 0
MAX_ENERGY_LEVEL = 9
ROWS = None
COLS = None


def print_board(board, cycle=None):
    """
    You guessed it -- print the board (debug).
    """
    print("\n-------------", f"after cycle {cycle}:" if cycle else "")
    for row in board:
        print(row)


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
    Calculate the effect of a flash taking place at [row, col].
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
flash_count = 0
for cycle in range(NR_OF_CYCLES):
    flashed = [[False for _ in range(COLS)] for _ in range(ROWS)]

    # Increase the counters
    for i in range(ROWS):
        for j in range(COLS):
            board[i][j] += 1

    # Keep on flashing until saturation
    while cells := get_non_flashed_but_charged_cells(board, flashed):
        for (i, j) in cells:
            flash_count += 1
            flashed[i][j] = True
            increase_energy_levels_around(board, i, j)

    # Reset the flashed cells
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] > MAX_ENERGY_LEVEL:
                board[i][j] = MIN_ENERGY_LEVEL

print(f"\nTotal flashes after {NR_OF_CYCLES} cycles: {flash_count}")
