from mafia.game.game import Game
from mafia.game.game_config import GameConfig, PlayerConfig
from mafia.player.role import Role


def test_game():
    config = GameConfig(
        players=[
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.VILLAGER),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.MAFIA),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.DETECTIVE),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.HUNTER),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.JAILOR),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.MAFIA),
        ],
        max_rounds=5,
    )
    game = Game(config)
    game.start()
