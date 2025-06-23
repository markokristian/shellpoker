from shellpoker.wins import Wins
from shellpoker.card import Card, Rank, Suit

def test_straight():
    hand = [
        Card(Rank("10", 10), Suit("Hearts", "♥️")),
        Card(Rank("J", 11), Suit("Spades", "♠️")),
        Card(Rank("Q", 12), Suit("Hearts", "♥️")),
        Card(Rank("K", 13), Suit("Hearts", "♥️")),
        Card(Rank("A", 14), Suit("Hearts", "♥️"))
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == "Straight"

def test_straight_low_ace():
    hand = [
        Card(Rank("A", 14), Suit("Hearts", "♥️")),
        Card(Rank("2", 2), Suit("Spades", "♠️")),
        Card(Rank("3", 3), Suit("Hearts", "♥️")),
        Card(Rank("4", 4), Suit("Hearts", "♥️")),
        Card(Rank("5", 5), Suit("Hearts", "♥️"))
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == "Straight"
