# https://adventofcode.com/2022/day/8
import operator
from functools import reduce


def count_visible_trees(trees, reverse=False):
    trees_visible = 0
    highest_scenic_score = 0
    # Keep the tallest tree for each column in a list as we iterate over rows
    tallest_from_up = [-1] * len(trees[0])

    left_score_idx, up_score_idx = 0, 1
    # Going through the array in reverse order could be done a bit of efficiently using range from end to start
    if reverse:
        trees.reverse()
        left_score_idx, up_score_idx = 2, 3
    for row_idx, row in enumerate(trees):
        if reverse:
            row.reverse()
        tallest_from_left = -1
        for col_idx, tree in enumerate(row):
            # Check if the tallest tree to the left or to the up is shorter than the current one - if so, it's
            # visible
            visible = False
            if tree[0] > tallest_from_up[col_idx]:
                tallest_from_up[col_idx] = tree[0]
                visible = True
            # Calculate how much up you can see from the tree. This is pretty bad for performance as in worst case
            # you might have to go all the way up each iteration - but not sure if it's possible to implement this
            # otherwise (at least if we want to keep the calculation in the same algorithm as part 1. Probably possible
            # with some dict magic but seems like a pain to implement)
            for i in range(row_idx-1, -1, -1):
                tree[2][up_score_idx] += 1
                if trees[i][col_idx][0] >= tree[0]:
                    break

            if tree[0] > tallest_from_left:
                tallest_from_left = tree[0]
                visible = True
            for i in range(col_idx-1, -1, -1):
                tree[2][left_score_idx] += 1
                if trees[row_idx][i][0] >= tree[0]:
                    break

            # Count only if tree is visible and hasn't been counted yet
            if visible and not tree[1]:
                trees_visible += 1
                tree[1] = True

            # Calculate the scenic score for each direction
            scenic_score = int(reduce(operator.mul, tree[2]))
            highest_scenic_score = max(highest_scenic_score, scenic_score)
    return trees_visible, highest_scenic_score


if __name__ == '__main__':
    trees = []
    trees_visible = 0
    highest_scenic_score = 0
    with open('inputs/day8') as f:
        for line in f:
            line = line.strip()
            print(line)
            row = []
            trees.append(row)
            for c in line:
                # Append tree height, visibility (false by default) and
                # trees seen in each direction (left, up, right, down)
                row.append([int(c), False, [0, 0, 0, 0]])
    # First go through the three top-bottom, left-right, and then do the same in reverse (by just reversing the lists)
    for r in (False, True):
        visible, score = count_visible_trees(trees, r)
        trees_visible += visible
        highest_scenic_score += score
    print(trees_visible)
    print(highest_scenic_score)
