from fastapi import FastAPI
from .database import Base, engine
from .routers import surveys, responses

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(surveys.router)
app.include_router(responses.router)

@app.get("/")
def root():
    return {"message": "Backend running"}