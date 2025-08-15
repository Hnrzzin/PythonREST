from fastapi import status
from fastapi.responses import JSONResponse
#=======================================================================
#                Mensagem de sucesso, erro e acesso negado
#========================================================================
def ok(message: str, data=None):
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
