"""
Módulo para calcular los conceptos de una factura de energía extrayendo datos desde PostgreSQL.

Conceptos calculados:
    - EA  : Energía Activa
    - EE1 : Excedentes de Energía tipo 1
    - EE2 : Excedentes de Energía tipo 2
    - EC  : Comercialización de Excedentes de Energía
"""
from config import get_client
from fastapi import FastAPI

app = FastAPI()

@app.get("/energia_activa/id_service/{id_service}/anio/{anio}/mes/{mes}")

def energia_activa(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    query_EA = f"""SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.cu) AS ea 
            FROM consumption t1
            LEFT JOIN records t2
	            ON t1.id_record = t2.id_record
            LEFT JOIN services t3
                ON t2.id_service = t3.id_service
            LEFT JOIN tariffs t4
                ON t3.id_market = t4.id_market 
                AND t3.voltage_level = t4.voltage_level 
                AND ((t3.cdi IS NOT NULL AND t3.cdi = t4.cdi) OR (t3.cdi IS NULL AND t4.cdi IS NULL))
            WHERE t3.id_service = {id_service} AND EXTRACT(YEAR FROM t2.record_timestamp) = {anio} AND EXTRACT(MONTH FROM t2.record_timestamp) = {mes}
            GROUP BY
                1, 2, 3;"""
    cursor.execute(query_EA)
    value = cursor.fetchone()
    ea = value[3]
    return {"EA": ea}

def comercializacion_excedentes(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    query_EC = f"""SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.c) AS ec 
            FROM consumption t1
            LEFT JOIN records t2
	            ON t1.id_record = t2.id_record
            LEFT JOIN services t3
                ON t2.id_service = t3.id_service
            LEFT JOIN tariffs t4
                ON t3.id_market = t4.id_market 
                AND t3.voltage_level = t4.voltage_level 
                AND ((t3.cdi IS NOT NULL AND t3.cdi = t4.cdi) OR (t3.cdi IS NULL AND t4.cdi IS NULL))
            WHERE t3.id_service = {id_service} AND EXTRACT(YEAR FROM t2.record_timestamp) = {anio} AND EXTRACT(MONTH FROM t2.record_timestamp) = {mes}
            GROUP BY
                1, 2, 3;"""
    cursor.execute(query_EC)
    value = cursor.fetchone()
    ec = value[3]
    return {"EC": ec}

def excedentes_tuno(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    

def main():
    print(energia_activa(2256,2023,9))
    print(comercializacion_excedentes(2256,2023,9))

if __name__ == "__main__":
    main()
