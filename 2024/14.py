from math import prod
import re
Coordinate = tuple[int, int]
Velocity = tuple[int, int]

def read_input(file="2024/14_calibration.txt"):
    return [tuple(map(int, re.findall(r'-?\d+', line))) for line in open(file).read().splitlines()]


def calc_position(p: Coordinate, v: Velocity, g: Coordinate, n: int) -> Coordinate:
    np = [(p[i] + v[i] * n) % g[i]for i in range(2)]
    return np[0], np[1]


def count_in_quadrants(positions, grid):
    width, height = grid
    quadrants = [0, 0, 0, 0]
    for x, y in positions:
        if x == width//2 or y == height //2:
            continue
        if x < width //2 and y < height//2:
            quadrants[0] +=1
        elif x > width //2 and y < height //2:
            quadrants[1] += 1
        elif x < width //2 and y > height //2:
            quadrants[2] += 1
        else:
            quadrants[3] +=1
    
    return quadrants


if __name__ == "__main__":
    input= read_input("2024/14_input.txt")
    grid_size = (101, 103)
    n_seconds = 100
    new_positions = []
    for x, y, vx, vy in input:
        new_pos = calc_position((x,y), (vx,vy), grid_size, n_seconds)
        new_positions.append(new_pos)
    
    quadrants = count_in_quadrants(new_positions, grid_size)
    print("Part 1: ", prod(quadrants))


