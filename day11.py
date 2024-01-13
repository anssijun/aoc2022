# https://adventofcode.com/2022/day/11
import copy
import math
import operator
import re


def simulate_monkeys(monkeys, rounds, inspection_stress_factor, op):
    # Simulate monkeys for 20 rounds
    for r in range(rounds):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['handled_items'] += 1
                # Using eval isn't great, but way easier than parsing the formula manually...
                new_stress_level = op(eval(monkey['operation'].replace('old', str(item))), inspection_stress_factor)
                # Throw the item to the correct monkey
                monkeys[monkey['false' if new_stress_level % monkey['test'] else 'true']]['items'].append(new_stress_level)
            # Monkey has thrown all their items away, so they don't have any left
            monkey['items'] = []
    return monkeys


if __name__ == '__main__':
    monkeys = []
    with open('inputs/day11') as f:
        input = f.readlines()

    for line in input:
        line = line.strip()
        # Parse the input and construct monkey objects (well dicts really). Not a very nice way to do it but since
        # the input structure is known, it works (doesn't have to be anything fancy anyway)
        if line.startswith('Monkey'):
            monkeys.append({'handled_items': 0})
        elif line.startswith('Starting items'):
            monkeys[-1]['items'] = [int(item) for item in re.findall(r'\d+', line)]
        elif line.startswith('Operation'):
            monkeys[-1]['operation'] = line.split('=')[1]
        elif line.startswith('Test'):
            monkeys[-1]['test'] = int(re.search(r'\d+', line).group())
        elif line.startswith('If true'):
            monkeys[-1]['true'] = int(re.search(r'\d+', line).group())
        elif line.startswith('If false'):
            monkeys[-1]['false'] = int(re.search(r'\d+', line).group())

    first_monkeys = simulate_monkeys(copy.deepcopy(monkeys), 20, 3, operator.floordiv)
    sorted_monkeys = sorted(first_monkeys, key=lambda x: x['handled_items'], reverse=True)
    print(sorted_monkeys[0]['handled_items'] * sorted_monkeys[1]['handled_items'])

    # The new way to reduce stress is product of the integers in test section, and using modulo operator
    # Had to look this up
    second_monkeys = simulate_monkeys(
        copy.deepcopy(monkeys),
        10000,
        math.prod(monkey['test'] for monkey in monkeys),
        operator.mod
    )
    sorted_monkeys = sorted(second_monkeys, key=lambda x: x['handled_items'], reverse=True)
    print(sorted_monkeys[0]['handled_items'] * sorted_monkeys[1]['handled_items'])
