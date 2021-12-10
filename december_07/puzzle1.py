#!/usr/bin/env python3

INPUT_FILE = "./input.txt"


def calculate_fuel_consumptions_at(target, positions):
    """
    Calculates the overall fuel consumption with respect to the given target.
    """
    fuel_consumption = 0
    for pos in positions:
        distance = abs(pos - target)
        fuel_consumption += distance

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

fuel_consumptions.sort()

print(f"Minimum fuel consumption: {fuel_consumptions[0]}")
