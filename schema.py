from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha_hash: Optional[str] = None

class Contato(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

class Login(BaseModel):
    email: str
    senha: str