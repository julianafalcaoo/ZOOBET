from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from auth_routes import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "API funcionando"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
# uvicorn main:app --reload 