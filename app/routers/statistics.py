"""Router de endpoints de estadísticas y carga del sistema."""

from fastapi import APIRouter

from app.services.statistics import (
    estadisticas_cliente,
    carga_sistema
)   

router = APIRouter(tags=["Statistics"])

@router.get("/client-statistics/{id_service}")
def client_statistics(id_service: int, anio: int = 2023, mes: int = 9):
    """Endpoint para obtener estadísticas de consumo e inyección de un servicio."""
    stats = estadisticas_cliente(id_service, anio, mes)
    return {
        "id_servicio": id_service,
        "anio": anio,
        "mes": mes,
        "estadisticas": stats
    }

@router.get("/system-load/")
def system_load(anio: int = 2023, mes: int = 9):
    """Endpoint para obtener la carga del sistema (consumo-inyeccion)."""
    load = carga_sistema(anio, mes)
    return {
        "anio": anio,
        "mes": mes,
        "carga": load
    }