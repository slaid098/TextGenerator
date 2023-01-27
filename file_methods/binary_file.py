import pickle
from pathlib import Path
from typing import Any


def load_pickle(path: Path) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)


def save_pickle(path: Path, data: Any) -> None:
    with open(path, "wb") as file:
        pickle.dump(data, file)
