from fastapi import FastAPI

from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello World"}
