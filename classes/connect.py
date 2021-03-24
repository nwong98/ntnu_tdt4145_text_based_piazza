import mysql.connector

class Database:
    def __init__(self):
        self._conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="AbA.,.123"
        )
        self._cursor = self._conn.cursor()

    def __enter__(self):
        """__enter__ and __exit__ methods
        - Used with Python to handle with statements in code.
        Connection to database will automatically close after each with statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property #decorator in Python that allows us to use function as object property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute('USE db')
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def execute_script(self, filename):
        """Execute multiple sql commands sequently

        Args:
            filename (txt): path to script to be excecuted
        """
        with open(filename, 'r') as f:
            sql_file = f.read()
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            try:
                if command.strip() != '':
                    self.cursor.execute(command)
            except:
                print("Command skipped: ")