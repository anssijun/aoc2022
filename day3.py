# https://adventofcode.com/2022/day/3

def get_score(item):
    # a=1, b=2 ... A=27, B=28...
    if item.isupper():
        return ord(item) - 38
    return ord(item) - 96


def calc_score(part2=False, n=3):
    score = 0
    rucksacks = []
    with open('inputs/day3') as f:
        for line in f:
            rucksack = line.strip()
            # Combine n rucksacks into one
            if part2:
                rucksacks.append(set(rucksack))
                if len(rucksacks) < n:
                    continue
            else:
                # Make sets out of compartments
                rucksacks = set(rucksack[:len(rucksack) // 2]), set(rucksack[len(rucksack) // 2:])

            # Find common item using intersection
            common = rucksacks[0].intersection(*rucksacks[1:]).pop()
            score += get_score(common)
            rucksacks = []
    return score


if __name__ == '__main__':
    print('Score', calc_score())
    print('Score', calc_score(True))
