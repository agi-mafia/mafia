import asyncio
from fastapi import FastAPI
from src.model.model import Model
# from src.game.game import Game

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": 'success'}

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
    return model.inference("Translate this sentence from English to French. I love programming.")

    
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