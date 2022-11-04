from fastapi import FastAPI

from routers import facade

app = FastAPI()

app.include_router(facade.router)


@app.get("/")
async def hello():
    return {"msg": "hello"}
