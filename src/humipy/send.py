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


def _construct_locations_table(metadata: MetaData) -> Tuple[MetaData, Table]:
    """
    This function initializes the locations table and add it to the metadata 
    object.

    Args:
        metadata (MetaData): metadata object to which to add the table.

    Returns:
        Tuple[MetaData, Table]: the metadata object and the locations table.
    """
    locations = Table(
        "locations",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
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
    db_username = os.getenv("_HUMIPY_DB_USERNAME")
    db_password = os.getenv("_HUMIPY_DB_PASSWORD")

    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@localhost/{db_name}"
    )

    metadata = MetaData()
    metadata, locations = _construct_locations_table(metadata)

    with engine.connect() as conn:
        locations = _get_locations(conn, locations)



if __name__ == "__main__":
    main()