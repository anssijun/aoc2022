# https://adventofcode.com/2022/day/13
import ast
from typing import Union


def compare_packet_pair(pair: list[Union[int, list]]):
    c = 0
    result = None
    # Loop through the lists in the pair, compare items and figure out whether they're in the correct order.
    # 1. First checks that both lists still have entries. If one has run out of entries (but the other has not),
    #    we have a result.
    # 2. If both have items, check entries themselves.
    # 2.1. If both are integers, compare them. If they're not equal, we have a result.
    # 2.2. If either side is a list and the other is not, call this function recursively and wrap the other side in a list.
    #      This might mean that we recurse multiple times before starting to check the values.
    while result is None:
        try:
            left = pair[0][c]
        except IndexError:
            left = None
        try:
            right = pair[1][c]
        except IndexError:
            right = None

        print(f'Compare {left} and {right}')

        if left is None and right is not None:
            # If left hand side runs out first, inputs are in the right order
            return True
        elif left is not None and right is None:
            # If right runs out first, inputs are not in the right order
            return False
        elif left is None and right is None:
            # Both left and right ran out so it's inconclusive - move on to next entries
            return

        # Compare elements. If both are ints, they can be compared directly. If either side is a list and the other one
        # and integer, convert the integer to list and call this function recursively. If both are lists, also call this
        # function recursively.
        if isinstance(left, int) and isinstance(right, int):
            result = compare_ints(left, right)
        elif isinstance(left, list) and isinstance(right, list):
            result = compare_packet_pair([left, right])
        elif isinstance(left, list):
            result = compare_packet_pair([left, [right]])
        elif isinstance(right, list):
            result = compare_packet_pair([[left], right])

        # Break to return a result only if we have one, otherwise check next elements
        if result:
            break

        c += 1

    return result


def compare_ints(left: int, right: int):
    if left > right:
        return False
    elif left < right:
        return True


def parse_input(filename: str):
    packets = []
    # Ugly but it's not prod code
    with open(filename) as f:
        c = 0
        for line in f.readlines():
            c += 1
            if c == 1:
                packets.append([parse_line(line)])
            elif c == 2:
                packets[-1].append(parse_line(line))
            else:
                c = 0
    return packets


def parse_line(line: str):
    # Using ast.literal_eval so we don't have to parse the line manually
    return ast.literal_eval(line.strip())


def main():
    packets = parse_input('inputs/day13')
    correct_packets = []
    for idx, packet in enumerate(packets):
        if compare_packet_pair(packet):
            correct_packets.append(idx + 1)
        print()
    print(sum(correct_packets))


if __name__ == '__main__':
    main()
