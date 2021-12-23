#!/usr/bin/env python3

import sys

from functools import reduce


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input_test_2_8.txt"
LAST_LITERAL_MARKER = "0"

TYPE_ID_SUM = 0
TYPE_ID_PRODUCT = 1
TYPE_ID_MINIMUM = 2
TYPE_ID_MAXIMUM = 3
TYPE_ID_LITERAL = 4
TYPE_ID_GREATER_THAN = 5
TYPE_ID_LESS_THAN = 6
TYPE_ID_EQUAL_TO = 7

OP_TYPE_0_FIELD_LENGTH = 15
OP_TYPE_1_FIELD_LENGTH = 11


def parse_literal(input, debug_pos = 0):
    """
    Parses a literal from the input stream
    """
    pos = 0
    literal = ""
    while True:
        pos += 5
        literal += input[pos - 4: pos]
        if input[pos - 5] == LAST_LITERAL_MARKER:
            break

    print(f"{' ' * debug_pos}{input[:pos]}")
    return (int(literal, 2), pos)


def parse_packet(input, stack, packets_to_read = 1, debug_pos = 0):
    """
    Parses a binary bitstream (represented as a string).
    Returns the parsed packet as a dictionary with the keys "version", "type_id", "children" and "value" (optionally).
    """
    pos = 0
    packets = []
    while input[pos:] and len(packets) < packets_to_read:

        print(f"{' ' * (debug_pos)}X {len(packets)}")
        packet = {"value": None, "children": []}

        version = int(input[pos: pos + 3], 2)
        type_id = int(input[pos + 3: pos + 6], 2)

        print(f"{' ' * (debug_pos + pos)}{input[pos: pos + 3]}")
        print(f"{' ' * (debug_pos + pos)}ty:{input[pos + 3: pos + 6]}")

        packet["version"] = version
        packet["type_id"] = type_id

        stack.append({"version": version, "type_id": type_id})

        if type_id == TYPE_ID_LITERAL:
            (literal, literal_length) = parse_literal(input[pos + 6:], debug_pos + pos + 6)
            packet["value"] = literal
            packet["length"] = 6 + literal_length

        else:
            length_type_id = input[pos + 6]
            print(f"{' ' * (debug_pos + pos + 6)}{length_type_id}")

            packet["length_type_id"] = length_type_id
            length_field_chars = 0
            subpackets = None
            subpacket_length = None
            field_start = pos + 7

            if length_type_id == "0":
                length_field_chars = OP_TYPE_0_FIELD_LENGTH
                field_end = field_start + length_field_chars
                subpacket_length = int(input[field_start: field_end], 2)
                print(f"{' ' * (debug_pos + field_start)}{input[field_start: field_end]} - {subpacket_length}")
                subpackets = parse_packet(input[field_end: field_end + subpacket_length], stack, 999, debug_pos + field_end)
                assert subpacket_length == sum([x["length"] for x in subpackets])

            else:
                length_field_chars = OP_TYPE_1_FIELD_LENGTH
                field_end = field_start + length_field_chars
                nr_of_subpackets_to_read = int(input[field_start: field_end], 2)
                print(f"{' ' * (debug_pos + pos + 7)}{input[field_start: field_end]} - #{nr_of_subpackets_to_read}")
                subpackets = parse_packet(input[field_end:], stack, nr_of_subpackets_to_read, debug_pos + field_end)
                subpacket_length = sum([x["length"] for x in subpackets])
                assert len(subpackets) == nr_of_subpackets_to_read

            packet["length"] = 7 + length_field_chars + subpacket_length
            packet["children"] = subpackets

        pos += packet["length"]
        packets.append(packet)

    return packets


def evaluate(packet, indent=0):
    """
    Evaluates a hierarchically structured packet and returns the result of the evaluation.
    """
    value = None
    op_str = None

    if packet["type_id"] == TYPE_ID_SUM:
        op_str = "SUM"

    elif packet["type_id"] == TYPE_ID_PRODUCT:
        op_str = "MUL"

    elif packet["type_id"] == TYPE_ID_MINIMUM:
        op_str = "MIN"

    elif packet["type_id"] == TYPE_ID_MAXIMUM:
        op_str = "MAX"

    elif packet["type_id"] == TYPE_ID_LITERAL:
        op_str = "val"

    elif packet["type_id"] == TYPE_ID_GREATER_THAN:
        op_str = "GT"

    elif packet["type_id"] == TYPE_ID_LESS_THAN:
        op_str = "LT"

    elif packet["type_id"] == TYPE_ID_EQUAL_TO:
        op_str = "EQ"

    length_type_info = (" (length info type: " + packet["length_type_id"] + ")") if "length_type_id" in packet else ""
    subpacket_info = (" (subpackets: " + str(len(packet["children"])) + ")") if len(packet["children"]) else ""
    value_info = (" " + str(packet["value"])) if packet["value"] else ""
    print(f"{' ' * indent}{op_str}{length_type_info}{subpacket_info}{value_info}")

    subpacket_values = [evaluate(subpacket, indent + 3) for subpacket in packet["children"]]

    if packet["type_id"] == TYPE_ID_SUM:
        value = sum(subpacket_values)

    elif packet["type_id"] == TYPE_ID_PRODUCT:
        value = reduce(lambda a, b: a*b, subpacket_values)

    elif packet["type_id"] == TYPE_ID_MINIMUM:
        value = min(subpacket_values)

    elif packet["type_id"] == TYPE_ID_MAXIMUM:
        value = max(subpacket_values)

    elif packet["type_id"] == TYPE_ID_LITERAL:
        value = packet["value"]

    elif packet["type_id"] == TYPE_ID_GREATER_THAN:
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] > subpacket_values[1] else 0

    elif packet["type_id"] == TYPE_ID_LESS_THAN:
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] < subpacket_values[1] else 0

    elif packet["type_id"] == TYPE_ID_EQUAL_TO:
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] == subpacket_values[1] else 0

    return value


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
packet = parse_packet(input, stack)
sum_of_version_numbers = sum(x["version"] for x in stack)
print(f"\nSum of the version numbers in the input: {sum_of_version_numbers}")

value = evaluate(packet[0])

print(f"\nEvaluated expression: {value}")
