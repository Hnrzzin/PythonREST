"""
Módulo de Respostas Padronizadas - API RESTful

Fornece funções utilitárias para respostas HTTP consistentes
em formato JSON seguindo padrões RESTful.

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Padrões de Resposta:
    - Estrutura consistente: message, data, status, HTTPStatus, HTTPStatusCode
    - Códigos HTTP semanticamente corretos
    - Mensagens claras e informativas
"""

from fastapi import status
from fastapi.responses import JSONResponse

# =============================================================================
#                           RESPOSTAS PADRONIZADAS
# =============================================================================

def ok(message: str, data=None):
    """
    Resposta de sucesso (200 OK).
    
    Args:
        message (str): Mensagem descritiva do sucesso
        data: Dados a serem retornados (opcional)
    
    Returns:
        JSONResponse: Resposta formatada com status 200
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message,
            "data": data,
            "status": "success",
            "HTTPStatus": "OK",
            "HTTPStatusCode": status.HTTP_200_OK
        }
    )

def bad_request(message: str):
    """
    Resposta de requisição inválida (400 Bad Request).
    
    Args:
        message (str): Mensagem de erro descritiva
    
    Returns:
        JSONResponse: Resposta formatada com status 400
    
    Use Cases:
        - Validação de dados falhou
        - Parâmetros obrigatórios ausentes
        - Formato de dados incorreto
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": message,
            "data": None,
            "status": "error",
            "HTTPStatus": "Bad Request",
            "HTTPStatusCode": status.HTTP_400_BAD_REQUEST
        }
    )

def server_error(message: str):
    """
    Resposta de erro interno do servidor (500 Internal Server Error).
    
    Args:
        message (str): Mensagem de erro genérica
    
    Returns:
        JSONResponse: Resposta formatada com status 500
    
    Notes:
        - Evitar expor detalhes internos em produção
        - Logar detalhes do erro internamente
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": message,
            "data": None,
            "status": "error_server",
            "HTTPStatus": "Internal Server Error",
            "HTTPStatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

def acesso_negado(message: str):
    """
    Resposta de acesso negado (403 Forbidden).
    
    Args:
        message (str): Mensagem explicando a negação de acesso
    
    Returns:
        JSONResponse: Resposta formatada com status 403
    
    Use Cases:
        - Token JWT inválido ou expirado
        - Usuário não tem permissão para recurso
        - Autenticação necessária mas não fornecida
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "message": message,
            "data": None,
            "status": "access_denied",
            "HTTPStatus": "Forbidden",
            "HTTPStatusCode": status.HTTP_403_FORBIDDEN
        }
    )