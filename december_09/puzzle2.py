#!/usr/bin/env python3

"""
--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

from functools import reduce


INPUT_FILE = "./input.txt"
MAX_HEIGHT = 9


def overwrite(ids, old, new):
    """
    Overwrite specific (=old) basin ids in the 2D input array with a new value.
    This operation is basically "merging" basins.
    """
    for row, id_row in enumerate(ids):
        for col, value in enumerate(id_row):
            if value == old:
                ids[row][col] = new


height_map = []  # 2D numerical representation of the input
basin_ids = []  # Basin ID register
basin_id_counts = {}

# Read the input and prepare the variable holding the data
with open(INPUT_FILE, "r") as infile:
    while line := infile.readline().rstrip():
        height_map_row = [int(x) for _, x in enumerate(line)]
        height_map.append(height_map_row)
        basin_ids.append([0] * len(line))

basin_id_sequence = 0

# Process the data: iterating over the height from the top left corner towards the bottom right one.
# For each spot we determine the basin ids of the spots to the left and upward. In case they match,
# we pick one of them. In case they are both zero, we generate a new basin id from the sequence and
# hence start a new basin. In case they differ we have once again two cases: is either of them zero,
# we pick the non-zero value and keep it. In case they differ, we pick the one which comes from above
# and use it to merge the two basins.
for i, height_map_row in enumerate(height_map):
    for j, height in enumerate(height_map_row):

        if height == MAX_HEIGHT:
            continue

        basin_id = None

        id_up = 0 if i == 0 else basin_ids[i - 1][j]
        id_left = 0 if j == 0 else basin_ids[i][j - 1]

        if id_up == 0 and id_left == 0:
            # Starting a new basin
            basin_id_sequence += 1
            basin_id = basin_id_sequence

        elif id_up != id_left:
            if id_up * id_left == 0:
                # One of them is irrelevant (=zero) -- we need the _other_ one
                basin_id = max(id_left, id_up)

            else:
                # Both are non-zero; we're gonna stick with the one which comes from above
                basin_id = id_up

                # And we also need to overwrite all the other values with this one
                overwrite(basin_ids, id_left, id_up)

                # Booking over the old values and removing the unnecessary ones
                basin_id_counts[id_up] += basin_id_counts[id_left]
                del basin_id_counts[id_left]

        else:
            # The same basin is to the left and up; any of them fits
            basin_id = id_left

        if basin_id not in basin_id_counts:
            basin_id_counts[basin_id] = 0

        basin_id_counts[basin_id] += 1
        basin_ids[i][j] = basin_id

basin_sizes = [basin_id_counts[x] for x in basin_id_counts]
basin_sizes.sort(reverse=True)
largest_three_basin_sizes_product = reduce((lambda x, y: x * y), basin_sizes[0:3])

print(f"Product of the largest three basin sizes: {largest_three_basin_sizes_product}")
