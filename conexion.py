"""Módulo para manejar conexiones a PostgreSQL usando psycopg2."""
import psycopg2

class PostgresClient:
    """Cliente para manejar conexiones a una base de datos PostgreSQL."""
    def _init_(self):
        """Inicializa el cliente con las credenciales de conexión."""
        self.host = None
        self.port = None
        self.dbname = None
        self.user = None
        self.password = None
        self.conn = None

    def connect(self, credentials):
        """Establece la conexión y la guarda en self.conn"""
        try:
            self.host = credentials['host']
            self.port = credentials['port']
            self.dbname = credentials['database']
            self.user = credentials['username']
            self.password = credentials['password']

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return self.conn
        except Exception as err:
            raise

    def get_cursor(self):
        """Devuelve un cursor para ejecutar queries"""
        try:
            if self.conn is None:
                self.connect()
            return self.conn.cursor()
        except Exception as err:
            raise

    def close(self):
        """Cierra la conexión"""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
        except Exception as err:
            raise

    def _exit_(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del contexto."""
        self.close()