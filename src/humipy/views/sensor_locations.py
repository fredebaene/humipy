import datetime
from humipy.database.read import get_open_sensor_locations
from humipy.database.write import start_sensor_placement
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import sqlalchemy


def render_open_sensor_locations_table(
        engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a table with all open sensor locations. The function 
    then returns menu option 'd'. The database menu is the only menu from 
    which the user can access a list of the open sensor locations. Therefore, 
    the app must redirect the user to the database menu

    Returns:
        str: menu option (always 'd').
    """
    console = Console()
    table = Table(caption="Sensor Locations", caption_justify="left")
    table.add_column("Sensor ID", style="cyan", justify="left", vertical="middle", min_width=10)
    table.add_column("Serial Nr.", justify="left", vertical="middle", min_width=30)
    table.add_column("Loc. ID", style="cyan", justify="left", vertical="middle", min_width=10)
    table.add_column("Location", justify="left", vertical="middle", min_width=30)
    table.add_column("Start", justify="left", vertical="middle", min_width=30)
    table.add_column("Stop", justify="left", vertical="middle", min_width=30)
    sensor_locs = get_open_sensor_locations(engine).to_dict(orient="records")

    for row in sensor_locs:
        start_placement = row["start_placement"].strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(row["stop_placement"], datetime.datetime):
            stop_placement = row["stop_placement"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            stop_placement = ""
        table.add_row(
            str(row["sensor_id"]),
            row["sensor_serial_number"],
            str(row["location_id"]),
            row["location_name"],
            start_placement,
            stop_placement,
        )
    
    console.print(Panel("Available Sensors"))
    console.print(Padding(table, (0, 0, 0, 2)))
    return "d"


def render_start_placement(engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a prompt which asks the user to start a sensor 
    placement. The prompt for a new sensor placement is repeated until the 
    user enters a sensor for which there is no open placement or enters the  
    word 'quit'. The function returns menu option 'd'. The database menu 
    is the only menu from which the user can start a new sensor placement. 
    Therefore, the app must redirect the user to the database menu.
    
    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        str: menu option (always 'd').
    """
    continue_asking = True
    prompt_msg_serial_nr = "  Enter serial number"
    prompt_msg_type = "  Enter location"
    console = Console()
    console.print(Panel("Add Sensor"))
    while continue_asking:
        sensor_serial_number = Prompt.ask(prompt_msg_serial_nr)
        location_name = Prompt.ask(prompt_msg_type)
        if sensor_serial_number == "quit" or location_name == "quit":
            continue_asking = False
        else:
            continue_asking = (
                False if start_sensor_placement(
                    engine, location_name, sensor_serial_number
                ) else True
            )
    return "d"