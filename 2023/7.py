from enum import Enum, auto
from collections import defaultdict


def read_input():
    res = []
    with open('des7.txt') as f:
        for line in f.readlines():
            hand, bid = line.split()
            res.append((hand, int(bid)))
    return res


class HandType(Enum):
    FIVE = auto()
    FOUR = auto()
    HOUSE = auto()
    THREE = auto()
    TWO_PAIR = auto()
    PAIR = auto()
    HIGH_CARD = auto()


def identify_hand_type(hand: str) -> HandType:
    d =defaultdict(int)
    for card in hand:
        d[card] += 1
        # how to count cards with J?

    if 5 in d.values():
        return HandType.FIVE
    elif 4 in d.values():
        return HandType.FOUR
    elif 3 in d.values() and 2 in d.values():
        return HandType.HOUSE
    elif 3 in d.values():
        return HandType.THREE
    elif list(d.values()).count(2) == 2:
        return HandType.TWO_PAIR
    elif 2 in d.values():
        return HandType.PAIR
    else:
        return HandType.HIGH_CARD

SORTING_ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
TRANSFORM = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
card_to_letter = {card: letter for card, letter in zip(SORTING_ORDER, TRANSFORM)}


def transform_hand(hand: str) -> str:
    return ''.join([card_to_letter[card] for card in hand])


def add_transform_hands(hands_and_bids: list) -> list:
    return [(hand, bid, transform_hand(hand)) for hand, bid in hands_and_bids]



if __name__ == "__main__":
    input = read_input()
    hands_with_transform = add_transform_hands(input)
    hands_per_type = {hand_type.value: [] for hand_type in HandType}

    for hand_and_bid in hands_with_transform:
        hand_type = identify_hand_type(hand_and_bid[0])
        hands_per_type[hand_type.value].append(hand_and_bid)

    top_rank = len(input)
    total = 0
    for hand_type, hands_and_bids in hands_per_type.items():
        only_hands = [alpha_hand for _, _, alpha_hand in hands_and_bids]
        ranks = {alpha_hand: top_rank - i for i, alpha_hand in enumerate(sorted(only_hands))}

        # sorted_hands = sorted(hands_and_bids, key=lambda x: sorted(x[2]), reverse=False)
        hand_type_total = sum([ranks[alpha_hand] * bid for _, bid, alpha_hand in hands_and_bids])

        total += hand_type_total
        top_rank = top_rank - len(only_hands)

    print(total)


    # did not do part 2
