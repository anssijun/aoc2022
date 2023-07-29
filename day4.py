# https://adventofcode.com/2022/day/4

def overlap(minx, maxx, miny, maxy, partially=True):
    if partially:
        return (maxx >= miny and maxy >= minx) or (maxy >= minx and maxx >= miny)
    return (minx <= miny and maxx >= maxy) or (miny <= minx and maxy >= maxx)

def calc_count(part2=False):
    c = 0
    with open('inputs/day4') as f:
        for line in f:
            pairs = line.strip().split(',')
            minx, maxx = pairs[0].split('-')
            miny, maxy = pairs[1].split('-')
            minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
            if overlap(minx, maxx, miny, maxy, part2):
                c += 1
    return c


if __name__ == '__main__':
    print(calc_count())
    print(calc_count(True))
