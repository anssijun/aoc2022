# https://adventofcode.com/2022/day/1
def calc_max_calories():
    # Max score
    max_calories = 0
    # Single elf calories
    calories = 0
    with open('inputs/day1') as f:
        for line in f:
            # Calculate single elf's calories
            try:
                calories += int(line.strip())
            except ValueError:
                # Empty line denotes a new elf - compare max scores and move to the next elf
                if calories > max_calories:
                    max_calories = calories
                calories = 0

    print('Max calories:', max_calories)


if __name__ == '__main__':
    calc_max_calories()
