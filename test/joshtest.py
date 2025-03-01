from src.game.game_config import GameConfig
from src.game.game import Game
from src.player.role import Role

gc = GameConfig(
    players={
        "model1": Role.mafia,
        "model2": Role.villager,
        "model2": Role.villager,
        "model2": Role.villager,
    },
)


game = Game(gc)

print(game.player2role)
game.player2role = 0
print(game.player2role)
