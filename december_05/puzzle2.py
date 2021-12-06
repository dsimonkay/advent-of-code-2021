#!/usr/bin/env python3

"""
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

"""


INPUT_FILE = "./input.txt"


# Read the input and prepare the variable holding the data
points = {}

with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():

        # Hello, input validation :-/
        [x1, y1, x2, y2] = [int(x) for x in line.replace(" -> ", ",").split(",")]

        dx = x2 - x1
        dy = y2 - y1

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
