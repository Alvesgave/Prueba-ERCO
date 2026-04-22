"""Consultas de estadísticas de cliente y carga del sistema."""

from app.core.config import get_client

def estadisticas_cliente(id_service, anio=2023, mes=9):
    """Devuelve estadísticas agregadas de consumo e inyección para un servicio."""
    db_client = get_client()
    cursor = db_client.get_cursor()
    query = f"""
    SELECT 
        SUM(t2.value) AS total_injection, 
        AVG(t2.value) AS prom_injection, 
        MAX(t2.value) AS max_injection,
        MIN(t2.value) AS min_injection,
        SUM(t3.value) AS total_consumo, 
        AVG(t3.value) AS prom_consumo, 
        MAX(t3.value) AS max_consumo, 
        MIN(t3.value) AS min_consumo
    FROM records t1
    LEFT JOIN injection t2 ON t1.id_record = t2.id_record
    LEFT JOIN consumption t3 ON t1.id_record = t3.id_record
    WHERE t1.id_service = {id_service} 
        AND EXTRACT(YEAR FROM t1.record_timestamp) = {anio} 
        AND EXTRACT(MONTH FROM t1.record_timestamp) = {mes};
    """
    cursor.execute(query)
    value = cursor.fetchone()
    stats = {
        "inyeccion_total": float(value[0]),
        "inyeccion_promedio": float(value[1]),
        "inyeccion_max": float(value[2]),
        "inyeccion_min": float(value[3]),
        "consumo_total": float(value[4]),
        "consumo_promedio": float(value[5]),
        "consumo_max": float(value[6]),
        "consumo_min": float(value[7])
    }
    return stats

def carga_sistema(anio=2023, mes=9):
    """Calcula la carga del sistema de un mes por hora: consumo - inyección."""
    db_client = get_client()
    cursor = db_client.get_cursor()
    query = f"""
    SELECT 	
        t1.record_timestamp, 
        SUM(t2.value-t3.value) AS carga_sistema 
    FROM records t1
    LEFT JOIN consumption t2 ON t1.id_record = t2.id_record
    LEFT JOIN injection t3 ON t1.id_record = t3.id_record
    WHERE EXTRACT(YEAR FROM t1.record_timestamp) = {anio} 
          AND EXTRACT(MONTH FROM t1.record_timestamp) = {mes}
    GROUP BY
        1
    ORDER BY
        1; 
    """
    cursor.execute(query)
    results = cursor.fetchall()
    carga_horaria = [{"timestamp": str(row[0]), "carga": float(row[1])} for row in results]
    return carga_horaria

