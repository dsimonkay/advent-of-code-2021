#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
NR_OF_DAYS = 80
NEW_FISH_LIFECYCLE = 8
FISH_LIFECYCLE = 6


# Read the input and prepare the variable holding the data
pool = []

with open(INPUT_FILE, "r") as infile:
    pool = [int(x) for x in infile.readline().rstrip().split(",")]

# Simulate the cycles (naive approach)
for _ in range(NR_OF_DAYS):
    new_pool = []
    for fish in pool:
        if fish == 0:
            new_pool.append(FISH_LIFECYCLE)
            new_pool.append(NEW_FISH_LIFECYCLE)
        else:
            new_pool.append(fish - 1)

    pool = new_pool

print(f"Number of fishes after {NR_OF_DAYS} days: {len(pool)}")
