Coordinate = tuple[int, int]
NORTH_SOUTH = [(1,0), (-1,0)]
EAST_WEST = [(0,1), (0,-1)]

def input_dimensions(file="2024/20_calibration.txt"):
    input = open(file).read().splitlines()
    return len(input), len(input[0])

def read_input(file = "2024/20_calibration.txt"):
    d = {}
    for i, line in enumerate(open(file).read().splitlines()):
        for j, val in enumerate(line):
            d[(i,j)]=val

    return d

# grid class
class Grid:

    def __init__(self, grid: dict[Coordinate, str]):
        self._grid = grid

    def get(self, coord: Coordinate) -> str:
        return self._grid.get(coord)

    def find_coord(self, val: str) -> Coordinate:
        for c, v in self._grid.items():
            if v == val:
                return c

    def is_available(self, coord: Coordinate) -> bool:
        val = self.get(coord)
        if val is None:
            return False
        if val == "#":
            return False
        return True
    
    def is_wall(self, coord: Coordinate) -> bool:
        return self.get(coord) == "#"

    def in_bounds(self, coord: Coordinate) -> bool:
        return self.get(coord) is not None

    # wall then available
    def neighbors2(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        ns = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        return [n for n in ns if self.in_bounds(n)]

    def neighbors(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        return [n for n in neighbors if self.is_available(n)]
    
    def well_neighbors(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        return [n for n in neighbors if self.is_wall(n)]
        
    
    def neighbors_ns(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        ns = [(x+1, y), (x-1, y)]
        return [n for n in ns if self.is_available(n)]
    
    def neighbors_ew(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        ns = [(x, y+1), (x, y-1)]
        return [n for n in ns if self.is_available(n)]
    

from collections import deque

class Queue:
    def __init__(self):
        self.elements = deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: int):
        self.elements.append(x)
    
    def get(self) -> int:
        return self.elements.popleft()
    
def bfs(grid: Grid, start: Coordinate, goal: Coordinate):
    frontier = Queue()
    frontier.put(start)
    distance = dict()
    distance[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next in grid.neighbors(current):
            if next not in distance:
                frontier.put(next)
                distance[next] = 1 + distance[current]
    
    return distance
from itertools import combinations
from collections import defaultdict

def calculate_time_saved(distance: dict[int, Coordinate], grid: Grid, h:int, w: int, min_time_saved: int):
    time_saved = defaultdict(list)
    for x in range(1,w): # skip border
        for y in range(1, h):
            val = grid.get((x,y))
            if val == "#":
                # get neighbors
                
                ns = grid.neighbors_ns((x,y))
                ew = grid.neighbors_ew((x,y))
                if len(ns)>1 :
                    c1, c2 = ns
                    diff_ns = abs(distance[c1]- distance[c2])
                    diff_ns -= 2
                    if diff_ns > min_time_saved:
                        time_saved[diff_ns].append((x,y,c1))

                if len(ew) > 1:                
                    c3, c4 = ew
                    diff_ew = abs(distance[c3]- distance[c4])
                    diff_ew -= 2
                    if diff_ew > min_time_saved:
                        time_saved[diff_ew].append((x,y,c3))


    return time_saved

def cheat_bfs(grid: Grid, start: Coordinate, order: dict[int, Coordinate], max_distance: int, min_time_saved: int):
        frontier = Queue()
        frontier.put(start)
        time_at_start = order[start]
        distance = dict()
        distance[start] = 0
        targets = dict()
        # targets_2 = 0

        while not frontier.empty():
            current = frontier.get()
            if distance[current] >= max_distance: # stop expanding when limit reached
                continue

            for next in grid.neighbors2(current):
                if next in distance:
                    continue
                
                new_dist = distance[current] + 1
                distance[next] = new_dist
                frontier.put(next)

                if grid.get(next) != "#":
                    time_at_goal = order[next]
                    time_saved = time_at_goal - new_dist - time_at_start
                    if time_saved < min_time_saved:
                        continue

                    if next in targets:
                        existing_distance = targets[next]
                        targets[next] = max(existing_distance, time_saved)
                    else:
                        targets[next] = time_saved
                        # targets_2 += 1

        
        return targets


def calculate_time_saved_2(grid: Grid, distance: dict[int, Coordinate], min_time_saved: int):
    time_saved = defaultdict(lambda : 0)
    counter = 0

    for coord in distance:
        # do a bfs to find all cheats from that coord
        t = cheat_bfs(grid, coord, distance, 20, min_time_saved)
        # counter += t2
        for _, ts in t.items():
            time_saved[ts] += 1# .append((coord, c))

    return time_saved

if __name__ == "__main__":
    file = "2024/20_input.txt"
    # file = "2024/20_calibration.txt"
    input = read_input(file)
    h, w = input_dimensions(file)
    grid= Grid(input)
    start = grid.find_coord("S")
    goal=grid.find_coord("E")
    distance = bfs(grid, start, goal)
    distance_to_coord = {v:k for k,v in distance.items()}
    time_saved = calculate_time_saved(distance, grid,h,w,99)
    # print(time_saved)
    num_cheats = 0
    for p_sec_saved, n_coord in time_saved.items():
        num_cheats += len(n_coord)
    print(num_cheats)

    time_saved_2 = calculate_time_saved_2(grid, distance, 100)
    num_cheats = 0
    for p_sec_saved, n_coord in time_saved_2.items():
        num_cheats += n_coord
    print(num_cheats)






        
