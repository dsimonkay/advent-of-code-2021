#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
NR_OF_DAYS = 256
NEW_FISH_LIFECYCLE = 8
RESET_FISH_LIFECYCLE = 6


def add(pool, fish_lifecycle, count=1):
    """
    Adds a certain number of fishes to the pool with a given lifecycle.
    """
    if fish_lifecycle not in pool:
        pool[fish_lifecycle] = 0

    pool[fish_lifecycle] += count


# Pool is an associative array holding a register of the number of fishes with a given lifecycle.
# The keys are the remaining lifecycle times before spawning a new offspring,
# the values are the number of fishes with that lifecycle.
pool = {}

# Read the input and prepare the variable holding the data
with open(INPUT_FILE, "r") as infile:
    input_pool = [int(x) for x in infile.readline().rstrip().split(",")]
    for input_fish in input_pool:
        add(pool, input_fish)

# Simulate the cycles
for _ in range(NR_OF_DAYS):

    new_pool = {}
    for lifecycle in pool:
        if lifecycle == 0:
            add(new_pool, RESET_FISH_LIFECYCLE, pool[lifecycle])
            add(new_pool, NEW_FISH_LIFECYCLE, pool[lifecycle])

        else:
            add(new_pool, lifecycle - 1, pool[lifecycle])

    pool = new_pool

fish_count = sum([pool[x] for x in pool])
print(f"Number of fishes after {NR_OF_DAYS} days: {fish_count}")
