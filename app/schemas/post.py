"""Modelos Pydantic para los endpoints de factura."""
from pydantic import BaseModel


class SolicitudFactura(BaseModel):
    """Cuerpo del POST /calculate-invoice: identifica servicio y período."""
    id_servicio: int
    anio: int = 2023
    mes: int = 9