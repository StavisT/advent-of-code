def read_input(file="2024/24_calibration.txt"):
    _register, _connections = open(file).read().split("\n\n")
    register = {}
    connections = {}

    for line in _register.splitlines():
        val = line.split(": ")
        register[val[0]] = int(val[1])
    
    for line in _connections.splitlines():
        val = line.split(" ")
        left = val[0]
        operation = val[1]
        right = val[2]
        out = val[-1]
        connections[out] = (operation, left, right)

    return register, connections

def calc_operation(operation: str, left, right):
    if operation == "AND":
        return int(left and right)
    elif operation == "OR":
        return int(left or right)
    else:
        return int(int(left) ^ int(right))
    
def get_z_key_bin(register):
    z_keys = [k for k in register if k.startswith("z")]
    z_keys.sort()
    print(z_keys)
    z_bin_number = [str(register[k]) for k in z_keys][::-1]
    z_bin_number = "".join(z_bin_number)
    return z_bin_number


def part1(register, connections):
    remaining = list(connections.keys())

    while remaining:
        for output, input in connections.items():
            operation, left, right = input
            if output in register:
                continue
            if left in register and right in register:
                register[output] = calc_operation(operation, register[left], register[right])
                remaining.remove(output)
    
    return get_z_key_bin(register)



if __name__ == "__main__":
    register, connections = read_input("2024/24_input.txt")
    bin_number = part1(register, connections)
    print(bin_number)
    print(int(bin_number, 2))
    

