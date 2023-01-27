from pathlib import Path
import shutil
import os

from telebot.types import Message
from loguru import logger
import requests

from bot import bot, admins
from logger import set_logger
from combinator import combinate_text
from file_methods.txt_file import read_write_file


def main() -> None:
    set_logger()
    try:
        bot.infinity_polling()
        logger.info("Script is finished")
    except KeyError as ex:
        logger.warning(ex)
    except Exception as ex:
        logger.warning(f"{type(ex)}: {ex}")


@bot.message_handler(commands=["start"])
def send_start_message(message: Message) -> None:
    if message.chat.id in admins:
        try:
            bot.send_message(message.chat.id,
                             'Send me blocks of text with separor "~"')
        except Exception as ex:
            logger.warning(f"Bot: {type(ex)} {ex}")


@bot.message_handler(content_types=["document", "text"])
def send_combinated_text(message: Message) -> None:
    if message.chat.id in admins:
        try:
            if message.content_type == "document":
                logger.debug("Получен документ")
                combinations = _get_raw_combinations(message)
            else:
                combinations = message.text
            bot.send_message(message.chat.id, 'In progress')
            combinate_text(combinations)
            _send_document(message)
        except Exception as ex:
            logger.warning(f"{type(ex)} {ex}")


def _get_raw_combinations(message: Message) -> None:
    try:
        path_file = Path("combinations.txt")
        url = bot.get_file_url(message.document.file_id)
        _download_file(url, path_file)
        raw_combinations = read_write_file(path_file)
        os.remove(path_file)
        return raw_combinations
    except Exception as ex:
        logger.warning(f"[bot]: {type(ex)} {ex}")


def _download_file(url: str, path_dst: Path) -> None:
    with requests.get(url, stream=True) as r:
        with open(path_dst, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def _send_document(message: Message) -> None:
    path = Path("generated.zip")
    if path.is_file():
        file = open(path, "rb")
        bot.send_document(message.chat.id, document=file)
        file.close()
    else:
        bot.send_message(message.chat.id, "File not found")


if __name__ == "__main__":
    main()
