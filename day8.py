# https://adventofcode.com/2022/day/8
import operator
from functools import reduce


def calculate_visibility(height, current_index, tallness_index):
    closest = current_index
    for i in range(height, 10):
        if -1 < tallness_index[i]:
            distance = current_index - tallness_index[i]
            if closest > distance:
                closest = distance
    return closest


def count_visible_trees(trees, reverse=False):
    trees_visible = 0
    highest_scenic_score = 0
    # Keep the tallest tree for each column in a list as we iterate over rows
    tallest_from_up = [-1] * len(trees[0])
    tallness_indexes_up = []
    for i in range(len(trees[0])):
        tallness_indexes_up.append({i: -1 for i in range(10)})

    left_score_idx, up_score_idx = 0, 1
    # Going through the array in reverse order could be done a bit of efficiently using range from end to start
    if reverse:
        trees.reverse()
        left_score_idx, up_score_idx = 2, 3
    for row_idx, row in enumerate(trees):
        if reverse:
            row.reverse()
        tallest_from_left = -1
        tallness_index_left = {i: -1 for i in range(10)}
        for col_idx, tree in enumerate(row):
            # Check if the tallest tree to the left or to the up is shorter than the current one - if so, it's
            # visible
            visible = False
            if tree[0] > tallest_from_up[col_idx]:
                tallest_from_up[col_idx] = tree[0]
                visible = True
            # Calculate how much up you can see from the tree by checking how far the closest tree that's as tall or
            # taller than the current one is. As the max three height is 9, this is probably OK performance
            tree[2][up_score_idx] = calculate_visibility(tree[0], row_idx, tallness_indexes_up[col_idx])

            if tree[0] > tallest_from_left:
                tallest_from_left = tree[0]
                visible = True
            tree[2][left_score_idx] = calculate_visibility(tree[0], col_idx, tallness_index_left)

            # Count only if tree is visible and hasn't been counted yet
            if visible and not tree[1]:
                trees_visible += 1
                tree[1] = True

            tallness_indexes_up[col_idx][tree[0]] = row_idx
            tallness_index_left[tree[0]] = col_idx
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
