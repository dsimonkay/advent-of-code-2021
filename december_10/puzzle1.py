#!/usr/bin/env python3


INPUT_FILE = "./input.txt"

# Read the input and prepare the variable holding the data
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        height_map_row = [int(x) for _, x in enumerate(line)]
        height_map.append(height_map_row)

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
