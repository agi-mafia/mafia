import asyncio
from fastapi import FastAPI
from src.game.game import Game

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": 'success'}

@app.on_event("startup")
async def startup_event():
    game = Game()
    game.start()
    app.state.game = game
    
    
@app.get("/game")
async def get_game():
    game: Game = app.state.game
    return game.get_game_state()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 