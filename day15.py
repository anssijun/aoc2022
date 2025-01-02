import re


def get_row_coverage(sensors: dict[tuple[int, int], int], row: int, min_x: int = None, max_x: int = None) -> list[tuple[int, int]]:
    # Calculate a given row's coverage using given a dict of sensors and their radiuses. For each sensor, we can calculate
    # the 'start' and 'end' positions of the sensor's coverage by comparing its y-coordinate to the row, and using
    # Manhattan distance to calculate the 'width' of the coverage. Finally, we merge the sensor's coverage with other sensors'
    # coverage as we go.
    coverages = []
    for sensor, radius in sensors.items():
        distance = abs(sensor[1] - row)
        # If the sensor's distance from given row is more than its radius, just move on to the next sensor
        if distance > radius:
            continue

        # Calculate the x-coordinates for the coverage's start and end
        coverage_width = abs(radius - distance) * 2 + 1
        coverage_start = sensor[0] - int(coverage_width / 2)
        coverage_end = sensor[0] + int(coverage_width / 2)

        # If there are min or max bound, we're only interested in those
        if min_x is not None:
            coverage_start = max(coverage_start, min_x)
        if max_x is not None:
            coverage_end = min(coverage_end, max_x)

        # We must see if there's overlap in the existing coverage for every new sensor, and, if needed, merge the coverages
        new_coverages = []
        for start, end in coverages:
            merged = False
            # If the new coverage is continuous with an existing coverage at the start, merge them
            if start < coverage_start and coverage_start - end <= 1:
                coverage_start = start
                merged = True
            # If the new coverage is continuous with an existing coverage from the end, merge them
            if end > coverage_end and start - coverage_end <= 1:
                coverage_end = end
                merged = True
            # If the new coverage does not overlap with an existing coverage at all, keep the existing coverage as is
            if not merged and not (start >= coverage_start and end <= coverage_end):
                new_coverages.append((start, end))

        new_coverages.append((coverage_start, coverage_end))
        coverages = new_coverages

        # If the entire search area is already covered, just bail out
        if coverage_start == min_x and coverage_end == max_x:
            break

    return coverages


def calculate_row_total_coverage(coverage: list[tuple[int, int]]) -> int:
    # Calculate the total number of covered positions given a list of coverage start and end positions
    return sum([c[1] - c[0] for c in coverage])


def calculate_sensor_radiuses(sensors: list[tuple[int, int]], beacons: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    sensor_radiuses = {}
    # Iterate sensors and beacons at the same time, and calculate the sensor's coverage radius using the Manhattan distance.
    # Each sensors' closest beacon is in the same index in the beacons list.
    for idx, sensor in enumerate(sensors):
        closest_beacon = beacons[idx]
        radius = manhattan(sensor, closest_beacon)
        sensor_radiuses[sensor] = radius

    return sensor_radiuses


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    # Calculate the manhattan distance between two points
    return sum((abs(a[0] - b[0]), abs(a[1] - b[1])))


def parse_input(filename: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    sensors = []
    beacons = []
    with open(filename) as f:
        matches = re.findall(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', f.read())

    for sensor_x, sensor_y, beacon_x, beacon_y in matches:
        sensors.append((int(sensor_x), int(sensor_y)))
        beacons.append((int(beacon_x), int(beacon_y)))

    return sensors, beacons


def main():
    sensors, beacons = parse_input('inputs/day15')
    sensor_radiuses = calculate_sensor_radiuses(sensors, beacons)
    row = 2000000
    coverages = get_row_coverage(sensor_radiuses, row)
    row_coverage = calculate_row_total_coverage(coverages)
    print(f'Distress beacon can\'t be on {row_coverage} positions on row {row}')
    print()

    # For part two, just brute force the search for each row. This is very slow - a much smarter solution probably exists
    for row in range(4000000):
        coverages = get_row_coverage(sensor_radiuses, row, 0, 4000000)
        total_row_coverage = calculate_row_total_coverage(coverages)
        if total_row_coverage < 4000000:
            coverages.sort()
            x = 0 if coverages[0][0] == 1 else coverages[0][1] + 1
            print(f'The tuning frequency is {4000000 * x + row}')
            break

if __name__ == '__main__':
    main()
