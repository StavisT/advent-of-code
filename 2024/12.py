from collections import deque
from dataclasses import dataclass

Coordinate = tuple[int, int]
DIRECTIONS = {"right": (0,1), "down":(-1,0),"left":(0,1), "up": (1,0) }
SURROUNDING_COORDS = ((-1,0), (1,0), (0, 1), (0,-1))
Adjacent = Coordinate
Diagonal = Coordinate
Vertice = tuple[Adjacent, Adjacent, Diagonal]

TOP_LEFT: Vertice = ((-1, 0), (0, -1), (-1, -1))
TOP_RGHT: Vertice = ((1, 0), (0, -1), (1, -1))
BTM_LEFT: Vertice = ((-1, 0), (0, 1), (-1, 1))
BTM_RGHT: Vertice = ((1, 0), (0, 1), (1, 1))


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return coord1[0] + coord2[0], coord1[1] + coord2[1]


def surrounding_coords(coord: Coordinate, surrounding: tuple[Coordinate] =SURROUNDING_COORDS) -> list[Coordinate]:
    sur_cor = []
    for c in surrounding:
        sur_cor.append(add_coordinates(coord, c))
    return sur_cor


class Queue:
    def __init__(self):
        self.elements = deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: int):
        self.elements.append(x)
    
    def get(self) -> int:
        return self.elements.popleft()
    

class Grid:
    def __init__(self, grid: dict[Coordinate, int]):
        self.grid=grid
    
    def neighbours(self, coord: Coordinate):
        coords = []
        val = self.grid[coord]
        sur_cors =surrounding_coords(coord)
        for sc in sur_cors:
            if sc in self.grid and self.grid[sc] == val:
                coords.append(sc)
        
        return coords

    def is_neighbours(self, coord, options: tuple[Coordinate]) -> list[int]:
        val = self.grid[coord]
        sur_cors = surrounding_coords(coord, options)
        return [1 if c in self.grid and self.grid.get(c) == val else 0 for c in sur_cors]
        
    def get(self, coord: Coordinate)-> int:
        return self.grid[coord]


@dataclass
class Region:
    letter: str
    area: int
    perimeter: int
    sides: int

    @property
    def cost(self) -> int:
        return self.area * self.perimeter

    @property
    def discounted_cost(self) -> int:
        return self.area * self.sides


def read_input(file= "2024/12_calibration.txt"):
    return open(file).read()


def create_grid(input: list[str]) -> Grid:
    grid= {}
    for i, line in enumerate(input):
        for j, val in enumerate(line):
            grid[(i,j)] = val
    return Grid(grid)


def find_sub_grid(grid, start) -> set[Coordinate]:
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

    return reached


def calc_perimeter(grid: Grid, coordinates: set[Coordinate]):
    perimeter = 0
    for c in coordinates:
        n_neighbours = len(grid.neighbours(c))
        perimeter += 4-n_neighbours
    return perimeter


def calc_corner(grid: Grid, coord: Coordinate) -> int:
    corners = 0
    for vert in (TOP_LEFT, TOP_RGHT, BTM_LEFT, BTM_RGHT):
        ns = grid.is_neighbours(coord,vert)
        corners += sum(ns[:2]) == 2 and ns[2] == 0  # diagonal is different, and has adjacent -> Is inner corner
        corners += sum(ns[:2]) == 0  # nothing adjacent. -> Is outer corner

    return corners


def calc_corners(grid: Grid, coordinates: list[Coordinate]):
    corners =0
    if len(coordinates) in [1,2]:
        return 4

    for c in coordinates:
        corners += calc_corner(grid, c)
    return corners


if __name__ == "__main__":
    input = read_input("2024/12_input.txt")
    grid = create_grid(input.splitlines())
    remaining_grid = set(grid.grid.keys())

    cost = 0
    discounted_cost = 0
    while len(remaining_grid) > 0:
        next_coord = remaining_grid.pop()
        sub_grid = find_sub_grid(grid, next_coord)
        area = len(sub_grid)
        perimeter = calc_perimeter(grid, sub_grid)
        sides = calc_corners(grid, list(sub_grid))
        res = Region(grid.get(next_coord), area=area, perimeter=perimeter, sides=sides)
        cost +=  res.cost
        discounted_cost += res.discounted_cost
        print(res)
        for c in sub_grid:
            if c in remaining_grid:
                remaining_grid.remove(c)
        
    print("Part 1: ", cost)
    print("Part 2:", discounted_cost)