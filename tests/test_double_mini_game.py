import pytest
from shellpoker.card import Card, Rank, Suits
from shellpoker.game import Game, Player, StateDoubleMiniGame, StateDoubleCheck
from shellpoker.inputs import BetLowEvent, BetHighEvent

INITIAL_MONEY = 100

@pytest.fixture
def doubling_got_joker():
    return StateDoubleMiniGame(
        game=Game(Player("TestPlayer")),
        money_won=INITIAL_MONEY,
        card_dealt=Card.create_joker(),
    )

def test_joker_wins_low(doubling_got_joker: StateDoubleMiniGame):
    next_state = doubling_got_joker.on_event(BetLowEvent())
    assert isinstance(next_state, StateDoubleCheck)
    assert next_state.win_name == "Correct Low Guess"
    assert next_state.money_won == INITIAL_MONEY * 2

def test_joker_wins_high(doubling_got_joker: StateDoubleMiniGame):
    next_state = doubling_got_joker.on_event(BetHighEvent())
    assert isinstance(next_state, StateDoubleCheck)
    assert next_state.win_name == "Correct High Guess"
    assert next_state.money_won == INITIAL_MONEY * 2

def test_eight_loses_low():
    game = Game(Player("TestPlayer"))
    doubling = StateDoubleMiniGame(
        game=game,
        money_won=INITIAL_MONEY,
        card_dealt=Card(rank=Rank("8", 8), suit=Suits.HEARTS),
    )
    next_state = doubling.on_event(BetLowEvent())
    assert next_state.game.last_win == (None, 0)

def test_eight_loses_high():
    game = Game(Player("TestPlayer"))
    doubling = StateDoubleMiniGame(
        game=game,
        money_won=INITIAL_MONEY,
        card_dealt=Card(rank=Rank("8", 8), suit=Suits.HEARTS),
    )
    next_state = doubling.on_event(BetHighEvent())
    assert next_state.game.last_win == (None, 0)

