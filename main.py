import asyncio

app = FastAPI()

async def async_operation():
    await asyncio.sleep(1)
    return "Async operation completed"

@app.get("/")
async def read_root():
    result = await async_operation()
    return {"message": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)