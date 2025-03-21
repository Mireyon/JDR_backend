from fastapi import FastAPI
from .lifespan import lifespan

from .routers.inventory import inventory_router

app = FastAPI(
    title="Ignifai API",
    description=(
        "Unified API for multiple services."
    ),
    version="0.0.1",
    openapi_tags=[],
    root_path="/",
    lifespan=lifespan,
)

# Mount each API under its respective path
app.include_router(inventory_router, prefix="/inventory")


@app.get("/version")
async def get_version():
    return {"version": "0.0.1", "app": "api_private"}