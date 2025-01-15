from collections import deque
from operator import itemgetter


def get_neighbor_coords(coords: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return [c for c in [tuple(sum(i) for i in zip(coords, delta)) for delta in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]]]


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
        total_surface_area += 6 - len([c for c in get_neighbor_coords(cube) if c in cubes])

    print(total_surface_area)

    min_x, min_y, min_z = (min(cubes, key=itemgetter(i))[i] - 1 for i in range(3))
    max_x, max_y, max_z = (max(cubes, key=itemgetter(i))[i] + 1 for i in range(3))

    queue = deque()

    start = (min_x, min_y, min_z)
    visited = {start}
    queue.append(start)
    exposed = 0
    while queue:
        a = queue.popleft()
        neighbors = [n for n in get_neighbor_coords(a) if min_x <= n[0] <= max_x and min_y <= n[1] <= max_y and min_z <= n[2] <= max_z]
        for neighbor in neighbors:
            if neighbor in cubes:
                exposed += 1
            elif neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    print(exposed)



if __name__ == '__main__':
    main()
