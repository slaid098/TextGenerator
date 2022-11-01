from dataclasses import dataclass
from pathlib import Path
import math
import random
from typing import Iterable

from loguru import logger

from bot import bot, send_progress, admins


def combinate_text(raw_text: str) -> None:
    _combinate_phrases(raw_text)
    logger.info("Done")


def _combinate_phrases(raw_text: str) -> None:
    blocks = _get_blocks(raw_text)
    rows_lists = _get_rows_lists(blocks)
    number_combinations = get_number_combinations(rows_lists)

    set_rows = set()
    counter = 0
    while not _is_all_combinations_got(set_rows, number_combinations):
        start_len = len(set_rows)
        row = _get_combined_row(rows_lists)
        set_rows.add(row)
        finish_len = len(set_rows)
        if finish_len > start_len:
            counter += 1
            _send_progress(counter, number_combinations)
        _print_progress(counter, number_combinations)
        

    list_rows = _convert_set_to_list(set_rows)
    _write_lines(list_rows)


def _get_blocks(raw_text: str) -> list[str]:
    blocks = raw_text.split("~")
    logger.debug("Text blocks is ready!")
    return blocks


def _get_rows_lists(text_blocks: list[str]) -> list[list[str]]:
    """
    Get lists of row from text blocks
    """
    rows_lists: list[list[str]] = []
    for block in text_blocks:
        rows = block.split("\n")
        rows = [i for i in rows if i]
        rows_lists.append(rows)
    logger.debug("Rows_lists is ready!")
    return rows_lists


def get_number_combinations(rows_lists: list[list[str]]) -> int:
    number_combinations = math.prod(len(i) for i in rows_lists)
    logger.info(f"Number combinations: {number_combinations}")
    return number_combinations


def _is_all_combinations_got(set_rows: set[str],
                             number_combinations: int) -> bool:
    if len(set_rows) != number_combinations:
        return False
    return True


def _get_combined_row(rows_lists: list[list[str]]) -> str:
    row = ""
    for i in range(len(rows_lists)):
        row += f"{random.choice(rows_lists[i])} "
        if i+1 == len(rows_lists):
            row += "|\n"
    return row


def _print_progress(counter: int, len_data: int) -> None:
    print(f'Done: {counter} из {len_data}\r', end="")


def _send_progress(counter: int, number_combinations: int) -> None:
    five_persent = number_combinations*0.1
    if counter % five_persent == 0:
        send_progress(bot, admins, counter, number_combinations)


def _convert_set_to_list(set_rows: set[str]) -> list[str]:
    return _delete_separator(list(set_rows))


def _delete_separator(list_rows: list[str]) -> list[str]:
    if len(list_rows) > 0:
        list_rows[-1] = list_rows[-1].replace("|\n", "")
        return list_rows
    logger.warning("Len of list_rows is 0")


def _write_lines(data: Iterable) -> None:
    path = Path("generated.txt")
    with open(path, mode="w", encoding="UTF-8") as file:
        file.writelines(data)
    logger.debug("successful writing to a file")
