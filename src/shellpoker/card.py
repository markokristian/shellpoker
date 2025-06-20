class Rank:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value

class Suit:
    def __init__(self, name: str, emoji: str) -> None:
        self.name = name
        self.emoji = emoji

class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.rank.name}{self.suit.emoji}"
