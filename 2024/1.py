from collections import defaultdict


def read_input_p1():
    l1 = []
    l2 = []
    with open('2024/1_input.txt') as f:
        for line in f.readlines():
            i, j = line.split()
            l1.append(int(i))
            l2.append(int(j))
    return l1, l2

def read_input_p2():
    l1 = []
    l2 = defaultdict(lambda:0)
    with open('2024/1_input.txt') as f:
        for line in f.readlines():
            i, j = line.split()
            l1.append(int(i))
            num2 = int(j)
            l2[num2] += 1
    return l1, l2


# part 1:
def main_p1():
    l1, l2 = read_input_p1()
    l1 .sort()
    l2.sort()
    diff = [abs(i - j) for i , j in zip(l1,l2)]
    print(sum(diff))


# part 2
def main_p2():
    l1, l2 = read_input_p2()
    s = 0
    for i in l1:
        s += i * l2[i]
    print(s) 


if __name__ == "__main__":
    main_p1()
    main_p2()