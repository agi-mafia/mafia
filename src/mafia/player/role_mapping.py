from mafia.player.detective import Detective
from mafia.player.hunter import Hunter
from mafia.player.jailor import Jailor
from mafia.player.mafia import Mafia
from mafia.player.role import Role
from mafia.player.villager import Villager

role_mapping = {
    Role.VILLAGER: Villager,
    Role.MAFIA: Mafia,
    Role.DETECTIVE: Detective,
    Role.JAILOR: Jailor,
    Role.HUNTER: Hunter,
}
