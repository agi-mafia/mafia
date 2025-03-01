from enum import Enum, auto

from src.player.detective import Detective
from src.player.hunter import Hunter
from src.player.jailor import Jailor
from src.player.mafia import Mafia
from src.player.villager import Villager


class Role(Enum):
    VILLAGER = auto()
    MAFIA = auto()
    DETECTIVE = auto()
    JAILOR = auto()
    HUNTER = auto()


role_mapping = {
    Role.VILLAGER: Villager,
    Role.MAFIA: Mafia,
    Role.DETECTIVE: Detective,
    Role.JAILOR: Jailor,
    Role.HUNTER: Hunter,
}
