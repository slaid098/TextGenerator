import json
from pathlib import Path


def load_json(path: Path) -> dict:
    """
    Deserializing the json file and returning dict
    """
    with open(path, "r") as read_file:
        return json.load(read_file)


def save_json(path: Path, data: dict) -> None:
    """
    Serialization the json file
    """
    with open(path, "w") as write_file:
        json.dump(data, write_file)