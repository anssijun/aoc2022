# https://adventofcode.com/2022/day/13
import ast
import math
from functools import cmp_to_key
from typing import Union


def compare_packet_pair(left: Union[int, list], right: Union[int, list]):
    c = 0
    result = 0
    # Loop through the lists in the pair, compare items and figure out whether they're in the correct order.
    # 1. First checks that both lists still have entries. If one has run out of entries (but the other has not),
    #    we have a result.
    # 2. If both have items, check entries themselves.
    # 2.1. If both are integers, compare them. If they're not equal, we have a result.
    # 2.2. If either side is a list and the other is not, call this function recursively and wrap the other side in a list.
    #      This might mean that we recurse multiple times before starting to check the values.
    while result == 0:
        try:
            left_value = left[c]
        except IndexError:
            left_value = None
        try:
            right_value = right[c]
        except IndexError:
            right_value = None

        print(f'Compare {left_value} and {right_value}')

        if left_value is None and right_value is not None:
            # If left hand side runs out first, inputs are in the right order
            return 1
        elif left_value is not None and right_value is None:
            # If right runs out first, inputs are not in the right order
            return -1
        elif left_value is None and right_value is None:
            # Both left and right ran out so it's inconclusive - move on to next entries
            return 0

        # Compare elements. If both are ints, they can be compared directly. If either side is a list and the other one
        # and integer, convert the integer to list and call this function recursively. If both are lists, also call this
        # function recursively.
        if isinstance(left_value, int) and isinstance(right_value, int):
            result = compare_ints(left_value, right_value)
        elif isinstance(left_value, list) and isinstance(right_value, list):
            result = compare_packet_pair(left_value, right_value)
        elif isinstance(left_value, list):
            result = compare_packet_pair(left_value, [right_value])
        elif isinstance(right_value, list):
            result = compare_packet_pair([left_value], right_value)

        # Break to return a result only if we have one, otherwise check next elements
        if result:
            break

        c += 1

    return result


def compare_ints(left: int, right: int):
    if left > right:
        return -1
    elif left < right:
        return 1
    return 0


def parse_input(filename: str):
    packets = []
    # Ugly but it's not prod code
    with open(filename) as f:
        c = 0
        for line in f.readlines():
            c += 1
            if c in (1, 2):
                packets.append(parse_line(line))
            else:
                c = 0
    return packets


def parse_line(line: str):
    # Using ast.literal_eval so we don't have to parse the line manually
    return ast.literal_eval(line.strip())


def main():
    packets = parse_input('inputs/day13')
    correct_packets = []
    # Loop through the list in steps of two, in order to compare packets
    for i in range(0, len(packets), 2):
        if compare_packet_pair(packets[i], packets[i+1]) == 1:
            # We're interested in the indices of package pairs, thus we need some simple math here
            correct_packets.append(math.ceil((i + 1) / 2))
        print()
    print('Sum of correct package\'s indices is: ', sum(correct_packets))

    # For part two, we need to add a couple of "divider" packets, sort the list and get a product of the divider packets'
    # indices (1-based). Simple enough as we can use the compare_packet_pair -function as the sort key. (Python's sort
    # natively takes only one argument, but luckily we can wrap the key function to cmp_to_key to support two arguments.)
    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=cmp_to_key(compare_packet_pair), reverse=True)

    two_index = packets.index([[2]]) + 1
    six_index = packets.index([[6]]) + 1

    print('The product of [[2]] and [[6]] indices is: ', two_index * six_index)


if __name__ == '__main__':
    main()
