#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input_test.txt"
NR_OF_FOLDS = 1


def print_paper(paper, rows=None, cols=None):
    """
    Prints the paper with dots
    """
    if not rows:
        rows = len(paper)
    if not cols:
        cols = len(paper[0])

    for i in range(rows):
        for j in range(cols):
            print("#" if paper[i][j] else ".", end="")
        print()


def fold_up(paper, y, rows, cols):
    """
    Folds the paper upward, mirroring the dots from the lower part to the upper one.
    """
    for col in range(cols):
        for i in range(1, y + 1):
            if y + i < rows:
                paper[y - i][col] |= paper[y + i][col]

    return y, cols


def fold_left(paper, x, rows, cols):
    """
    Folds the paper to the left, mirroring the dots from the right part to the left one.
    """
    for row in range(rows):
        for i in range(1, x + 1):
            if x + i < cols:
                paper[row][x - i] |= paper[row][x + i]

    return rows, x


# Read the input and prepare the variable holding the data
dots = []
instructions = []
with open(INPUT_FILE, "r") as infile:
    # Read the dot position information
    while line := infile.readline().rstrip():
        (x, y) = [int(x) for x in line.split(",")]
        dots.append((x, y))

    # Read the folding instructions information
    while line := infile.readline().rstrip():
        words_in_line = line.split(" ")
        raw_instructions = words_in_line[2].split("=")
        instructions.append((raw_instructions[0], int(raw_instructions[1])))

# Get the paper dimensions
rows = 0
cols = 0
for dot in dots:
    rows = max(rows, dot[1])
    cols = max(cols, dot[0])
# As the values are indexes
rows += 1
cols += 1

print(f"Found {rows} rows and {cols} columns.\n")
paper = [[False for _ in range(cols)] for _ in range(rows)]

# Add the dots to the paper
for dot in dots:
    paper[dot[1]][dot[0]] = True

# Do the folding
NR_OF_FOLDS = len(instructions)
for i in range(NR_OF_FOLDS):
    axis = instructions[i][0]
    if axis == "y":
        rows, cols = fold_up(paper, instructions[i][1], rows, cols)
    elif axis == "x":
        rows, cols = fold_left(paper, instructions[i][1], rows, cols)

print_paper(paper, rows, cols)
