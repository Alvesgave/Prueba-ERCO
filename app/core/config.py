"""
Módulo para manejar las cofiguraciones del aplicativo
"""

from app.db.connection import PostgresClient

def get_credentials():
    """Devuelve las credenciales de PostgreSQL para conectarse"""
    creds = {'host': 'localhost',
             'port': 5432,
             'database': 'erco',
             'username': 'postgres',
             'password': ''}
    return creds

def get_client():
    """Devuelve el cliente de PostgreSQL a partir de la clase PostgresClient"""
    credentials = get_credentials()
    db_client = PostgresClient(credentials)
    return db_client
