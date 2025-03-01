from enum import Enum, auto

from src.player.detective import Detective
from src.player.hunter import Hunter
from src.player.jailer import Jailor
from src.player.mafia import Mafia
from src.player.villager import Villager


class Role(Enum):
    villager = auto()
    mafia = auto()
    detective = auto()
    jailor = auto()
    hunter = auto()


role_mapping = {
    Role.villager: Villager,
    Role.mafia: Mafia,
    Role.detective: Detective,
    Role.jailor: Jailor,
    Role.hunter: Hunter,
}
