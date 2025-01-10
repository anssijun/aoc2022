# https://adventofcode.com/2022/day/17

from itertools import cycle
from operator import itemgetter


def simulate_rocks(cavern: list[list[list[int]]], rocks: list[list[list[int | None]]], jet_pattern, max_rocks: int) -> list[list[list[int]]]:
    # Simulate the falling rocks. The cavern is 7 unit wide, and each vertical space is represented by ranges of solid rock,
    # where we store each range's start and end coordinates. As the rocks keep falling down, we add them to the cavern's
    # representation once they've fallen onto the floor or another rock.
    current_rock = 0
    for rock in cycle(rocks):  # Cycle through rocks until we break out manually
        current_rock += 1
        if current_rock > max_rocks:
            break

        # Calculate rock's starting coords, and change its representation to be 7 units wide so it matches cavern, so we
        # know its horizontal position in the cavern.
        highest_rock = get_highest_rock(cavern)
        rock_coords = [[None, None]] * 2
        for r in rock:
            rock_coords.extend(get_rock_starting_coords(r, highest_rock))
        rock_coords.extend([[None, None]] * (7 - len(rock) - 2))

        # Move the rock until it falls down. First it gets moved one spot by a jet of gas, after which it falls down one spot
        while True:
            jet_pattern_direction = next(jet_pattern)
            rock_coords, _ = move_rock(rock_coords, cavern, jet_pattern_direction)
            rock_coords, moved = move_rock(rock_coords, cavern, 'down')
            if not moved:
                break

        # Once the rock has settled down, add its coordinates to the cavern's representation
        for idx, coords in enumerate(rock_coords):
            if not isinstance(coords[0], int):
                continue

            cavern[idx].append(coords)
            # Merge any connected ranges together
            cavern[idx] = sorted(cavern[idx], key=itemgetter(1))
            cavern[idx] = merge_rocks(cavern[idx])

        cavern = raise_floor(cavern)
        # print(cavern)

    return cavern


def move_rock(rock: list[list[int | None]], cavern: list[list[list[int]]], direction: str) -> tuple[list[list[int | None]], bool]:
    # Move rock one space to either left, right or down. Finally, check if the new coordinates would overlap with anything
    # in the cavern (walls, floor, already fallen rocks), and if so, return the original coords (so the rock doesn't actually move).
    new_rock_coords = rock.copy()
    if direction == '<' and rock[0] == [None, None]:
        new_rock_coords = rock[1:] + [[None, None]]
    elif direction == '>' and rock[-1] == [None, None]:
        new_rock_coords = [[None, None]] + rock[:-1]
    elif direction == 'down':
        for idx, coords in enumerate(rock):
            if isinstance(coords[0], int):
                new_rock_coords[idx] = [coords[0] - 1, coords[1] - 1]

    if overlap(new_rock_coords, cavern):
        return rock, False

    return new_rock_coords, True


def overlap(rock: list[list[int | None]], cavern: list[list[list[int]]]) -> bool:
    # Do teh rock coordinates overlap with any other rock coordinates in the cavern
    for idx, coords in enumerate(rock):
        if not isinstance(coords[0], int):
            continue

        c = cavern[idx]
        for cc in c:
            if coords[1] >= cc[0] and cc[1] >= coords[0]:
                return True
    return False


def get_rock_starting_coords(rock: list[int | None], highest_rock: int) -> list[list[int | None]]:
    # Calculates the coords where the rock starts falling from
    coords = []
    for idx, i in enumerate(rock):
        # In rock's representation, 0 is an "empty" space and 1 is solid rock. This is needed as rocks can be oddly shaped.
        # We only care about solid rock in this case.
        if i == 1:
            # Build vertical ranges of solid rock
            if coords:
                coords[-1][1] += 1
            else:
                coords.append([highest_rock + 4 + idx, highest_rock + 4 + idx])
    return coords


def get_highest_rock(cavern: list[list[list[int]]]):
    # Get the highest rock coordinate
    return max([c[-1] for c in cavern], key=itemgetter(1))[1]


def merge_rocks(rocks: list[list[int]]) -> list[list[int]]:
    # Merge ranges of rocks so that two connected ranges get merged into one. Assumes the rock range is sorted.
    merged_rocks = []

    for current in rocks:
        # If merged is empty or the current range doesn't overlap with the last one, add it
        if not merged_rocks or merged_rocks[-1][1] < current[0] - 1:
            merged_rocks.append(current)
        else:
            # Merge the current range with the last range in the merged list
            merged_rocks[-1][1] = max(merged_rocks[-1][1], current[1])

    return merged_rocks


def raise_floor(cavern: list[list[list[int]]]):
    # "Raise" the floor of the cavern, by discarding all rock ranges below the lowest vertical space in the cavern.
    # Pruning the cavern like this will make e.g. range merging calculations significantly faster (as we don't have to
    # keep considering ranges that are unreachable for the falling rocks in the first place).
    lowest_point = min([c[-1] for c in cavern], key=itemgetter(1))[1]
    raised_cavern = []
    for c in cavern:
        for idx, rock_ranges in enumerate(c):
            # If the current range ends above the lowest high point in the cavern, only keep that and any subsequent ranges
            if rock_ranges[1] >= lowest_point:
                # We need inclusive slice of the list but also account for the start of the list leading to silly if-else
                # slicing (this could be prettier!)
                raised_cavern.append(c[idx - 1 if idx > 0 else idx:])
                break
    return raised_cavern


def parse_input(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def main():
    jet_pattern = cycle(parse_input('inputs/day17'))
    cavern = [[[0, 0]] for _ in range(7)]
    # Representation of rocks, where each list the number of spaces the rock takes up vertically.
    # (These probably could've been done using ranges as we deal with ranges elsewhere as well?)
    rocks = [
        [[1], [1], [1], [1]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]]
    ]

    cavern = simulate_rocks(cavern, rocks, jet_pattern, max_rocks=2022)
    print(get_highest_rock(cavern))


if __name__ == '__main__':
    main()
