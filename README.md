# Prueba-ERCO
## Prerequisitos
1. Tener instalado PostgreSQL localmente.
2. Tener instalado uv https://docs.astral.sh/uv/getting-started/installation/
3. Dentro de PostgreSQL crear la base de datos con el siguiente comando:
    ```
    CREATE DATABASE erco;
    ```
4. Modificar el archivo config.py con el usuario  y contraseña para la conexión con PostgreSQL.

## Cambios
Dentro de la tabla de services se cambia el cdi por vacio ya que al ser voltage_level = 2 no importa ya asi encuentra su equivalente en tariffs 
id_service,id_market,cdi,voltage_level
3222,4,101,2