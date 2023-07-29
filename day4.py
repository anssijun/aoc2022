# https://adventofcode.com/2022/day/4

if __name__ == '__main__':
    c = 0
    with open('inputs/day4') as f:
        for line in f:
            pairs = line.strip().split(',')
            minx, maxx = pairs[0].split('-')
            miny, maxy = pairs[1].split('-')
            minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
            if (minx <= miny and maxx >= maxy) or (miny <= minx and maxy >= maxx):
                c += 1
    print(c)
