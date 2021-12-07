#!/usr/bin/env python3

"""
--- Part Two ---
The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

Move from 16 to 5: 66 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 0 to 5: 15 fuel
Move from 4 to 5: 1 fuel
Move from 2 to 5: 6 fuel
Move from 7 to 5: 3 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 14 to 5: 45 fuel
This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?
"""


INPUT_FILE = "./input.txt"


def calculate_fuel_consumptions_at(target, positions):
    """
    Calculates the overall fuel consumption with respect to the given target.
    """
    fuel_consumption = 0
    for pos in positions:
        distance = abs(pos - target)
        # Sum of an arithmetic progression by a difference of 1, starting at, hmm, 1
        fuel_consumption += int((1 + distance) * distance / 2)

    return fuel_consumption


# Read the input and prepare the variable holding the data
positions = None

with open(INPUT_FILE, "r") as infile:
    positions = [int(x) for x in infile.readline().rstrip().split(",")]
    positions.sort()

# Calculate the minimum fuel consumption (brute force :-/)
fuel_consumptions = []
for target in range(positions[0], positions[-1]):
    fuel_consumptions.append(calculate_fuel_consumptions_at(target, positions))

print(positions)
fuel_consumptions.sort()

print(f"Minimum fuel consumption: {fuel_consumptions[0]}")
