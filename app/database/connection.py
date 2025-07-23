import mysql.connector

class Database:
    def __init__(self):
        self.conexao = None
        self.cursor = None

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
                self.cursor = self.conexao.cursor()
                print(f'Conectado ao MySQL Server versão {self.conexao.get_server_info()}')
                self.cursor.execute('SELECT DATABASE()')
                db_name = self.cursor.fetchone()
                print(f'Você está conectado ao banco de dados: {db_name[0]}')
                print('--'*30)
            else:
                print('Erro ao conectar ao banco de dados.')

        except mysql.connector.Error as err:
            print(f'Erro ao conectar ao banco de dados: {err}')

    def sair_banco(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexao:
                self.conexao.close()
            print('Conexão com o banco encerrada com sucesso.')
        except mysql.connector.Error as err:
            print(f'Erro ao encerrar a conexão: {err}')