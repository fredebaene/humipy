from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt


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
    console.print(Padding("- Add location \[a]", (0, 0, 0, 2)))
    console.print(Padding("- List sensors \[s]", (0, 0, 0, 2)))
    console.print(Padding("- Add sensor \[w]", (0, 0, 0, 2)))
    console.print(Padding("- List open sensor locations \[o]", (0, 0, 0, 2)))
    console.print(Padding("- Go back to main menu \[m]", (0, 0, 0, 2)))
    console.print(Padding("- Quit \[q]", (0, 0, 0, 2)))
    console.print("")
    return Prompt.ask(
        "  What do you want to do?",
        choices=["l", "a", "s", "w", "o", "m", "q"],
    )