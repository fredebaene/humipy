from dotenv import load_dotenv
from humipy.database.models import metadata
from humipy.database.write import (
    add_location, add_sensor, start_sensor_placement, push_measurement
)
from os import getenv
import random
import sqlalchemy
from sqlalchemy import create_engine


_SENSORS = ["XIE-385A92H20-T0", "XIA-502A92V37-T7"]


def get_engine(dev: bool = False) -> sqlalchemy.engine.base.Engine:
    """
    This function initializes an engine. This engine functions as a connection 
    factory and connection pool.

    Args:
        dev (bool, optional): indicator to indicate to use the test 
            environment or a production environment. Defaults to False.

    Returns:
        sqlalchemy.engine.base.Engine: a SQLAlchemy engine object.
    """
    if dev:
        engine = create_engine("sqlite+pysqlite:///:memory:")
        _create_test_database(engine)
        return engine
    
    load_dotenv()
    db = getenv("DB_NAME")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    username = getenv("DB_USERNAME")
    password = getenv("DB_PASSWORD")
    return create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
    )


def _create_test_database(engine: sqlalchemy.engine.base.Engine) -> None:
    """
    This function create a test database. The test database is populated with 
    dummy data. The test database enables the user to interacht with the 
    application

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
    """
    metadata.create_all(engine)
    for location in ["Kitchen", "Bathroom", "Bedroom"]:
        add_location(engine, location)
    for sensor in _SENSORS:
        add_sensor(engine, sensor, "DHT11")
    start_sensor_placement(engine, "Bathroom", _SENSORS[0])
    start_sensor_placement(engine, "Kitchen", _SENSORS[1])
    _push_dummy_measurements(engine)


def _push_dummy_measurements(engine: sqlalchemy.engine.base.Engine) -> None:
    """
    This function inserts dummy humidity measurements into the test database.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
    """
    for _ in range(1000):
        push_measurement(
            engine, random.choice(_SENSORS), random.uniform(55., 75.),
        )