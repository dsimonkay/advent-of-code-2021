#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
NR_OF_STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 1

def add(register, key):
    """
    Adds a single key to a register (if not already there) and increases its corresponding counter value.
    """
    if key:
        if key not in register:
            register[key] = 0

        register[key] += 1

def add_with_pos(register, key, position):
    """
    Adds a single key to a register (if not already there) and increases its corresponding counter value.
    """
    if key not in register or register[key] < position:
        register[key] = position

def get_last_pair(polymer):
    max_pos = -1
    last_pair = None
    for pair in polymer:
        position = polymer[pair]
        if position > max_pos:
            max_pos = position
            last_pair = pair

    return last_pair 


# Read the input and prepare the variable holding the data
polymer = {}
rules = {}
with open(INPUT_FILE, "r") as infile:

    template = infile.readline().rstrip()
    print("template:", template)
    for i in range(len(template) - 1):
        pair = template[i: i + 2]
        print("adding pair:", pair)
        add_with_pos(polymer, pair, i)

    infile.readline()

    # Read the pair insertion rules
    while line := infile.readline().rstrip():
        rule = line.split(" -> ")
        rules[rule[0]] = rule[1]

assert polymer
assert rules

print("Polymer at the beginning:", polymer)

# Do the processing
register = {}
for step in range(NR_OF_STEPS):
    print(f"\nPolymer at step {step}: {polymer}")
    register = {}
    new_polymer = {}

    for pair in polymer:
        position = polymer[pair]
        add(register, pair[0])

        if pair in rules:
            to_insert = rules[pair]
            add_with_pos(new_polymer, pair[0] + to_insert, position)
            add_with_pos(new_polymer, to_insert + pair[1], position + 1)
            add(register, to_insert)

        else:
            add_with_pos(new_polymer, pair, position)

    last_pair = get_last_pair(polymer)
    add(register, last_pair[1])

    polymer = new_polymer
    print("register:", register)
    print("polymer:", polymer)


# Calculate the posterior
frequencies = [register[ch] for ch in register]
frequencies.sort()
result = frequencies[-1] - frequencies[0]

print(f"\nBlablabla result after {NR_OF_STEPS} steps: {result}")
