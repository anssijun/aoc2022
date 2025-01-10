# https://adventofcode.com/2022/day/16

import re
from collections import deque
from functools import cache
from typing import Union


def calculate_max_pressure_release(starting_valve, minutes: int, valves: dict, teach_elephant: bool = False) -> int:
    # Recursively calculate pressure releases for different paths, and pick the best using max (each iteration will produce
    # one value, which are put together in a list). This uses an inner function in order to nicely make the valves dict
    # available for the walk -algorithm that actually calculates the pressure release (and to make it cacheable, though
    # caching is not 100% required - (update: for part 1, it is required for part 2)).
    # For part two, for each recursion we also check the max pressure the elephant could help release, if it started from
    # the beginning (keeping in mind that it should not revisit already visited valves), and return the highest value.
    # This solution likely traverses the graph needlessly many times - but it works.

    @cache
    def walk(valve: str, remaining_minutes: int, unvisited: frozenset[str], has_elephant: bool = False) -> int:
        unvisited -= {valve}
        pressure = valves[valve]['flow_rate'] * remaining_minutes

        elephant_pressure = 0
        if has_elephant:
            # The elephant has no elephant of its own, so has_elephant will be false here! (Otherwise we'll recurse
            # forever due to each elephant spawning a new elephant of its own.)
            # Hardcode the starting valve and minutes as the elephant always starts "from the beginning".
            elephant_pressure = walk(starting_valve, 26, unvisited, False)

        # Go deeper but only if there's still enough time (to both go and open the valve).
        # When we have an elephant, take its pressure release potential into account as well.
        return pressure + max(
            [walk(next_valve, remaining_minutes - valves[valve]['distances'][next_valve] - 1, unvisited, has_elephant) for
             next_valve in unvisited
             if remaining_minutes - valves[valve]['distances'][next_valve] - 1 > 0] + [elephant_pressure], default=0)

    # Only interested in valves that have a positive flow rate (this is a bit ugly)
    return max([walk(valve, minutes - valves[starting_valve]['distances'][valve] - 1, frozenset(valves[starting_valve]['distances'].keys()), teach_elephant)
                for valve in valves if valves[valve]['flow_rate'] > 0])


def calculate_distances(valve: str, valve_map: dict[str, dict[str, Union[int, list[str], dict[str, int]]]]) -> dict[str, int]:
    # Breadth first search to find distances to all other valves from a given valve
    distances = {v: float('inf') for v in valve_map}
    distances[valve] = 0
    queue = deque([valve])

    while queue:
        current_valve = queue.popleft()
        distance = distances[current_valve]

        for neighbor in valve_map[current_valve]['tunnels']:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distance + 1
                queue.append(neighbor)

    return distances

def parse_input(filename: str) -> dict[str, dict[str, Union[int, list[str], dict[str, int]]]]:
    with open(filename) as f:
        matches = re.findall(r'Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? (.+)', f.read())

    valves = {}
    for valve, flow_rate, tunnels in matches:
        neighbors = tunnels.split(', ')
        valves[valve] = {
            'flow_rate': int(flow_rate),
            'tunnels': neighbors,
            'distances': {}
        }

    return valves


def main():
    valves = parse_input('inputs/day16')
    for valve in valves:
        valves[valve]['distances'] = calculate_distances(valve, valves)

    # Clean up valves with zero flow as we're not interested in those (opening them just takes time and is, thus,
    # counterproductive). Cleaning these up also makes finding the solution MUCH faster.
    for label, valve in valves.items():
        new_distances = {}
        for v in valve['distances']:
            if valves[v]['flow_rate'] > 0:
                new_distances[v] = valve['distances'][v]
        valve['distances'] = new_distances

    print(calculate_max_pressure_release('AA', 30, valves))
    print(calculate_max_pressure_release('AA', 26, valves, True))


if __name__ == '__main__':
    main()
