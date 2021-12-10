#!/usr/bin/env python3

INPUT_FILE = "./input.txt"


# Read the input and prepare the variable holding the data
points = {}

with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():

        # Hello, input validation :-/
        [x1, y1, x2, y2] = [int(x) for x in line.replace(" -> ", ",").split(",")]

        dx = x2 - x1
        dy = y2 - y1

        # Skip non-horizontal or non-vertical lines for now
        if dx != 0 and dy != 0:
            continue

        x_step = 0 if dx == 0 else int(dx / abs(dx))
        y_step = 0 if dy == 0 else int(dy / abs(dy))

        # off-by-one
        target_x = x2 + x_step
        target_y = y2 + y_step

        x = x1
        y = y1
        while not (x == target_x and y == target_y):
            key = str(x) + "_" + str(y)
            if key not in points:
                points[key] = 0

            points[key] += 1

            x += x_step
            y += y_step


# Process the input
points_we_are_looking_for = [key for key in points if points[key] > 1]

print(
    f"\nNumber of points at which at least two lines overlap: {len(points_we_are_looking_for)}"
)
