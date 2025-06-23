from dataclasses import dataclass

class GameEvent: pass

class QuitEvent(GameEvent): pass
class ThrowHandEvent(GameEvent): pass
class KeepHandEvent(GameEvent): pass
class IncreaseBetEvent(GameEvent): pass
class DecreaseBetEvent(GameEvent): pass
class ConfirmBetEvent(GameEvent): pass
class InvalidEvent(GameEvent): pass
class ConfirmEvent(GameEvent): pass
class CancelEvent(GameEvent): pass
class BetLowEvent(GameEvent): pass
class BetHighEvent(GameEvent): pass

@dataclass
class SelectCardsEvent(GameEvent):
    indices: list[int]

def parse_input(user_input: str) -> GameEvent:
    s = user_input.strip().replace(" ", "").lower()
    match s:
        case 'q' | 'quit' | 'exit':
            return QuitEvent()
        case 't' | 'throw':
            return ThrowHandEvent()
        case 'k' | 'keep':
            return KeepHandEvent()
        case '+' | 'increase' | 'add':
            return IncreaseBetEvent()
        case '-' | 'decrease' | 'subtract':
            return DecreaseBetEvent()
        case _ if all(c.isdigit() and c in "12345" for c in s) and s:
            indices = sorted(set(int(c) for c in s))
            return SelectCardsEvent(indices)
        case 'n' | 'no':
            return CancelEvent()
        case 'y' | 'yes':
            return ConfirmEvent()
        case 'l' | 'low':
            return BetLowEvent()
        case 'h' | 'high':
            return BetHighEvent()
        case 'd' | 'deal' | 'confirm':
            return ConfirmBetEvent()
        case _:
            return InvalidEvent()
