"""
Módulo de Esquemas de Dados - API RESTful

Define modelos Pydantic para validação e documentação automática
dos dados de entrada e saída da API.

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Benefícios:
    - Validação automática de dados de entrada
    - Documentação interativa da API
    - Serialização/Deserialização consistente
    - Tipagem estática para melhor desenvolvimento
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# =============================================================================
#                           ESQUEMAS DE DADOS
# =============================================================================

class Usuario(BaseModel):
    """
    Modelo de dados para criação e atualização de usuários.
    
    Attributes:
        nome (Optional[str]): Nome completo do usuário
        email (Optional[str]): Email único do usuário
        senha_hash (Optional[str]): Senha em texto plano (será hasheada)
    
    Notes:
        - Campos Optional para permitir updates parciais
        - Validações específicas são feitas nos endpoints
    """
    nome: Optional[str] = Field(
        default=None,
        description="Nome completo do usuário (mínimo 4 caracteres)",
        min_length=4
    )
    email: Optional[str] = Field(
        default=None,
        description="Email único do usuário (formato válido requerido)"
    )
    senha_hash: Optional[str] = Field(
        default=None,
        description="Senha em texto plano (será hasheada no servidor)",
        min_length=6
    )

    class Config:
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao@email.com",
                "senha_hash": "Senha123"
            }
        }

class Contato(BaseModel):
    """
    Modelo de dados para criação e atualização de contatos.
    
    Attributes:
        nome (Optional[str]): Nome do contato
        email (Optional[str]): Email do contato
        telefone (Optional[str]): Telefone do contato
    
    Notes:
        - Campos Optional para permitir updates parciais
        - Validações específicas são feitas nos endpoints
    """
    nome: Optional[str] = Field(
        default=None,
        description="Nome do contato (mínimo 4 caracteres)",
        min_length=4
    )
    email: Optional[str] = Field(
        default=None,
        description="Email do contato (formato válido requerido)"
    )
    telefone: Optional[str] = Field(
        default=None,
        description="Telefone do contato (11 dígitos, apenas números)"
    )

    class Config:
        schema_extra = {
            "example": {
                "nome": "Maria Santos",
                "email": "maria@email.com",
                "telefone": "11999998888"
            }
        }

class Login(BaseModel):
    """
    Modelo de dados para operações de login.
    
    Attributes:
        email (str): Email do usuário
        senha (str): Senha em texto plano
    
    Notes:
        - Campos obrigatórios para login
        - Validações básicas de formato
    """
    email: str = Field(
        ...,
        description="Email do usuário para login",
        example="usuario@email.com"
    )
    senha: str = Field(
        ...,
        description="Senha do usuário para login",
        example="Senha123",
        min_length=6
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@email.com",
                "senha": "Senha123"
            }
        }