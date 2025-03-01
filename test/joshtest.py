from src.game.game import Game
from src.game.game_config import GameConfig, PlayerConfig
from src.player.role import Role

gc = GameConfig(
    players=[
        PlayerConfig(modelname="model2", role=Role.villager),
        PlayerConfig(modelname="model1", role=Role.mafia),
        PlayerConfig(modelname="model3", role=Role.villager),
        PlayerConfig(modelname="model4", role=Role.villager),
    ],
)


game = Game(gc)
print(game._role2ids)
game.start()
