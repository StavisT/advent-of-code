""""
input
Time: 7  15   30
distance: 9  40  200

for each whole ms you hold the button down, the boat speed increases with 1 ms / mm

race of 7 ms:
hold down 1 ms - 1ms/mm for 6 seconds -> 6mm
hold down 2 ms - 2 ms/mm for 5 seconds -> 10mm
hold down 3 ms - 3 ms/mm for 4 seconds -> 12mm
hold down 4 ms - 4 ms/mm for 3 seconds -> 12mm
hold down 5 ms - 5 ms/mm for 2 seconds -> 10mm


since the record is 9 mm, we can win in 4 different ways

puzle input:
Time:        52     94     75     94
Distance:   426   1374   1279   1216
"""
import math


def calibration_input():
    time = [7, 15, 30]
    distance = [9, 40, 200]
    return time, distance


def puzzle_input():
    time = [52, 94, 75, 94]
    distance = [426, 1374, 1279, 1216]
    return time, distance


def calibration_input2():
    time = 71530
    distance = 940200
    return time, distance


def puzzle_input2():
    time = 52947594
    distance = 426137412791216
    return time, distance


def winning_races(time, distance):
    wins_this_round = 0
    counter = 0
    for i in range(1, time):

        if i * (time - i) > distance:
            wins_this_round += 1
        elif wins_this_round > 0:
            counter = 1

        if counter > 0:
            break
    return wins_this_round


def main():
    times, distances = puzzle_input()

    # how many possible ways to win per game?
    wins = []
    for time, distance in zip(times, distances):
        wins.append(winning_races(time, distance))

    print(wins)
    print(math.prod(wins))

    #-- part 2
    print(winning_races(*calibration_input2()))
    print(winning_races(*puzzle_input2()))



if __name__ == '__main__':
    main()
