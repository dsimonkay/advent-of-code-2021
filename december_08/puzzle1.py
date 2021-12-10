#!/usr/bin/env python3

INPUT_FILE = "./input.txt"
LENGTHS = (2, 4, 3, 7)  # 1, 4, 7 and 8, respectively

# Read the input and prepare the variable holding the data
inputs = []
outputs = []

with open(INPUT_FILE, "r") as infile:
    while inline := infile.readline().rstrip():

        (tmp_inputs, tmp_outputs) = inline.split(" | ")

        tmp_inputs = tmp_inputs.split(" ")
        tmp_inputs.sort(key=len)

        inputs.append(tmp_inputs)

        tmp_outputs = tmp_outputs.split(" ")
        tmp_outputs.sort(key=len)
        outputs.append(tmp_outputs)

appearences_found = 0

# Process the data
for output in outputs:
    for digit in output:
        appearences_found += 1 if len(digit) in LENGTHS else 0

print(f"Number of times 1, 4, 7 or 8 appears: {appearences_found}")
