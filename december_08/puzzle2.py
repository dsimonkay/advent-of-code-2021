#!/usr/bin/env python3

INPUT_FILE = "./input.txt"

# Nr of segments --> the digit itself
LENGTHS = {2: 1, 4: 4, 3: 7, 7: 8}


def contains(code, substring):
    """
    Checks whether a given code contains each letter from the given substring.
    """
    contained = [ch for ch in substring if ch in code]
    return len(contained) == len(substring)


def remove(code, substring):
    """
    Removes the characters in the specified substring from the given code.
    """
    difference = [ch for ch in code if ch not in substring]
    return "".join(difference)


def decode_digits(digits):
    """
    Figure out which string in the input list corresponds to which digit.
    Works by applying brute force and a very naive approach.

    Digit: nr. of segments
    0: 6 -check-
    1: 2 (unique)
    2: 5 -check-
    3: 5 -check-
    4: 4 (unique)
    5: 5 -check-
    6: 6 -check-
    7: 3 (unique)
    8: 7 (unique)
    9: 6 -check-
    """
    assert len(digits) == 10

    codes = [""] * 10

    # Store the well-known numbers (1, 4, 7, 8)
    for digit_code in digits:
        nr_of_segments = len(digit_code)
        if nr_of_segments in LENGTHS:
            codes[LENGTHS[nr_of_segments]] = digit_code

    # 3 (=size of 5) has the same segments as 7 _plus_ some two others
    for digit_code in digits:
        if len(digit_code) == 5 and contains(digit_code, codes[7]):
            codes[3] = digit_code

    # We can easily locate the three horizontal segments if we "subtract" 1 from 3
    horizontal_segments = remove(codes[3], codes[1])

    # 9 (=size of 6) contains 3 and 1
    for digit_code in digits:
        if (
            len(digit_code) == 6
            and contains(digit_code, codes[1])
            and contains(digit_code, codes[3])
        ):
            codes[9] = digit_code

    # 9 minus 3 yields the top-left vertical segment
    top_left_segment = remove(codes[9], codes[3])

    # 5 (=size of 5) contains the horizontal segments and the top-left one
    for digit_code in digits:
        if (
            len(digit_code) == 5
            and digit_code not in codes
            and contains(digit_code, horizontal_segments)
            and contains(digit_code, top_left_segment)
        ):
            codes[5] = digit_code

    # 2 is the last digit which has a size of 5 and is not yet in the code register
    for digit_code in digits:
        if len(digit_code) == 5 and digit_code not in codes:
            codes[2] = digit_code

    # 6 has all the three horizontal segments and has a size of 6
    for digit_code in digits:
        if (
            len(digit_code) == 6
            and digit_code not in codes
            and contains(digit_code, horizontal_segments)
        ):
            codes[6] = digit_code

    # 0 is the remaining one
    for digit_code in digits:
        if len(digit_code) == 6 and digit_code not in codes:
            codes[0] = digit_code

    return codes


# Read the input and prepare the variable holding the data
inputs = []
outputs = []

with open(INPUT_FILE, "r") as infile:
    while inline := infile.readline().rstrip():

        (tmp_inputs, tmp_outputs) = inline.split(" | ")

        tmp_inputs = tmp_inputs.split(" ")
        # Sort the strings in order to make them comparable to those in the output
        tmp_inputs = ["".join(sorted(x)) for x in tmp_inputs]
        inputs.append(tmp_inputs)

        tmp_outputs = tmp_outputs.split(" ")
        # Sort the strings in order to make them comparable to those in the input
        tmp_outputs = ["".join(sorted(x)) for x in tmp_outputs]
        outputs.append(tmp_outputs)


decoded_sum = 0

# Process the data
for i, input_case in enumerate(inputs):

    codes = decode_digits(input_case)
    decoded_number = 0

    for output_digit in outputs[i]:
        decoded_number = 10 * decoded_number + codes.index(output_digit)

    decoded_sum += decoded_number

print(f"\nSum of the decoded numbers: {decoded_sum}")
