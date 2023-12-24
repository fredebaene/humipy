from humipy.database.models import locations_table, sensors_table
import sqlalchemy
from sqlalchemy import insert, select
from typing import Optional


def add_location(
        engine: sqlalchemy.engine.base.Engine,
        location_name: str) -> bool:
    """
    This function adds a location to the locations database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        location_name (str): location name.
    """
    # Check if there is already a record in the locations table with the same 
    # name. If so, the insert must be aborted, the location names must be 
    # unique.
    stmt = (
        select(locations_table)
        .where(locations_table.c.location_name == location_name)
    )
    with engine.connect() as conn:
        res = conn.execute(stmt)
    if res.rowcount > 0:
        return False
    
    # Proceed with inserting a new location to the locations database table
    with engine.connect() as conn:
        res = conn.execute(
            insert(locations_table), {"location_name": location_name}
        )
        conn.commit()
    return True


def add_sensor(
        engine: sqlalchemy.engine.base.Engine,
        sensor_serial_number: str,
        sensor_type: Optional[str] = None) -> bool:
    """
    This function adds a sensor to the sensors database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        sensor_serial_number (str): sensor serial number.
        sensor_type (Optional[str], optional): the sensor type. Defaults to 
            None.
    """
    # Check if there is already a record in the sensors table with the same 
    # serialnumber. If so, the insert must be aborted, the serial numbers must 
    # be unique.
    stmt = (
        select(sensors_table)
        .where(sensors_table.c.sensor_serial_number == sensor_serial_number)
    )
    with engine.connect() as conn:
        res = conn.execute(stmt)
    if res.rowcount > 0:
        return False

    # Proceed with inserting a new sensor to the sensors database table
    with engine.connect() as conn:
        res = conn.execute(
            insert(sensors_table),
            {
                "sensor_serial_number": sensor_serial_number,
                "sensor_type": sensor_type,
            },
        )
        conn.commit()
    return True


def start_sensor_placement(
        engine: sqlalchemy.engine.base.Engine,
        location_name: str,
        sensor_serial_number: str,
        start_placement: Optional[datetime] = None):
    # Initialize a start placement date if required (i.e., if the user did not 
    # specify a start date)
    start_placement = (
        datetime.now() if start_placement is None else start_placement
    )

    # Initialize subqueries
    scalar_sensor_subquery = (
        select(sensors_table.c.sensor_id)
        .where(sensors_table.c.sensor_serial_number == bindparam("sensor_serial_number"))
        .scalar_subquery()
    )
    scalar_location_subquery = (
        select(locations_table.c.location_id)
        .where(locations_table.c.location_name == bindparam("location_name"))
        .scalar_subquery()
    )

    # Create insert construct
    stmt = (
        insert(sensor_locations_table)
        .values(
            sensor_id=scalar_sensor_subquery,
            location_id=scalar_location_subquery,
        )
    )

    with engine.connect() as conn:
        res = conn.execute(
            stmt,
            {
                "location_name": location_name,
                "sensor_serial_number": sensor_serial_number,
                "start_placement": start_placement,
            }
        )
        conn.commit()