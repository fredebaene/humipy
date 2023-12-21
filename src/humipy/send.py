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


def _get_engine():
    load_dotenv()
    db_name = os.getenv("_HUMIPY_DB_NAME")
    db_port = os.getenv("_HUMIPY_DB_PORT")
    db_username = os.getenv("_HUMIPY_DB_USERNAME")
    db_password = os.getenv("_HUMIPY_DB_PASSWORD")

    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@localhost:{db_port}/{db_name}"
    )

    return engine


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


def _get_locations(
        conn: sqlalchemy.engine.base.Connection,
        locations: Table) -> pd.DataFrame:
    """
    This function gets all the sensor locations and returns them in a data 
    frame.

    Args:
        conn (sqlalchemy.engine.base.Connection): the connection to the 
            database.
        locations (Table): the locations table.

    Returns:
        pd.DataFrame: a data frame with all sensor locations.
    """
    stmt = select(locations)
    return pd.read_sql_query(sql=stmt, con=conn)


def main() -> None:
    load_dotenv()
    db_name = os.getenv("_HUMIPY_DB_NAME")
    db_port = os.getenv("_HUMIPY_DB_PORT")
    db_username = os.getenv("_HUMIPY_DB_USERNAME")
    db_password = os.getenv("_HUMIPY_DB_PASSWORD")

    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@localhost:{db_port}/{db_name}"
    )

    metadata = MetaData()
    metadata, locations = _construct_locations_table(metadata)

    with engine.connect() as conn:
        locations = _get_locations(conn, locations)



if __name__ == "__main__":
    main()