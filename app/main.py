from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.health_check import router as health_check_router
from app.config.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
