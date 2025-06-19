
from abc import ABC

from enum import Enum, auto

class GameEventType(Enum):
    QUIT = auto()
    THROW_HAND = auto()
    KEEP_HAND = auto()
    INCREASE_BET = auto()
    DECREASE_BET = auto()
    SELECT_CARDS = auto()
    INVALID = auto()
    CONFIRM = auto()
    CANCEL = auto()
    BET_LOW = auto()
    BET_HIGH = auto()

class GameEvent(ABC):
    pass

class QuitEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.QUIT

class ThrowHandEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.THROW_HAND

class KeepHandEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.KEEP_HAND 

class IncreaseBetEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.INCREASE_BET
    
class DecreaseBetEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.DECREASE_BET

class SelectCardsEvent(GameEvent):
    def __init__(self, indices: list[int]):
        self.type = GameEventType.SELECT_CARDS
        self.indices = indices

class InvalidEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.INVALID

class ConfirmEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.CONFIRM

class CancelEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.CANCEL

class BetLowEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.BET_LOW

class BetHighEvent(GameEvent):
    def __init__(self):
        self.type = GameEventType.BET_HIGH

def parse_input(user_input: str) -> GameEvent:
    s = user_input.strip().replace(" ", "").lower()
    match s:
        case 'q' | 'quit' | 'exit' | 'Q':
            return QuitEvent()
        case 't' | 'throw' | 'T':
            return ThrowHandEvent()
        case 'k' | 'keep' | 'K':
            return KeepHandEvent()
        case '+' | 'increase' | 'add':
            return IncreaseBetEvent()
        case '-' | 'decrease' | 'subtract':
            return DecreaseBetEvent()
        case _ if all(c.isdigit() and c in "12345" for c in s) and s:
            indices = sorted([int(c) for c in s])
            return SelectCardsEvent(list(set(indices)))
        case 'n' | 'no':
            return CancelEvent()
        case 'y' | 'yes':
            return ConfirmEvent()
        case 'l' | 'low':
            return BetLowEvent()
        case 'h' | 'high':
            return BetHighEvent()
        case _:
            return InvalidEvent()
