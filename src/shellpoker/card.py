from dataclasses import dataclass

JOKER_SYMBOL = "Jkr"

@dataclass(frozen=True)
class Rank:
    name: str
    value: int

@dataclass(frozen=True)
class Suit:
    name: str
    emoji: str

class Suits:
    HEARTS = Suit("Hearts", "♥")
    DIAMONDS = Suit("Diamonds", "♦")
    CLUBS = Suit("Clubs", "♣")
    SPADES = Suit("Spades", "♠")

@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __repr__(self) -> str:
        return f"{self.rank.name}{self.suit.emoji}"
    
    def is_joker(self) -> bool:
        return self.suit.emoji == JOKER_SYMBOL
    
    @staticmethod
    def create_joker() -> 'Card':
        return Card(Rank("", 0), Suit("", JOKER_SYMBOL))
