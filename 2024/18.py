import re
import heapq

Coordinate = tuple[int, int]

def read_input(file = "2024/18_calibration.txt"):
    return [tuple(map(int, re.findall(r'\d+', line))) for line in open(file).read().splitlines()]


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, str]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: str, cost: float):
        heapq.heappush(self.elements, (cost, item))

    def get(self):
        return heapq.heappop(self.elements)

class Grid:
    def __init__(self, bounds: tuple[int, int], walls: list[Coordinate]):
        self.bounds = bounds
        self.walls = walls

    def is_in_grid(self, coord: Coordinate):
        x, y = coord
        if 0 <= x <= self.bounds[0] and 0 <= y <= self.bounds[1]:
            return True
        return False

    def is_available(self, coord: Coordinate) -> bool:
        if self.is_in_grid(coord) and coord not in self.walls:
            return True
        return False


    def neighbors(self, curr: Coordinate) -> list[Coordinate]:
        x, y = curr
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        return [n for n in neighbors if self.is_available(n)]


def djikstra(grid, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cost_so_far = dict()
    cost_so_far[start] = 0

    while not frontier.empty():
        cur_cost, cur_coord = frontier.get()

        if cur_coord == goal:
            break
        
        for next in grid.neighbors(cur_coord):
            new_cost = cur_cost + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
    
    return cost_so_far

def search_for_byte_breaking_path(bounds, all_walls):
    start = (0,0)
    goal = bounds
    reached_goal = []
    not_reached_goal = []
    cur_idx = 1024
    step_size = 254
    while True:
        cur_idx += step_size
        grid = Grid(bounds=bounds, walls= all_walls[:cur_idx])
        cost_so_far = djikstra(grid, start, goal)
        if goal in cost_so_far:
            reached_goal.append(cur_idx)
            if step_size < 0:
                step_size = max(-1 * int(step_size/2),1)
        else:
            if (cur_idx-1) in reached_goal:
                break
            not_reached_goal.append(cur_idx)
            if step_size > 0:
                step_size = min(int(-1 * step_size/2),-1)

    return all_walls[min(not_reached_goal) - 1]


if __name__ == "__main__":
    input = read_input("2024/18_input.txt")
    max_byte = 1024
    start = (0,0)
    goal = (70,70)
    grid = Grid(bounds=goal, walls=input[:max_byte])
    cost_so_far = djikstra(grid, start, goal)
    print("Part 1: ", cost_so_far[goal])
    print("Part 2: ", search_for_byte_breaking_path(goal, input))