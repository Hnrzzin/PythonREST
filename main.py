from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) #tranforma o valor em inteiro, pois o valor é string no .env

app = FastAPI()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from contatos import router
from autenticacao import router as auth_router

app.include_router(router) #inclui as rotas no aplicativo FastAPI
app.include_router(auth_router) #inclui as rotas de autenticação no aplicativo FastAPI

