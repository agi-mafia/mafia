import asyncio

from fastapi import FastAPI

from src.game.game import Game
from src.game.game import Game
from src.game.game_config import GameConfig, PlayerConfig
from src.model.model import Model
from src.player.detective import Detective
from src.player.hunter import Hunter
from src.player.jailor import Jailor
from src.player.mafia import Mafia
from src.player.role import Role

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "success"}


@app.on_event("startup")
async def startup_event():
    return
    # game = Game()
    # game.start()
    # app.state.game = game


@app.get("/game/start")
async def start_game():
    return


@app.get("/test/model_test")
async def model_test():
    model = Model(model_name="gpt-3.5-turbo")
    return model.inference(
        "Translate this sentence from English to French. I love programming."
    )


@app.get("/test/player_detective_choose_target")
async def player_detective_choose_target():
    player = Detective(index=0, model_name="gpt-3.5-turbo")
    return player.choose_target([4, 6, 7])


@app.get("/test/player_detective_receive_info")
async def player_detective_receive_info():
    player = Detective(index=0, model_name="gpt-3.5-turbo")
    return player.receive_info("Player 0 is killed by Mafia last night.")


@app.get("/test/player_hunter_shoot")
async def player_hunter_shoot():
    player = Hunter(index=0, model_name="gpt-3.5-turbo")
    return player.shoot([8, 11, 14])


@app.get("/test/player_jailor_choose_target")
async def player_jailor_choose_target():
    player = Jailor(index=0, model_name="gpt-3.5-turbo")
    return player.choose_target([0, 1, 2])


@app.get("/test/player_mafia_propose_victim")
async def player_mafia_propose_victim():
    player = Mafia(index=0, model_name="gpt-3.5-turbo")
    return player.propose_victim([0, 1, 2])


@app.get("/test/josh")
async def josh_test():

    print("=" * 80)

    gc = GameConfig(
        players=[
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.VILLAGER),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.MAFIA),
            PlayerConfig(model_name="gpt-3.5-turbo", role=Role.VILLAGER),
        ],
        max_rounds=1,
        max_mafia_negotiation_rounds=3,
    )

    game = Game(gc)
    print("Role 2 IDs")
    print(game._role2ids)
    print()
    print("ID 2 player")
    print(game._players)
    game.start()

    print("=" * 80)
    print("=" * 80)


@app.get("/game")
async def get_game():
    return {"message": "success"}
    # game: Game = app.state.game
    # return game.get_game_state()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
