# https://adventofcode.com/2022/day/6
from collections import deque


def unique_seq_end_idx(length):
    counter = 0
    buffer = deque()
    with open('inputs/day6') as f:
        # Read the file a character at a time (IRL we'd read more at a time to a buffer)
        while c := f.read(1):
            counter += 1
            buffer.append(c)
            if len(buffer) == length:
                # If the deque is full, check if all characters are unique by casting to set
                if len(set(buffer)) == length:
                    break
                buffer.popleft()
    return counter


if __name__ == '__main__':
    print(unique_seq_end_idx(4))
    print(unique_seq_end_idx(14))
