from rich import print
from rich.console import Group
from rich.panel import Panel
from humipy.database import connect, read, write
from humipy.views.locations import render_locations_table
from humipy.views.sensors import render_sensors_table
from humipy.views.menus import render_main_menu, render_database_menu
from humipy.views.exit import render_app_exit


def render_app(menu_option: str = "m") -> None:
    # Initialize a SQLAlchemy engine
    engine = connect.get_engine()
    # Render the different menu options
    while menu_option != "q":
        if menu_option == "m":
            menu_option = render_main_menu()
        elif menu_option == "d":
            menu_option = render_database_menu()
        elif menu_option == "l":
            menu_option = render_locations_table(engine)
        elif menu_option == "s":
            menu_option = render_sensors_table(engine)

    # Exit from the application and give a nice message to the user
    render_app_exit()