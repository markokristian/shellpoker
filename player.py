from card import Card


MAX_CARDS_IN_HAND = 5

class Player:
    def __init__(self, name: str, money: int = 20):
        self.name = name
        self.hand = list()
        self.money = 20

    def clear_hand(self):
        self.hand.clear()

    def add_card(self, card: 'Card'):
        self.hand.append(card)

    def render_hand(self):
        return '  '.join(card.render() for card in self.hand)

    def n_missing_cards(self):
        return MAX_CARDS_IN_HAND - len(self.hand)
    
    def subtract_bet(self, bet: int):
        assert bet >= 0, "Amount to subtract must be non-negative"
        assert self.money >= bet, "Not enough money to subtract"
        self.money -= bet

    def can_afford(self, bet: int) -> bool:
        return self.money + bet >= bet
    