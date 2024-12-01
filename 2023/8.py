from math import lcm


def read_file(filename:str):
    with open(filename) as f:
        lines = f.readlines()

    instructions = lines[0].strip()
    nodes = {x[0]: (x[2].strip("(,"), x[3].strip(")")) for x in map(lambda x: x.split(), lines[2:])}
    return instructions, nodes


def instructions_to_binary(instructions: str) -> str:
    return "".join(["1" if x == "R" else "0" for x in instructions])


def count_nodes(nodes: dict, instructions: str, start_node: str, end_node: str) -> int:
    instructions = instructions*100
    cur_node = start_node
    i, counter = 0, 0
    while cur_node != end_node:
        if i >= len(instructions):
            i = 0
        cur_node = nodes[cur_node][int(instructions[i])]
        i += 1
        counter += 1

    return counter


def count_nodes_p2(nodes: dict, instructions: str, start_node) -> int:
    cur_node = start_node
    i, counter = 0, 0
    while not cur_node.endswith("Z"):
        if i >= len(instructions):
            i = 0
        cur_node = nodes[cur_node][int(instructions[i])]
        i += 1
        counter += 1

    return counter


if __name__ == "__main__":
    instrctions, nodes = read_file("des8.txt")
    binary_instructions = instructions_to_binary(instrctions)
    binary_instructions = binary_instructions
    # print(count_nodes(nodes, binary_instructions, "AAA", "ZZZ"))
    print("Part 1: ", count_nodes(nodes, binary_instructions, "AAA", "ZZZ"))

    start_nodes = [node for node in nodes if node.endswith("A")]
    p2_counts = []
    part2_lcm = 1
    for start_node in start_nodes:
        count = count_nodes_p2(nodes, binary_instructions, start_node)
        p2_counts.append(count)
        print(start_node, count)
        part2_lcm = lcm(part2_lcm, count)
    print("Part 2: ", part2_lcm)
