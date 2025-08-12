from fastapi import APIRouter
from model import postContato  # Import your Base from the model module
import re #experessão regular para validar o telefone/email/cpf...

router = APIRouter(prefix="/contatos", tags=["contatos"]) 
#banco = Database()

"""
Rota que retorna todos os contatos cadastrados.

"""
@router.get("/") #decorador (@) que define a rota GET para listar todos os contatos
async def listar_contatos():
    return {"message": "Listando todos os contatos"}


"""
Rota que retorna cadastro por ID.

"""

@router.get("/{contato_id}") #decorador (@) que define a rota GET para listar um contato específico pelo ID
async def obter_contato(contato_id: int):
    return {"message": f"Obtendo o contato com ID {contato_id}"}

"""
Rota que cria um novo contato.
"""


@router.post("/create")
async def criar_contato(nome: str, email: str, telefone: str):
    if not nome or not email or not telefone:
        return {"message": "Nome, email e telefone são obrigatórios."}
    
    if len(nome) < 4:
        return {"message": "O nome deve ter pelo menos 4 dígitos."}
    
    telefone_limpo = re.sub(r"\D", "", telefone)
    if len(telefone_limpo) != 11 or not telefone_limpo.isdigit():
        return {"message": "O telefone deve ter exatamente 11 dígitos numéricos."}
    
    if '@' not in email:
        return {"message": "O email deve conter '@'"}
    
    resultado = postContato(nome, email, telefone_limpo)
    return resultado

"""
Rota que atualiza um contato existente.
"""

@router.put("/update/{contato_id}") #decorador (@) que define a rota PUT para atualizar um contato existente
async def atualizar_contato(contato_id: int):
    return {"message": f"Atualizando o contato com ID {contato_id}"}

"""
Rota que exclui um contato existente.
"""

@router.delete("/delete/{contato_id}") #decorador (@) que define a rota DELETE para excluir um contato existente
async def excluir_contato(contato_id: int):
    return {"message": f"Excluindo o contato com ID {contato_id}"}