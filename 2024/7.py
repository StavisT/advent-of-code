
import itertools

def read_input(f = "2024/7_input.txt"):
    d= {}
    for line in open(f).read().splitlines():
        i, j = line.split(": ")
        d[int(i)] = list(map(int, j.split()))
    return d

def generate_combinations(c, n):
    return list(itertools.product(range(c), repeat=n))


def calc_operation(nums, comb):
    s = nums[0]
    for i, n in enumerate(nums[1:]):
        if comb[i]==0: # + operator
            s+=n
        elif comb[i]==1: # * operator
            s*=n
        else:  # || operator
            s= int(str(s) + str(n))
    return s


def is_valid_calculation(total, elements, c=2):
    sum_prod_comb = generate_combinations(c, len(elements)-1)
    for comb in sum_prod_comb:
        test = calc_operation(elements, comb)
        if test == total:
            return total 
    return 0

if __name__ == "__main__":
    input = read_input()
    print("P1: ",sum((is_valid_calculation(i, j) for i, j in input.items())))
    print("P2: ", sum((is_valid_calculation(i, j, 3) for i, j in input.items())))