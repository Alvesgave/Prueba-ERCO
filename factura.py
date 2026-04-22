"""
Módulo para calcular los conceptos de una factura de energía extrayendo datos desde PostgreSQL.

Conceptos calculados:
    - EA  : Energía Activa
    - EE1 : Excedentes de Energía tipo 1
    - EE2 : Excedentes de Energía tipo 2
    - EC  : Comercialización de Excedentes de Energía
"""

from config import get_client

def energia_activa(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    query_EA = f"""
        SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.cu) AS ea 
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
            1, 2, 3;
        """
    cursor.execute(query_EA)
    value = cursor.fetchone()
    ea = float(value[3])
    return {"EA": ea}

def comercializacion_excedentes(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    query_EC = f"""
        SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.c) AS ec 
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
            1, 2, 3;
        """
    cursor.execute(query_EC)
    value = cursor.fetchone()
    ec = float(value[3])
    return {"EC": ec}

def excedentes_tuno(id_service, anio=2023, mes=9):
    db_client = get_client()
    cursor = db_client.get_cursor()
    query_EE1 = f"""
        SELECT t1.id_service, EXTRACT(YEAR FROM t1.record_timestamp) AS anio, EXTRACT(MONTH FROM t1.record_timestamp) AS mes, 
        SUM(t2.value) AS injection, SUM(t3.value) AS consumption, CASE WHEN SUM(t2.value)>SUM(t3.value) THEN SUM(t3.value*t5.cu*-1) ELSE SUM(t2.value*t5.cu*-1)
        END AS ee1
        FROM records t1
        LEFT JOIN injection t2
            ON t1.id_record = t2.id_record
        LEFT JOIN consumption t3
            ON t1.id_record = t3.id_record
        LEFT JOIN services t4
            ON t1.id_service = t4.id_service
        LEFT JOIN tariffs t5
            ON t4.id_market = t5.id_market 
            AND t4.voltage_level = t5.voltage_level 
            AND ((t4.cdi IS NOT NULL AND t4.cdi = t5.cdi) OR (t4.cdi IS NULL AND t5.cdi IS NULL))
        WHERE t1.id_service = {id_service} AND EXTRACT(YEAR FROM t1.record_timestamp) = {anio} AND EXTRACT(MONTH FROM t1.record_timestamp) = {mes}    
        GROUP BY
            1, 2, 3;
        """
    cursor.execute(query_EE1)
    value = cursor.fetchone()
    ee1 = float(value[5])
    return {"EE1": ee1}

def excedentes_tdos(id_service, anio=2023, mes=9):
    db_client=get_client()
    cursor = db_client.get_cursor()
    query_EE2 = f"""
        WITH ee1_diario AS (SELECT t1.id_service, EXTRACT(YEAR FROM t1.record_timestamp) AS anio, EXTRACT(MONTH FROM t1.record_timestamp) AS mes, 
        EXTRACT(DAY FROM t1.record_timestamp) AS dia,
        SUM(t2.value) AS injection, SUM(t3.value) AS consumption, CASE WHEN SUM(t2.value)>SUM(t3.value) THEN SUM(t3.value) ELSE SUM(t2.value)
        END AS ee1
        FROM records t1
        LEFT JOIN injection t2
            ON t1.id_record = t2.id_record
        LEFT JOIN consumption t3
            ON t1.id_record = t3.id_record	
        GROUP BY
            1, 2, 3, 4), 

        tbl_acumulado AS (

        SELECT t1.id_service, t1.record_timestamp, t2.value AS injection, t3.value AS consumption, 
        SUM(t2.value) OVER(PARTITION BY t1.id_service, EXTRACT(YEAR FROM t1.record_timestamp), EXTRACT(MONTH FROM t1.record_timestamp), EXTRACT(DAY FROM t1.record_timestamp) 
        ORDER BY t1.record_timestamp ASC) AS acumulado_inj, t4.ee1, t5.value AS tarifa_xm
        FROM records t1
        LEFT JOIN injection t2
            ON t1.id_record = t2.id_record
        LEFT JOIN consumption t3
            ON t1.id_record = t3.id_record
        LEFT JOIN ee1_diario t4
            ON t1.id_service = t4.id_service AND EXTRACT(YEAR FROM t1.record_timestamp) = t4.anio AND EXTRACT(MONTH FROM t1.record_timestamp) = t4.mes AND EXTRACT(DAY FROM t1.record_timestamp) = t4.dia
        LEFT JOIN xm_data_hourly_per_agent t5
            ON t5.record_timestamp = t1.record_timestamp),

        tbl_final AS (
        SELECT t1.*, 
        CASE WHEN t1.acumulado_inj < t1.ee1 THEN 0.0 
        ELSE LEAST(t1.acumulado_inj - t1.ee1, t1.injection) END AS exceso_ee2
        FROM tbl_acumulado t1)

        SELECT id_service, EXTRACT(YEAR FROM record_timestamp) AS anio, EXTRACT(MONTH FROM record_timestamp) AS mes, SUM(exceso_ee2) AS exceso, SUM(exceso_ee2*tarifa_xm) AS ee2 FROM tbl_final
        WHERE id_service = {id_service} AND EXTRACT(YEAR FROM record_timestamp) = {anio} AND EXTRACT(MONTH FROM record_timestamp) = {mes}
        GROUP BY 1, 2, 3;
        """
    cursor.execute(query_EE2)
    value = cursor.fetchone()
    ee2 = float(value[4])
    return {"EE2": ee2}