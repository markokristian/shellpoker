import random

from shellpoker.card import Card, Rank, Suits

class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        ranks = [
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("J", 11),
            Rank("Q", 12),
            Rank("K", 13),
            Rank("A", 14),
        ]
        suits = [
            Suits.HEARTS,
            Suits.DIAMONDS,
            Suits.CLUBS,
            Suits.SPADES,
        ]
        return [
            Card(rank, suit)
            for rank in ranks
            for suit in suits
        ]

    def add_joker(self):
        self.cards.append(Card.create_joker())

    def shuffle(self):        
        random.shuffle(self.cards)
