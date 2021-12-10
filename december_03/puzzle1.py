#!/usr/bin/env python3

INPUT_FILE = "./input.txt"

"""
The digit_counter dictionary stores the number of occurences of "0"s and "1"s in the input.
The index in the list at the respective key corresponds to the position of an input binary number.
In case the input numbers consist of 5 digits (as in the example), the lists under the keys will have a size of 5, too.
"""
digit_counter = {"0": [], "1": []}

nr_of_digits = 0

with open(INPUT_FILE, "r") as infile:
    for line in infile:

        # Chop off the newline character
        line = line.strip()

        if not digit_counter["0"]:

            nr_of_digits = len(line)
            # Initialize the counters
            digit_counter["0"] = [0] * nr_of_digits
            digit_counter["1"] = [0] * nr_of_digits

        else:
            # Validate the input
            assert len(digit_counter["0"]) == nr_of_digits

        # Update the digit counters
        for i, digit in enumerate(line):
            digit_counter[digit][i] += 1

epsilon = ""
gamma = ""
for i in range(nr_of_digits):
    if digit_counter["0"][i] > digit_counter["1"][i]:
        epsilon += "0"
        gamma += "1"

    elif digit_counter["1"][i] > digit_counter["0"][i]:
        epsilon += "1"
        gamma += "0"

    else:
        print("Houston, we have a little problem (unspecified input)")

epsilon_rate = int(epsilon, 2)
gamma_rate = int(gamma, 2)

print(f"Power consumption (epsilon_rate * gamma_rate): {epsilon_rate * gamma_rate}")
