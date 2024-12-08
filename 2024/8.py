import re
from collections import defaultdict


Coordinate = tuple[int, int]

def read_input(f = "2024/8_input.txt"):
    d= {}
    for i, line in enumerate(open(f).read().splitlines()):
        for j, val in enumerate(line):
            d[i,j] = val
    return d

def is_alphanumeric(val: str) -> bool:
    v = re.search(r"(\d|[a-z]|[A-Z])", val)
    return v is not None

def subtract_coordinates(c1: Coordinate, c2: Coordinate):
    return c1[0] - c2[0], c1[1] - c2[1]

def add_coordinates(c1: Coordinate, c2: Coordinate):
    return c1[0]+  c2[0], c1[1] + c2[1]


def find_antinodes(c1: Coordinate, c2: Coordinate, grid, p2=False):
    diff_1 = subtract_coordinates(c1, c2)
    diff_2 = subtract_coordinates(c2,c1)
    antinodes = []
    for c, d in zip([c1,c2], [diff_1, diff_2]):
        temp_c = c
        for i in range(1000):
            temp_c = add_coordinates(temp_c,d)
            if temp_c in grid:
                antinodes.append(temp_c)
            else:
                break
            
            if not p2:
                # only a single loop
                break
            

    return antinodes


def find_all_antinodes(alphanumeric_coordinates, grid, p2 = False):
    antinodes = []
    for a, coords in alphanumeric_coordinates.items():
        if len(coords) == 1:
            continue
        for i, current_coord in enumerate(coords[:-1]):
            for other_coord in coords[i+1:]:
                a = find_antinodes(current_coord, other_coord, grid, p2)
                for _a in a:
                    antinodes.append(_a)
    return antinodes

def print_map(grid, antinodes, r=12, c = 12):
    m = grid
    for antinode in antinodes:
        m[antinode] = "#"

    for i in range(r):
        print("".join([m[i,j] for j in range(c)]))


if __name__ == "__main__":
    grid = read_input(f="2024/8_input.txt")
    alphanumeric_coordinates = defaultdict(list)
    for k, v in grid.items():
        if is_alphanumeric(v):
            alphanumeric_coordinates[v].append(k)
    
    antinodes = find_all_antinodes(alphanumeric_coordinates, grid)
    print("Part1: ", len(set(antinodes)))

    antinodes = find_all_antinodes(alphanumeric_coordinates, grid, True)
    all_alphanum_coords = [x for xs in alphanumeric_coordinates.values() for x in xs ]
    anti_and_alpha_num = antinodes + all_alphanum_coords
    print("Part 2: ", len(set(anti_and_alpha_num)))

    
                

