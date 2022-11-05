from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine, Base
from routers import facade


def include_cors(fast_api: FastAPI):
    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=["*"],
        allow_headers=["*"],
    )


def include_router(fast_api: FastAPI):
    fast_api.include_router(facade.router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    create_tables()
    fast_api_app = FastAPI()
    include_cors(fast_api_app)
    include_router(fast_api_app)
    return fast_api_app


app = start_application()
