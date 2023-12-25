from humipy.database.models import locations_table, sensors_table
import pandas as pd
import sqlalchemy
from sqlalchemy import select


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