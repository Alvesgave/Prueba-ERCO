from conexion import PostgresClient

def get_credentials():
    creds = {'host': 'localhost',
             'port': 5432,
             'database': 'erco',
             'username': 'postgres',
             'password': ''}
    return creds

def get_client():
    credentials = get_credentials()
    db_client = PostgresClient()
    db_client.connect(credentials)
    return db_client
