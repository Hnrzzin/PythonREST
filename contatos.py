from fastapi import APIRouter
from model import postContato, getContatos, getContatoById, updateContato, deleteContato, getUsuarioById
import re
from response import ok, bad_request, server_error
from schema import Contato   
from autenticacao import decodificar_token
from fastapi import Depends

router = APIRouter(prefix="/contatos", tags=["contatos"], dependencies= [Depends(decodificar_token)]) # Cria um roteador para as rotas de contatos

# -----------------------
# Modelo para validar entrada de dados
# -----------------------
# ps: o ID não é necessário no corpo da requisição, pois é gerado automaticamente
# ps: os dados que são acessados (ex: usuario["id"]) são aqueles que vem de dicionarios, já quando se usa (ex: usuario.id) é porque o dado é um objeto, e não um dicionário


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
async def obter_contato_ID(contato_id: int, id_usuario_logado: int = Depends(decodificar_token)):
    try:
        # busca somente o contato do usuário logado
        if not contato_id or contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        # Validação de usuário logado
        usuario = getUsuarioById(id_usuario_logado)  
        if not usuario:
            return bad_request("Usuário não encontrado.")
        
        # usuario["id"] representa o dono do contato no banco de dados, já id_usuario_logado representa o usuário que está tentando criar o contato
        if usuario["id"] != id_usuario_logado:
            return bad_request("Você não tem permissão para realizar esta ação.")
        
        return getContatoById(contato_id)
    except Exception as e:
        return server_error(f"Erro ao obter contato: {str(e)}")

# -----------------------
# Rota que cria um novo contato
# -----------------------
@router.post("/create")
async def criar_contato(contato: Contato, id_usuario_logado: int = Depends(decodificar_token)):
    try:
        # --- Validações obrigatórias ---
        if not contato.nome or len(contato.nome) < 4:
            return bad_request("Nome inválido. Deve ter pelo menos 4 caracteres.")
        
        if not contato.telefone:
            return bad_request("Telefone obrigatório.")
        
        telefone_limpo = re.sub(r"\D", "", contato.telefone)
        if len(telefone_limpo) != 11:
            return bad_request("Telefone inválido. Deve ter 11 números.")
        
        if not contato.email or "@" not in contato.email:
            return bad_request("Email inválido. Insira um email válido.")

        # Validação de usuário logado
        usuario = getUsuarioById(id_usuario_logado)  
        if not usuario:
            return bad_request("Usuário não encontrado.")
        
        # usuario["id"] representa o dono do contato no banco de dados, já id_usuario_logado representa o usuário que está tentando criar o contato
        if usuario["id"] != id_usuario_logado:
            return bad_request("Você não tem permissão para realizar esta ação.")

        # Criação do contato 
        novo_contato = postContato(
            contato.nome,
            contato.email,
            telefone_limpo,
            id_usuario_logado  # garante vínculo com o dono
        )

        return ok("Contato criado com sucesso.", novo_contato)

    except Exception as e:
        return server_error(f"Erro ao criar contato: {str(e)}")

# -----------------------
# Rota que atualiza um contato
# -----------------------
@router.put("/update/{contato_id}")
async def atualizar_contato(contato_id: int, contato: Contato, id_usuario_logado: int = Depends(decodificar_token)):
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
        
        # Validação de usuário logado
        usuario = getUsuarioById(id_usuario_logado)  
        if not usuario:
            return bad_request("Usuário não encontrado.")
        
        # usuario["id"] representa o dono do contato no banco de dados, já id_usuario_logado representa o usuário que está tentando criar o contato
        if usuario["id"] != id_usuario_logado:
            return bad_request("Você não tem permissão para realizar esta ação.")

        
        return updateContato(contato_id, contato.nome, contato.email, telefone_limpo)
    
    except Exception as e:
        return server_error(f"Erro ao atualizar contato: {str(e)}")
# -----------------------
# Rota que exclui um contato
# -----------------------
@router.delete("/delete/{contato_id}")
async def excluir_contato(contato_id: int, id_usuario_logado: int = Depends(decodificar_token)):
    try:
        if contato_id <= 0:
            return bad_request("ID inválido. Deve ser positivo.")
        else:
            usuario = getUsuarioById(id_usuario_logado)  
            if not usuario:
                return bad_request("Usuário não encontrado.")
            if usuario["id"] != id_usuario_logado:
                return bad_request("Você não tem permissão para realizar esta ação.")
            
            return deleteContato(contato_id)
    except Exception as e:
        return server_error(f"Erro ao excluir contato: {str(e)}")