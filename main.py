from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer 
import os

#=======================================================================
#                   Importa as variáveis de ambiente
#========================================================================
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) #tranforma o valor em inteiro, pois o valor é string no .env

#=======================================================================
#                   Cria o contexto de criptografia
#========================================================================
app = FastAPI()
#bycypt se trata de um algoritmo de hash para senhas
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#oauth2 se trata de um esquema de autenticação que usa tokens
oauth2_schema = OAuth2PasswordBearer(tokenUrl="autenticacao/login")

from contatos import router
from autenticacao import router as auth_router

#=======================================================================
#                   Inclui as rotas no aplicativo FastAPI
#========================================================================
app.include_router(router) #inclui as rotas no aplicativo FastAPI
app.include_router(auth_router) #inclui as rotas de autenticação no aplicativo FastAPI

