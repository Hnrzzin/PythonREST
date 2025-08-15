import mysql.connector
from response import ok, bad_request, server_error
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

#=======================================================================
#                   Importa as variáveis de ambiente
#========================================================================
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#=======================================================================
#                Funçoes para manipulação do banco de dados
#========================================================================
#=======================================================================
#                Abre e fecha a conexão com o banco de dados
#========================================================================
def entrarBanco():
   
    try:
        global conexao
        conexao = mysql.connector.connect(
            host='localhost',   
            user='root',
            password='Henry45*', # Certifique-se de que esta senha está correta ou use variáveis de ambiente
            database='contacts',
            auth_plugin ='mysql_native_password'
            )

        if conexao.is_connected():
            global tbltemp
            infbanco = conexao.get_server_info()
            
            tbltemp = conexao.cursor()
            tbltemp.execute('SELECT DATABASE()')
            nameBanco = tbltemp.fetchone()  
            global tabletupla # Esta variável não está sendo usada, pode ser removida se não for necessária
            return {"mensagem": f"Conectado ao banco de dados: {nameBanco[0]}"}
        else:
            return {"mensagem": "Erro ao conectar ao banco de dados."}

    except Exception as error:
        return {"mensagem":"Erro ao conectar ao banco de dados:" + str(error)}

def fecharConexao():
    if 'conexao' in globals() and conexao.is_connected(): # Verifica se 'conexao' existe e está conectada
        tbltemp.close()
        conexao.close()
        return {"mensagem": "Conexão com o banco de dados fechada."}
    else:
        return {"mensagem": "Nenhuma conexão aberta para fechar."}

#=======================================================================
#                   Cria e manipula os contatos
#========================================================================
def postContato(nome: str, email: str, telefone: str):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)  # dictionary=True para acessar por nome da coluna
        
        # Verifica telefone
        tbltemp.execute("SELECT * FROM info WHERE telefone = %s", (telefone,))
        if tbltemp.fetchone():  # Retorna 1 registro ou None
            return bad_request("Telefone já cadastrado.")
        
        # Verifica email
        tbltemp.execute("SELECT * FROM info WHERE email = %s", (email,))
        if tbltemp.fetchone():
            return bad_request("Email já cadastrado.")
        
        # Se chegou até aqui, pode inserir
        tbltemp.execute(
            "INSERT INTO info (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone)
        )
        conexao.commit()
        
        return ok("Contato criado com sucesso.", {"nome": nome, "email": email, "telefone": telefone})
    
    except Exception as error:
        return server_error(f"Erro ao inserir contato: {str(error)}")
    
    finally:
        fecharConexao()
#=======================================================================

#=======================================================================    
def getContatos():
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        tbltemp.execute("SELECT * FROM info")
        contatos = tbltemp.fetchall()
        return ok("Contatos listados com sucesso.", contatos)
    except Exception as error:
        return server_error(f"Erro ao listar contatos: {str(error)}")
    finally:
        fecharConexao()
#=======================================================================

#=======================================================================  
def getContatoById(contato_id: int):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        tbltemp.execute("SELECT * FROM info WHERE id = %s", (contato_id,))
        contato = tbltemp.fetchone()
        if contato:
            return ok("Contato encontrado.", contato)
        else:
            return bad_request("Contato não encontrado.")
    except Exception as error:
        return server_error(f"Erro ao obter contato: {str(error)}")
    finally:
        fecharConexao()
#=======================================================================

#=======================================================================          
def updateContato(contato_id: int, nome: str = None, email: str = None, telefone: str = None):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        
        # Verifica se o contato existe
        tbltemp.execute("SELECT * FROM info WHERE id = %s", (contato_id,))
        if not tbltemp.fetchone():
            return bad_request("Contato não encontrado.")
        
        # Monta a query dinamicamente para atualizar apenas os campos fornecidos
        updates = []
        params = []
        if nome:
            updates.append("nome = %s")
            params.append(nome)
        if email:
            updates.append("email = %s")
            params.append(email)
        if telefone:
            updates.append("telefone = %s")
            params.append(telefone)
        
        if not updates:
            return bad_request("Nenhum campo para atualizar.")
        
        params.append(contato_id)
        query = f"UPDATE info SET {', '.join(updates)} WHERE id = %s"
        tbltemp.execute(query, tuple(params))
        conexao.commit()
        
        return ok("Contato atualizado com sucesso.")
    
    except Exception as error:
        return server_error(f"Erro ao atualizar contato: {str(error)}")
    
    finally:
        fecharConexao()
#=======================================================================

#=======================================================================          
def deleteContato(contato_id: int):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        
        # Verifica se o contato existe
        tbltemp.execute("SELECT * FROM info WHERE id = %s", (contato_id,))
        if not tbltemp.fetchone():
            return bad_request("Contato não encontrado.")
        
        # Deleta o contato
        tbltemp.execute("DELETE FROM info WHERE id = %s", (contato_id,))
        conexao.commit()
        
        return ok("Contato deletado com sucesso.")
    
    except Exception as error:
        return server_error(f"Erro ao deletar contato: {str(error)}")
    
    finally:
        fecharConexao()
#=======================================================================
#                          Cria os usuários
#=======================================================================      
def postUsuario(nome: str, email: str, senha_hash: str):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)  # dictionary=True para acessar por nome da coluna
        
        # Verifica email
        tbltemp.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if tbltemp.fetchone():
            return bad_request("Email já cadastrado.")
        
        # Se chegou até aqui, pode inserir
        tbltemp.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )
        conexao.commit()
        
        return ok("Usuário criado com sucesso.", {"nome": nome, "email": email})
    
    except Exception as error:
        return server_error(f"Erro ao inserir usuário: {str(error)}")
    
    finally:
        fecharConexao()
#=======================================================================
#                         Faz o login do usuário
#=======================================================================      
def loginUsuario(email: str):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        
        # Busca usuário pelo email
        tbltemp.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario_login = tbltemp.fetchone()
        
        if not usuario_login:
            return None  # Retorna None se não existe usuário
        
        return usuario_login  # Retorna o dict completo: id, nome, email, senha_hash
    
    except Exception as error:
        return None  
    
    finally:
        fecharConexao()
#=======================================================================
#            Busca o usuário pelo ID (usado para verificar token)
#=======================================================================  
def getUsuarioById(usuario_id: int): # É chamada para verificar o usuário do token
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)
        
        tbltemp.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = tbltemp.fetchone()
        
        if usuario:
            return usuario  # Retorna o dict completo: id, nome, email, senha_hash
        else:
            return None
    except Exception as error:
        return None
    finally:
        fecharConexao()

