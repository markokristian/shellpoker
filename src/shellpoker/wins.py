from dataclasses import dataclass
from shellpoker.card import Card
from collections import defaultdict
from typing import Optional

@dataclass
class Win:
    name: str
    factor: int

class WinType:
    name: str
    factor: int
    def check(self, _: "Wins") -> bool:
        pass

class RoyalFlush(WinType):
    name = "Royal Flush"
    factor = 20
    def check(self, wins: "Wins") -> bool:
        needed = {10, 11, 12, 13, 14}
        present = set(wins.ranks_no_joker)
        missing = needed - present
        return (
            len(wins.suits_no_joker) == 1 and
            len(missing) <= wins.joker_count and
            len(wins.ranks_no_joker) + wins.joker_count == 5
        )

class StraightFlush(WinType):
    name = "Straight Flush"
    factor = 15
    def check(self, wins: "Wins") -> bool:
        return wins.is_straight_flush_with_joker

class FourOfAKind(WinType):
    name = "Four of a Kind"
    factor = 10
    def check(self, wins: "Wins") -> bool:
        for rank, count in wins.rank_counts_no_joker.items():
            if count + wins.joker_count >= 4:
                return True
        return False

class FullHouse(WinType):
    name = "Full House"
    factor = 8
    def check(self, wins: "Wins") -> bool:
        counts = list(wins.rank_counts_no_joker.values())
        counts.sort(reverse=True)
        jokers = wins.joker_count
        if len(counts) == 2:
            if counts[0] + counts[1] + jokers >= 5 and counts[0] >= 2 and counts[1] >= 2:
                return True
        if len(counts) == 1 and counts[0] + jokers >= 5:
            return True
        if len(counts) == 3:
            if 2 in counts and counts.count(2) == 2 and jokers >= 1:
                return True
        return False

class Flush(WinType):
    name = "Flush"
    factor = 6
    def check(self, wins: "Wins") -> bool:
        return len(wins.suits_no_joker) == 1 and len(wins.ranks_no_joker) + wins.joker_count == 5

class Straight(WinType):
    name = "Straight"
    factor = 5
    def check(self, wins: "Wins") -> bool:
        return wins.is_straight_with_joker

class ThreeOfAKind(WinType):
    name = "Three of a Kind"
    factor = 4
    def check(self, wins: "Wins") -> bool:
        for rank, count in wins.rank_counts_no_joker.items():
            if count + wins.joker_count >= 3:
                return True
        return False

class TwoPairs(WinType):
    name = "Two Pairs"
    factor = 2
    def check(self, wins: "Wins") -> bool:
        pairs = [count for count in wins.rank_counts_no_joker.values() if count == 2]
        singles = [count for count in wins.rank_counts_no_joker.values() if count == 1]
        jokers = wins.joker_count
        if len(pairs) == 2:
            return True
        if len(pairs) == 1 and len(singles) >= 1 and jokers >= 1:
            return True
        if len(pairs) == 0 and len(singles) >= 2 and jokers >= 2:
            return True
        return False

class OnePair(WinType):
    name = "One Pair"
    factor = 1
    def check(self, wins: "Wins") -> bool:
        for rank, count in wins.rank_counts_no_joker.items():
            if count + wins.joker_count >= 2:
                return True
        return wins.joker_count >= 2

WIN_TYPES = [
    RoyalFlush(),
    StraightFlush(),
    FourOfAKind(),
    FullHouse(),
    Flush(),
    Straight(),
    ThreeOfAKind(),
    TwoPairs(),
    OnePair(),
]

def render_win_list(bet: int, jokers: int):
    bet = max(bet, 1)
    joker_info = f" (Jokers in deck: {jokers})" if jokers > 0 else ""
    header = f"Possible Wins for Bet {bet}{joker_info}:\n"
    win_lines = [
        f"{win_type.name:<20} {win_type.factor * bet:<3} $"
        for win_type in sorted(WIN_TYPES, key=lambda w: w.factor, reverse=True)
    ]
    return header + "\n".join(win_lines)

class Wins:
    def __init__(self, hand: list['Card']):
        self.hand = hand
        self.joker_count = sum(1 for card in hand if card.is_joker())
        self.non_joker_cards = [card for card in hand if not card.is_joker()]
        self.rank_counts_no_joker = defaultdict(int)
        for card in self.non_joker_cards:
            self.rank_counts_no_joker[card.rank.value] += 1
        self.suits_no_joker = {card.suit for card in self.non_joker_cards}
        self.ranks_no_joker = sorted(card.rank.value for card in self.non_joker_cards)
        self.is_straight_with_joker = self._is_straight_with_joker()
        self.is_straight_flush_with_joker = self._is_straight_flush_with_joker()

    def _is_straight_with_joker(self) -> bool:
        if not self.ranks_no_joker:
            return False
        ranks = self.ranks_no_joker
        jokers = self.joker_count
        needed = 5 - len(ranks)
        if needed > jokers:
            return False
        min_rank = min(ranks)
        max_rank = max(ranks)
        for start in range(min_rank - jokers, max_rank + 1):
            window = set(range(start, start + 5))
            missing = window - set(ranks)
            if len(missing) <= jokers:
                return True
        if set([14, 2, 3, 4, 5]).intersection(ranks) and len(set([14, 2, 3, 4, 5]) - set(ranks)) <= jokers:
            return True
        return False

    def _is_straight_flush_with_joker(self) -> bool:
        if len(self.suits_no_joker) > 1:
            return False
        return self.is_straight_with_joker

    def get_best_win(self) -> Optional[Win]:
        for win_type in WIN_TYPES:
            if win_type.check(self):
                return Win(name=win_type.name, factor=win_type.factor)
        return Win(name=None, factor=0)