from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.DBSettings.database import Base, engine
from app.routers import auth, exercises
from app.settings.logging_config import logger
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application is starting")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application is shutting down")

app.include_router(auth.router)
app.include_router(exercises.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
