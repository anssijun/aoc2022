# https://adventofcode.com/2022/day/5
import re
from collections import defaultdict, deque


def top_crates(part2=False):
    # Stacks is a dict of deques (could be list of deques but this is easier to build when reading through input)
    # Deques are used because you can appendleft, so it's more natural from building the stack top to bottom
    stacks = defaultdict(deque)
    with open('inputs/day5') as f:
        for line in f:
            line = line.rstrip()
            sl = line.lstrip()
            if sl.startswith('['):
                stack_counter = 0
                for i, v in enumerate(line):
                    if v.isalnum():
                        # We know square brackets denote a crate, and we're interested in the letter inside. There's a
                        # space between crates, so we can use the index to calculate which stack the number belongs to:
                        # first stack would be index 1, second stack would be index 5, this stack index 9 etc
                        stacks[((i-1)//4)+1].appendleft(v)
                        stack_counter += 1
            elif sl.startswith('move'):
                count, source, target = re.findall(r'\d+', sl)
                count, source, target = int(count), int(source), int(target)
                crates = []
                for i in range(count):
                    crates.append(stacks[source].pop())
                # We need to reverse the order of moving crates for part 2 as multiple are moved at a time
                order = -1 if part2 else 1
                stacks[target].extend(crates[::order])

    for i in sorted(stacks.keys()):
        print(stacks[i][-1], end='')
    print()


if __name__ == '__main__':
    top_crates()
    top_crates(True)
