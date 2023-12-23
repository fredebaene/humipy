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