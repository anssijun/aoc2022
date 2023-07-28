# https://adventofcode.com/2022/day/1
import heapq


def calc_max_calories(top_n=1):
    # Max score
    max_calories = [0] * top_n
    # Single elf calories
    calories = 0
    with open('inputs/day1') as f:
        for line in f:
            # Calculate single elf's calories
            try:
                calories += int(line.strip())
            except ValueError:
                # Empty line denotes a new elf - compare max scores and move to the next elf
                # Handle max_calories as a min heap for easily replacing the smallest "top score" with a new one
                if calories > max_calories[0]:
                    heapq.heappushpop(max_calories, calories)
                calories = 0

    print('Max calories:', sum(max_calories))


if __name__ == '__main__':
    calc_max_calories()
    calc_max_calories(top_n=3)
