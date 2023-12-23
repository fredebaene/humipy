from humipy.models import metadata, locations_table, sensors_table
from sqlalchemy import insert
from humipy.send import _get_engine
import sqlalchemy


def add_new_location(
        engine: sqlalchemy.engine.base.Engine,
        location_name: str) -> None:
    """
    This function adds a new location to the locations database table.

    Args:
        location_name (str): location name.
    """
    stmt = insert(locations_table).values(location_name=location_name)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
    return result