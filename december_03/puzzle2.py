#!/usr/bin/env python3

INPUT_FILE = "./input.txt"


def get_counters(numbers, position):
    """
    Calculate the digit counts at a certain postion in a list of (binary) numbers represented as strings.
    """
    counters = {"0": 0, "1": 0}

    for number in numbers:
        counters[number[position]] += 1

    return counters


def filter_candidates(candidates, position, filter_value):
    """
    Filter out the matching candidates which have a specific value at a given position.
    """
    matching_candidates = []
    for candidate in candidates:
        if candidate[position] == filter_value:
            matching_candidates.append(candidate)

    return matching_candidates


# Read the input
oxygen_candidates = []
with open(INPUT_FILE, "r") as infile:
    oxygen_candidates = infile.read().splitlines()

# The Pythonic way to determine whether it's empty or not.
assert oxygen_candidates
NR_OF_DIGITS = len(lines[0])
co2_candidates = oxygen_candidates.copy()

# Main processing loop
for position in range(NR_OF_DIGITS):

    if len(oxygen_candidates) == 1 and len(co2_candidates) == 1:
        break

    if len(oxygen_candidates) > 1:
        # Filter the oxygen candidates
        counters = get_counters(oxygen_candidates, position)
        filter_value = "0" if counters["0"] > counters["1"] else "1"
        oxygen_candidates = filter_candidates(oxygen_candidates, position, filter_value)

    if len(co2_candidates) > 1:
        # Filter the CO2 candidates
        counters = get_counters(co2_candidates, position)
        filter_value = "1" if counters["1"] < counters["0"] else "0"
        co2_candidates = filter_candidates(co2_candidates, position, filter_value)


assert len(oxygen_candidates) == 1
assert len(co2_candidates) == 1

print("Oxygen candidates:", oxygen_candidates)
print("CO2 candidates:", co2_candidates)

oxygen_generator_rating = int(oxygen_candidates[0], 2)
co2_scrubber_rating = int(co2_candidates[0], 2)

print(
    f"Life support rating (oxygen_generator_rating * co2_scrubber_rating): {oxygen_generator_rating * co2_scrubber_rating}"
)
