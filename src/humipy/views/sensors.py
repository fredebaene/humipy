from humipy.database.read import get_sensors
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
import sqlalchemy


def render_sensors_table(engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a table with all available sensors. The function 
    then returns menu option 'd'. The database menu is the only menu from 
    which the user can access a list of the sensors. Therefore, the app must 
    redirect the user to the database menu

    Returns:
        str: menu option (always 'd').
    """
    console = Console()
    table = Table(caption="Sensors", caption_justify="left")
    table.add_column("ID", style="cyan", justify="left", vertical="middle", min_width=4)
    table.add_column("Serial Nr.", justify="left", vertical="middle", min_width=30)
    table.add_column("Type", justify="left", vertical="middle", min_width=30)
    sensors = get_sensors(engine).to_dict(orient="records")

    for row in sensors:
        table.add_row(
            str(row["sensor_id"]),
            row["sensor_serial_number"],
            row["sensor_type"],
        )

    console.print(Panel("Available Sensors"))
    console.print(Padding(table, (0, 0, 0, 2)))
    return "d"