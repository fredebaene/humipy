from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.padding import Padding
from humipy.send import get_locations


def render_locations_table() -> str:
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
    locations = get_locations().to_dict(orient="records")

    for row in locations:
        table.add_row(str(row["location_id"]), row["location_name"])

    console.print(Panel("Available Locations"))
    console.print(Padding(table, (0, 0, 0, 2)))
    return "d"


def render_main_menu() -> str:
    """
    This function renders the main menu. This main menu offers the users the 
    possibility to go into different submenus.
    """
    console = Console()
    console.print(Panel("Main Menu"))
    console.print(Padding("- Manage database \[d]", (0, 0, 0, 2)))
    console.print(Padding("- Quit \[q]", (0, 0, 0, 2)))
    console.print("")
    return Prompt.ask("  What do you want to do?", choices=["d", "q"])


def render_database_menu() -> str:
    """
    This function renders the menu that allows the user to interact with the 
    database.

    Returns:
        str: menu option.
    """
    console = Console()
    console.print(Panel("Database Management"))
    console.print(Padding("- List locations \[l]", (0, 0, 0, 2)))
    console.print(Padding("- Go back to main menu \[m]", (0, 0, 0, 2)))
    console.print(Padding("- Quit \[q]", (0, 0, 0, 2)))
    console.print("")
    return Prompt.ask("  What do you want to do?", choices=["l", "m", "q"])


def render_app_exit():
    """
    This function renders the exit message.
    """
    console = Console()
    console.print(Panel("Goodbye!"))