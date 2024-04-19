from fastapi import FastAPI

from src.lifespan import lifespan
from src.config import settings


app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)


@app.get("/")
def root():
    return {"message": "Hello World"}
