def read_and_clean_input(filename = '2024/2_input.txt'):
    return [[*map(int, l.split())] for l in open(filename)]
    

def is_acceptable_diff(diffs):
    return all( 0 < d <= 3 for d in diffs)

def get_diffs(l):
    return [a - b for a,b in zip(l[1:], l[:-1])]

def is_safe(l):
    diffs = get_diffs(l)
    diffs_backwards = get_diffs(l[::-1])
    if is_acceptable_diff(diffs) or is_acceptable_diff(diffs_backwards):
        return True
    return False


def split_list(l):
    return [l[:i] + l[i+1:] for i in range(len(l))]


def is_safe_part2(l):
    for l_c in split_list(l):
        if is_safe(l_c):
            return True
    return False


def part_1(reports):
    count_reports = 0
    for l in reports:
        if is_safe(l):
            count_reports += 1
    print(count_reports)

def part_2(reports):
    count_reports = 0
    for l in reports:
        if is_safe(l):
            count_reports +=1
        else:
            if is_safe_part2(l):
                count_reports += 1
    
    print(count_reports)

        

if __name__ == "__main__":
    level_reports = read_and_clean_input()
    part_1(level_reports)
    part_2(level_reports)
