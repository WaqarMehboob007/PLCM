from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine

app = FastAPI(title="PLM System")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "PLM FastAPI running"}