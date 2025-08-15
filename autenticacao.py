from fastapi import APIRouter, Depends
from response import ok, bad_request, server_error, acesso_negado
import re
from schema import Usuario, Login
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, oauth2_schema # Importa oauth2_schema
from model import postUsuario, loginUsuario, getUsuarioById # Importa getUsuarioById
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

#========================================================================
#           Cria um roteador para as rotas de autenticação
#========================================================================
router = APIRouter(prefix="/autenticacao", tags=["autenticacao"]) 

#=======================================================================
#                   Cria um e verifica o token JWT
#========================================================================
def criar_token(id_usuario: int, duracao_token: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    horario_expiracao = datetime.now(timezone.utc) + duracao_token
    info_token = {
        "sub": str(id_usuario), # "sub" deve ser uma string
        "exp": horario_expiracao #data de expiração do token
    }
    JWT_codificado = jwt.encode(info_token, SECRET_KEY, ALGORITHM)
    return JWT_codificado # Retorna o token diretamente

# Função para decodificar e validar o token JWT
# Esta função será usada como uma dependência do FastAPI
# Vai descodificar o token e transcrever no ID do usuário

async def decodificar_token(token: str = Depends(oauth2_schema)):
    try:
        info_usuario = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = info_usuario.get("sub")
        if user_id is None:
            raise JWTError("Token inválido: ID do usuário não encontrado.")
        return int(user_id) # Retorna o ID do usuário validado como parametro para o refresh_token
    except JWTError:
        raise JWTError("Token inválido ou expirado.") # Lança a exceção para ser capturada pelo FastAPI

#======================================================================
#                           Cria o usuário 
#=======================================================================
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
#======================================================================
#                       Faz o login do usuário
#=======================================================================
@router.post("/login")
async def login_usuario(login: Login):
    try:
        usuario = loginUsuario(login.email)
        
        if usuario is None:
            return bad_request("Usuário não encontrado.")
        if not bcrypt_context.verify(login.senha, usuario['senha_hash']): #verifica se a senha é a mesma que foi cadastrada 
            return bad_request("Senha incorreta.")
        access_token = criar_token(usuario['id'])
        refresh_token = criar_token(usuario['id'], duracao_token= timedelta(days = 3))  # Implementar refresh token se necessário
        return ok("Login realizado com sucesso.", {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
    except Exception as e:
        return server_error(f"Erro ao realizar login: {str(e)}")
#=======================================================================
#                       Faz a atualização do token
#========================================================================    
@router.get("/refresh")
async def refresh_token(id_atual: int = Depends(decodificar_token)): # Usa a dependência para obter o ID do usuário
    # A rota só funcionará se o ID do usuário for válido (verificado pelo decodificar_token)
    try:
        usuario = getUsuarioById(id_atual) # Busca o usuário no DB usando o ID do token
        if usuario is None:
            # Mesmo que o token seja válido, o usuário pode ter sido deletado do DB
            return acesso_negado("Usuário não encontrado no sistema.") 
        
        access_token = criar_token(usuario['id'])
        
        return ok("Token atualizado com sucesso.", {
            "access_token": access_token,
            "token_type": "bearer"
        })
    except JWTError as e: # Captura erros específicos do JWT
        return acesso_negado(f"Erro de autenticação: {str(e)}")
    except Exception as e:  # Captura qualquer outra exceção
        return server_error(f"Erro ao atualizar o token: {str(e)}")

