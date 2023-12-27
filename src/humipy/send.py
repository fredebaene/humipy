"""
This module implements functionality to upload/send data to the appropriate 
database tables.
"""


import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, text, select, Table, Column, Integer, String, MetaData
import pandas as pd
from typing import Tuple


def _get_engine() -> sqlalchemy.engine.base.Engine:
    """
    This function initializes an engine. This engine functions as a connection 
    factory and connection pool.

    Returns:
        sqlalchemy.engine.base.Engine: engine object.
    """
    load_dotenv()
    db = os.getenv("_HUMIPY_DB_NAME")
    port = os.getenv("_HUMIPY_DB_PORT")
    username = os.getenv("_HUMIPY_DB_USERNAME")
    password = os.getenv("_HUMIPY_DB_PASSWORD")
    return create_engine(
        f"postgresql+psycopg2://{username}:{password}@localhost:{port}/{db}"
    )


def _construct_locations_table() -> Tuple[MetaData, Table]:
    """
    This function initializes the locations table and adds it to the metadata 
    object.

    Returns:
        Tuple[MetaData, Table]: the metadata object and the locations table.
    """
    metadata = MetaData()
    locations = Table(
        "locations",
        metadata,
        Column("location_id", Integer, primary_key=True),
        Column("location_name", String),
    )
    return (metadata, locations)


def get_locations() -> pd.DataFrame:
    """
    This function gets all the sensor locations and returns them in a data 
    frame.

    Returns:
        pd.DataFrame: a data frame with all sensor locations.
    """
    engine = _get_engine()
    metadata, locations = _construct_locations_table()
    stmt = select(locations)
    with engine.connect() as conn:
        locations = pd.read_sql_query(sql=stmt, con=conn)
    return locations