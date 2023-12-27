from rich.console import Console
from rich.panel import Panel


def render_app_exit():
    """
    This function renders the exit message.
    """
    console = Console()
    console.print(Panel("Goodbye!"))