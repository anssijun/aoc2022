def simulate_sand(cave: list[list[str]], source_coords: tuple[int, int]):
    # Simulate the falling sand by finding the landing spot for each unit of sand and counting them. Once an IndexError
    # is raised, we know that the sand will start falling into the abyss and can stop the simulation.
    counter = 0
    while True:
        try:
            landing_coords = find_landing_coords(cave, source_coords)
        except IndexError:
            break
        cave[landing_coords[1]][landing_coords[0]] = 'o'
        counter += 1
        # for i in cave: print(''.join(i))
        # print()
    return counter


def find_landing_coords(cave: list[list[str]], current_coords: tuple[int, int]):
    # Finds the landing coords for the sand by recursively searching first down, the down and left and finally down and
    # right. Valid landing coords are have a unit of air '.' in them but either rock or sand below, including to the
    # left and right. If the sand would fall out of the bounds of the cave, an index error is raised as this is the
    # terminal state for the algorithm (could/should be some other error or mechanism but whatever).
    if cave[current_coords[1] + 1][current_coords[0]] != '.':
        if cave[current_coords[1] + 1][current_coords[0] - 1] != '.':
            if cave[current_coords[1] + 1][current_coords[0] + 1] != '.':
                return current_coords
            return find_landing_coords(cave, (current_coords[0] + 1, current_coords[1] + 1))
        return find_landing_coords(cave, (current_coords[0] - 1, current_coords[1] + 1))
    return find_landing_coords(cave, (current_coords[0], current_coords[1] + 1))


def build_cave(data: list[str]):
    # minimum y coordinate is 0 so don't need to calculate that
    rock_coords, min_x, max_x, max_y = get_rock_coords_and_cave_dimensions(data)

    # Build the outline of the cave (2-dimensional list)
    # This also means that when accessing individual items of the list of lists, y coordinate is given first, which is
    # a bit confusing.
    cave = [['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y + 1)]

    # Iterate over the coords for the rock lines and add them to the cave
    for start_coords, end_coords in rock_coords:
        # If x coordinates are the same, build a vertical line
        if start_coords[0] == end_coords[0]:
            for i in range(max(start_coords[1], end_coords[1]) - min(start_coords[1], end_coords[1]) + 1):
                cave[min(start_coords[1], end_coords[1]) + i][start_coords[0] - min_x] = '#'
        # If y coordinates are the same, build a horizontal line
        elif start_coords[1] == end_coords[1]:
            for i in range(max(start_coords[0], end_coords[0]) - min(start_coords[0], end_coords[0]) + 1):
                cave[start_coords[1]][min(start_coords[0], end_coords[0]) - min_x + i] = '#'

    # Return the min_x coord to calculate for the x offset (needed because the minimum x coordinate isn't actually 0)
    return cave, min_x


def get_rock_coords_and_cave_dimensions(data: list[str]):
    rock_coords = []
    min_x, max_x, max_y = 99999, -99999, -99999
    # Build the rock line coords as a list of tuples, each containing the x and y coordinates of the start and end of the line
    # Also note down the cave dimensions while doing this as they can be used build out the cave map
    for line in data:
        coords = line.split('->')
        for idx in range(0, len(coords) - 1):
            start = coords[idx].strip().split(',')
            end = coords[idx + 1].strip().split(',')
            start_x = int(start[0])
            end_x = int(end[0])
            start_y = int(start[1])
            end_y = int(end[1])

            min_x = min(min_x, start_x, end_x)
            max_x = max(max_x, start_x, end_x)
            max_y = max(max_y, start_y, end_y)

            rock_coords.append(((start_x, start_y), (end_x, end_y)))

    return rock_coords, min_x, max_x, max_y



def parse_input(filename: str):
    with open(filename) as f:
        return f.readlines()


def main():
    cave, x_offset = build_cave(parse_input('inputs/day14'))
    max_sand = simulate_sand(cave, (500 - x_offset, 0))
    print(f'{max_sand} unit of sand can fall before it starts to flow into the abyss')



if __name__ == '__main__':
    main()
