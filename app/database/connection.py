import mysql.connector

class Database:
    def __init__(self):
        self.conexao = None #acesso ao banco de dados
        self.tbltemp = None #tabela temporaria

    def entrar_banco(self):
        try:
            self.conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Henry45*1',
                database='contacts',
                auth_plugin='mysql_native_password'
            )
            if self.conexao.is_connected():
                self.tbltemp = self.conexao.cursor()
                print(f'Conectado ao MySQL Server versão {self.conexao.get_server_info()}')
                self.tbltemp.execute('SELECT DATABASE()')
                db_name = self.tbltemp.fetchone()
                print(f'Você está conectado ao banco de dados: {db_name[0]}')
                print('--'*30)
            else:
                print('Erro ao conectar ao banco de dados.')

        except mysql.connector.Error as err:
            print(f'Erro ao buscar contatos: {err} ({type(err)})')
            return []

    def sair_banco(self):
        try:
            if self.tbltemp is not None and not callable(self.tbltemp): #callable verifica se o cursor (tbltemp) é uma função
                self.tbltemp.close()
            if self.conexao is not None and not callable(self.conexao):
                self.conexao.close()
            print('Conexão com o banco encerrada com sucesso.')
        except mysql.connector.Error as err:
            print(f'Erro ao encerrar a conexão: {err}')
            
    def todos_contatos(self):
        try:
            self.entrar_banco()
            self.tbltemp.execute('SELECT * FROM info;')
            contatos = self.tbltemp.fetchall()
            return contatos
        except mysql.connector.Error as err:
            print(f'Erro ao buscar contatos: {err} ({type(err)})')
            raise
        finally:
            self.sair_banco()