from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = "locations"

    location_id: Mapped[int] = mapped_column(primary_key=True)
    location_name: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"Location(ID: {self.location_id}, Name: {self.location_name})"
    

class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id: Mapped[int] = mapped_column(primary_key=True)
    sensor_name: Mapped[str] = mapped_column()
    sensor_serial_number: Mapped[Optional[int]] = mapped_column()

    def __repr__(self):
        return f"Sensor(ID: {self.sensor_id}, Name: {self.sensor_name}, Serial nr.: {self.sensor_serial_number})"