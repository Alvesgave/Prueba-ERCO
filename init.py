from config import get_client

def read_sql(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo_sql:
        sql = archivo_sql.read()

    sentencias = sql.split(';')

    return sentencias

def _execute_query(db_client, query):
    cursor = db_client.get_cursor()
    cursor.execute(query)
    db_client.conn.commit()

def execute_queries(db_client, queries):
    for query in queries:
        _execute_query(db_client, query)

def fill_data(tabla, ruta_csv, db_client):
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        cursor = db_client.get_cursor()
        cursor.copy_expert(
            f"COPY {tabla} FROM STDIN WITH CSV HEADER DELIMITER ','", 
            f
        )
        db_client.conn.commit()

def main():

    """Creación de las tablas dentro de la base de datos"""
    db_client = get_client()
    queries = read_sql('Database/create_database.sql')
    execute_queries(db_client, queries)

    """Llenar las tablas dentro de la base de datos"""
    fill_data('tariffs', 'Data/tariffs 4.csv', db_client)
    fill_data('services', 'Data/services 4.csv', db_client)
    fill_data('xm_data_hourly_per_agent', 'Data/xm_data_hourly_per_agent 4.csv', db_client)
    fill_data('records', 'Data/records 4.csv', db_client)
    fill_data('injection', 'Data/injection 4.csv', db_client)
    fill_data('consumption', 'Data/consumption 4.csv', db_client)



if __name__ == "__main__":
    main()

