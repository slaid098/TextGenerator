from pathlib import Path
from typing import Literal


def get_list(path: Path | str, encoding: str = "utf-8",
             separator: str = "\n") -> list[str]:
    """
    Get list from a .txt file. Separator is a line break
    """
    with open(path, "r", encoding=encoding) as file:
        data = (file.read()).split(separator)
    return [value for value in data if value]


def read_write_file(path: Path,
                    recorded_data: str = "",
                    mode: Literal["w", "a", "r"] = "r",
                    encoding: str = "utf-8") -> None | str:
    """
    Writing, reading or overwriting a .txt file
    If mode == 'a' recorded_data += line_break
    """

    if mode == "w":
        _write_file(path, recorded_data, "w", encoding)
    elif mode == "a":
        _write_file(path, recorded_data, "a", encoding)
    elif mode == "r":
        return _read_file(path)
    else:
        raise ValueError("Неверный режим чтения/записи файла")

    return None


def _write_file(path: Path, data: str, mode: str = "w",
                encoding: str = "utf-8") -> None:
    if mode != "w":
        line_break = "\n"
    else:
        line_break = ""

    with open(path, mode, encoding=encoding) as file:
        file.write(data + line_break)


def _read_file(path: Path, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as file:
        data_file = file.read()
    return data_file
