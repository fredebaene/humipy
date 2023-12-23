from humipy.models import locations_table, sensors_table
import pandas as pd
import sqlalchemy
from sqlalchemy import select


def get_locations(engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    """
    This function retrieves all locations from the locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): an SQLAlchemy engine object.

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
        engine (sqlalchemy.engine.base.Engine): an SQLAlchemy engine object.

    Returns:
        pd.DataFrame: a data frame with all sensors.
    """
    stmt = select(sensors_table)
    with engine.connect() as conn:
        df = pd.read_sql_query(stmt, conn)
    return df