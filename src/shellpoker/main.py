import typer
from rich.console import Console
import toml
from shellpoker.game import game_loop

console = Console()
app = typer.Typer()

def get_version():
    pyproject = toml.load("pyproject.toml")
    return pyproject["project"]["version"]

@app.command()
def greet():
    console.print(f"SHELL POKER {get_version()}", style="bold green")
    console.print("Press any key to start playing...", style="bold blue")
    input()  # Wait for user input to start the game
    console.clear()
    game_loop()

def main():
    app()

if __name__ == "__main__":
    main()
