import mysql.connector

def entrarBanco():
   
    try:
        global conexao
        conexao = mysql.connector.connect(
            host='localhost',   
            user='root',
            password='Henry45*1',
            database='contacts',
            auth_plugin ='mysql_native_password'
            )

        if conexao.is_connected():
            global tbltemp
            infbanco = conexao.get_server_info()
            
            tbltemp = conexao.cursor()
            tbltemp.execute('SELECT DATABASE()')
            nameBanco = tbltemp.fetchone()  
            global tabletupla
            return {"mensagem": f"Conectado ao banco de dados: {nameBanco[0]}"}
        else:
            return {"mensagem": "Erro ao conectar ao banco de dados."}

    except Exception as error:
        return {"mensagem":"Erro ao conectar ao banco de dados:" + str(error)}

def fecharConexao():
    if conexao.is_connected():
        tbltemp.close()
        conexao.close()
        return {"mensagem": "Conexão com o banco de dados fechada."}
    else:
        return {"mensagem": "Nenhuma conexão aberta para fechar."}

def postContato(nome: str, email: str, telefone: str):
    try:
        entrarBanco()
        tbltemp = conexao.cursor(dictionary=True)  # dictionary=True para acessar por nome da coluna
        
        # Verifica telefone
        tbltemp.execute("SELECT * FROM info WHERE telefone = %s", (telefone,))
        if tbltemp.fetchone():  # Retorna 1 registro ou None
            return {"mensagem": "Telefone já cadastrado."}
        
        # Verifica email
        tbltemp.execute("SELECT * FROM info WHERE email = %s", (email,))
        if tbltemp.fetchone():
            return {"mensagem": "Email já cadastrado."}
        
        # Se chegou até aqui, pode inserir
        tbltemp.execute(
            "INSERT INTO info (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone)
        )
        conexao.commit()
        
        return {"mensagem": "Contato criado com sucesso!"}
    
    except Exception as error:
        return {"mensagem": "Erro ao criar contato: " + str(error)}
    
    finally:
        fecharConexao()