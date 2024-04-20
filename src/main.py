from fastapi import FastAPI

from src.config import settings
from src.items.views import router as items_router
from src.lifespan import lifespan

app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)

app.include_router(items_router, prefix="/items", tags=["items"])


@app.get("/ping")
def root() -> dict[str, str]:
    return {"ping": "pong"}
