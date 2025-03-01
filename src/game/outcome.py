from enum import Enum, auto


class GameStatus(Enum):
    IN_PROGRESS = auto()
    MAFIA_WIN = auto()
    INNOCENT_WIN = auto()
