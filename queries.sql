select * from consumption;
select * from tariffs;
select * from records;
select * from services;
select * from xm_data_hourly_per_agent;

SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.cu) AS ea FROM consumption t1
LEFT JOIN records t2
	ON t1.id_record = t2.id_record
LEFT JOIN services t3
	ON t2.id_service = t3.id_service
LEFT JOIN tariffs t4
	ON t3.id_market = t4.id_market 
	AND t3.voltage_level = t4.voltage_level 
	AND ((t3.cdi IS NOT NULL AND t3.cdi = t4.cdi) OR (t3.cdi IS NULL AND t4.cdi IS NULL))
WHERE t3.id_service = 2256 AND EXTRACT(YEAR FROM t2.record_timestamp) = 2023 AND EXTRACT(MONTH FROM t2.record_timestamp) = 9
GROUP BY
	1, 2, 3;

SELECT t3.id_service, EXTRACT(YEAR FROM t2.record_timestamp) AS anio, EXTRACT(MONTH FROM t2.record_timestamp) AS mes, SUM(t1.value*t4.c) AS ec FROM injection t1
LEFT JOIN records t2
	ON t1.id_record = t2.id_record
LEFT JOIN services t3
	ON t2.id_service = t3.id_service
LEFT JOIN tariffs t4
	ON t3.id_market = t4.id_market 
	AND t3.voltage_level = t4.voltage_level 
	AND ((t3.cdi IS NOT NULL AND t3.cdi = t4.cdi) OR (t3.cdi IS NULL AND t4.cdi IS NULL))
WHERE t3.id_service = 2256 AND EXTRACT(YEAR FROM t2.record_timestamp) = 2023 AND EXTRACT(MONTH FROM t2.record_timestamp) = 9
GROUP BY
	1, 2, 3;

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
GROUP BY
	1, 2, 3;

SELECT * FROM tariffs t1
LEFT JOIN services t2
	ON t1.id_market = t2.id_market 
	AND t1.voltage_level = t2.voltage_level 
	AND ((t1.cdi IS NOT NULL AND t1.cdi = t2.cdi) OR (t1.cdi IS NULL AND t2.cdi IS NULL))

WITH ee1_mensual AS (SELECT t1.id_service, EXTRACT(YEAR FROM t1.record_timestamp) AS anio, EXTRACT(MONTH FROM t1.record_timestamp) AS mes, 
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
LEFT JOIN ee1_mensual t4
	ON t1.id_service = t4.id_service AND EXTRACT(YEAR FROM t1.record_timestamp) = t4.anio AND EXTRACT(MONTH FROM t1.record_timestamp) = t4.mes AND EXTRACT(DAY FROM t1.record_timestamp) = t4.dia
LEFT JOIN xm_data_hourly_per_agent t5
	ON t5.record_timestamp = t1.record_timestamp),

tbl_final AS (
SELECT t1.*, 
CASE WHEN t1.acumulado_inj < t1.ee1 THEN 0.0 
ELSE LEAST(t1.acumulado_inj - t1.ee1, t1.injection) END AS exceso_ee2
FROM tbl_acumulado t1)

SELECT id_service, EXTRACT(YEAR FROM record_timestamp) AS anio, EXTRACT(MONTH FROM record_timestamp) AS mes, SUM(exceso_ee2) AS exceso, SUM(exceso_ee2*tarifa_xm) AS ee2 FROM tbl_final
GROUP BY 1, 2, 3

