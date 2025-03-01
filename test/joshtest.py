from src.game.game import Game
from src.game.game_config import GameConfig, PlayerConfig
from src.player.role import Role

gc = GameConfig(
    players=[
        PlayerConfig(model_name="model2", role=Role.VILLAGER),
        PlayerConfig(model_name="model1", role=Role.MAFIA),
        PlayerConfig(model_name="model3", role=Role.VILLAGER),
        PlayerConfig(model_name="model4", role=Role.VILLAGER),
    ],
)


game = Game(gc)
print(game._role2ids)
print(game._id2player)
game.start()
