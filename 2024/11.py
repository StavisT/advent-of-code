stone_number_to_blinks = dict()


def split_in_two(num:str):
    n=len(num)
    i = int(n /2)
    x,y = num[:i], num[i:]
    y = str(int(y))  # trim leading zeros
    return [x,y]


def flatten_list(nums):
    updated = []
    for l in nums:
        if isinstance(l, list):
            updated += l
        else:
            updated.append(l)

    return updated


def multiply_w_2024(num):
    return str(int(num) * 2024)


def get_function(num: str):
    if num == "0":
        return lambda x: "1"
    elif len(num) % 2 ==0:
        #even
        return split_in_two
    else:
        return multiply_w_2024


def update_nums(nums):
    updated = []
    for n in nums:
        func = get_function(n)
        updated.append(func(n))
    
    return flatten_list(updated)


def blink(stone, n_blinks):
    if n_blinks == 0:
        return 1
    
    if (stone, n_blinks) in stone_number_to_blinks:
        return stone_number_to_blinks[(stone, n_blinks)]
    
    if stone == "0":
        size = blink("1", n_blinks-1)
    elif len(stone) % 2 ==0:
        left, right = split_in_two(stone)
        size = blink(left, n_blinks-1) + blink(right, n_blinks-1)
    else:
        size=blink(multiply_w_2024(stone), n_blinks-1)
    
    stone_number_to_blinks[(stone, n_blinks)] = size
    return size


if __name__ =="__main__":
    n_blinks = 25
    calibration = "125 17"
    input = "4 4841539 66 5279 49207 134 609568 0"

    # Part 1: Brute force
    nums = input.split(" ")
    for i in range(n_blinks):
        nums = update_nums(nums)
    print("Part 1: ", len(nums))

    # Part 2: hashmap + recursion
    tot_stones = 0
    stones = input.split(" ")
    for stone in stones:
        num_stones = blink(stone, 75)
        tot_stones += num_stones
    
    print("Part 2: ", tot_stones)
    
