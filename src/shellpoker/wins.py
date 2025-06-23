from dataclasses import dataclass
from shellpoker.card import Card
from collections import defaultdict
from typing import Optional

@dataclass
class Win:
    name: str
    factor: int

class WinType:
    factor: int
    def check(self, _: "Wins") -> bool:
        pass

class RoyalFlush(WinType):
    factor = 20
    def check(self, wins: "Wins") -> bool:
        return (
            len(wins.suits) == 1 and
            wins.ranks == [10, 11, 12, 13, 14]
        )

class StraightFlush(WinType):
    factor = 15
    def check(self, wins: "Wins") -> bool:
        return len(wins.suits) == 1 and wins.is_straight

class FourOfAKind(WinType):
    factor = 10
    def check(self, wins: "Wins") -> bool:
        return 4 in wins.rank_counts.values()

class FullHouse(WinType):
    factor = 8
    def check(self, wins: "Wins") -> bool:
        return sorted(wins.rank_counts.values()) == [2, 3]

class Flush(WinType):
    factor = 6
    def check(self, wins: "Wins") -> bool:
        return len(wins.suits) == 1

class Straight(WinType):
    factor = 5
    def check(self, wins: "Wins") -> bool:
        return wins.is_straight and len(wins.suits) > 1

class ThreeOfAKind(WinType):
    factor = 4
    def check(self, wins: "Wins") -> bool:
        return 3 in wins.rank_counts.values() and len(wins.rank_counts) > 2

class TwoPairs(WinType):
    factor = 2
    def check(self, wins: "Wins") -> bool:
        return list(wins.rank_counts.values()).count(2) == 2

class OnePair(WinType):
    factor = 1
    def check(self, wins: "Wins") -> bool:
        return 2 in wins.rank_counts.values() and len(wins.rank_counts) > 3

WIN_TYPES: dict[str, WinType] = {
    "Royal Flush": RoyalFlush(),
    "Straight Flush": StraightFlush(),
    "Four of a Kind": FourOfAKind(),
    "Full House": FullHouse(),
    "Flush": Flush(),
    "Straight": Straight(),
    "Three of a Kind": ThreeOfAKind(),
    "Two Pairs": TwoPairs(),
    "One Pair": OnePair(),
}

def render_win_list(bet: int):
    bet = max(bet, 1)
    return "\n".join(
        f"{name:<20} {factor * bet:<3} $"
        for name, factor in sorted(
            ((win_name, win.factor) for win_name, win in WIN_TYPES.items()),
            key=lambda x: x[1],
            reverse=True
        )
    )

class Wins:
    def __init__(self, hand: list['Card']):
        self.hand = hand
        self.rank_counts = defaultdict(int)
        for card in hand:
            self.rank_counts[card.rank.value] += 1
        self.suits = {card.suit for card in hand}
        self.ranks = sorted(card.rank.value for card in hand)
        self.is_straight = len(self.ranks) == 5 and (
            self.ranks == list(range(self.ranks[0], self.ranks[0] + 5)) or self.ranks == [2, 3, 4, 5, 14]
        )

    def get_best_win(self) -> Optional[Win]:
        for win_name, win_type in WIN_TYPES.items():
            if win_type.check(self):
                return Win(name=win_name, factor=win_type.factor)
        return Win(name=None, factor=0)
