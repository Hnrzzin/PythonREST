"""
Módulo de Acesso ao Banco de Dados - Operações CRUD

Fornece funções para manipulação das tabelas 'usuarios' e 'info'
com tratamento de erros e gerenciamento de conexões.

Responsabilidades:
    - Gerenciamento de conexões MySQL
    - Operações de usuários (criação, login, busca)
    - Operações de contatos (CRUD completo)
    - Validação de integridade de dados

Autor: Henrique Teixeira
Versão: 1.0.0
Data: 2024-01-15

Estrutura do Banco:
    - usuarios: id, nome, email, senha_hash
    - info: id, nome, email, telefone, usuario_id (FK)
"""

import mysql.connector
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# =============================================================================
#                           CONFIGURAÇÃO
# =============================================================================

# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Configura contexto de criptografia para senhas
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================================================================
#                       GERENCIAMENTO DE CONEXÕES
# =============================================================================

def entrarBanco():
    """
    Estabelece conexão com o banco de dados MySQL.
    
    Returns:
        tuple: (conexao, cursor) se bem-sucedido, (None, None) em caso de erro
    
    Raises:
        Exception: Erros de conexão com o banco são silenciados para evitar
                   exposição de detalhes internos
    """
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Henry45*1',  # Considerar usar variável de ambiente
            database='contacts',
            auth_plugin='mysql_native_password'
        )

        if conexao.is_connected():
            cursor = conexao.cursor(dictionary=True)  # Retorna resultados como dicionários
            return conexao, cursor
        return None, None

    except Exception as error:
        # Em produção, registrar o erro em logs
        return None, None

def fecharConexao(conexao, cursor):
    """
    Fecha conexão e cursor do banco de dados de forma segura.
    
    Args:
        conexao: Objeto de conexão MySQL
        cursor: Objeto cursor MySQL
    
    Notes:
        - Verifica se a conexão existe e está ativa antes de fechar
        - Operação silenciosa (não levanta exceções)
    """
    if conexao and conexao.is_connected():
        cursor.close()
        conexao.close()

# =============================================================================
#                           OPERAÇÕES DE CONTATOS
# =============================================================================

def postContato(nome: str, email: str, telefone: str, usuario_id: int):
    """
    Cria um novo contato associado a um usuário.
    
    Args:
        nome (str): Nome do contato
        email (str): Email do contato
        telefone (str): Telefone do contato (apenas números)
        usuario_id (int): ID do usuário proprietário
    
    Returns:
        dict: Dados do contato criado ou None em caso de erro/duplicata
    
    Validations:
        - Verifica duplicatas de telefone
        - Verifica duplicatas de email
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
        
        # Verifica duplicatas de telefone
        cursor.execute("SELECT * FROM info WHERE telefone = %s", (telefone,))
        if cursor.fetchone():
            return None  # Telefone já existe
        
        # Verifica duplicatas de email
        cursor.execute("SELECT * FROM info WHERE email = %s", (email,))
        if cursor.fetchone():
            return None  # Email já existe
        
        # Insere novo contato
        cursor.execute(
            "INSERT INTO info (nome, email, telefone, usuario_id) VALUES (%s, %s, %s, %s)",
            (nome, email, telefone, usuario_id)
        )
        conexao.commit()
        
        # Retorna dados do contato criado
        return {
            "id": cursor.lastrowid,
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "usuario_id": usuario_id
        }
    
    except Exception as error:
        # Rollback implícito pela desconexão
        return None
    
    finally:
        # Garante fechamento da conexão
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def getContatos(usuario_id: int):
    """
    Recupera todos os contatos de um usuário.
    
    Args:
        usuario_id (int): ID do usuário proprietário
    
    Returns:
        list: Lista de contatos ou None em caso de erro
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
            
        cursor.execute("SELECT * FROM info WHERE usuario_id = %s", (usuario_id,))
        return cursor.fetchall()
    except Exception as error:
        return None
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def getContatoById(contato_id: int, usuario_id: int):
    """
    Recupera um contato específico pelo ID com verificação de propriedade.
    
    Args:
        contato_id (int): ID do contato
        usuario_id (int): ID do usuário proprietário
    
    Returns:
        dict: Dados do contato ou None se não encontrado/erro
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
            
        cursor.execute("SELECT * FROM info WHERE id = %s AND usuario_id = %s", (contato_id, usuario_id))
        return cursor.fetchone()
    except Exception as error:
        return None
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def updateContato(contato_id: int, usuario_id: int, nome: str = None, email: str = None, telefone: str = None):
    """
    Atualiza um contato existente com campos opcionais.
    
    Args:
        contato_id (int): ID do contato
        usuario_id (int): ID do usuário proprietário
        nome (str, optional): Novo nome
        email (str, optional): Novo email
        telefone (str, optional): Novo telefone
    
    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return False
        
        # Verifica existência e propriedade do contato
        cursor.execute("SELECT * FROM info WHERE id = %s AND usuario_id = %s", (contato_id, usuario_id))
        if not cursor.fetchone():
            return False
        
        # Constrói query dinamicamente com campos fornecidos
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
        
        # Se nenhum campo para atualizar
        if not updates:
            return False
        
        # Adiciona condições WHERE
        params.extend([contato_id, usuario_id])
        query = f"UPDATE info SET {', '.join(updates)} WHERE id = %s AND usuario_id = %s"
        
        cursor.execute(query, tuple(params))
        conexao.commit()
        
        return True
    
    except Exception as error:
        return False
    
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def deleteContato(contato_id: int, usuario_id: int):
    """
    Exclui um contato com verificação de propriedade.
    
    Args:
        contato_id (int): ID do contato
        usuario_id (int): ID do usuário proprietário
    
    Returns:
        bool: True se excluído com sucesso, False caso contrário
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return False
        
        # Verifica existência e propriedade antes de excluir
        cursor.execute("SELECT * FROM info WHERE id = %s AND usuario_id = %s", (contato_id, usuario_id))
        if not cursor.fetchone():
            return False
        
        # Executa exclusão
        cursor.execute("DELETE FROM info WHERE id = %s AND usuario_id = %s", (contato_id, usuario_id))
        conexao.commit()
        
        return True
    
    except Exception as error:
        return False
    
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

# =============================================================================
#                           OPERAÇÕES DE USUÁRIOS
# =============================================================================

def postUsuario(nome: str, email: str, senha_hash: str):
    """
    Cria um novo usuário no sistema.
    
    Args:
        nome (str): Nome do usuário
        email (str): Email do usuário
        senha_hash (str): Senha já hasheada
    
    Returns:
        dict: Dados do usuário criado ou None em caso de erro/duplicata
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
        
        # Verifica duplicata de email
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return None
        
        # Insere novo usuário
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )
        conexao.commit()
        
        # Retorna dados do usuário criado (sem senha)
        return {
            "id": cursor.lastrowid,
            "nome": nome,
            "email": email
        }
    
    except Exception as error:
        return None
    
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def loginUsuario(email: str):
    """
    Busca um usuário pelo email para operações de login.
    
    Args:
        email (str): Email do usuário
    
    Returns:
        dict: Dados completos do usuário (incluindo senha_hash) ou None
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
            
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        return cursor.fetchone()
    
    except Exception as error:
        return None
    
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)

def getUsuarioById(usuario_id: int):
    """
    Busca um usuário pelo ID para verificação de token.
    
    Args:
        usuario_id (int): ID do usuário
    
    Returns:
        dict: Dados do usuário ou None se não encontrado
    """
    try:
        conexao, cursor = entrarBanco()
        if not conexao:
            return None
            
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        return cursor.fetchone()
    except Exception as error:
        return None
    finally:
        if 'conexao' in locals():
            fecharConexao(conexao, cursor)