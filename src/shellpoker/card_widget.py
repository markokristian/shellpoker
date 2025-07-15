from shellpoker.card import Card
from textual.widgets import Static
from textual.containers import Container
from textual.app import ComposeResult

class CardWidget(Container):
    def __init__(self, card: Card) -> None:
        super().__init__(classes="card open")
        self.rank = card.rank.name
        self.suit = card.suit
        self.is_joker = card.is_joker()

    def compose(self) -> ComposeResult:
        if self.is_joker:
            yield from self.compose_joker()
        else:
            yield Static("       ", classes=f"card-line {self.suit.name.lower()}")
            yield Static(f" {self.rank:<2}    ", classes=f"card-line {self.suit.name.lower()}")
            yield Static(f"   {self.suit.emoji}  ", classes=f"card-line {self.suit.name.lower()}")
            yield Static(f"     {self.rank:>2} ", classes=f"card-line {self.suit.name.lower()}")
            yield Static("       ", classes=f"card-line {self.suit.name.lower()}")

    def compose_joker(self) -> ComposeResult:
        yield Static("       ", classes="card-line joker")
        yield Static(" ♥    ♣ ", classes="card-line joker")
        yield Static("  JKR! ", classes="card-line joker")
        yield Static(" ♠    ♦ ", classes="card-line joker")
        yield Static("       ", classes="card-line joker")

class ObfuscatedCardWidget(Container):
    def __init__(self, _: Card) -> None:
        super().__init__(classes="card obfuscated")

    def compose(self) -> ComposeResult:
        yield Static("       ", classes="card-line obfuscated")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static(" ░░░░░ ", classes="card-line obfuscated mid")
        yield Static("       ", classes="card-line obfuscated")
