# https://adventofcode.com/2022/day/2

rock = 'A'
paper = 'B'
scissors = 'C'
scores = {
    rock: 1,
    paper: 2,
    scissors: 3
}
# Which option wins
winner = {
    rock: paper,
    paper: scissors,
    scissors: rock,
}
# Reverse the winner dict
loser = {v: k for k, v in winner.items()}


def won(opponent, own):
    return (opponent == rock and own == paper) or \
           (opponent == paper and own == scissors) or \
           (opponent == scissors and own == rock)


def get_own(own):
    return {
        'X': rock,
        'Y': paper,
        'Z': scissors
    }[own]


def get_own2(opponent, scenario):
    return {
        'X': loser[opponent],
        'Y': opponent,
        'Z': winner[opponent]
    }[scenario]


def calc_score(part2=False):
    score = 0
    with open('inputs/day2') as f:
        for line in f:
            opponent, scenario = line.strip().split()
            # Sanitize input for easier handling
            if part2:
                own = get_own2(opponent, scenario)
            else:
                own = get_own(scenario)

            score += scores[own]
            if opponent == own:
                score += 3
            elif won(opponent, own):
                score += 6
    return score


if __name__ == '__main__':
    print('Score:', calc_score())
    print('Score:', calc_score(True))
