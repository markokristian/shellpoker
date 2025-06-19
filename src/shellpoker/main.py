import toml
from shellpoker.game import main as poker_main

def get_version():
    pyproject = toml.load("pyproject.toml")
    return pyproject["project"]["version"]

def main():
    poker_main()

if __name__ == "__main__":
    main()
