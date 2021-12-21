#!/usr/bin/env python3

import sys


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input_test_2.txt"
LAST_LITERAL_MARKER = "0"
TYPE_ID_LITERAL = 4


def parse_literal(input, start_pos = 0):
    """
    Parses a literal from the input stream
    """
    ch_count = 0
    literal = ""
    while True:
        ch_count += 5
        literal += input[ch_count - 4: ch_count]
        if input[ch_count - 5] == LAST_LITERAL_MARKER:
            break

    print(f"{' ' * start_pos}{input[:ch_count]}")
    return (int(literal, 2), ch_count)


def parse_packet(input, stack, packets_to_read = 1, start_pos = 0):
    """
    Parses an input bitstream (represented as a string).
    Returns the number of characters consumed from the input.
    """
    packets_read = 0
    ch_count = 0
    while input[ch_count:] and packets_read < packets_to_read:

        version = int(input[ch_count: ch_count + 3], 2)
        type_id = int(input[ch_count + 3: ch_count + 6], 2)
        print(f"{' ' * (start_pos + ch_count)}{input[ch_count: ch_count + 3]}")
        print(f"{' ' * (start_pos + ch_count)}---{input[ch_count + 3: ch_count + 6]}")

        stack_element = {"version": version, "type_id": type_id}
        stack.append(stack_element)

        if type_id == TYPE_ID_LITERAL:
            (literal, literal_ch_count) = parse_literal(input[ch_count + 6:], start_pos + ch_count + 6)
            stack_element["literal"] = literal
            ch_count += 6 + literal_ch_count

        else:
            length_type_id = input[ch_count + 6]
            print(f"{' ' * (start_pos + ch_count + 6)}{length_type_id}")
            subpacket_chars = 0
            length_field_chars = 0
            if length_type_id == "0":
                length_field_chars = 15
                subpacket_length = int(input[ch_count + 7: ch_count + 7 + length_field_chars], 2)
                print(f"{' ' * (start_pos + ch_count + 7)}{input[ch_count + 7: ch_count + 22]}")
                subpacket_chars = parse_packet(input[ch_count + 22: ch_count + 22 + subpacket_length], stack, 999, start_pos + ch_count + 22)
                assert subpacket_chars == subpacket_length

            else:
                length_field_chars = 11
                nr_of_packets_to_read = int(input[ch_count + 7: ch_count + 7 + length_field_chars], 2)
                print(f"{' ' * (start_pos + ch_count + 7)}{input[ch_count + 7: ch_count + 18]}")
                subpacket_chars = parse_packet(input[ch_count + 18:], stack, nr_of_packets_to_read, start_pos + ch_count + 18)

            ch_count += 7 + length_field_chars + subpacket_chars

        packets_read += 1

    return ch_count

input = ""

# Read the input
with open(INPUT_FILE, "r") as infile:
    line = infile.readline().rstrip()
    for _, ch in enumerate(line):
        print(f"   {ch}", end="")
        input += bin(int(ch, 16))[2:].zfill(4)
    print()

print(input)
stack = []

parse_packet(input, stack)

for elem in stack:
    print(elem)

sum_of_version_numbers = sum(x["version"] for x in stack)

print(f"\nSum of the version numbers in the input: {sum_of_version_numbers}")
