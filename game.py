
from abc import ABC
import sys
from card import Card
from deck import Deck
from player import Player
from rich.console import Console

from wins import Win

class UserInput:
    def __init__(self, user_input: str):
        self.user_input = user_input.strip().replace(" ", "").lower()

    def is_quit(self):
        return self.user_input == 'q'

    def is_throw_hand(self):
        return self.user_input == 't'

    def is_keep_hand(self):
        return self.user_input == 'k'
    
    def is_increase_bet(self):
        return self.user_input == '+'

    def is_decrease_bet(self):
        return self.user_input == '-'

    def get_card_indices_strings(self):
        if ',' in self.user_input:
            return self.user_input.split(',')
        else:
            return [self.user_input]
        
    def get_card_indices(self) -> list[int]:
        # sorted so that we pick selected cards in order
        return sorted([int(i) for i in self.get_card_indices_strings()])

    def is_valid_input(self):
        if (
            self.is_keep_hand()
            or self.is_throw_hand()
            or self.is_increase_bet()
            or self.is_decrease_bet()
            or self.is_quit()
        ):
            return True

        return all(
            s.isdigit() and int(s) > 0 for s in self.get_card_indices_strings()
        )

class Game:
    def __init__(self):
        self.state = "initial"
        self.player = Player("Player 1")
        self.deck = None
        self.bet = 1
        # track last win and the amount won given the bet at that point
        self.last_win: tuple[Win, int] = (None, 0)

    def start(self):
        self.deck = Deck()  # reset the deck
        self.state = "running"
        self.deck.shuffle()

    def stop(self):
        self.state = "stopped"
        sys.exit(0)

    def reset(self):
        self.state = "initial"

    def render_hand(self):
        return self.player.render_hand()
    
    def render_status(self):
        if self.last_win is None:
            return f"Money: {self.player.money} $ | Bet: {self.bet} $"
        _, amount_won = self.last_win
        return f"Money: {self.player.money} $ | Bet: {self.bet} $ | Wins: {amount_won} $)"

    def deal_hand(self):
        self.player.subtract_bet(self.bet)
        self.player.clear_hand()
        self.fill_hand()

    def deal_one_card(self) -> Card:
        card = self.deck.cards.pop()
        self.player.clear_hand()
        self.player.add_card(card)
        return card

    def are_valid_indices(self, indices):
        "Note that the UI uses 1-based indexing for cards."
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
        from wins import Wins
        wins = Wins(self.player.hand)
        best_win = wins.get_best_win()
        # side effect: track the last win
        self.last_win = best_win, best_win.factor * self.bet
        return best_win.name, best_win.factor * self.bet
    
    def reimburse(self):
        self.player.money += self.bet

    def collect_wins(self):
        _, amount_won = self.last_win
        self.player.money += amount_won
        self.last_win = (None, 0)  # reset last win after collecting

    def increase_bet(self, amount: int):
        assert amount > 0
        self.bet += amount
        self.player.subtract_bet(amount)

    def decrease_bet(self, amount: int):
        assert amount > 0
        self.bet -= amount
        self.player.money += amount


class GameState(ABC):
    pass

class StateDoubleMiniGame(GameState):
    def __init__(self, game: Game, money_won: int, ui: Console = Console()):
        self.ui = ui
        self.game = game
        self.money_won = money_won

    def enter(self):
        ui, game = self.ui, self.game
        money_won = self.money_won
        money_won *= 2
        card_dealt: Card = game.deal_one_card()

        while True:
            ui.clear()
            ui.print(game.render_status())
            ui.print()
            ui.print("Low or High? (l/h)")
            ui.print("\n >> ", end="")

            lh_input = input().strip().lower()
            if lh_input == 'l':
                ui.clear()
                ui.print(game.render_status())
                ui.print(f"{game.player.render_hand()}")
                if card_dealt.rank.value < 8:
                    game.player.money += money_won
                    game.last_win = (Win("Double Win", 0), money_won)
                    ui.print(f"You guessed low, you win {money_won} $!")
                else:
                    game.last_win = (None, 0) # needs reset sigh
                    ui.print("You guessed low, you lose your wins!")
                break
            elif lh_input == 'h':
                ui.clear()
                ui.print(game.render_status())
                ui.print(f"{game.player.render_hand()}")
                if card_dealt.rank.value >= 8:
                    game.player.money += money_won
                    game.last_win = (Win("Double Win", 0), money_won)
                    ui.print(f"You guessed high, you win {money_won} $!")
                else:
                    game.last_win = (None, 0) # needs reset sigh
                    ui.print("You guessed high, you lose your wins!")
                break
            else:
                ui.print("Invalid input. Type 'l' for low (1-7) or 'h' for high (8-13).")
                ui.print("Press any key to try again...")
                ui.print("\n >> ", end="")
                input()

        ui.print("Press any key to try again...")
        ui.print("\n >> ", end="")
        input()
        return StateDealing(game, ui)

    def exit(self):
        pass

class StateDoubleCheck(GameState):
    def __init__(self, game: Game, money_won: int, ui: Console):
        self.ui = ui
        self.game = game
        self.money_won = money_won

    def enter(self):
        ui, game = self.ui, self.game
        ui.clear()
        ui.print(game.render_status())
        ui.print()
        ui.print("Do you want to double? (y/n)")
        ui.print("\n >> ", end="")
        double_input = input().strip().lower()
        if not double_input.startswith("y"):
            ui.clear()
            ui.print(game.render_status())
            ui.print()
            ui.print("You chose not to double.")
            ui.print("Press any key to continue...")
            ui.print("\n >> ", end="")
            input()
            return StateDealing(game, ui)
        else:
            return StateDoubleMiniGame(game, self.money_won, ui)
        
    def exit(self):
        pass

class StateWinCheck(GameState):
    def __init__(self, game: Game, ui: Console):
        self.ui = ui
        self.game = game

    def enter(self):
        ui, game = self.ui, self.game
        win_name, money_won = game.get_win()
        ui.clear()

        if win_name is None:
            ui.print(game.render_status())
            ui.print(f"Hand: {game.render_hand()}")
            ui.print()
            ui.print("No win this time. Better luck next time!")
            ui.print("Press any key to continue...")
            ui.print("\n >> ", end="")
            input()
            return StateDealing(game, ui)
        else:
            ui.print(game.render_status())
            ui.print(f"Hand: {game.render_hand()}\n")
            ui.print(f"Got [bold magenta]{win_name}[/bold magenta], won {money_won} $!")
            ui.print("Press any key to continue...")
            ui.print("\n >> ", end="")
            input()
            return StateDoubleCheck(game, money_won, ui)
        
    def exit(self):
        pass

class StateExited(GameState):
    def __init__(self, game: Game, ui: Console):
        self.game = game
        self.ui = ui

    def enter(self):
        ui, game = self.ui, self.game
        ui.clear()
        ui.print(f"You left with {game.player.money} $")
        ui.print("Thanks for playing!")
        game.stop()

    def exit(self):
        pass

class StateDealing(GameState):
    def __init__(self, game: Game, ui: Console):
        self.game: Game = game
        game.start()
        self.ui = ui

    def enter(self):
        ui, game = self.ui, self.game

        if not game.player.can_afford(game.bet):
            ui.clear()
            ui.print(game.render_status())
            ui.print()
            ui.print(f"You cannot afford the current bet of {game.bet} $.")
            ui.print("Decrease your bet or quit the game.")
            ui.print("Press any key to continue...")
            ui.print("\n >> ", end="")
            input()
            return StateDealing(game, ui)
    
        game.deal_hand()
        game.collect_wins()

        while True:
            ui.clear()
            ui.print(game.render_status())
            ui.print(f"Hand: {game.render_hand()}\n")
            ui.print("'1,3' to keep cards 1 and 3")
            ui.print("'t' to throw hand")
            ui.print("'k' to keep hand")
            ui.print("'+' to increase bet")
            ui.print("'-' to decrease bet")
            ui.print("'q' to quit")
            ui.print("\n >> ", end="")

            user_input = UserInput(input())
            if not user_input.is_valid_input():
                ui.clear()
                ui.print(game.render_status())
                ui.print(f"Hand: {game.render_hand()}\n")
                ui.print("Invalid input. Please try again.")
                ui.print("Press any key to continue...")
                ui.print("\n >> ", end="")
                input()
                continue

            if user_input.is_quit():
                return StateExited(self.game, self.ui)
            elif user_input.is_increase_bet():
                if game.player.can_afford(game.bet + 1):
                    game.increase_bet(1)
                else:
                    ui.print("You cannot afford to increase your bet.")
                    ui.print("Press any key to continue...")
                    ui.print("\n >> ", end="")
                    input()
                continue
            elif user_input.is_decrease_bet():
                if game.bet > 1:
                    game.decrease_bet(1)
                else:
                    ui.print("You cannot decrease your bet below 1 $.")
                    ui.print("Press any key to continue...")
                    ui.print("\n >> ", end="")
                    input()
                continue
            elif user_input.is_throw_hand():
                self.game.throw_hand()
                return StateWinCheck(self.game, self.ui)
            elif user_input.is_keep_hand():
                pass
                return StateWinCheck(self.game, self.ui)
            elif user_input.get_card_indices():
                indices = user_input.get_card_indices()
                if self.game.are_valid_indices(indices):
                    self.game.keep_selected_cards(indices)
                return StateWinCheck(self.game, self.ui)

    def exit(self):
        pass

def game_loop():
    ui = Console()
    game = Game()
    state: GameState = StateDealing(game, ui)
    while True:
        next_state = state.enter()
        state.exit()
        state = next_state


if __name__ == "__main__":
    game_loop()
