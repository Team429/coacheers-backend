from fastapi import FastAPI

from config.database import engine, Base
from routers import facade

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(facade.router)


@app.get("/")
async def hello():
    return {"msg": "hello"}
