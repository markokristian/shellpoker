from shellpoker.wins import Wins
from shellpoker.card import Card, Rank, Suits
from shellpoker.wins import Straight, TwoPairs, ThreeOfAKind

def test_straight():
    hand = [
        Card(Rank("10", 10), Suits.HEARTS),
        Card(Rank("J", 11), Suits.SPADES),
        Card(Rank("Q", 12), Suits.HEARTS),
        Card(Rank("K", 13), Suits.HEARTS),
        Card(Rank("A", 14), Suits.HEARTS)
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == Straight.name

def test_straight_low_ace():
    hand = [
        Card(Rank("A", 14), Suits.HEARTS),
        Card(Rank("2", 2), Suits.SPADES),
        Card(Rank("3", 3), Suits.HEARTS),
        Card(Rank("4", 4), Suits.HEARTS),
        Card(Rank("5", 5), Suits.HEARTS)
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == Straight.name

def test_straight_with_joker():
    hand = [
        Card(Rank("10", 10), Suits.HEARTS),
        Card(Rank("J", 11), Suits.SPADES),
        Card(Rank("Q", 12), Suits.HEARTS),
        Card(Rank("K", 13), Suits.HEARTS),
        Card.create_joker()
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == Straight.name

def test_two_pairs_with_joker():
    hand = [
        Card(Rank("6", 6), Suits.HEARTS),
        Card(Rank("10", 10), Suits.SPADES),
        Card(Rank("K", 13), Suits.HEARTS),
        Card(Rank("K", 13), Suits.DIAMONDS),
        Card.create_joker()
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == ThreeOfAKind.name
    assert TwoPairs().check(wins)

def test_straight_is_better_than_three_of_a_kind():
    hand = [
        Card(Rank("10", 10), Suits.SPADES),
        Card(Rank("J", 11), Suits.HEARTS),
        Card(Rank("D", 12), Suits.HEARTS),
        Card.create_joker(),
        Card.create_joker()
    ]

    wins = Wins(hand)
    assert wins.get_best_win().name == Straight.name
