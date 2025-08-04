from fastapi import FastAPI

app = FastAPI()

from contatos import router

app.include_router(router) #inclui as rotas no aplicativo FastAPI

