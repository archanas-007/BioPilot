from fastapi import FastAPI
from app.routers import hello

app = FastAPI()

app.include_router(hello.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
