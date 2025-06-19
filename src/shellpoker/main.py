from shellpoker.game import main as poker_main
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("shellpoker")
except PackageNotFoundError:
    __version__ = "dev"

def main():
    poker_main(__version__)

if __name__ == "__main__":
    main()
