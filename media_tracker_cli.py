import typer
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()


@app.command(short_help="Adds an item to the list")
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    show()


