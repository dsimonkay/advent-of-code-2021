#!/usr/bin/env python3

INPUT_FILE = "./input.txt"

increase_count = 0
z = []

# Collect all the measurements
with open(INPUT_FILE, "r") as infile:
    for line in infile:
        z.append(float(line))

# Precompute the first previous sliding window sum
prev_sliding_sum = sum(z[0:3])

# Process the rest of the input
for i in range(1, len(z) - 2):
    sliding_sum = sum(z[i : i + 3])
    if sliding_sum > prev_sliding_sum:
        increase_count += 1

    prev_sliding_sum = sliding_sum

print(f"The sliding window sum has increased {increase_count} times.")
