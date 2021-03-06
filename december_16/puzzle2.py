#!/usr/bin/env python3

import sys

from functools import reduce


INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "./input.txt"
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


def parse_literal(input):
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

    return (int(literal, 2), pos)


def parse_packet(input, packets_to_read = 1):
    """
    Parses a binary bitstream (represented as a string).
    Returns the parsed packet as a dictionary with the keys "version", "type_id", "children" and "value" (optionally).
    """
    pos = 0
    packets = []
    while input[pos:] and len(packets) < packets_to_read:

        packet = {
            "version": int(input[pos: pos + 3], 2),
            "type_id": int(input[pos + 3: pos + 6], 2),
            "length": None,
            "value": None,
            "children": []
        }

        if packet["type_id"] == TYPE_ID_LITERAL:
            (literal, literal_length) = parse_literal(input[pos + 6:])
            packet["value"] = literal
            packet["length"] = 6 + literal_length

        else:
            packet["length_type_id"] = input[pos + 6]
            length_field_chars = 0
            subpackets = None
            subpacket_length = None
            field_start = pos + 7

            if packet["length_type_id"] == "0":
                length_field_chars = OP_TYPE_0_FIELD_LENGTH
                field_end = field_start + length_field_chars
                subpacket_length = int(input[field_start: field_end], 2)
                subpackets = parse_packet(input[field_end: field_end + subpacket_length], 999)
                assert sum([x["length"] for x in subpackets]) == subpacket_length

            else:
                length_field_chars = OP_TYPE_1_FIELD_LENGTH
                field_end = field_start + length_field_chars
                nr_of_subpackets_to_read = int(input[field_start: field_end], 2)
                subpackets = parse_packet(input[field_end:], nr_of_subpackets_to_read)
                subpacket_length = sum([x["length"] for x in subpackets])
                assert len(subpackets) == nr_of_subpackets_to_read

            packet["length"] = 7 + length_field_chars + subpacket_length
            packet["children"] = subpackets

        pos += packet["length"]
        packets.append(packet)

    return packets


def evaluate(packet):
    """
    Evaluates a hierarchically structured packet and returns the result of the evaluation.
    """
    value = None
    subpacket_values = [evaluate(subpacket) for subpacket in packet["children"]]

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
        input += bin(int(ch, 16))[2:].zfill(4)

# Parse and evaluate
packet = parse_packet(input)
value = evaluate(packet[0])
print(f"\nEvaluated expression: {value}")
