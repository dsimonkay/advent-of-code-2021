#!/usr/bin/env python3

INPUT_FILE = "./input.txt"

horizontal_pos = 0
depth = 0


def forward(x):
    global horizontal_pos
    horizontal_pos += x


def down(x):
    global depth
    depth += x


def up(x):
    global depth
    depth = max(0, depth - x)


interpreter = {"forward": forward, "down": down, "up": up}

with open(INPUT_FILE, "r") as infile:
    for line in infile:
        (command, argument) = line.split()
        interpreter[command](int(argument))

print(f"Final position * depth: {horizontal_pos * depth}")
