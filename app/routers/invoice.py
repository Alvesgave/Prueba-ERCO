"""Modulo para Router de endpoints de facturación."""
from fastapi import APIRouter

from app.schemas.post import SolicitudFactura
from app.services.invoice import (
    energia_activa,
    comercializacion_excedentes,
    excedentes_tuno,
    excedentes_tdos,
)

router = APIRouter(tags=["Invoice"])

@router.post("/calculate-invoice/")
def calcular_factura(req: SolicitudFactura):
    """Calcula los conceptos de la factura de un servicio en un período dado."""
    id_service = req.id_servicio
    anio = req.anio
    mes = req.mes
    
    ea = energia_activa(id_service, anio, mes)
    ec = comercializacion_excedentes(id_service, anio, mes)
    ee1 = excedentes_tuno(id_service, anio, mes)
    ee2 = excedentes_tdos(id_service, anio, mes)
    
    return {
        "id_servicio": req.id_servicio,
        "anio": req.anio,
        "mes": req.mes,
        "EA":  ea["EA"],
        "EC":  ec["EC"],
        "EE1": ee1["EE1"],
        "EE2": ee2["EE2"],
        "total": ea["EA"] + ec["EC"] + ee1["EE1"] + ee2["EE2"]
    }

@router.get("/energia_activa/")
def energia_activa_endpoint(id_service: int, anio: int = 2023, mes: int = 9):
    ea = energia_activa(id_service, anio, mes)
    return {
        "id_servicio": id_service,
        "anio": anio,
        "mes": mes,
        "EA":  ea["EA"]
    }

@router.get("/comercializacion_excedentes/")
def comercializacion_excedentes_endpoint(id_service: int, anio: int = 2023, mes: int = 9):
    ec = comercializacion_excedentes(id_service, anio, mes)
    return {
        "id_servicio": id_service,
        "anio": anio,
        "mes": mes,
        "EC":  ec["EC"]
    }

@router.get("/excedentes_tuno/")
def excedentes_tuno_endpoint(id_service: int, anio: int = 2023, mes: int = 9):
    ee1 = excedentes_tuno(id_service, anio, mes)
    return {
        "id_servicio": id_service,
        "anio": anio,
        "mes": mes,
        "EE1":  ee1["EE1"]
    }

@router.get("/excedentes_tdos/")
def excedentes_tdos_endpoint(id_service: int, anio: int = 2023, mes: int = 9):
    ee2 = excedentes_tdos(id_service, anio, mes)
    return {
        "id_servicio": id_service,
        "anio": anio,
        "mes": mes,
        "EE2":  ee2["EE2"]
    }