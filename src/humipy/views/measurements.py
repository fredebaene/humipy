import contextlib
from humipy.database.read import get_recent_measurements
from rich.live import Live
from rich.table import Table
import sqlalchemy
import time


def get_measurements_table(
        engine: sqlalchemy.engine.base.Engine,
        top_n: int) -> Table:
    """
    This function returns the most recent humidity measurements from the 
    measurements database table.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        top_n (int): the n most recent measurements to retrieve.

    Returns:
        Table: a table object with the n most recent measurements
    """
    table = Table(caption="Humidity Measurements", caption_justify="left")
    table.add_column("Time", justify="left", vertical="middle", min_width=25)
    table.add_column("Location", justify="left", vertical="middle", min_width=25)
    table.add_column("Serial Nr.", justify="left", vertical="middle", min_width=25)
    table.add_column("Humidity", justify="right", vertical="middle", min_width=25)
    measurements = (
        get_recent_measurements(engine, top_n).to_dict(orient="records")
    )
    
    for row in measurements:
        measurement_time = row["measurement_time"].strftime("%Y-%d-%m %H:%M:%S")
        humidity_measurement = str(round(row["humidity"], 4))
        table.add_row(
            measurement_time,
            row["location_name"],
            row["sensor_serial_number"],
            humidity_measurement,
        )

    return table

def render_measurements_view(
        engine: sqlalchemy.engine.base.Engine,
        top_n: int,
        dev: bool = False) -> str:
    """
    This function renders a live view showing the n most recent humidity 
    measurements. The function returns menu option 'm'. The main menu is the 
    only menu from which the user can access a live view of the humidity 
    measurements. Therefore, the app must redirect the user to the main menu.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
        top_n (int): the n most recent measurements to retrieve.

    Returns:
        str: menu option (always 'm').
    """
    with Live(get_measurements_table(engine, top_n), screen=True) as live:
        index = 0
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                live.update(get_measurements_table(engine, top_n))
                time.sleep(0.5)
    return "m"