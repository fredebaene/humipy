from humipy.database.read import get_locations
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
import sqlalchemy


def render_locations_table(engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a table with all available locations. The function 
    then returns menu option 'd'. The database menu is the only menu from 
    which the user can access a list of the locations. Therefore, the app must 
    redirect the user to the database menu

    Returns:
        str: menu option (always 'd').
    """
    console = Console()
    table = Table(caption="Locations", caption_justify="left")
    table.add_column("ID", style="cyan", justify="left", vertical="middle", min_width=4)
    table.add_column("Location", justify="left", vertical="middle", min_width=30)
    locations = get_locations(engine).to_dict(orient="records")

    for row in locations:
        table.add_row(str(row["location_id"]), row["location_name"])

    console.print(Panel("Available Locations"))
    console.print(Padding(table, (0, 0, 0, 2)))
    return "d"


def render_location_addition(engine: sqlalchemy.engine.base.Engine) -> str:
    """
    This function renders a prompt which asks the user for a new location. The 
    prompt for a new location is repeated until the user enters a new 
    location, i.e., a location that is not already in the database, or enters 
    the word 'quit'. The function returns menu option 'd'. The database menu 
    is the only menu from which the user can access a list of the locations. 
    Therefore, the app must redirect the user to the database menu.
    
    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.

    Returns:
        str: menu option (always 'd').
    """
    continue_asking = True
    prompt_msg = "  What location do you want to add (enter 'quit' to abort)?"
    console = Console()
    console.print(Panel("Add Location"))
    while continue_asking:
        location_name = Prompt.ask(prompt_msg)
        if location_name == "quit":
            continue_asking = False
        else:
            continue_asking = (
                False if add_location(engine, location_name) else True
            )
    return "d"