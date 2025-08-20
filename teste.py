"""
Script de Teste Manual - API RESTful

Script para testes manuais dos endpoints da API usando requests.
Útil para desenvolvimento e debug rápido.

Autor: Henrique Teixeira
Data: 2024-01-15

Uso:
    python teste.py

Notas:
    - Substituir token JWT por um válido
    - Verificar se a API está rodando (normalmente http://127.0.0.1:8000)
    - Usar apenas para desenvolvimento
"""

import requests

# Configuração do headers com token de autenticação
headers = { 
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiZXhwIjoxNzU1NTU5ODE2fQ.Dt3YwVfvMFIl_TWOlP7_RAag1DKm4dD1GlcmmFXpwCI",
}

# Realiza requisição GET para endpoint de refresh token
requisicao = requests.get("http://127.0.0.1:8000/autenticacao/refresh", headers=headers)

# Exibe resultados da requisição
print("Status Code:", requisicao.status_code)
print("Resposta JSON:", requisicao.json())

# Exemplo de saída esperada:
# Status Code: 200
# Resposta JSON: {'message': 'Token atualizado com sucesso.', 'data': {...}, ...}