#!/usr/bin/env python3

"""
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
"""


INPUT_FILE = "./input.txt"

# Read the input and prepare the variable holding the data
height_map = []

with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        height_map_row = [int(x) for _, x in enumerate(line)]
        height_map.append(height_map_row)

risk_level_sum = 0

# Process the data
for i, height_map_row in enumerate(height_map):
    for j, height in enumerate(height_map_row):
        lower_than_up = True if i == 0 else height < height_map[i - 1][j]
        lower_than_down = (
            True if i == len(height_map) - 1 else height < height_map[i + 1][j]
        )
        lower_than_left = True if j == 0 else height < height_map[i][j - 1]
        lower_than_right = (
            True if j == len(height_map_row) - 1 else height < height_map[i][j + 1]
        )

        if lower_than_up and lower_than_down and lower_than_left and lower_than_right:
            risk_level_sum += height + 1

print(f"Sum of the risk levels: {risk_level_sum}")
