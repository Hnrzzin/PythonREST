from fastapi import APIRouter
from app.database.connection import Database
from fastapi import HTTPException
from app.schemas.contato_schema import ContatoSchema
from typing import List

router = APIRouter() 
banco = Database()

"""
Rota que retorna todos os contatos cadastrados.
Parâmetros opcionais: skip e limit para paginação.
"""

@router.get("/contatos", response_model=List[ContatoSchema])  #Aqui define como será o modelo JSON de resposta
async def get_contatos():
    try:
        contatos = banco.todos_contatos() #instancia o metodo que busca os contatos (todos_contatos)
        
        if not contatos: #se nao existir nada em contatos
            raise HTTPException(status_code=404, detail="Nenhum contato encontrado") #mensgem de erro
        else:
            return contatos #retorna os dados encontrados 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar contatos: {e}")



@router.get("/")
def home():
    return {"msg": "Funcionando!"}