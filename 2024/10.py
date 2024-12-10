from collections import deque

Coordinate = tuple[int, int]


class Queue:
    def __init__(self):
        self.elements = deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: int):
        self.elements.append(x)
    
    def get(self) -> int:
        return self.elements.popleft()

def read_input(file="2024/10_input.txt"):
    input = open(file).read().splitlines()
    grid = dict()
    for i, line in enumerate(input):
        for j, val in enumerate(line):
            grid[i, j] = int(val)
    return grid

def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return coord1[0] + coord2[0], coord1[1] + coord2[1]


def surrounding_coords(coord: Coordinate) -> list[Coordinate]:
    coords = [(-1,0), (1,0), (0, 1), (0,-1)]
    sur_cor = []
    for c in coords:
        sur_cor.append(add_coordinates(coord, c))
    return sur_cor


class Grid:
    def __init__(self, grid: dict[Coordinate, int]):
        self.grid=grid
    
    def neighbours(self, coord: Coordinate):
        coords = []
        val = self.grid[coord]
        pos_val = [val+1]
        sur_cors =surrounding_coords(coord)
        for sc in sur_cors:
            if sc in self.grid and self.grid[sc] in pos_val:
                coords.append(sc)
        
        return coords
            
    def get(self, coord: Coordinate)-> int:
        return self.grid[coord]


def find_paths(grid, start):
    frontier = Queue()
    frontier.put(start)
    reached: set[Coordinate] = set()
    reached.add(start)
    
    while not frontier.empty():
        current: Coordinate = frontier.get()
        for next in grid.neighbours(current):
            if next not in reached:
                frontier.put(next)
                reached.add(next)
    
    reached_values = [grid.get(r) for r in reached]

    return reached_values

def find_unique_trails(grid, start):
    frontier = Queue()
    frontier.put(start)
    unique_paths = 0
    
    while not frontier.empty():
        current: Coordinate = frontier.get()
        for next in grid.neighbours(current):
            frontier.put(next)
            if grid.get(next) == 9:
                unique_paths +=1
    

    return unique_paths


def main(grid):
    trailheads = {}
    tot_trails = 0
    for start in grid.grid:
        if grid.get(start) == 0:
            reached_vals = find_paths(grid, start)
            trailheads[start] = reached_vals.count(9)
            u_trails = find_unique_trails(grid, start)
            tot_trails += u_trails
    print("Part 1:", sum(peaks_from_trailhead for peaks_from_trailhead in trailheads.values()))
    print("Part 2:", tot_trails)
    

if __name__ == "__main__":
    _grid = read_input("2024/10_input.txt")
    grid = Grid(_grid)
    main(grid)
