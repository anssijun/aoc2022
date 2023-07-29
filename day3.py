# https://adventofcode.com/2022/day/3

def get_score(item):
    if item.isupper():
        return ord(item) - 38
    return ord(item) - 96


if __name__ == '__main__':
    score = 0
    with open('inputs/day3') as f:
        for line in f:
            rucksack = line.strip()
            # Make sets out of compartments, so we can use intersection to find out the common item
            comp1, comp2 = set(rucksack[:len(rucksack)//2]), set(rucksack[len(rucksack)//2:])
            common = comp1.intersection(comp2)
            score += get_score(common.pop())
    print('Score', score)
