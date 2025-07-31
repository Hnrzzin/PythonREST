from pydantic import BaseModel

class ContatoSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str