from humipy.database.models import (
    humidity_measurements_table,
    locations_table,
    sensors_table,
    sensor_locations_table,
)
import pandas as pd
import sqlalchemy
from sqlalchemy import select
from typing import Optional


def get_locations(engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    """
    This function retrieves all locations from the locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        pd.DataFrame: a data frame with all locations.
    """
    stmt = select(locations_table)
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df


def get_sensors(engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    """
    This function retrieves all sensors from the sensors database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        pd.DataFrame: a data frame with all sensors.
    """
    stmt = select(sensors_table)
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df


def get_sensor_locations(
        engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    """
    This function retrieves all sensor locations, both open and closed, from 
    the sensor locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        pd.DataFrame: a data frame with all sensor locations.
    """
    stmt = _get_sensor_locations_base_query()
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df


def get_open_sensor_location(
        engine: sqlalchemy.engine.base.Engine,
        sensor_serial_number: Optional[str] = None) -> pd.DataFrame:
    """
    This function queries the database to look for a particular sensor if 
    there is an open sensor location.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        sensor_serial_number (str): the sensor serial number.

    Returns:
        pd.DataFrame: a data frame with the open sensor location for the 
            specific sensor, if there is an open location.
    """
    stmt = (
        _get_sensor_locations_base_query()
        .where(sensor_locations_table.c.stop_placement == None)
        .where(sensors_table.c.sensor_serial_number == sensor_serial_number)
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df

def get_open_sensor_locations(
        engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    """
    This function retrieves all open sensor locations from the sensor 
    locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        pd.DataFrame: a data frame with all open sensor locations.
    """
    stmt = (
        _get_sensor_locations_base_query()
        .where(sensor_locations_table.c.stop_placement == None)
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df


def _get_sensor_locations_base_query() -> sqlalchemy.sql.selectable.Select:
    """
    This function creates a base query to retrieve all sensor locations, both 
    open and closed, from the sensor locations database table.

    Returns:
        sqlalchemy.sql.selectable.Select: a SQLAlchemy select construct.
    """
    return (
        select(sensor_locations_table, sensors_table, locations_table)
        .join_from(
            sensor_locations_table,
            sensors_table,
            sensor_locations_table.c.sensor_id == sensors_table.c.sensor_id,
        )
        .join_from(
            sensor_locations_table,
            locations_table,
            sensor_locations_table.c.location_id == locations_table.c.location_id
        )
    )


def get_recent_measurements(
        engine: sqlalchemy.engine.base.Engine,
        top_n: int) -> pd.DataFrame:
    """
    This function retrieves the n most recent humidity measurements from the 
    appropriate database tables.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        top_n (int): the n most recent measurements to retrieve.

    Returns:
        pd.DataFrame: a data frame with the most recent humidity measurements.
    """
    stmt = (
        select(
            humidity_measurements_table,
            sensor_locations_table,
            sensors_table,
            locations_table,
        )
        .join_from(
            humidity_measurements_table,
            sensor_locations_table,
            (
                humidity_measurements_table.c.sensor_location_id
                == sensor_locations_table.c.sensor_location_id
            ),
        )
        .join_from(
            sensor_locations_table,
            sensors_table,
            (
                sensor_locations_table.c.sensor_id
                == sensors_table.c.sensor_id
            ),
        )
        .join_from(
            sensor_locations_table,
            locations_table,
            (
                sensor_locations_table.c.location_id
                == locations_table.c.location_id
            ),
        )
        .order_by(humidity_measurements_table.c.measurement_time.desc())
        .limit(top_n)
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df
