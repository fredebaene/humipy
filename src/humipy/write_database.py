from humipy.models import metadata, locations_table, sensors_table
from sqlalchemy import insert
from humipy.send import _get_engine
import sqlalchemy
from typing import Optional


def add_location(
        engine: sqlalchemy.engine.base.Engine,
        location_name: str) -> None:
    """
    This function adds a location to the locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): engine object to create 
            connection.
        location_name (str): location name.
    """
    stmt = insert(locations_table).values(location_name=location_name)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
    return result


def add_sensor(
        engine: sqlalchemy.engine.base.Engine,
        sensor_name: str,
        sensor_serial_number: Optional[int] = None) -> None:
    """
    This function adds a sensor to the sensors database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): engine object to create 
            connection.
        sensor_name (str): the sensor name.
        sensor_serial_number (Optional[int], optional): the sensor serial 
            number. Defaults to None.
    """
    stmt = (
        insert(sensors_table)
        .values(
            sensor_name=sensor_name,
            sensor_serial_number=sensor_serial_number
        )
    )
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
    return result