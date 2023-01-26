from pathlib import Path
import math
# import random
from typing import Iterable
import os
from numpy import random
from zipfile import ZipFile, ZIP_DEFLATED

from loguru import logger

from bot import bot, send_progress, admins


def combinate_text(raw_text: str) -> None:
    _combinate_text(raw_text)
    logger.info("Done")


def _combinate_text(raw_text: str) -> None:
    _delete_old_files()
    blocks = _get_blocks(raw_text)
    rows = _get_rows(blocks)
    number_combinations = get_number_combinations(rows)

    unique_rows = set()
    counter = 0
    while not _is_all_combinations_got(unique_rows, number_combinations):
        start_len = len(unique_rows)
        row = _get_combinated_row(rows)
        unique_rows.add(row)
        finish_len = len(unique_rows)
        if finish_len > start_len:
            counter += 1
            _send_progress(counter, number_combinations)
        _print_progress(counter, number_combinations)

    list_rows = _convert_set_to_list(unique_rows)
    _write_lines(list_rows)


def _delete_old_files() -> None:
    path_list = [Path("generated.txt"), Path("generated.zip")]
    for path in path_list:
        if path.is_file():
            os.remove(path)


def _get_blocks(raw_text: str) -> list[str]:
    blocks = raw_text.split("~")
    logger.debug("Text blocks is ready!")
    return blocks


def _get_rows(text_blocks: list[str]) -> list[list[str]]:
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
    if len(set_rows) < number_combinations*0.8:
        return False
    return True


def _get_combinated_row(rows_lists: list[list[str]]) -> str:
    row = ""
    for i in range(len(rows_lists)):
        if i+1 != len(rows_lists):
            row += f"{random.choice(rows_lists[i])}&"
        else:
            row += f"{random.choice(rows_lists[i])}|\n"
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
    _add_to_zip()


def _add_to_zip() -> None:
    path_txt = Path("generated.txt")
    path_zip = Path("generated.zip")
    try:
        with ZipFile(path_zip, 'w') as zipf:
            zipf.write(path_txt, compress_type=ZIP_DEFLATED, compresslevel=9)
        logger.debug("successful added to a zip")
    except Exception as ex:
        logger.warning(f"{type(ex)}: {ex}")


if __name__ == "__main__":
    raw_text = (
        """A very vulgar girl missed a real guy
An experienced girl without scandals and nerves will give pleasure
A petite beauty wants attention. I'm good, really
I love when they fuck me, not the brain
I love cheeky guys who are able to directly say what they want
My hands are able to relax and deliver rilax, and my mouth will fill your body with passion
Hi! I'm your gift, I want you to unwrap me as soon as possible. I wonder what's inside?
We miss each other with a girlfriend. We want to meet someone and have fun
I live with my sister. We spend time together. We are ready to meet and discuss LJ. Do you like this format of meetings?
They can be your slave or mistress, I can do nice and turn on the passive. I'll be whatever you want.
~
✨
🍑
🍒
🐒
🧚
👧
👩‍🦰
👩
🙊
💋
💕
💞
☺️
😘
~
it's been a long time since anyone punished
me at all,
I really want
to think about meetings every day.
I'm waiting for brave guys.
I like initiative men.
I appreciate guys if they are the first to take the initiative.
I want to finally relax.
I dream of a wonderful evening
my secret desire is to spend the evening with a normal man
~
✨
🍑
🍒
🐒
🧚
👧
👩‍🦰
👩
🙊
💋
💕
💞
☺️
😘"""
    )

    combinate_text(raw_text)
