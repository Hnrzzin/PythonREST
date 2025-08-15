from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from model import postContato, getContatos, getContatoById, updateContato, deleteContato
import re
from response import ok, bad_request, server_error
from schema import Contato   
router = APIRouter(prefix="/contatos", tags=["contatos"]) 

# -----------------------
# Modelo para validar entrada de dados
# -----------------------
# ps: o ID não é necessário no corpo da requisição, pois é gerado automaticamente
# ps: 


# -----------------------
# Rota que retorna todos os contatos
# -----------------------
@router.get("/list")
async def listar_contatos():
    try:
        return getContatos()
    except Exception as e:
        return server_error(f"Erro ao listar contatos: {str(e)}")

# -----------------------
# Rota que retorna um contato pelo ID
# -----------------------
@router.get("/list/{contato_id}")
async def obter_contato(contato_id: int):
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        return getContatoById(contato_id)
    except Exception as e:
        return server_error(f"Erro ao obter contato: {str(e)}")

# -----------------------
# Rota que cria um novo contato
# -----------------------
@router.post("/create")
async def criar_contato(contato: Contato):
    try:
        # Validação obrigatória
        if not contato.nome or len(contato.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        if not contato.telefone:
            return bad_request("Telefone obrigatório.")
        telefone_limpo = re.sub(r"\D", "", contato.telefone)
        if len(telefone_limpo) != 11:
            return bad_request("Telefone inválido. Deve ter 11 números.")
        
        if not contato.email:
            return bad_request("Email inválido. Insira um email.")
        if not '@' in contato.email:
            return bad_request("Email inválido. Deve conter '@'.")
        
        return postContato(contato.nome, contato.email, telefone_limpo)
    except Exception as e:
        return server_error(f"Erro ao criar contato: {str(e)}")

# -----------------------
# Rota que atualiza um contato
# -----------------------
@router.put("/update/{contato_id}")
async def atualizar_contato(contato_id: int, contato: Contato):
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        
        # Validação dos campos se foram enviados
        if contato.nome and len(contato.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        telefone_limpo = None
        if contato.telefone:
            telefone_limpo = re.sub(r"\D", "", contato.telefone)
            if len(telefone_limpo) != 11:
                return bad_request("Telefone inválido. Deve ter 11 números.")
        
        if contato.email and '@' not in contato.email:
            return bad_request("Email inválido. Deve conter '@'.")
        
        return updateContato(contato_id, contato.nome, contato.email, telefone_limpo)
    
    except Exception as e:
        return server_error(f"Erro ao atualizar contato: {str(e)}")
# -----------------------
# Rota que exclui um contato
# -----------------------
@router.delete("/delete/{contato_id}")
async def excluir_contato(contato_id: int):
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        else:
            return deleteContato(contato_id)
    except Exception as e:
        return server_error(f"Erro ao excluir contato: {str(e)}")
    
