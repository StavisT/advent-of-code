from collections import defaultdict

input = [line.strip() for line in open("2024/4_input.txt")]
grid_map = defaultdict(str) | {(i,j):c for i,r in enumerate(input) for j,c in enumerate(r)}
grid_positions = list(grid_map.keys())
offsets = [-1,0,1]
pattern = list('XMAS'),  # tuple to compare below

s = 0
for i, j in grid_positions:
    for dj in offsets:
        for di in offsets:
            
            # search in all directions around i, j
            val = [grid_map[i+di*n, j+dj*n] for n in range(4)]

            if val in pattern:
                s += 1

print(s)

# Part 2:
# mas X mas
# go through and find the sub grids
def create_sub_grid(grid_map, i, j):
    rs = [i-1, i, i +1]
    
    cs = [j-1, j, j +1 ]
    sub_grid = []
    for r in rs:
        sub_grid.append([grid_map[r, c] for c in cs])
    return sub_grid


def check_sub_grid(sub_grid) -> bool:
    diag_1 = sub_grid[0][0] + sub_grid[1][1] + sub_grid[2][2]
    diag_2 = sub_grid[0][2] + sub_grid[1][1] + sub_grid[2][0]
    diag_1_valid = "MAS" in diag_1 or "SAM" in diag_1
    diag_2_valid = "MAS" in diag_2 or "SAM" in diag_2
    return diag_1_valid and diag_2_valid


N_r = len(input[0])
N_c = len(input)
s = 0
for i, j in grid_positions:
    if 0 < i < N_r and 0 < j < N_c:
        sub_grid = create_sub_grid(grid_map, i, j)
        if check_sub_grid(sub_grid):
            s += 1
print(s)