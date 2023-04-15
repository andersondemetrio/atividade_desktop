import sqlite3

from model.model import Cliente


class DataBase:
    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_cliente(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS NOTEPAD(
            ID TEXT,
            TITULO_DA_NOTA TEXT,
            NOTA TEXT,
            PRIMARY KEY (ID)             
            );
            """)
        self.close_connection()

    def registrar_cliente(self, cliente):
        self.connect()
        cursor = self.connection.cursor()
        campos_cliente = ('ID', 'TITULO_DA_NOTA', 'NOTA')
        valores = f"'{str(cliente.ID).replace('.', '').replace('-', '')}', '{cliente.Titulo_da_nota}', '{cliente.nota}'"
        try:
            cursor.execute(f"""INSERT INTO NOTEPAD {campos_cliente} VALUES ({valores})""")
            self.connection.commit()
            return 'Ok'

        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def consultar_cliente(self, ID):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT * FROM NOTEPAD WHERE ID = '{str(ID).replace('.', '').replace('-', '')}'""")
            return cursor.fetchone()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()

    def consultar_todos_clientes(self):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM NOTEPAD")
            clientes = cursor.fetchall()
            return clientes
        except sqlite3.Error as e:
            print(f'Erro{e}')
            return None
        finally:
            self.close_connection()

    def deletar_cliente(self, ID):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""DELETE FROM NOTEPAD WHERE ID = '{str(ID).replace('.', '').replace('-', '')}'""")
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def atualizar_cliente(self, cliente):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE NOTEPAD SET
                 ID = '{cliente.ID}',
                 TITULO_DA_NOTA = '{cliente.Titulo_da_nota}',
                 NOTA = '{cliente.nota}'
                 WHERE ID = '{str(cliente.ID).replace('.', '').replace('-', '')}'""")

            self.connection.commit()
            return 'OK'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

