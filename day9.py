# https://adventofcode.com/2022/day/9

def move(direction, distance, moves, knots, rope_length):
    for i in range(distance):
        match direction:
            # Move the head
            case 'L':
                knots[0][0] -= 1
            case 'U':
                knots[0][1] += 1
            case 'R':
                knots[0][0] += 1
            case 'D':
                knots[0][1] -= 1
            case default:
                pass

        # After the head has been moved, move the rest of the rope
        for j in range(1, rope_length):
            # Figure out how the current knot has to move compared to the previous knot
            need_to_move_horizontally = abs(knots[j][0] - knots[j-1][0]) > 1
            need_to_move_vertically = abs(knots[j][1] - knots[j-1][1]) > 1

            if need_to_move_horizontally:
                knots[j][0] += 1 if knots[j-1][0] > knots[j][0] else -1
                # Do we also need to move diagonally?
                if knots[j-1][1] != knots[j][1]:
                    knots[j][1] += 1 if knots[j-1][1] > knots[j][1] else -1
            elif need_to_move_vertically:
                knots[j][1] += 1 if knots[j-1][1] > knots[j][1] else -1
                if knots[j-1][0] != knots[j][0]:
                    knots[j][0] += 1 if knots[j-1][0] > knots[j][0] else -1

            # Only interested in tail positions
            if j == rope_length - 1:
                # Add the tail position to moves set (tuple is immutable so can be used as key)
                moves.add((knots[j][0], knots[j][1]))


def calculate_position(cmds, rope_length=2):
    moves = set()
    knots = []
    for i in range(rope_length):
        knots.append([0, 0])
    for cmd in cmds:
        cmd = cmd.split()
        move(cmd[0], int(cmd[1]), moves, knots, rope_length=rope_length)
    return len(moves)


if __name__ == '__main__':
    with open('inputs/day9') as f:
        cmds = f.readlines()
    print(calculate_position(cmds))
    print(calculate_position(cmds, rope_length=10))
