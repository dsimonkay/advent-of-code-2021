#!/usr/bin/env python3

INPUT_FILE = "./input.txt"

horizontal_pos = 0
depth = 0
aim = 0


def forward(x):
    global horizontal_pos, depth
    horizontal_pos += x
    depth += aim * x


def down(x):
    global aim
    aim += x


def up(x):
    global aim
    aim -= x


interpreter = {"forward": forward, "down": down, "up": up}

with open(INPUT_FILE, "r") as infile:
    for line in infile:
        (command, argument) = line.split()
        interpreter[command](int(argument))

print(f"Final position * depth: {horizontal_pos * depth}")
