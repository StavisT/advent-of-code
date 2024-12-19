from functools import cache

def read_input(file="2024/19_calibration.txt"):
    input = open(file).read()
    towels, logos = input.split("\n\n")
    towels = towels.strip().split(", ")
    logos = logos.splitlines()
    return towels, logos

@cache
def can_towels_create_design(towels: tuple[str], design: str) -> bool:
    if len(design) == 0:
        return 1
    return sum(can_towels_create_design(towels, design[len(t):]) for t in towels if design.startswith(t))


if __name__ == "__main__":
    towels, designs = read_input("2024/19_input.txt")
    print("Part 1: ", sum([1 for d in designs if can_towels_create_design(tuple(towels), d)]))
    print("Part 2: ", sum([can_towels_create_design(tuple(towels), d) for d in designs]))

