calibration_text = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
calibration_text2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

import re

# setup
regex_pattern = r"mul\(\d{1,3},\d{1,3}\)"
input = "".join(l for l in open("2024/3_input.txt"))
mult_exprs = lambda x: re.findall(regex_pattern, x)
multiply = lambda x,y: x * y

part_1 = sum([multiply(*map(int, re.findall(r"(\d+)", expr))) for expr in mult_exprs(input)])
print("part 1: ", part_1)

# Part 2:
do_indexes = [m.end() for m in re.finditer(r"do\(\)", input)]
dont_indexes = [m.start() for m in re.finditer(r"don\'t\(\)", input)]

index_pairs = [] 
start = 0
get_do_idx = lambda min_idx: next((x for x in do_indexes if x > min_idx), None)
for dont_idx in dont_indexes:
    index_pairs.append((start, dont_idx))
    # find next start index
    start = get_do_idx(dont_idx)
index_pairs.append((start, len(input)))

input_2 = "".join(input[start:stop] for start, stop in index_pairs)
part_2 = sum([multiply(*map(int, re.findall(r"(\d+)", expr))) for expr in mult_exprs(input_2)])
print("Part 2: ", part_2)

