"""
Módulo de Gerenciamento de Contatos - API RESTful

Fornece endpoints CRUD completos para operações com contatos.
Todos os endpoints requerem autenticação JWT válida.

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Segurança:
    - Autenticação JWT obrigatória em todas as rotas
    - Validação de propriedade (usuário só acessa seus contatos)
    - Validação de dados de entrada
"""

from fastapi import APIRouter, Depends
from model import postContato, getContatos, getContatoById, updateContato, deleteContato, getUsuarioById
import re
from response import ok, bad_request, server_error
from schema import Contato
from autenticacao import decodificar_token

# =============================================================================
#                           CONFIGURAÇÃO DO ROTEADOR
# =============================================================================
router = APIRouter(
    prefix="/contatos",
    tags=["contatos"],
    dependencies=[Depends(decodificar_token)]  # Autenticação obrigatória
)

# =============================================================================
#                           ENDPOINTS DE CONTATOS
# =============================================================================

@router.get("/list")
async def listar_contatos(id_usuario_logado: int = Depends(decodificar_token)):
    """
    Lista todos os contatos do usuário autenticado.
    
    Args:
        id_usuario_logado (int): ID do usuário extraído do token JWT
    
    Returns:
        JSONResponse: Lista de contatos ou mensagem de erro
    """
    try:
        contatos = getContatos(id_usuario_logado)
        if contatos is None:
            return server_error("Erro interno ao buscar contatos.")
        return ok("Contatos listados com sucesso.", contatos)
    except Exception as e:
        return server_error(f"Erro ao listar contatos: {str(e)}")

@router.get("/list/{contato_id}")
async def obter_contato_ID(contato_id: int, id_usuario_logado: int = Depends(decodificar_token)):
    """
    Obtém um contato específico pelo ID.
    
    Args:
        contato_id (int): ID do contato a ser recuperado
        id_usuario_logado (int): ID do usuário autenticado
    
    Returns:
        JSONResponse: Dados do contato ou mensagem de erro
    
    Validations:
        - ID do contato deve ser positivo
        - Contato deve pertencer ao usuário autenticado
    """
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        
        contato = getContatoById(contato_id, id_usuario_logado)
        if contato is None:
            return server_error("Erro interno ao buscar contato.")
        
        if not contato:
            return bad_request("Contato não encontrado ou acesso não autorizado.")
        
        return ok("Contato obtido com sucesso.", contato)
    except Exception as e:
        return server_error(f"Erro ao obter contato: {str(e)}")

@router.post("/create")
async def criar_contato(contato: Contato, id_usuario_logado: int = Depends(decodificar_token)):
    """
    Cria um novo contato para o usuário autenticado.
    
    Args:
        contato (Contato): Dados do novo contato
        id_usuario_logado (int): ID do usuário autenticado
    
    Returns:
        JSONResponse: Contato criado ou mensagem de erro
    
    Validations:
        - Nome mínimo de 4 caracteres
        - Telefone com 11 dígitos numéricos
        - Email com formato válido
        - Verificação de duplicatas
    """
    try:
        # Validação de nome
        if not contato.nome or len(contato.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        # Validação de telefone
        if not contato.telefone:
            return bad_request("Telefone obrigatório.")
        
        telefone_limpo = re.sub(r"\D", "", contato.telefone)
        if len(telefone_limpo) != 11:
            return bad_request("Telefone inválido. Deve ter 11 números.")
        
        # Validação de email
        if not contato.email or "@" not in contato.email:
            return bad_request("Email inválido. Insira um email válido.")

        # Criação do contato no banco
        novo_contato = postContato(
            contato.nome,
            contato.email,
            telefone_limpo,
            id_usuario_logado
        )
        
        if novo_contato is None:
            return bad_request("Telefone ou email já cadastrado.")

        return ok("Contato criado com sucesso.", novo_contato)

    except Exception as e:
        return server_error(f"Erro ao criar contato: {str(e)}")

@router.put("/update/{contato_id}")
async def atualizar_contato(contato_id: int, contato: Contato, id_usuario_logado: int = Depends(decodificar_token)):
    """
    Atualiza um contato existente.
    
    Args:
        contato_id (int): ID do contato a ser atualizado
        contato (Contato): Dados atualizados do contato
        id_usuario_logado (int): ID do usuário autenticado
    
    Returns:
        JSONResponse: Mensagem de sucesso ou erro
    
    Validations:
        - ID do contato deve ser positivo
        - Campos opcionais são validados se fornecidos
        - Contato deve pertencer ao usuário
    """
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        
        # Validação condicional do nome
        if contato.nome and len(contato.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        # Validação condicional do telefone
        telefone_limpo = None
        if contato.telefone:
            telefone_limpo = re.sub(r"\D", "", contato.telefone)
            if len(telefone_limpo) != 11:
                return bad_request("Telefone inválido. Deve ter 11 números.")
        
        # Validação condicional do email
        if contato.email and '@' not in contato.email:
            return bad_request("Email inválido. Deve conter '@'.")

        # Atualização do contato
        sucesso = updateContato(contato_id, id_usuario_logado, contato.nome, contato.email, telefone_limpo)
        
        if not sucesso:
            return bad_request("Contato não encontrado ou acesso não autorizado.")
        
        return ok("Contato atualizado com sucesso.")
    
    except Exception as e:
        return server_error(f"Erro ao atualizar contato: {str(e)}")

@router.delete("/delete/{contato_id}")
async def excluir_contato(contato_id: int, id_usuario_logado: int = Depends(decodificar_token)):
    """
    Exclui um contato existente.
    
    Args:
        contato_id (int): ID do contato a ser excluído
        id_usuario_logado (int): ID do usuário autenticado
    
    Returns:
        JSONResponse: Mensagem de sucesso ou erro
    
    Validations:
        - ID do contato deve ser positivo
        - Contato deve pertencer ao usuário
    """
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        
        # Exclusão do contato
        sucesso = deleteContato(contato_id, id_usuario_logado)
        
        if not sucesso:
            return bad_request("Contato não encontrado ou acesso não autorizado.")
        
        return ok("Contato deletado com sucesso.")
    except Exception as e:
        return server_error(f"Erro ao excluir contato: {str(e)}")