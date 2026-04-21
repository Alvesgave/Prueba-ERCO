"""Módulo para manejar conexiones a PostgreSQL usando psycopg2."""
import psycopg2

class PostgresClient:
    """Cliente para manejar conexiones a una base de datos PostgreSQL."""
    def __init__(self, credentials):
        """Inicializa el cliente con las credenciales de conexión."""
        self.host = credentials['host']
        self.port = credentials['port']
        self.dbname = credentials['database']
        self.user = credentials['username']
        self.password = credentials['password']
        self.conn = None

    def connect(self):
        """Establece la conexión y la guarda en self.conn"""
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
        return self.conn

    def get_cursor(self):
        """Devuelve un cursor para ejecutar queries"""
        if self.conn is None or self.conn.closed:
            self.connect()
        return self.conn.cursor()


    def close(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Conecta solo si no hay una conexión activa."""
        if self.conn is None or self.conn.closed:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del contexto."""
        self.close()
