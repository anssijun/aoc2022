def get_adjacent_cubes(cube, cubes):
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
        # the amount of neighbors from 6
        total_surface_area += 6 - len(get_adjacent_cubes(cube, cubes))

    print(total_surface_area)


if __name__ == '__main__':
    main()
