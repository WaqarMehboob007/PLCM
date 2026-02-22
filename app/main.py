from fastapi import FastAPI
from .database import init_db, close_db
from contextlib import asynccontextmanager
from app.routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() 
    try:
        yield
    finally:
        # shutdown
        close_db()
    yield

app: FastAPI = FastAPI(title="PLCM System", lifespan=lifespan)
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "PLM FastAPI running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)