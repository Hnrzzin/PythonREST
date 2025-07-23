from fastapi import FastAPI
from app.routes import contatos

app = FastAPI()

app.include_router(contatos.router)