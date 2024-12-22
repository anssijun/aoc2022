# https://adventofcode.com/2022/day/12
from collections import defaultdict


def find_path(height_idx, path, visited, position, path_to_goal):
    # Dijkstra-esque algorithm that recursively traverses the path and attempts to find the shortest path to the goal.
    # Visits all unvisited neighbors of every node, as well as any already visited neighbors if a shorter path is found.
    current = height_idx[position]
    visited.add(position)
    path.append(position)
    current['path_length'] = len(path)

    if current['value'] == 'E':
        # If we find the path, make a copy of it to pass to future recursions (as we may still find a shorter path)
        path_to_goal = path.copy()

    # Prefer going up (this was actually needed to avoid max recursion depth error)
    neighbors = sorted(current['neighbors'], key=lambda x: _get_height(height_idx[x]['value']), reverse=True)
    for neighbor in neighbors:
        # Only go to neighbor if we haven't visited there, or if we've found a shorter path
        # (Might be possible to optimize the solution by using already calculated paths so we wouldn't have to recurse
        # all over again if we've found a shorter path - would have to either look in the current path stack or save
        # partial results in another data structure.)
        if neighbor not in visited or height_idx[neighbor]['path_length'] > len(path) + 1:
            # Should probably make copies instead of passing the same data structures around to make this a pure
            # function...
            path_to_goal = find_path(height_idx, path, visited, neighbor, path_to_goal)

    # If we can't go forward, track back
    path.pop()

    return path_to_goal


def _get_height(s):
    if s == 'S':
        return ord('a')
    elif s == 'E':
        return ord('z')
    return ord(s)


def main():
    with open('inputs/day12') as f:
        heightmap = [list(l.strip()) for l in f.readlines()]
    starting_point = None
    height_idx = defaultdict(dict)
    for row_nb, line in enumerate(heightmap):
        for col_nb, entry in enumerate(line):
            current = row_nb, col_nb
            if entry == 'S':
                starting_point = current
            height_idx[current]['value'] = entry
            height_idx[current]['path_length'] = 99999999
            height_idx[current]['neighbors'] = []
            current_height = _get_height(entry)

            # Build a graph where each square is a node and all the neighboring squares that one can move to are edges.
            # One can move to the neighboring square if it's at most 1 higher up, on the same level, or on lower level
            # compared to the current node.
            # Check the square to the left
            if col_nb > 0 and _get_height(heightmap[row_nb][col_nb - 1]) - current_height <= 1:
                height_idx[current]['neighbors'].append((row_nb, col_nb - 1))
            # To the right
            if col_nb < len(line) - 1 and _get_height(heightmap[row_nb][col_nb + 1]) - current_height <= 1:
                height_idx[current]['neighbors'].append((row_nb, col_nb + 1))
            # To down
            if row_nb < len(heightmap) - 1 and _get_height(heightmap[row_nb + 1][col_nb]) - current_height <= 1:
                height_idx[current]['neighbors'].append((row_nb + 1, col_nb))
            # To up
            if row_nb > 0 and _get_height(heightmap[row_nb - 1][col_nb]) - current_height <= 1:
                height_idx[current]['neighbors'].append((row_nb - 1, col_nb))

    path = find_path(height_idx, [], set(), starting_point, [])
    print(path)
    print('Shortest path length: ', len(path) - 1)  # Subtract 1 from the path length as the path includes the starting point


if __name__ == '__main__':
    main()
