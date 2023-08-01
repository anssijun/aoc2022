# https://adventofcode.com/2022/day/8


def count_visible_trees(trees, order=None):
    trees_visible = 0
    # Keep the tallest tree for each column in a list as we iterate over rows
    tallest_from_up = [-1] * len(trees[0])
    # Going through the array in reverse order could be done a bit of efficiently using range from end to start
    if order == -1:
        trees.reverse()
    for row_idx, row in enumerate(trees):
        if order == -1:
            row.reverse()
        tallest_from_left = -1
        for col_idx, tree in enumerate(row):
            # Check if the tallest tree to the left or to the up is shorter than the current one - if so, it's
            # visible
            visible = False
            if tree[0] > tallest_from_up[col_idx]:
                tallest_from_up[col_idx] = tree[0]
                visible = True
            if tree[0] > tallest_from_left:
                tallest_from_left = tree[0]
                visible = True
            if visible and not tree[1]:
                trees_visible += 1
                tree[1] = True
    return trees_visible


if __name__ == '__main__':
    trees = []
    trees_visible = 0
    with open('inputs/day8') as f:
        for line in f:
            line = line.strip()
            print(line)
            row = []
            trees.append(row)
            for c in line:
                # Append tree height and visibility (false by default)
                row.append([int(c), False])
    # First go through the three top-bottom, left-right, and then do the same in reverse (by just reversing the lists)
    trees_visible += count_visible_trees(trees)
    trees_visible += count_visible_trees(trees, -1)
    print(trees_visible)
