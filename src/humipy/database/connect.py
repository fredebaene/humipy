from dotenv import load_dotenv
from humipy.database.models import metadata
from humipy.database.write import (
    add_location, add_sensor, start_sensor_placement
)
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine


def get_engine(dev: bool = False) -> sqlalchemy.engine.base.Engine:
    """
    This function initializes an engine. This engine functions as a connection 
    factory and connection pool.

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
    sensors = [("XIE-385A92H20-T0", "DHT11"), ("XIA-502A92V37-T7", "DHT11")]
    for sensor in sensors:
        add_sensor(engine, sensor[0], sensor[1])
