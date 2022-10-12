import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from db import engine
from routers import cars, web, auth
app = FastAPI(title="Car Sharing")
app.include_router(cars.router)
app.include_router(web.router)
app.include_router(auth.router)

origins = [
    "http://localhost:8080",
    "http://localhost:8080"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials =True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#db = load_db()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)