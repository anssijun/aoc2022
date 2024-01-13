# https://adventofcode.com/2022/day/11
import re


def simulate_monkeys(monkeys):
    # Simulate monkeys for 20 rounds
    for _ in range(20):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['handled_items'] += 1
                # Using eval isn't great, but way easier than parsing the formula manually...
                new_stress_level = int(eval(monkey['operation'].replace('old', str(item))) / 3)
                # Throw the item to the correct monkey
                monkeys[monkey['false' if new_stress_level % monkey['test'] else 'true']]['items'].append(new_stress_level)
            # Monkey has thrown all their items away, so they don't have any left
            monkey['items'] = []


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

    simulate_monkeys(monkeys)
    sorted_monkey = sorted(monkeys, key=lambda x: x['handled_items'], reverse=True)
    print(sorted_monkey[0]['handled_items'] * sorted_monkey[1]['handled_items'])
