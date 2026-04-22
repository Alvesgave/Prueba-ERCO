"""
Módulo para API RESTful para el cálculo de facturación de energía (FastAPI).

Endpoints:
    POST /calculate-invoice                → Factura completa (EA + EC + EE1 + EE2)
    GET  /client-statistics/{id_servicio}   → Estadísticas de consumo e inyección
    GET  /system-load                      → Carga del sistema por hora del día
    GET  /invoice/ea|ec|ee1|ee2/{id_servicio} → Concepto individual

"""
from fastapi import FastAPI
from app.routers import invoice, statistics

app = FastAPI(title="ERCO - API de Facturación de Energía")

app.include_router(invoice.router)
app.include_router(statistics.router)

def main():
    return

if __name__ == "__main__":
    main()
