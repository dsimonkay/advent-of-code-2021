#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
OPENINGS = ("(", "[", "{", "<")
CLOSINGS = (")", "]", "}", ">")
ERROR_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}


def is_matching_closing(stack, ch):
    """
    Check whether an input closing character matches the opening character on the stack.
    """
    assert len(stack)
    ch_out = stack.pop()
    return OPENINGS.index(ch_out) == CLOSINGS.index(ch)


# Read the input and prepare the variable holding the data
input_lines = []
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        input_lines.append(line)


# Process the data
error_score = 0
for line in input_lines:
    stack = []
    for ch in line:
        assert ch in OPENINGS or ch in CLOSINGS

        if ch in OPENINGS:
            stack.append(ch)

        elif ch in CLOSINGS:
            if not is_matching_closing(stack, ch):
                error_score += ERROR_SCORES[ch]
                break

print(f"Total syntax error score: {error_score}")
