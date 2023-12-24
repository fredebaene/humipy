from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String


metadata = MetaData()


locations_table = Table(
    "locations",
    metadata,
    Column("location_id", Integer, primary_key=True),
    Column("location_name", String, nullable=False),
)


sensors_table = Table(
    "sensors",
    metadata,
    Column("sensor_id", Integer, primary_key=True),
    Column("sensor_serial_number", String, nullable=False),
    Column("sensor_type", String, nullable=True),
)


sensor_locations_table = Table(
    "sensor_locations",
    metadata,
    Column("sensor_location_id", Integer, primary_key=True),
    Column("sensor_id", Integer, nullable=False),
    Column("location_id", Integer, nullable=False),
    Column("start_placement", Date, nullable=False),
    Column("stop_placement", Date, nullable=True),
)