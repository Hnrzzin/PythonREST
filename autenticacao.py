from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from response import ok, bad_request, server_error
import re
from schema import Usuario, Login
from main import bcrypt_context
from model import postUsuario, loginUsuario

router = APIRouter(prefix="/autenticacao", tags=["autenticacao"]) 

def criar_token(id_usuario: int):
    token = f"fsdfsddg997ff{ id_usuario}" 
    return token

    

@router.post("/create")
async def criar_usuario(usuario: Usuario):
    try:
        # Validação obrigatória
        if not usuario.nome or len(usuario.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        if not usuario.senha_hash:
            return bad_request("Senha obrigatória.")
        if len(usuario.senha_hash) < 6:
            return bad_request("Senha inválida. Deve ter pelo menos 6 caracteres.")
        if not re.search(r"[A-Z]", usuario.senha_hash):
            return bad_request("Senha inválida. Deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[0-9]", usuario.senha_hash):
            return bad_request("Senha inválida. Deve conter pelo menos um número.")
        senha_hashed = bcrypt_context.hash(usuario.senha_hash)
        if not usuario.email:
            return bad_request("Email inválido. Insira um email.")
        if not '@' in usuario.email:
            return bad_request("Email inválido. Deve conter '@'.")
        
        return postUsuario(usuario.nome, usuario.email, senha_hashed)
    except Exception as e:
        return server_error(f"Erro ao criar usuario: {str(e)}")

@router.post("/login")
async def login_usuario(login: Login):
    try:
        usuario = loginUsuario(login.email)
        
        if usuario is None:
            return bad_request("Usuário não encontrado.")
        if not bcrypt_context.verify(login.senha, usuario['senha_hash']): #verifica se a senha é a mesma que foi cadastrada 
            return bad_request("Senha incorreta.")
        access_token = criar_token(usuario['id'])
        return ok("Login realizado com sucesso.", {
            "access_token": access_token,
            "token_type": "bearer"
        })
    except Exception as e:
        return server_error(f"Erro ao realizar login: {str(e)}")