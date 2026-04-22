"""
Módulo para ...

"""
from config import get_client

from factura import (
    energia_activa,
    comercializacion_excedentes,
    excedentes_tuno,
    excedentes_tdos
)
from fastapi import FastAPI

app = FastAPI()

@app.get("/energia_activa/")
def energia_activa_endpoint(id_service: int, anio: int, mes: int):
    return energia_activa(id_service, anio, mes)

@app.get("/energia_activa/")
def energia_activa_endpoint(id_service: int, anio: int, mes: int):
    return energia_activa(id_service, anio, mes)

@app.get("/energia_activa/")
def energia_activa_endpoint(id_service: int, anio: int, mes: int):
    return energia_activa(id_service, anio, mes)

@app.get("/energia_activa/")
def energia_activa_endpoint(id_service: int, anio: int, mes: int):
    return energia_activa(id_service, anio, mes)


def main():
    print(energia_activa(2256,2023,9))
    print(comercializacion_excedentes(2256,2023,9))
    print(excedentes_tuno(2256,2023,9))
    print(excedentes_tdos(2256,2023,9))

if __name__ == "__main__":
    main()
