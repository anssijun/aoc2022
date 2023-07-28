rock = 'A'
paper = 'B'
scissors = 'C'
scores = {
    rock: 1,
    paper: 2,
    scissors: 3
}


def won(opponent, own):
    return (opponent == rock and own == paper) or \
           (opponent == paper and own == scissors) or \
           (opponent == scissors and own == rock)


if __name__ == '__main__':
    score = 0
    with open('inputs/day2') as f:
        for line in f:
            opponent, own = line.strip().split()
            # Sanitize input for easier handling
            if own == 'X':
                own = rock
            elif own == 'Y':
                own = paper
            elif own == 'Z':
                own = scissors

            score += scores[own]
            if opponent == own:
                score += 3
            elif won(opponent, own):
                score += 6
    print('Score:', score)
