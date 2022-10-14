from fastapi import FastAPI
from config import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def hello():
    return {"msg": "hello"}
