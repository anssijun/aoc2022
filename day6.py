# https://adventofcode.com/2022/day/6
from collections import deque


if __name__ == '__main__':
    header_len = 4
    counter = 0
    buffer = deque()
    char_to_idx = {}
    with open('inputs/day6') as f:
        # Read the file a character at a time (IRL we'd read more at a time to a buffer)
        while c := f.read(1):
            counter += 1
            buffer.append(c)
            if len(buffer) == header_len:
                # If the deque is full, check if all characters are unique by casting to set
                if len(set(buffer)) == header_len:
                    break
                buffer.popleft()
    print(counter)
