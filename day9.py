# https://adventofcode.com/2022/day/9

def move(direction, distance, moves, head, tail):
    for i in range(distance):
        # Move the head
        match direction:
            case 'L':
                head[0] -= 1
            case 'U':
                head[1] += 1
            case 'R':
                head[0] += 1
            case 'D':
                head[1] -= 1
            case default:
                pass

        # Figure out whether the tail needs to move
        need_to_move_horizontally = abs(tail[0] - head[0]) > 1
        need_to_move_vertically = abs(tail[1] - head[1]) > 1

        if need_to_move_horizontally:
            tail[0] += 1 if head[0] > tail[0] else -1
            # Do we also need to move diagonally?
            if head[1] != tail[1]:
                tail[1] += 1 if head[1] > tail[1] else -1
        elif need_to_move_vertically:
            tail[1] += 1 if head[1] > tail[1] else -1
            if head[0] != tail[0]:
                tail[0] += 1 if head[0] > tail[0] else -1
        # Add the tail position to moves set (tuple is immutable so can be used as key)
        moves.add(tuple(tail))


if __name__ == '__main__':
    moves = set()
    head = [0, 0]
    tail = [0, 0]
    with open('inputs/day9') as f:
        for line in f.readlines():
            cmd = line.split()
            move(cmd[0], int(cmd[1]), moves, head, tail)
    print(len(moves))
