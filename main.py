"""
Ponto de Entrada da API - FastAPI Application

Configura e inicializa a aplicação FastAPI com todas as dependências
e rotas necessárias para o funcionamento da API de contatos.

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Funcionalidades:
    - Configuração de variáveis de ambiente
    - Inicialização do FastAPI com metadados
    - Configuração de autenticação OAuth2
    - Registro de rotas da aplicação
"""

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os

# =============================================================================
#                           CONFIGURAÇÃO DE AMBIENTE
# =============================================================================

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de segurança para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Padrão: HS256
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# =============================================================================
#                           INICIALIZAÇÃO DO FASTAPI
# =============================================================================

# Cria instância principal do FastAPI
app = FastAPI(
    title="API de Gerenciamento de Contatos",
    description="API RESTful para gerenciamento de contatos com autenticação JWT",
    version="1.0.0",
    docs_url="/docs",  # Documentação interativa Swagger
    redoc_url="/redoc"  # Documentação alternativa ReDoc
)

# Configura contexto de criptografia para senhas
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configura esquema OAuth2 para autenticação
oauth2_schema = OAuth2PasswordBearer(tokenUrl="autenticacao/login-form")

# =============================================================================
#                           REGISTRO DE ROTAS
# =============================================================================

# Importa e registra roteadores (import circular evitado)
from contatos import router
from autenticacao import router as auth_router

# Registra roteador de contatos
app.include_router(router)

# Registra roteador de autenticação
app.include_router(auth_router)

