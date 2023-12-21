from rich import print
from rich.console import Group
from rich.panel import Panel
from humipy.views import (
    render_app_exit,
    render_database_menu,
    render_locations_table,
    render_main_menu,
)


def render_app(menu_option: str = "m") -> None:
    # Render the different menu options
    while menu_option != "q":
        if menu_option == "m":
            menu_option = render_main_menu()
        elif menu_option == "d":
            menu_option = render_database_menu()
        elif menu_option == "l":
            menu_option = render_locations_table()

    # Exit from the application and give a nice message to the user
    render_app_exit()