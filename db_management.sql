CREATE TABLE IF NOT EXISTS sensors (
    sensor_id SMALLSERIAL PRIMARY KEY,
    sensor_serial_number VARCHAR(20) UNIQUE,
    sensor_type VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS locations (
    location_id SMALLSERIAL PRIMARY KEY,
    location_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sensor_locations (
    sensor_location_id SERIAL PRIMARY KEY,
    sensor_id SMALLINT NOT NULL,
    location_id SMALLINT NOT NULL,
    start_placement TIMESTAMP NOT NULL,
    stop_placement TIMESTAMP NULL,
    CONSTRAINT fk_sensor FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id),
    CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS humidity_measurements (
    humidity_measurement_id BIGSERIAL PRIMARY KEY,
    sensor_location_id INT NOT NULL,
    humidity REAL NULL,
    measurement_time TIMESTAMP NOT NULL,
    CONSTRAINT fk_sensor_location FOREIGN KEY (sensor_location_id) REFERENCES sensor_locations(sensor_location_id)
);