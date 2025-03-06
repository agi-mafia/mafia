from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "success"}


@app.on_event("startup")
async def startup_event():
    return


@app.on_event("shutdown")
async def shutdown_event():
    return


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/game")
async def get_game():
    return {"message": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
