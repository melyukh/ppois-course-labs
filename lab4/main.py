"""Точка входа лабы 4. Данные для коллекций и графа читаются из data.json рядом с этим файлом."""
from pathlib import Path

from source.cli.cli_application import run

DATA_FILE = Path(__file__).resolve().parent / "datafiles" / "data.json"


if __name__ == "__main__":
    run(DATA_FILE)
