from enum import Enum, auto


class GameStatus(Enum):
    IN_PROGRESS = auto()
    DRAW = auto()
    MAFIA_WIN = auto()
    TOWN_WIN = auto()
