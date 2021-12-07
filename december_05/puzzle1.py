#!/usr/bin/env python3

"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
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
