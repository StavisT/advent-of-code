from copy import deepcopy
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
Coordinate = tuple[int, int]
UP_DOWN = "|"
LEFT_RIGHT = "-"
ALL = "+"
OBSTACLE = "O"
direction_to_trace = {UP: UP_DOWN, DOWN: UP_DOWN, LEFT: LEFT_RIGHT, RIGHT: LEFT_RIGHT}

movement = {UP: (-1,0), DOWN: (1,0), LEFT: (0, -1), RIGHT:(0,1)}
turn_movement ={UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

def add_coordinates(coord_1: Coordinate, coord_2: Coordinate):
    return coord_1[0] + coord_2[0], coord_1[1] + coord_2[1]

def get_new_trace(existing_trace: str ,direction: str):
    new_trace = direction_to_trace[direction]
    # 
    if existing_trace == ALL:
        return ALL
    elif existing_trace not in [UP_DOWN, LEFT_RIGHT]:
        return new_trace
    elif existing_trace != new_trace:
        return ALL
    else:
        return new_trace
        
from collections import defaultdict

class Grid:
    def __init__(self, grid_list, start: Coordinate):
        self._grid = grid_list
        self.guard = start
        self.obstacles = []
        self.touched_obstacles = []
        self._temp_obstacle = None
        self._temp_obstacle_val = None
        self.is_looping = False
        self.loops = 0
        self.guard_replaced = None
        self.traversed_coord = defaultdict(list)
    
    def get(self, coord: Coordinate):
        r, c = coord
        return self._grid[r][c]
    
    def set_value(self,coord: Coordinate, val: str):
        r, c = coord
        self._grid[r][c] = val
    
    def print_grid(self):
        for l in self._grid:
            print("".join(l))
        
        print()
    
    def is_in_grid(self, coord: Coordinate) -> bool:
        try:
            _ = self.get(coord)
            return True
        except IndexError as e:
            return False

    def is_obstacle(self, coord: Coordinate) -> bool:
        val = self.get(coord)
        return val == "#" or val == OBSTACLE

    def turn_90_deg(self):
        direction = self.get(self.guard)
        new_direction = turn_movement[direction]
        self.set_value(self.guard, new_direction)
    
    def get_next_coord(self):
        direction = self.get(self.guard)
        delta = movement[direction]
        new_coord = add_coordinates(self.guard, delta)
        return new_coord

    def move_guard_p1(self):
        direction = self.get(self.guard)
        delta = movement[direction]
        new_coord = add_coordinates(self.guard, delta)
        if not self.is_in_grid(new_coord):
            self.set_value(self.guard, "X")
            return False
        else:
            if self.is_obstacle(new_coord):
                # self.touched_obstacles.append(new_coord)
                # turn 90 deg
                self.turn_90_deg()
            else:
                self.set_value(self.guard, "X")
                self.set_value(new_coord, direction)
                self.guard = new_coord

        return True
    
    def add_obstacle(self, coord: Coordinate):
        prev_val = self.get(coord)
        self.set_value(coord, OBSTACLE)
        self._temp_obstacle = coord
        self.temp_obstacle_val = prev_val
    
    def remove_obstacle(self):
        ob_coord= self._temp_obstacle
        prev_value = self._temp_obstacle_val
        self.set_value(ob_coord, prev_value)


    def walk(self):
        in_grid = True
        
        while in_grid:
            in_grid = self.move()
            if self.is_looping:
                return 


    def move(self):
        next_coord = self.get_next_coord()
        direction = self.get(self.guard)
        if direction in self.traversed_coord[self.guard]:
            self.is_looping = True
        else:
            self.traversed_coord[self.guard].append(direction)

        if not self.is_in_grid(next_coord):
            return False
        
        if self.is_obstacle(next_coord):
                # turn 90 deg
            self.turn_90_deg()
        else:
            previous_trace = self.guard_replaced
            if previous_trace is None:
                previous_trace = "."
            new_trace = get_new_trace(previous_trace, direction)
            self.guard_replaced = self.get(next_coord)
            self.set_value(self.guard, new_trace)
            self.set_value(next_coord, direction)
            self.guard = next_coord
        return True


    def count_trace(self) -> int:
        c=0
        for line in self._grid:
            c += line.count("X")
        return c

def read_input(file = "2024/6_input.txt"):
    return [list(line) for line in open(file).read().splitlines()]

def get_start(grid):
    for i, line in enumerate(grid):
        if "^" in line:
            j = line.index("^")
            return i, j
    raise ValueError("Could not find start")


def traverse_grid(grid: Grid):
    
    in_grid = True
    while in_grid:
        in_grid = grid.move_guard_p1()
        
    print(grid.count_trace())

def place_obstacles(grid: Grid):
    in_grid = True
    while in_grid:
        # place obstacle in front of guard
        next_coord = grid.get_next_coord()
        if not grid.is_in_grid(next_coord):
            break
        elif grid.is_obstacle(next_coord):
            in_grid = grid.move()
        elif next_coord in grid.obstacles:
            in_grid = grid.move()
            continue
        _grid = deepcopy(grid._grid)
        
        looping_grid = Grid(_grid,grid.guard )
        # looping_grid = deepcopy(grid)
        looping_grid.add_obstacle(next_coord)
        looping_grid.walk()
        # should not count obstacle when going back
        if looping_grid.is_looping:
            looping_grid.print_grid()
            grid.obstacles.append(looping_grid._temp_obstacle)
        

        in_grid = grid.move()

    
    print(len(grid.obstacles))  # should be 1688
    print(len(set(grid.obstacles)))

# not removing obstacles correctly

if __name__ == "__main__":
    _grid = read_input("2024/6_input.txt")
    # _grid = read_input()
    start = get_start(_grid)
    grid = Grid(_grid, start)
    traverse_grid(grid)
    place_obstacles(grid)

