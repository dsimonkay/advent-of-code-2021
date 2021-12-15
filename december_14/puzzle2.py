#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
NR_OF_STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 1


def add(register, key, count, is_last=False):
    """
    Adds a key to a register (if not already there) and increases its corresponding counter value.
    The register also holds an extra boolean flag (wherever this information is applicable.)
    In our case the flag marks an element to be the last one if the register is the polymer itself.
    (Actually, it's True for the last polymer pair only).
    """
    count_so_far = 0
    is_last_so_far = False
    if key in register:
        (count_so_far, is_last_so_far) = register[key]

    register[key] = (count_so_far + count, is_last_so_far or is_last)


# The polymer pairs are stored as dictionary keys. They hold the information of how many times
# the given pair occurs in the actual polymer (which we don't see in this version in its entire
# form) and whether it's about the last pair in the chain.
polymer = {}
rules = {}

# Read the input and prepare the variable holding the data
with open(INPUT_FILE, "r") as infile:

    template = infile.readline().rstrip()
    for i in range(len(template) - 1):
        pair = template[i: i + 2]
        add(polymer, pair, 1)

    # Mark the last pair as such
    last_pair = template[-2:]
    last_polymer_count = polymer[last_pair][0]
    polymer[last_pair] = (last_polymer_count, True)

    infile.readline()

    # Read the pair insertion rules
    while line := infile.readline().rstrip():
        rule = line.split(" -> ")
        rules[rule[0]] = rule[1]

assert polymer
assert rules

# Do the processing
for _ in range(NR_OF_STEPS):
    new_polymer = {}

    for pair, (count, is_last) in polymer.items():
        if pair in rules:
            to_insert = rules[pair]
            add(new_polymer, pair[0] + to_insert, count)
            add(new_polymer, to_insert + pair[1], count, is_last)

        else:
            # This will never be the case, but for the sake of completeness it's been left here
            add(new_polymer, pair, count, is_last)

    polymer = new_polymer

# Collect the results
char_register = {}
for pair, (count, _) in polymer.items():
    add(char_register, pair[0], count)

    # Extrawurst in case of the last pair: counting the very last charater, too
    if polymer[pair][1]:
        add(char_register, pair[1], 1)

# Calculate the posterior
frequencies = [char_register[ch][0] for ch in char_register]
frequencies.sort()
result = frequencies[-1] - frequencies[0]

print(f"\nBlablabla ... result after {NR_OF_STEPS} steps: {result}")
