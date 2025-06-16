from dataclasses import dataclass
from shellpoker.card import Card
from collections import defaultdict

@dataclass
class Win:
    name: str
    factor: int

class Wins:
    def __init__(self, hand: list['Card']):
        self.hand = hand

        self.rank_counts = defaultdict(int)
        for card in hand:
            self.rank_counts[card.rank.value] += 1

        self.suits = {card.suit for card in hand}
        self.ranks = sorted(card.rank.value for card in hand)

        self.is_flush = len(self.suits) == 1
        self.is_straight = (len(self.ranks) == 5 and
                           self.ranks == list(range(self.ranks[0], self.ranks[0] + 5)))
        self.is_royal_flush = (self.is_flush and
                             self.ranks == [10, 11, 12, 13, 14])
        self.is_straight_flush = (self.is_flush and self.is_straight)
        self.is_four_of_a_kind = 4 in self.rank_counts.values()
        self.is_full_house = sorted(self.rank_counts.values()) == [2, 3]

        self.is_three_of_a_kind = 3 in self.rank_counts.values() and len(self.rank_counts) > 2

        self.is_two_pair = list(self.rank_counts.values()).count(2) == 2
        self.is_pair = 2 in self.rank_counts.values() and len(self.rank_counts) > 3

    def get_best_win(self) -> Win | None:
        if self.is_royal_flush:
            return Win("Royal Flush", 20)
        elif self.is_straight_flush:
            return Win("Straight Flush", 15)
        elif self.is_four_of_a_kind:
            return Win("Four of a Kind", 10)
        elif self.is_full_house:
            return Win("Full House", 8)
        elif self.is_flush:
            return Win("Flush", 6)
        elif self.is_straight:
            return Win("Straight", 5)
        elif self.is_three_of_a_kind:
            return Win("Three of a Kind", 4)
        elif self.is_two_pair:
            return Win("Two Pairs", 2)
        # elif self.is_pair:
        #     return Win("One Pair", 1)
        return Win(None, 0)
