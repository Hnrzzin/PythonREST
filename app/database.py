import mysql.connector

def entrarBanco():
   
    try:
        global conexao
        conexao = mysql.connector.connect(
            host='localhost',   
            user='root',
            password='Henry45*1',
            database='univap',
            auth_plugin ='mysql_native_password'
            )

        if conexao.is_connected():
            global tbltemp
            infbanco = conexao.get_server_info()
            print(f'Conectado ao MySQL Server versão {infbanco}')
            print('Conexão bem-sucedida!')
            tbltemp = conexao.cursor()
            tbltemp.execute('SELECT DATABASE()')
            nameBanco = tbltemp.fetchone()
            for nome in nameBanco:
                print(f'Você está conectado ao banco de dados: {nome}')
            print ('--'*60)
            global tabletupla
        else:
            print('Erro ao conectar ao banco de dados.')

    except Exception as error:
        print(f'Erro ao conectar ao banco de dados: {error}')
        
def sairBanco():
    try:
        if conexao.is_connected():
            tbltemp.close()
            conexao.close()
            print('Conexão com o banco de dados encerrada.')
        else:
            print('Nenhuma conexão ativa para encerrar.')
    except Exception as error:
        print(f'Erro ao encerrar a conexão: {error}')