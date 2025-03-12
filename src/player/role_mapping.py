from src.player.detective import Detective
from src.player.hunter import Hunter
from src.player.jailor import Jailor
from src.player.mafia import Mafia
from src.player.role import Role
from src.player.villager import Villager

role_mapping = {
    Role.VILLAGER: Villager,
    Role.MAFIA: Mafia,
    Role.DETECTIVE: Detective,
    Role.JAILOR: Jailor,
    Role.HUNTER: Hunter,
}
