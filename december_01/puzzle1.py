#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
MINUS_INF = float("-INF")

prev_z = MINUS_INF
increase_count = 0

with open(INPUT_FILE, "r") as infile:
    for line in infile:
        z = float(line)
        if prev_z != MINUS_INF and z > prev_z:
            increase_count += 1

        prev_z = z

print(f"Depth has increased {increase_count} times.")
