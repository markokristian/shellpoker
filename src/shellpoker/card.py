class Rank:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

class Suit:
    def __init__(self, name: str, emoji: str):
        self.name = name
        self.emoji = emoji

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def render(self):
        return f"{self.rank.name}{self.suit.emoji}"

    def __repr__(self):
        return f"{self.rank.name}{self.suit.emoji}"
