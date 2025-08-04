from fastapi import APIRouter


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

@router.post("/create") #decorador (@) que define a rota POST para criar um novo contato
async def criar_contato():
    return {"message": "Criando um novo contato"}

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