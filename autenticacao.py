"""
Módulo de Autenticação e Autorização - API RESTful

Fornece endpoints para registro, login, refresh token e validação JWT.
Implementa autenticação OAuth2 com tokens JWT para segurança da API.

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Dependências:
    - FastAPI Security (OAuth2)
    - Python-JOSE (JWT tokens)
    - Passlib (hash de senhas)
"""

from fastapi import APIRouter, Depends
from response import ok, bad_request, server_error, acesso_negado
import re
from schema import Usuario, Login
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, oauth2_schema
from model import postUsuario, loginUsuario, getUsuarioById
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

# =============================================================================
#                           CONFIGURAÇÃO DO ROTEADOR
# =============================================================================
router = APIRouter(prefix="/autenticacao", tags=["autenticacao"])

# =============================================================================
#                           GERENCIAMENTO DE TOKENS JWT
# =============================================================================

def criar_token(id_usuario: int, duracao_token: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Gera um token JWT para autenticação do usuário.
    
    Args:
        id_usuario (int): ID do usuário para incluir no token
        duracao_token (timedelta): Duração de validade do token (padrão: 30 minutos)
    
    Returns:
        str: Token JWT codificado
    """
    horario_expiracao = datetime.now(timezone.utc) + duracao_token
    info_token = {
        "sub": str(id_usuario),  # Subject deve ser string conforme especificação JWT
        "exp": horario_expiracao  # Timestamp de expiração
    }
    return jwt.encode(info_token, SECRET_KEY, ALGORITHM)

async def decodificar_token(token: str = Depends(oauth2_schema)):
    """
    Decodifica e valida um token JWT.
    
    Args:
        token (str): Token JWT a ser validado
    
    Returns:
        int: ID do usuário extraído do token
    
    Raises:
        JWTError: Se o token for inválido ou expirado
    """
    try:
        info_usuario = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(info_usuario.get("sub"))
        if user_id is None:
            raise JWTError("Token inválido: ID do usuário não encontrado.")
        return user_id
    except JWTError:
        raise JWTError("Token inválido ou expirado.")

# =============================================================================
#                           ENDPOINTS DE AUTENTICAÇÃO
# =============================================================================

@router.post("/create")
async def criar_usuario(usuario: Usuario):
    """
    Cria um novo usuário no sistema.
    
    Args:
        usuario (Usuario): Dados do usuário para registro
    
    Returns:
        JSONResponse: Sucesso ou erro com mensagem apropriada
    
    Validations:
        - Nome mínimo de 4 caracteres
        - Senha com mínimo 6 caracteres, 1 maiúscula e 1 número
        - Email válido com formato correto
    """
    try:
        # Validação de nome
        if not usuario.nome or len(usuario.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        # Validação de senha
        if not usuario.senha_hash:
            return bad_request("Senha obrigatória.")
        if len(usuario.senha_hash) < 6:
            return bad_request("Senha inválida. Deve ter pelo menos 6 caracteres.")
        if not re.search(r"[A-Z]", usuario.senha_hash):
            return bad_request("Senha inválida. Deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[0-9]", usuario.senha_hash):
            return bad_request("Senha inválida. Deve conter pelo menos um número.")
        
        # Hash da senha antes de armazenar
        senha_hashed = bcrypt_context.hash(usuario.senha_hash)
        
        # Validação de email
        if not usuario.email:
            return bad_request("Email inválido. Insira um email.")
        if not '@' in usuario.email:
            return bad_request("Email inválido. Deve conter '@'.")
        
        # Criação do usuário no banco
        novo_usuario = postUsuario(usuario.nome, usuario.email, senha_hashed)
        if not novo_usuario:
            return bad_request("Email já cadastrado.")
        
        return ok("Usuário criado com sucesso.", novo_usuario)
    except Exception as e:
        return server_error(f"Erro ao criar usuario: {str(e)}")

@router.post("/login")
async def login_usuario(login: Login):
    """
    Autentica um usuário e retorna tokens JWT.
    
    Args:
        login (Login): Credenciais de email e senha
    
    Returns:
        JSONResponse: Tokens de acesso e refresh em caso de sucesso
    """
    try:
        if not login.email or not login.senha:
            return bad_request("Email e senha são obrigatórios.")
        
        # Busca usuário pelo email
        usuario = loginUsuario(login.email)
        if usuario is None:
            return bad_request("Usuário não encontrado.")
        
        # Verifica se a senha corresponde ao hash armazenado
        if not bcrypt_context.verify(login.senha, usuario['senha_hash']):
            return bad_request("Senha incorreta.")
        
        # Gera tokens de acesso e refresh
        access_token = criar_token(usuario['id'])
        refresh_token = criar_token(usuario['id'], duracao_token=timedelta(days=3))
        
        return ok("Login realizado com sucesso.", {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
    except Exception as e:
        return server_error(f"Erro ao realizar login: {str(e)}")

@router.get("/refresh")
async def refresh_token(id_atual: int = Depends(decodificar_token)):
    """
    Renova o token de acesso usando um refresh token válido.
    
    Args:
        id_atual (int): ID do usuário extraído do token (via dependência)
    
    Returns:
        JSONResponse: Novo token de acesso
    """
    try:
        # Verifica se o usuário ainda existe no banco
        usuario = getUsuarioById(id_atual)
        if usuario is None:
            return acesso_negado("Usuário não encontrado no sistema.")
        
        # Gera novo token de acesso
        access_token = criar_token(usuario['id'])
        
        return ok("Token atualizado com sucesso.", {
            "access_token": access_token,
            "token_type": "bearer"
        })
    except JWTError as e:
        return acesso_negado(f"Erro de autenticação: {str(e)}")
    except Exception as e:
        return server_error(f"Erro ao atualizar o token: {str(e)}")

@router.post("/login-form")
async def login_usuario(dados_form: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint compatível com OAuth2 para integração com documentação automática.
    
    Args:
        dados_form (OAuth2PasswordRequestForm): Formulário padrão OAuth2
    
    Returns:
        dict: Token de acesso no formato OAuth2
    """
    try:
        if not dados_form.username or not dados_form.password:
            return bad_request("Email e senha são obrigatórios.")
        
        usuario = loginUsuario(dados_form.username)
        if usuario is None:
            return bad_request("Usuário não encontrado.")
        
        if not bcrypt_context.verify(dados_form.password, usuario['senha_hash']):
            return bad_request("Senha incorreta.")
        
        access_token = criar_token(usuario['id'])
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        return server_error(f"Erro ao realizar login: {str(e)}")