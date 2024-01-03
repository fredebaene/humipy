from humipy.database.read import get_sensors
from humipy.database.write import add_sensor
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
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


def render_sensor_addition(engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a prompt which asks the user for a new sensor. The 
    prompt for a new sensor is repeated until the user enters a new 
    sensor, i.e., a sensor that is not already in the database, or enters 
    the word 'quit'. The function returns menu option 'd'. The database menu 
    is the only menu from which the user can access a list of the sensors. 
    Therefore, the app must redirect the user to the database menu.
    
    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        str: menu option (always 'd').
    """
    continue_asking = True
    prompt_msg_serial_nr = "  Enter serial number"
    prompt_msg_type = "  Enter type"
    console = Console()
    console.print(Panel("Add Sensor"))
    while continue_asking:
        sensor_sn = Prompt.ask(prompt_msg_serial_nr)
        if sensor_sn == "quit":
            break
        sensor_type = Prompt.ask(prompt_msg_type)
        if sensor_type == "quit":
            break
        continue_asking = not add_sensor(engine, sensor_sn, sensor_type)
    return "d"