# Prueba-ERCO

API RESTful en FastAPI para el cálculo de facturación de energía.

## Prerequisitos
1. Intalar PostgreSQL local
2. Instalar `uv` en el entorno de Python: https://docs.astral.sh/uv/getting-started/installation/
3. Crear la base de datos dentro de PostgreSQL:
```
CREATE DATABASE erco;
```
4. Ajustar credenciales en [app/core/config.py](app/core/config.py).

## Instalación
```
uv sync
```

## Poblar la base de datos
```
uv run python init.py
```

## Levantar la API
```
uv run uvicorn app.main:app --reload
```
Docs interactivas: http://127.0.0.1:8000/docs

## Estructura del proyecto
```
app/
├── main.py               # FastAPI app + registro de routers
├── core/
│   └── config.py         # Credenciales y fábrica del cliente DB
├── db/
│   └── session.py        # PostgresClient (psycopg2)
├── schemas/
│   └── invoice.py        # Modelos Pydantic
├── services/
│   ├── invoice.py        # Cálculos EA / EC / EE1 / EE2
│   └── statistics.py     # Estadísticas y carga del sistema
└── routers/
    ├── invoice.py        # /calculate-invoice + /invoice/*
    └── statistics.py     # /client-statistics + /system-load

init.py                   # Script de creación y carga de la DB
Data/, Database/          # Datos CSV y DDL
```

## Endpoints

| Método | Ruta                                     | Descripción                                               |
|--------|------------------------------------------|-----------------------------------------------------------|
| POST   | `/calculate-invoice/`                    | Factura completa (EA + EC + EE1 + EE2 + total)            |
| GET    | `/client-statistics/{id_servicio}`       | Estadísticas de consumo e inyección del servicio          |
| GET    | `/system-load/`                          | Carga neta (consumo − inyección) por timestamp del mes    |
| GET    | `/energia_activa/`                       | Un solo concepto (`ea`)                                  |
| GET    | `/comercializacion_excedentes/`          | Un solo concepto (`ec`)                                  |
| GET    | `/excedentes_tuno/`                      | Un solo concepto (`ee1`)                                  |
| GET    | `/excedentes_tdos/`                      | Un solo concepto (`ee2`)                                  |

Los GET de factura aceptan `?anio=` y `?mes=` (por defecto 2023 y 9). `/system-load/` requiere `anio` y `mes`.

### Ejemplos
```
curl "http://127.0.0.1:8000/energia_activa/?id_service=2256&anio=2023&mes=9"
curl "http://127.0.0.1:8000/excedentes_tdos/?id_service=2256&anio=2023&mes=9"
curl http://127.0.0.1:8000/client-statistics/2256
curl "http://127.0.0.1:8000/system-load/?anio=2023&mes=9"
curl -X POST http://127.0.0.1:8000/calculate-invoice \
     -H "Content-Type: application/json" \
     -d '{"id_servicio":2256,"anio":2023,"mes":9}'
```

## Cambios
Se reemplaza el valor de cdi por NULL cuando voltage_level es 2 o 3 en la tablaservices porque, según la regla de negocio, ese campo no tiene relevancia tarifaria para esos niveles de tensión. 
Almacenar el valor original violaría la integridad referencial con la tabla tariffs y generaría inconsistencias en los cálculos de facturación
id_service,id_market,cdi,voltage_level
3222,4,101,2

## Posibles mejoras a futuro
1. Como mejora de seguridad, se recomienda migrar las credenciales de la base de datos a variables de entorno mediante un archivo .env ignorado por Git, utilizando la librería python-dotenv. Esto permite gestionar distintos entornos (desarrollo, producción) sin modificar el código y elimina el riesgo de exponer credenciales sensibles en el repositorio.
Durante el desarrollo y fase de pruebas, las credenciales se dejaron directamente en el código para simplificar la implementación y enfocarse en la lógica de negocio. Esto es aceptable en un entorno local controlado, pero representa un riesgo de seguridad en producción.

2. Las consultas SQL construidas con format() o f-strings representan un riesgo de SQL Injection, ya que un usuario malicioso podría manipular los parámetros para alterar o destruir datos. Como mejora, se deben reemplazar por consultas parametrizadas usando el mecanismo nativo de psycopg2 con %s, que sanitiza automáticamente los valores antes de enviarlos a la base de datos

3. Varias funciones comparten la misma estructura base (conexión a la BD, construcción del JOIN y filtros). Se recomienda extraer esta lógica común en una función privada reutilizable, de modo que cada función pública solo defina los parámetros que la diferencian. Esto reduce la duplicación de código y centraliza cualquier cambio futuro en un único lugar.

4. Actualmente las funciones de carga asumen una inserción inicial única. En un entorno real, los datos de consumo, inyección y precios XM se actualizan periódicamente (diaria o mensualmente). Se recomienda implementar funciones de actualización incremental que permitan añadir nuevos registros sin recargar toda la tabla, evitando duplicados.

