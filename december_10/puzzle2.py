#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
OPENINGS = ('(', '[', '{', '<')
CLOSINGS = (')', ']', '}', '>')
# In order to avoid unnecessary cross-referencing, we simply use
# the opening characters for the points, as the indexes are the same
POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

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
scores = []
for line in input_lines:
    stack = []
    line_is_corrupt = False

    for ch in line:
        assert ch in OPENINGS or ch in CLOSINGS

        if ch in OPENINGS:
            stack.append(ch)

        elif ch in CLOSINGS:
            if not is_matching_closing(stack, ch):
                line_is_corrupt = True
                break

    if not line_is_corrupt and stack:

        # We have an incomplete line here
        score = 0
        for ch in stack[::-1]:
            score *= 5
            score += POINTS[ch]
        scores.append(score)


assert len(scores) % 2 == 1
scores.sort()
middle_score = scores[int((len(scores) - 1)/2)]
print(f"Middle score: {middle_score}")
