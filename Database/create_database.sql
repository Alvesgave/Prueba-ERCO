CREATE TABLE IF NOT EXISTS tariffs (
    id_market           INT,
    voltage_level       INT,
    cdi                 INT,
    G                   NUMERIC(20,10),
    T                   NUMERIC(20,10),
    D                   NUMERIC(20,10),
    R                   NUMERIC(20,10),
    C                   NUMERIC(20,10),
    P                   NUMERIC(20,10),
    CU                  NUMERIC(20,10),
    UNIQUE (id_market, voltage_level, cdi)
);

CREATE TABLE IF NOT EXISTS services (
    id_service          INT PRIMARY KEY,
    id_market           INT,
    cdi                 INT,
    voltage_level       INT,
    FOREIGN KEY (id_market, voltage_level, cdi ) REFERENCES tariffs(id_market, voltage_level, cdi)
);

CREATE TABLE IF NOT EXISTS xm_data_hourly_per_agent (
    record_timestamp    TIMESTAMP PRIMARY KEY,
    value               NUMERIC(20,10)   
);

CREATE TABLE IF NOT EXISTS records (
    id_record           INT PRIMARY KEY,
    id_service          INT,
    record_timestamp    TIMESTAMP,
    FOREIGN KEY (id_service) REFERENCES services(id_service),
    FOREIGN KEY (record_timestamp) REFERENCES xm_data_hourly_per_agent(record_timestamp)
);

CREATE TABLE IF NOT EXISTS injection (
    id_record           INT PRIMARY KEY,
    value               NUMERIC(20,10),
    FOREIGN KEY (id_record) REFERENCES records(id_record)
);

CREATE TABLE IF NOT EXISTS consumption (
    id_record           INT PRIMARY KEY,
    value               NUMERIC(20,10),
    FOREIGN KEY (id_record) REFERENCES records(id_record)
)