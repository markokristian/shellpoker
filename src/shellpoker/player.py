from shellpoker.card import Card
from shellpoker.card_widget import CardWidget, ObfuscatedCardWidget

MAX_CARDS_IN_HAND = 5

class Player:
    def __init__(self, name: str, money: int = 0):
        self.name = name
        self.hand = list[Card]()
        self.money = money

    def clear_hand(self):
        self.hand.clear()

    def add_card(self, card: 'Card'):
        self.hand.append(card)
    
    def render_card(self, card: Card, obfuscate: bool) -> CardWidget | ObfuscatedCardWidget:
        return CardWidget(card) if not obfuscate else ObfuscatedCardWidget(card)
    
    def render_hand(self, obfuscate: bool = False):
        return [self.render_card(card, obfuscate) for card in self.hand]

    def n_missing_cards(self):
        return MAX_CARDS_IN_HAND - len(self.hand)

    def subtract_bet(self, bet: int):
        assert bet >= 0, "Amount to subtract must be non-negative"
        assert self.money >= bet, "Not enough money to subtract"
        self.money -= bet

