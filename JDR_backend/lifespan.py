from fastapi import FastAPI
from loguru import logger
from os import environ
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        app.state.config = {}
    except Exception as e:
        logger.exception(e)
        raise

    logger.info("Starting the app")

    yield

    logger.info("Stopping the app")