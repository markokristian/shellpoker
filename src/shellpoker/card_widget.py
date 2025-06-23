from shellpoker.card import Card
from textual.widgets import Static
from textual.containers import Container
from textual.app import ComposeResult

class CardWidget(Container):
    def __init__(self, card: Card) -> None:
        super().__init__(classes="card open")
        self.rank = card.rank.name
        self.suit = card.suit

    def compose(self) -> ComposeResult:
        yield Static("       ", classes=f"card-line {self.suit.name.lower()}")
        yield Static(f" {self.rank:<2}    ", classes=f"card-line {self.suit.name.lower()}")
        yield Static(f"   {self.suit.emoji}  ", classes=f"card-line {self.suit.name.lower()}")
        yield Static(f"     {self.rank:>2} ", classes=f"card-line {self.suit.name.lower()}")
        yield Static("       ", classes=f"card-line {self.suit.name.lower()}")

class ObfuscatedCardWidget(Container):
    def __init__(self, card: Card) -> None:
        super().__init__(classes="card obfuscated")

    def compose(self) -> ComposeResult:
        yield Static("       ", classes="card-line obfuscated")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static("       ", classes="card-line obfuscated")
