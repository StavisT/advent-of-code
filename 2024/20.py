from collections import deque

Coordinate = tuple[int, int]


class Grid:
    def __init__(self, grid: dict[Coordinate, str], height: int, width: int):
        self._grid = grid
        self.height = height
        self.width = width

    def get(self, coord: Coordinate) -> str:
        return self._grid.get(coord)

    def find_coord(self, val: str) -> Coordinate:
        for c, v in self._grid.items():
            if v == val:
                return c

    def in_bounds(self, coord: Coordinate) -> bool:
        return self.get(coord) is not None

    def neighbors(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        ns = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        return [n for n in ns if self.in_bounds(n)]


def read_and_process_input(file = "2024/20_calibration.txt") -> Grid:
    d = {}
    data = open(file).read().splitlines()
    H = len(data)
    W = len(data[0])
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            d[(i,j)]=val

    return Grid(d, H, W)


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
            if grid.get(next) == "#":
                continue
            if next not in distance:
                frontier.put(next)
                distance[next] = 1 + distance[current]
    
    return distance


def cheat_bfs(grid: Grid, start: Coordinate, order: dict[int, Coordinate], max_distance: int, min_time_saved: int):
        frontier = Queue()
        frontier.put(start)
        distance = dict()
        distance[start] = 0
        reached_targets = dict()

        while not frontier.empty():
            current = frontier.get()
            if distance[current] >= max_distance:
                continue

            for next in grid.neighbors(current):
                if next in distance:
                    continue
                
                distance[next] = distance[current] + 1
                frontier.put(next)

                if grid.get(next) != "#":
                    time_saved = order[next] - distance[next] - order[start]
                    if time_saved >= min_time_saved and next not in reached_targets:
                        reached_targets[next] = time_saved
        
        return len(list(reached_targets.keys()))


def calculate_time_saved_2(grid: Grid, distance: dict[int, Coordinate], min_time_saved: int, max_distance: int):
    return sum([cheat_bfs(grid, coord, distance, max_distance, min_time_saved) for coord in distance])


if __name__ == "__main__":
    file = "2024/20_input.txt"
    # file = "2024/20_calibration.txt"
    grid = read_and_process_input(file)
    start, goal = grid.find_coord("S"), grid.find_coord("E")
    distance = bfs(grid, start, goal)
    num_cheats_p1 = calculate_time_saved_2(grid, distance, 100, 2)
    print("Part 1: ", num_cheats_p1)
    
    num_cheats_p2 = calculate_time_saved_2(grid, distance, 100, 20)
    print("Part 2: ", num_cheats_p2)






        

# def calculate_time_saved(distance: dict[int, Coordinate], grid: Grid, min_time_saved: int):
#     time_saved = defaultdict(list)
#     for x in range(1,grid.width): # skip border
#         for y in range(1, grid.height):
#             val = grid.get((x,y))
#             if val == "#":
#                 # get neighbors
                
#                 ns = grid.neighbors_ns((x,y))
#                 ew = grid.neighbors_ew((x,y))
#                 if len(ns)>1 :
#                     c1, c2 = ns
#                     diff_ns = abs(distance[c1]- distance[c2])
#                     diff_ns -= 2
#                     if diff_ns > min_time_saved:
#                         time_saved[diff_ns].append((x,y,c1))

#                 if len(ew) > 1:                
#                     c3, c4 = ew
#                     diff_ew = abs(distance[c3]- distance[c4])
#                     diff_ew -= 2
#                     if diff_ew > min_time_saved:
#                         time_saved[diff_ew].append((x,y,c3))


#     return time_saved