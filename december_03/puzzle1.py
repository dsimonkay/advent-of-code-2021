#!/usr/bin/env python3

"""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

"""

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
