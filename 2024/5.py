# read and clean input
from collections import defaultdict

def read_and_clean_input(file="2024/5_input.txt"):
    raw_page_order, raw_updates = open(file).read().split("\n\n")
    
    page_order = defaultdict(list)
    for line in raw_page_order.splitlines():
        x, y = tuple(map(int,line.split("|")))
        page_order[x].append(y)

    updates = []
    for line in raw_updates.splitlines():
        updates.append(tuple(map(int, line.split(","))))
    
    return page_order, updates


def verify_page_order(pages, p_order) -> bool:
    for i, page in enumerate(pages):
        for p in pages[i:]:
            if page in p_order[p]:
                return False

    return True


def get_middle_page(pages):
    middle = int(round((len(pages) -1) / 2 ,0) )
    return pages[middle]


def order_pages(pages, page_order):
    new_order = []
    for p in pages:
        if verify_page_order(new_order + [p], page_order):
            new_order.append(p)
        else:

            for i in range(1, len(new_order)+1):
                # j = N - i -1
                test_order = new_order[:-i] + [p] + new_order[-i:]
                if verify_page_order(test_order, page_order):
                    break
            
            new_order = test_order

    return new_order

           
if __name__ == "__main__":
    page_order, updates = read_and_clean_input()
    correct_updates = [u for u in updates if verify_page_order(u, page_order)]
    print("Part 1: ", sum(map(get_middle_page, correct_updates)))

    not_correct_updates = [u for u in updates if not verify_page_order(u, page_order)]
    reordered_updates = [order_pages(u, page_order) for u in not_correct_updates]
    print("Part 2: ", sum(map(get_middle_page, reordered_updates)))


