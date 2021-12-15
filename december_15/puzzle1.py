#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
NR_OF_STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 1

def add(register, ch):
    """
    Adds a single character to the register (if not already there) and increases its corresponding counter value.
    """
    if ch:
        if ch not in register:
            register[ch] = 0

        register[ch] += 1


# Read the input and prepare the variable holding the data
polymer = None  # The ever-growing polymer as a simple string
rules = {}
with open(INPUT_FILE, "r") as infile:

    polymer = infile.readline().rstrip()
    infile.readline()

    # Read the pair insertion rules
    while line := infile.readline().rstrip():
        rule = line.split(" -> ")
        rules[rule[0]] = rule[1]

assert polymer
assert rules

# Do the processing
register = {}
for _ in range(NR_OF_STEPS):
    register = {}
    new_polymer = ""

    for i in range(len(polymer) - 1):
        pair = polymer[i: i + 2]
        to_insert = rules[pair] if pair in rules else ""
        add(register, pair[0])
        add(register, to_insert)

        # This is the step where the ineffectiveness comes from: growing the string
        new_polymer += pair[0] + to_insert

    # Extrawurst for the last character
    last_char = polymer[-1]
    add(register, last_char)
    polymer = new_polymer + last_char

# Calculate the posterior
frequencies = [register[ch] for ch in register]
frequencies.sort()
result = frequencies[-1] - frequencies[0]

print(f"\nBlablabla ... result after {NR_OF_STEPS} steps: {result}")
