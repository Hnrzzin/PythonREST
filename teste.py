import requests 

headears = { 
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiZXhwIjoxNzU1NTU5ODE2fQ.Dt3YwVfvMFIl_TWOlP7_RAag1DKm4dD1GlcmmFXpwCI",
}

requisao = requests.get("http://127.0.0.1:8000/autenticacao/refresh", headers=headears)
print(requisao)
print(requisao.json())