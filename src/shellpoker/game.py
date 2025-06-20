from abc import ABC
import sys
from shellpoker.css import css
from shellpoker.card import Card
from shellpoker.deck import Deck
from shellpoker.inputs import (
    BetHighEvent,
    BetLowEvent,
    CancelEvent,
    ConfirmBetEvent,
    ConfirmEvent,
    DecreaseBetEvent,
    GameEvent,
    IncreaseBetEvent,
    KeepHandEvent,
    QuitEvent,
    SelectCardsEvent,
    ThrowHandEvent,
    parse_input,
)
from shellpoker.logger import create_logger
from shellpoker.player import Player

from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import Container
from textual.reactive import reactive

from shellpoker.wins import Win, Wins

log = create_logger()

class Config:
    MAX_BET = 5
    INITIAL_MONEY = 20

class Game:
    def __init__(self, player: Player):
        self.player = player
        self.obfuscate_hand = False  # whether to show the hand or not

    def start_new_game(self):
        log.info("Starting a new game.")
        self.deck = None
        self.bet = 1
        self.player.money = Config.INITIAL_MONEY
        # track last win and the amount won given the bet at that point
        self.last_win: tuple[Win, int] = (None, 0)

    def shuffle_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def stop(self):
        sys.exit(0)

    def render_hand(self):
        return self.player.render_hand(obfuscate=self.obfuscate_hand)

    def render_status(self):
        if self.last_win is None:
            return (f"Money: {self.player.money} $"
                    f"| Bet: {self.bet} $")

        _, amount_won = self.last_win
        return (f"Money: {self.player.money} $"
                f"| Bet: {self.bet} $ "
                f"| Wins: {amount_won} $")

    def deal_hand(self):
        self.player.clear_hand()
        self.fill_hand()

    def deal_one_card(self) -> Card:
        card = self.deck.cards.pop()
        self.player.clear_hand()
        self.player.add_card(card)
        return card

    def are_valid_indices(self, indices: list[int]) -> bool:
        return all(0 <= i - 1 < len(self.player.hand) for i in indices)

    def throw_hand(self):
        self.new_cards(keep=[])

    def keep_selected_cards(self, keep: list[int]):
        self.new_cards(keep=keep)

    def new_cards(self, keep: list):
        kept_cards = [self.player.hand[i - 1] for i in keep]
        self.player.hand = kept_cards
        self.fill_hand()

    def fill_hand(self):
        n_cards_to_deal = self.player.n_missing_cards()
        for _ in range(n_cards_to_deal):
            card = self.deck.cards.pop()
            self.player.add_card(card)

    def get_win(self):
        wins = Wins(self.player.hand)
        best_win = wins.get_best_win()
        # side effect: track the last win
        self.last_win = best_win, best_win.factor * self.bet
        return best_win.name, best_win.factor * self.bet

    def collect_wins(self):
        _, amount_won = self.last_win
        self.player.money += amount_won
        self.last_win = (None, 0)  # reset last win after collecting

    def can_afford_bet_increase_of(self, bet_increase: int) -> bool:
        return self.player.money >= bet_increase

    def increase_bet(self, amount: int):
        assert amount > 0
        self.bet += amount
        self.player.money -= amount

    def decrease_bet(self, amount: int):
        assert amount > 0
        self.bet -= amount
        self.player.money += amount


class GameState(ABC):
    def on_event(self, event: GameEvent):
        log.debug("Got an event in GameState %s: %s", self, event)
        match event:
            case QuitEvent():
                return StateExited(self.game)
            case _:
                log.debug("No transition for unknown event: %s", event)
                return self

class StateDoubleMiniGame(GameState):
    def __init__(self, game: Game, money_won: int):
        self.game = game
        self.money_won = money_won
        self.message = "Low or High?\n1-7 are low, 8-K are high\n(l/h)"
        self.card_dealt: Card = game.deal_one_card()
        game.obfuscate_hand = True  # Hide the hand in this state

    def on_event(self, event):
        game = self.game
        prize = self.money_won * 2
        card_dealt: Card = self.card_dealt

        if isinstance(event, (BetLowEvent, BetHighEvent)):
            game.obfuscate_hand = False  # Show the hand again when betting

        match event:
            case BetLowEvent():
                if card_dealt.rank.value < 8:
                    game.last_win = (Win("Double Win", 0), prize)
                    return StateDoubleCheck(game, "Correct Low Guess", prize)
                else:
                    game.last_win = (None, 0)
                    return LostDoubleMiniGame(game)
            case BetHighEvent():
                if card_dealt.rank.value >= 8:
                    game.last_win = (Win("Double Win", 0), prize)
                    return StateDoubleCheck(game, "Correct High Guess", prize)
                else:
                    return LostDoubleMiniGame(game)
            case _:
                return super().on_event(event)

class StateDoubleCheck(GameState):
    def __init__(self, game: Game, win_name: str, money_won: int):
        self.game = game
        self.money_won = money_won
        self.win_name = win_name
        self.message = f"{self.win_name}! You won {self.money_won} $!\nDo you want to double your winnings?\n(y/n)?"
       
    def on_event(self, event: GameEvent):
        game = self.game
        match event:
            case ConfirmEvent():
                return StateDoubleMiniGame(game, self.money_won)
            case CancelEvent():
                game.collect_wins()
                return StatePlaceBet(game)
            case _:
                return super().on_event(event)

class LostDoubleMiniGame(GameState):
    def __init__(self, game: Game):
        self.game = game
        game.last_win = (None, 0)
        self.previous_bet = game.bet
        self.game.bet = 0 # lost the bet
        self.message = "You guessed wrong :( Press Enter to continue..."
        self.game.obfuscate_hand = False  # Show the hand in this state

    def on_event(self, event: GameEvent):
        super().on_event(event)  # TODO decorator
        if self.game.player.money <= 0:
            return StateGameOver(self.game)
        self.game.bet = min(self.previous_bet, self.game.player.money)
        return StatePlaceBet(self.game)

class NoWinState(GameState):
    def __init__(self, game: Game):
        self.game = game
        self.previous_bet = game.bet
        self.game.bet = 0 # lost the bet
        self.message = "No win this time. Press Enter to continue..."

    def on_event(self, event: GameEvent):
        super().on_event(event)  # TODO decorator
        if self.game.player.money <= 0:
            return StateGameOver(self.game)
        self.game.bet = min(self.previous_bet, self.game.player.money)
        return StatePlaceBet(self.game)

class StateGameOver(GameState):
    def __init__(self, game: Game):
        self.game = game
        self.message = "Game over! You have no money left to play. \nPress q to quit or Enter to play again."

    def on_event(self, event: GameEvent):
        game = self.game
        match event:
            case QuitEvent():
                return StateExited(game)
            case _:
                game.start_new_game()
                return StatePlaceBet(game)

class StateExited(GameState):
    def __init__(self, game: Game):
        self.message = f"Thanks for playing! You left with {game.player.money} $"
        print(self.message)
        game.stop()

class StateDealing(GameState):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        game.shuffle_deck()
        game.deal_hand()
        self.message = "\n".join([
            "(t) to throw your hand",
            "(k) to keep your hand",
            "(124) to keep cards 1, 2 and 4"
        ])
 
    def on_event(self, event: GameEvent):
        super().on_event(event) # TODO decorator
        game = self.game

        if game.player.money <= 0 and game.bet == 0:
            return StateGameOver(game)

        match event:
            case ThrowHandEvent():
                log.info("Player chose to throw the hand.")
                game.throw_hand()
                game.deal_hand()
                return self.check_win()
            case KeepHandEvent():
                log.info("Player chose to keep the hand.")
                return self.check_win()
            case SelectCardsEvent():
                indices = event.indices
                log.info(f"Player chose to select cards: {indices}")
                if game.are_valid_indices(indices):
                    game.keep_selected_cards(indices)
                    return self.check_win()
            case _:
                return super().on_event(event)

        
    def check_win(self):
        game = self.game
        win_name, money_won = game.get_win()
        if win_name is None:
            return NoWinState(game)
        else:
            return StateDoubleCheck(game, win_name, money_won)

class StatePlaceBet(GameState):
    def __init__(self, game: Game):
        self.game = game
        game.shuffle_deck()
        game.deal_hand()
        game.player.subtract_bet(game.bet)
        self.game.obfuscate_hand = True
        self.message = (
            f"Place your bet (1-{Config.MAX_BET})\n"
            "(+) to increase\n"
            "(-) to decrease\n"
            "(d) to deal cards\n"
            "(q) to quit"
        )

    def on_event(self, event: GameEvent):
        super().on_event(event)  # TODO decorator
        game = self.game

        if game.player.money <= 0 and game.bet == 0:
            return StateGameOver(game)

        match event:
            case IncreaseBetEvent():
                if game.can_afford_bet_increase_of(bet_increase=1) and game.bet + 1 <= Config.MAX_BET:
                    game.increase_bet(1)
                return self
            case DecreaseBetEvent():
                if game.bet > 1:
                    game.decrease_bet(1)
                return self
            case ConfirmBetEvent():
                self.game.obfuscate_hand = False
                return StateDealing(game)
            case _:
                return self

class PokerApp(App):
    CSS = css()
    user_input = reactive("")

    def __init__(self, version: str):
        super().__init__()
        self.version = version
        self.game = Game(Player("Player 1", 0))
        self.game.start_new_game()
        self.state = StatePlaceBet(self.game)
        self.hand_container: Container | None = None
    
    def compose(self) -> ComposeResult:
        self.hand_container = Container(id="hand")
        yield Container(
            Container(
                Static("SHELL POKER", id="title"),
                Static(f"v{self.version}", id="version"),
                id="header"
            ),
            Static(self.game.render_status(), id="status"),
            self.hand_container,
            Static(self.state.message, id="message"),
            Input(placeholder="Enter to submit", id="action_input", max_length=5),
            id="container",
        )

    def on_mount(self):
        self.update_ui()

    def update_ui(self):
        status = self.game.render_status()
        message = self.state.message
        self.query_one("#status", Static).update(status)
        self.hand_container.remove_children()
        self.hand_container.mount(*self.game.render_hand())
        self.query_one("#message", Static).update(message)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        event = parse_input(event.value)
        log.debug("Parsed event: %s", event)
        log.debug("Current state: %s", self.state)
        self.state = self.state.on_event(event)
        self.game = self.state.game
        log.debug("New state: %s", self.state)
        self.query_one("#action_input", Input).value = ""
        self.update_ui()


def main(version: str):
    app = PokerApp(version)
    app.run()

if __name__ == "__main__":
    main()
