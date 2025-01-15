from collections import deque
from operator import itemgetter


def bfs_find_way_out(coords: tuple[int, int, int], trapped_air: set[tuple[int, int, int]], min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> tuple[set[tuple[int, int, int]], bool]:
    # Use BFS to see if it's possible to find a way out from given coords in an air pocket
    # This will return all other cubes it's possible to get to from a given cube, and whether a way out was found
    queue = deque()
    queue.append(coords)

    way_out = False
    visited = {coords}
    while queue:
        i = queue.popleft()

        for neighbor in get_adjacent_cubes(i, trapped_air):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

        if not (min_x < i[0] < max_x and min_y < i[1] < max_y and min_z < i[2] < max_z):
            way_out = True

    return visited, way_out


def get_exposed_sides(cube: tuple[int, int, int], cubes: set[tuple[int, int, int]], trapped_air) -> list[tuple[int, int, int]]:
    # Get all neighbors for a cube by checking the neighboring spots
    return [c for c in [tuple(sum(i) for i in zip(cube, delta)) for delta in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]] if c not in cubes and c not in trapped_air]



def get_adjacent_cubes(cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # Get all neighbors for a cube by checking the neighboring spots
    return [c for c in [tuple(sum(i) for i in zip(cube, delta)) for delta in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]] if c in cubes]


def main():
    with open('inputs/day18') as f:
        coords = f.readlines()

    cubes = set()
    for c in coords:
        x, y, z = [int(coord) for coord in c.split(',')]
        cubes.add((x, y, z))

    total_surface_area = 0
    for cube in cubes:
        # A cube has a total potential surface area of 6, so calculate the non-connected sides by simply subtracting
        # the amount of adjacent cubes from 6
        total_surface_area += 6 - len(get_adjacent_cubes(cube, cubes))

    print(total_surface_area)

    min_x, min_y, min_z = (min(cubes, key=itemgetter(i))[i] for i in range(3))
    max_x, max_y, max_z = (max(cubes, key=itemgetter(i))[i] for i in range(3))

    # Potential "trapped air cubes" are cubes within the boundaries of the droplet, that are not part of the droplet itself
    potential_trapped_air = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in cubes:
                    potential_trapped_air.add((x, y, z))

    trapped_air = set()
    non_trapped_air = set()
    for coords in potential_trapped_air:
        # If coords have already been checked, just skip
        if coords in trapped_air or coords in non_trapped_air:
            continue

        visited, found_way_out = bfs_find_way_out(coords, potential_trapped_air, min_x, max_x, min_y, max_y, min_z, max_z)
        if found_way_out:
            non_trapped_air.update(visited)
        else:
            trapped_air.update(visited)

    exposed_surface_area = 0
    for cube in cubes:
        exposed_surface_area += len(get_exposed_sides(cube, cubes, trapped_air))
    print(exposed_surface_area)


if __name__ == '__main__':
    main()
