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
    Column("sensor_name", String, nullable=False),
    Column("sensor_serial_number", Integer, nullable=False),
)